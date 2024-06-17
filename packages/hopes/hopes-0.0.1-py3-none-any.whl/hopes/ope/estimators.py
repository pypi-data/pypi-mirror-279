import re
from abc import ABC, abstractmethod

import numpy as np
import scipy

from hopes.assert_utils import check_array
from hopes.dev_utils import override
from hopes.rew.rewards import RegressionBasedRewardModel


class BaseEstimator(ABC):
    """Base class for all estimators."""

    def __init__(self):
        self.target_policy_action_probabilities: np.ndarray | None = None
        self.behavior_policy_action_probabilities: np.ndarray | None = None
        self.rewards: np.ndarray | None = None

    def set_parameters(
        self,
        target_policy_action_probabilities: np.ndarray,
        behavior_policy_action_probabilities: np.ndarray | None,
        rewards: np.ndarray | None,
    ) -> None:
        """Set the parameters for estimating the policy value.

        :param target_policy_action_probabilities: the probabilities of taking actions under
            the target policy.
        :param behavior_policy_action_probabilities: the probabilities of taking actions
            under the behavior policy.
        :param rewards: the rewards received under the behavior policy.
        :return: None
        """
        self.target_policy_action_probabilities = target_policy_action_probabilities
        self.behavior_policy_action_probabilities = behavior_policy_action_probabilities
        self.rewards = rewards

        self.check_parameters()

    def check_parameters(self) -> None:
        """Check if the estimator parameters are valid.

        This method should be called before estimating the policy value. It can be
        overridden by subclasses to add additional checks.

        Importance sampling estimators have several assumptions that must be met:

        - coverage: the target and behavior policies must have non-zero probability of taking the actions.
            This is not 100% necessary, i.e. if both policies have zero probability of taking an action under some
            state, but we enforce this assumption here to avoid numerical issues.
        - positivity: the rewards must be non-negative to be able to get a lower bound estimate of the
            target policy.
        """

        if self.behavior_policy_action_probabilities is None:
            behavior_policy_action_probabilities = np.ones_like(
                self.target_policy_action_probabilities
            )
            behavior_policy_action_probabilities /= behavior_policy_action_probabilities.sum(
                axis=1, keepdims=True
            )
        else:
            behavior_policy_action_probabilities = self.behavior_policy_action_probabilities

        if self.rewards is None:
            rewards = np.zeros(self.target_policy_action_probabilities.shape[0])
        else:
            rewards = self.rewards

        if (
            self.target_policy_action_probabilities is None
            or behavior_policy_action_probabilities is None
            or rewards is None
        ):
            raise ValueError("You must set the parameters before estimating the policy value.")

        for array, name, ndims in zip(
            [
                self.target_policy_action_probabilities,
                behavior_policy_action_probabilities,
                rewards,
            ],
            [
                "target_policy_action_probabilities",
                "behavior_policy_action_probabilities",
                "rewards",
            ],
            [2, 2, 1],
        ):
            check_array(
                array=array, name=name, expected_ndim=ndims, expected_dtype=(float, np.float32)
            )

        if not (
            self.target_policy_action_probabilities.shape[0]
            == behavior_policy_action_probabilities.shape[0]
            == rewards.shape[0]
        ):
            raise ValueError("The number of samples must be the same for all parameters.")

        if not (
            self.target_policy_action_probabilities.shape[1]
            == behavior_policy_action_probabilities.shape[1]
        ):
            raise ValueError(
                "The probabilities of taking actions under the target and "
                "behavior policies must have the same shape."
            )

        if np.any(self.target_policy_action_probabilities <= 0):
            raise ValueError("The target policy action probabilities must be positive.")

        if np.any(behavior_policy_action_probabilities <= 0):
            raise ValueError("The behavior policy action probabilities must be positive.")

        if np.any(rewards < 0):
            raise ValueError(
                "The rewards must be non-negative to be able to get a lower bound estimate of the target policy. "
                "Use a positive reward estimator or an appropriate scaler (i.e MinMaxScaler) to scale the rewards."
            )

        for array, name in zip(
            [self.target_policy_action_probabilities, behavior_policy_action_probabilities],
            ["target_policy_action_probabilities", "behavior_policy_action_probabilities"],
        ):
            if not np.allclose(np.sum(array, axis=1), np.ones(array.shape[0], dtype=float)):
                raise ValueError(f"The {name} must sum to 1 on each sample.")

    def estimate_policy_value_with_confidence_interval(
        self,
        method: str = "bootstrap",
        significance_level: float = 0.05,
        num_samples: int = 1000,
    ) -> dict[str, float]:
        r"""Estimate the confidence interval of the policy value.

        The `bootstrap` method uses bootstrapping to estimate the confidence interval of the policy value. Bootstrapping
        consists in resampling the data with replacement to infer the distribution of the estimated weighted rewards.
        The confidence interval is then computed as the quantiles of the bootstrapped samples.

        The `t-test` method (or `Student's t-test`) uses the t-distribution of the estimated weighted rewards - assuming
        that the weighted rewards are normally distributed - to estimate the confidence interval of the policy value.
        It follows the t-distribution formula :math:`t = \frac{\hat{\mu} - \mu}{\hat{\sigma} / \sqrt{n}}`, where
        :math:`\hat{\mu}` is the mean of the weighted rewards, :math:`\mu` is the true mean of the weighted rewards,
        :math:`\hat{\sigma}` is the standard deviation of the weighted rewards, and :math:`n` is the number of samples.
        The confidence interval is then computed as:

        .. math::
            [\hat{\mu} - t_{\mathrm{test}}(1 - \alpha, n-1) \frac{\hat{\sigma}}{\sqrt{n}},
            \hat{\mu} + t_{\mathrm{test}}(1 - \alpha, n-1) \frac{\hat{\sigma}}{\sqrt{n}}]

        The input data is sampled from the estimated weighted rewards, using :meth:`estimate_weighted_rewards`.

        Example:

        .. code-block:: python

            ipw = InverseProbabilityWeighting()
            ipw.set_parameters(
                target_policy_action_probabilities=target_policy_action_probabilities,
                behavior_policy_action_probabilities=behavior_policy_action_probabilities,
                rewards=rewards,
            )
            metrics = ipw.estimate_policy_value_with_confidence_interval(
                method="bootstrap", significance_level=0.05
            )
            print(metrics)

        Should output something like:

        .. code-block:: python

            {
                "lower_bound": 10.2128,
                "upper_bound": 10.6167,
                "mean": 10.4148,
                "std": 6.72408,
            }

        :param method: the method to use for estimating the confidence interval. Currently, only "bootstrap" and
            "t-test" are supported.
        :param significance_level: the significance level of the confidence interval.
        :param num_samples: the number of bootstrap samples to use. Only used when `method` is "bootstrap".
        :return: a dictionary containing the confidence interval of the policy value. The keys are:

            - "lower_bound": the lower bound of the policy value, given the significance level.
            - "upper_bound": the upper bound of the policy value, given the significance level.
            - "mean": the mean of the policy value.
            - "std": the standard deviation of the policy value.
        """
        assert method in ["bootstrap", "t-test"], "The method must be 'bootstrap' or 't-test'."
        assert 0 < significance_level < 1, "The significance level must be in (0, 1)."

        weighted_rewards = self.estimate_weighted_rewards()
        assert (
            weighted_rewards is not None and len(weighted_rewards) > 0
        ), "The weighted rewards must not be empty."

        weighted_rewards = weighted_rewards.reshape(-1)

        if method == "bootstrap":
            boot_samples = [
                np.mean(
                    np.random.choice(weighted_rewards, size=weighted_rewards.shape[0], replace=True)
                )
                for _ in np.arange(num_samples)
            ]

            lower_bound = np.quantile(boot_samples, significance_level / 2)
            upper_bound = np.quantile(boot_samples, 1 - significance_level / 2)

            return {
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "mean": np.mean(boot_samples),
                "std": np.std(boot_samples),
            }

        elif method == "t-test":
            num_samples = weighted_rewards.shape[0]
            mean = np.mean(weighted_rewards)
            # compute the standard deviation of the weighted rewards, using degrees of freedom = num_samples - 1
            std = np.std(weighted_rewards, ddof=1)
            # compute t, with alpha = significance_level / 2 and degrees of freedom = num_samples - 1
            t = scipy.stats.t.ppf(1 - significance_level / 2, num_samples - 1)
            # compute the confidence interval
            ci = t * std / np.sqrt(num_samples)

            return {
                "lower_bound": mean - ci,
                "upper_bound": mean + ci,
                "mean": mean,
                "std": std,
            }

    def short_name(self) -> str:
        """Return the short name of the estimator.

        This method can be overridden by subclasses to customize the short name.

        :return: the short name of the estimator. By default, it returns the abbreviation of
            the class name, ie "IPW".
        """
        return re.sub("[^A-Z]", "", self.__class__.__name__)

    @abstractmethod
    def estimate_weighted_rewards(self) -> np.ndarray:
        """Estimate the weighted rewards.

        This method should be overridden by subclasses to implement the specific estimator.

        :return: the weighted rewards.
        """
        pass

    @abstractmethod
    def estimate_policy_value(self) -> float:
        """Estimate the value of the target policy.

        This method should be overridden by subclasses to implement the specific estimator. The typical implementation
        should call :meth:`estimate_weighted_rewards` to compute the weighted rewards, then compute the policy value.

        :return: the estimated value of the target policy.
        """
        pass


class InverseProbabilityWeighting(BaseEstimator):
    r"""Inverse Probability Weighting (IPW) estimator.

    :math:`V_{IPW}(\pi_e, D)=\frac {1}{n} \sum_{t=1}^n p(s_t,a_t) r_t`

    Where:
        - :math:`D` is the offline collected dataset.
        - :math:`p(s_t,a_t)` is the importance weight defined as :math:`p(s_t,a_t)=\frac{\pi_e(a_t|s_t)}{\pi_b(a_t|s_t)}`.
        - :math:`\pi_e` is the target policy and :math:`\pi_b` is the behavior policy.
        - :math:`r_t` is the reward observed at time :math:`t` for the behavior policy.
        - :math:`n` is the number of samples.

    This estimator has generally high variance, especially on small datasets, and can be improved by using
    self-normalized importance weights.

    .. rubric:: References

    https://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1079&context=cs_faculty_pubs
    """

    def __init__(self) -> None:
        super().__init__()

        # computed importance weights, saved for reuse by subclasses
        # shape: (n, num_actions)
        self.importance_weights: np.ndarray | None = None

    @override(BaseEstimator)
    def estimate_weighted_rewards(self) -> np.ndarray:
        """Estimate the weighted rewards using the IPW estimator."""
        self.importance_weights = None
        self.check_parameters()

        self.importance_weights = (
            self.target_policy_action_probabilities / self.behavior_policy_action_probabilities
        )
        return self.importance_weights * self.rewards.reshape(-1, 1)

    @override(BaseEstimator)
    def estimate_policy_value(self) -> float:
        """Estimate the value of the target policy using the IPW estimator."""
        return np.mean(self.estimate_weighted_rewards())


class SelfNormalizedInverseProbabilityWeighting(InverseProbabilityWeighting):
    r"""Self-Normalized Inverse Probability Weighting (SNIPW) estimator.

    :math:`V_{SNIPW}(\pi_e, D)= \frac {\sum_{t=1}^n p(s_t,a_t) r_t}{\sum_{t=1}^n p(s_t,a_t)}`

    Where:
        - :math:`D` is the offline collected dataset.
        - :math:`p(s_t,a_t)` is the importance weight defined as :math:`p(s_t,a_t)=\frac{\pi_e(a_t|s_t)}{\pi_b(a_t|s_t)}`.
        - :math:`\pi_e` is the target policy and :math:`\pi_b` is the behavior policy.
        - :math:`r_t` is the reward at time :math:`t`.
        - :math:`n` is the number of samples.

    .. rubric:: References

    https://papers.nips.cc/paper_files/paper/2015/hash/39027dfad5138c9ca0c474d71db915c3-Abstract.html
    """

    def __init__(self) -> None:
        super().__init__()

    @override(BaseEstimator)
    def estimate_weighted_rewards(self) -> np.ndarray:
        """Estimate the weighted rewards using the SNIPW estimator."""
        super().estimate_weighted_rewards()

        weighted_rewards = self.importance_weights * self.rewards.reshape(-1, 1)
        return weighted_rewards / self.importance_weights

    @override(BaseEstimator)
    def estimate_policy_value(self) -> float:
        """Estimate the value of the target policy using the SNIPW estimator."""
        super().estimate_weighted_rewards()

        weighted_rewards = self.importance_weights * self.rewards.reshape(-1, 1)
        return np.sum(weighted_rewards) / np.sum(self.importance_weights)


class DirectMethod(BaseEstimator):
    r"""Direct Method (DM) estimator.

    :math:`V_{DM}(\pi_e, D, Q)=\frac {1}{n} \sum_{t=1}^n \sum_{a \in A} \pi_e(a|s_0) Q(s_0, a)`

    Where:
        - :math:`D` is the offline collected dataset.
        - :math:`\pi_e` is the target policy.
        - :math:`Q` is the Q model trained to estimate the expected reward of the initial state under the behavior policy.
        - :math:`n` is the number of samples.
        - :math:`a` is the action taken in the set of actions :math:`A`.
        - :math:`s_0` is the initial state.

    This estimator trains a Q model using supervised learning, then uses it to estimate the expected reward of the
    initial state under the target policy. The performance of this estimator depends on the quality of the Q model.
    """

    def __init__(
        self,
        q_model_cls: type[RegressionBasedRewardModel],
        behavior_policy_obs: np.ndarray,
        behavior_policy_act: np.ndarray,
        behavior_policy_rewards: np.ndarray,
        steps_per_episode: int,
        q_model_type: str = "random_forest",
        q_model_params: dict | None = None,
    ) -> None:
        """Initialize the Direct Method estimator.

        :param q_model_cls: the class of the Q model to use.
        :param behavior_policy_obs: the observations for training the Q model, shape:
            (batch_size, obs_dim).
        :param behavior_policy_act: the actions for training the Q model, shape:
            (batch_size,).
        :param behavior_policy_rewards: the rewards for training the Q model, shape:
            (batch_size,).
        :param steps_per_episode: the number of steps per episode. The number of samples
            must be divisible by this number.
        :param q_model_type: the type of regression model to use for the Q model.
        :param q_model_params: the parameters of the regression model.
        """
        super().__init__()

        assert issubclass(
            q_model_cls, RegressionBasedRewardModel
        ), "The Q model must be a subclass of RegressionBasedRewardModel."
        assert (
            behavior_policy_obs.ndim == 2
        ), "The observations must have shape (batch_size, obs_dim)."
        assert behavior_policy_act.ndim == 1, "The actions must have shape (batch_size,)."
        assert behavior_policy_rewards.ndim == 1, "The rewards must have shape (batch_size,)."
        assert (
            behavior_policy_obs.shape[0]
            == behavior_policy_act.shape[0]
            == behavior_policy_rewards.shape[0]
        ), "The number of samples must be the same for all parameters."
        assert steps_per_episode > 0, "The number of steps per episode must be positive."
        assert (
            behavior_policy_obs.shape[0] % steps_per_episode == 0
        ), "The number of samples must be divisible by the number of steps per episode."

        self.q_model_cls = q_model_cls
        self.q_model_type = q_model_type
        self.q_model_params = q_model_params
        self.q_model: RegressionBasedRewardModel | None = None
        self.behavior_policy_obs = behavior_policy_obs
        self.behavior_policy_act = behavior_policy_act
        self.behavior_policy_rewards = behavior_policy_rewards
        self.steps_per_episode = steps_per_episode

    def fit(self) -> dict[str, float] | None:
        """Fit the Q model to estimate the expected reward of the initial state under the behavior
        policy.

        :return: the fit statistics of the Q model.
        """
        self.q_model = self.q_model_cls(
            obs=self.behavior_policy_obs,
            act=self.behavior_policy_act,
            rew=self.behavior_policy_rewards,
            regression_model=self.q_model_type,
            model_params=self.q_model_params,
        )
        return self.q_model.fit()

    def check_parameters(self) -> None:
        """Check if the estimator parameters are valid.

        Base estimator checks plus additional checks for the Q model.
        """
        super().check_parameters()

        assert (
            self.behavior_policy_obs.shape[0] == self.target_policy_action_probabilities.shape[0]
        ), "The number of samples must be the same for the behavior policy and the target policy."

    @override(BaseEstimator)
    def estimate_weighted_rewards(self) -> np.ndarray:
        """Estimate the weighted rewards using the Direct Method estimator."""
        self.check_parameters()

        # use the Q model to predict the expected rewards
        state_action_value_prediction = self.q_model.estimate(
            obs=self.behavior_policy_obs,
            act=self.behavior_policy_act,
        ).reshape(-1, 1)

        # compute the expected reward of the initial state under the target policy
        # shape: (n, steps_per_episode)
        state_value = (
            (state_action_value_prediction * self.target_policy_action_probabilities)
            # sum over the actions
            .sum(axis=1).reshape(-1, self.steps_per_episode)
        )
        # take the value of the initial state
        initial_state_value = state_value[:, 0]

        return initial_state_value

    @override(BaseEstimator)
    def estimate_policy_value(self) -> float:
        """Estimate the value of the target policy using the Direct Method estimator."""
        return np.mean(self.estimate_weighted_rewards())


class TrajectoryPerDecisionMixin(ABC):
    """Mixin for trajectory-wise and per-decision estimators.

    It provides a method to compute the weighted rewards for both trajectory-wise and per-
    decision estimators.
    """

    def compute_weighted_rewards(
        self,
        target_policy_action_probabilities: np.ndarray,
        behavior_policy_action_probabilities: np.ndarray,
        rewards: np.ndarray,
        steps_per_episode: int,
        discount_factor: float,
        is_per_decision: bool,
    ) -> np.ndarray:
        """Compute the weighted rewards for given type of estimator. See the specific estimator for
        more details.

        :param target_policy_action_probabilities: the probabilities of taking actions under
            the target policy.
        :param behavior_policy_action_probabilities: the probabilities of taking actions
            under the behavior policy.
        :param rewards: the rewards received under the behavior policy.
        :param steps_per_episode: the number of steps per episode.
        :param discount_factor: the discount factor.
        :param is_per_decision: whether the estimator is per decision or per trajectory.
        """

        # compute importance ratios
        importance_weights = (
            target_policy_action_probabilities / behavior_policy_action_probabilities
        )
        num_actions = target_policy_action_probabilities.shape[1]
        # shape: (n, T * num_actions)
        importance_weights = importance_weights.reshape(-1, steps_per_episode * num_actions)

        # compute the importance weights per decision, which is the cumulative product of the
        # importance weights over the trajectory; at each step t, we'll have the product from 0 to t-1.
        # shape: (n, T * num_actions)
        importance_weights = np.cumprod(importance_weights, axis=1)

        if not is_per_decision:
            # in trajectory-wise estimators, we only need the last importance weight, which is the product
            # over the whole trajectory.
            # shape: (n, 1)
            importance_weights = importance_weights[:, -1].reshape(-1, 1)

        # normalize the importance weights. Normalization technique depends on the estimator (see implementations).
        importance_weights = self.normalize(importance_weights)

        # rewards, shape: (n, T)
        rewards = rewards.reshape(-1, steps_per_episode)

        # discount factors
        # compute a matrix of discount factors, shape: (n, T)
        num_trajectories = rewards.shape[0]
        discount_factors = np.full((num_trajectories, steps_per_episode), discount_factor)
        # compute the discount factor at each step as
        # [gamma^0, gamma^1, ..., gamma^(T-1)] = [gamma^1, gamma^2, ..., gamma^T] / gamma
        discount_factors = np.cumprod(discount_factors, axis=1) / discount_factor

        # if the estimator is per decision, we need to repeat the discount factors and rewards for each action.
        # shape: (n, T * num_actions)
        if is_per_decision:
            discount_factors = np.tile(discount_factors, (1, num_actions))
            rewards = np.tile(rewards, (1, num_actions))

        # compute the weighted rewards per trajectory.
        # shape: (n, 1)
        weighted_rewards = np.sum(
            # element-wise product
            # trajectory wise: (n, 1) * (n, T) * (n, T) -> (n, T)
            # per decision: (n, T * num_actions) * (n, T * num_actions) * (n, T * num_actions) -> (n, T * num_actions)
            importance_weights * discount_factors * rewards,
            # sum weights over the trajectory length
            axis=1,
        ).reshape(-1, 1)

        return weighted_rewards

    def normalize(self, weights: np.ndarray) -> np.ndarray:
        """Normalize the importance weights. This method can be overridden by subclasses to
        implement a specific normalization strategy.

        :param weights: the importance weights to normalize.
        :return: the normalized importance weights.
        """
        return weights


class TrajectoryWiseImportanceSampling(BaseEstimator, TrajectoryPerDecisionMixin):
    r"""Trajectory-wise Importance Sampling (TIS) estimator.

    :math:`V_{TIS} (\pi_e, D) = \frac {1}{n} \sum_{i=1}^ n\sum_{t=0}^{T-1} \gamma^t w^{(i)}_{0:T-1} r_t^{(i)}`

    Where:

    - :math:`D` is the offline collected dataset.
    - :math:`w^{(i)}_{0:T-1}` is the importance weight of the trajectory :math:`i` defined as :math:`w_{0:T-1} = \prod_{t=0}^{T-1} \frac {\pi_e(a_t|s_t)} {\pi_b(a_t|s_t)}`
    - :math:`\pi_e` is the target policy and :math:`\pi_b` is the behavior policy.
    - :math:`n` is the number of trajectories.
    - :math:`T` is the length of the trajectory.
    - :math:`\gamma_t` is the discount factor at time :math:`t`.
    - :math:`r_t^{(i)}` is the reward at time :math:`t` of trajectory :math:`i`.

    TIS can suffer from high variance due to the product operation of the importance weights, also when action space is
    large.

    .. rubric:: References

    https://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1079&context=cs_faculty_pubs
    """

    def __init__(self, steps_per_episode: int, discount_factor: float = 1.0) -> None:
        super().__init__()

        assert steps_per_episode > 0, "The number of steps per episode must be positive."
        assert 0 <= discount_factor <= 1, "The discount factor must be in [0, 1]."

        self.steps_per_episode = steps_per_episode
        self.discount_factor = discount_factor

        self.importance_weights: np.ndarray | None = None

    @override(BaseEstimator)
    def short_name(self) -> str:
        return "TIS"

    @override(BaseEstimator)
    def check_parameters(self) -> None:
        """Check if the estimator parameters are valid."""
        super().check_parameters()

        assert (
            self.target_policy_action_probabilities.shape[0] % self.steps_per_episode == 0
        ), "The number of samples must be divisible by the number of steps per episode."

    @override(BaseEstimator)
    def estimate_weighted_rewards(self) -> np.ndarray:
        """Estimate the weighted rewards using the Trajectory-wise Importance Sampling estimator.

        :return: the weighted rewards, or here the policy value per trajectory.
        """
        self.check_parameters()

        return self.compute_weighted_rewards(
            target_policy_action_probabilities=self.target_policy_action_probabilities,
            behavior_policy_action_probabilities=self.behavior_policy_action_probabilities,
            rewards=self.rewards,
            steps_per_episode=self.steps_per_episode,
            discount_factor=self.discount_factor,
            is_per_decision=False,
        )

    @override(BaseEstimator)
    def estimate_policy_value(self) -> float:
        """Estimate the value of the target policy using the Trajectory-wise Importance Sampling
        estimator."""
        return np.mean(self.estimate_weighted_rewards())


class SelfNormalizedTrajectoryWiseImportanceSampling(TrajectoryWiseImportanceSampling):
    r"""Self-Normalized Trajectory-wise Importance Sampling (TIS) estimator.

    .. math::
        V_{TIS} (\pi_e, D) = \frac {1}{n} \sum_{i=1}^n \sum_{t=0}^{T-1}
            \gamma^t \frac {w^{(i)}_{0:T-1}} {\frac {1}{n} \sum_{j=1}^n w^{(j)}_{0:T-1}} r_t^{(i)}

    Where:

    - :math:`D` is the offline collected dataset.
    - :math:`w^{(i)}_{0:T-1}` is the importance weight of the trajectory :math:`i` defined as :math:`w_{0:T-1} = \prod_{t=0}^{T-1} \frac {\pi_e(a_t|s_t)} {\pi_b(a_t|s_t)}`
    - :math:`\pi_e` is the target policy and :math:`\pi_b` is the behavior policy.
    - :math:`n` is the number of trajectories.
    - :math:`T` is the length of the trajectory.
    - :math:`\gamma_t` is the discount factor at time :math:`t`.
    - :math:`r_t^{(i)}` is the reward at time :math:`t` of trajectory :math:`i`.

    SNTIS is a variance reduction technique for TIS. It divides the weighted rewards by the mean of the importance
    weights of the trajectories.

    .. rubric:: References

    https://arxiv.org/abs/1906.03735
    """

    @override(TrajectoryWiseImportanceSampling)
    def short_name(self) -> str:
        return "SNTIS"

    @override(TrajectoryPerDecisionMixin)
    def normalize(self, weights: np.ndarray) -> np.ndarray:
        """Normalize the importance weights using the self-normalization strategy.

        It uses self-normalization to reduce the variance of the estimator, using the mean
        of the importance weights over the trajectories.

        :param weights: the importance weights to normalize.
        :return: the normalized importance weights.
        """
        return weights / (np.mean(weights) + 1e-10)


class PerDecisionImportanceSampling(BaseEstimator, TrajectoryPerDecisionMixin):
    r"""Per-Decision Importance Sampling (PDIS) estimator.

    :math:`V_{PDIS} (\pi_e, D) = \frac {1}{n} \sum_{i=1}^n \sum_{t=0}^{T-1} \gamma^t w^{(i)}_{t} r_t^{(i)}`

    Where:

    - :math:`D` is the offline collected dataset.
    - :math:`w^{(i)}_{t}` is the importance weight of the decision :math:`t` of trajectory :math:`i` defined as :math:`w_{t} = \frac {\pi_e(a_t|s_t)} {\pi_b(a_t|s_t)}`
    - :math:`\pi_e` is the target policy and :math:`\pi_b` is the behavior policy.
    - :math:`n` is the number of trajectories.
    - :math:`T` is the length of the trajectory.
    - :math:`\gamma_t` is the discount factor at time :math:`t`.
    - :math:`r_t^{(i)}` is the reward at time :math:`t` of trajectory :math:`i`.

    .. rubric:: References

    https://arxiv.org/abs/1906.03735
    """

    def __init__(self, steps_per_episode: int, discount_factor: float = 1.0) -> None:
        super().__init__()

        assert steps_per_episode > 0, "The number of steps per episode must be positive."
        assert 0 <= discount_factor <= 1, "The discount factor must be in [0, 1]."

        self.steps_per_episode = steps_per_episode
        self.discount_factor = discount_factor

        self.importance_weights: np.ndarray | None = None

    @override(BaseEstimator)
    def check_parameters(self) -> None:
        """Check if the estimator parameters are valid."""
        super().check_parameters()

        assert (
            self.target_policy_action_probabilities.shape[0] % self.steps_per_episode == 0
        ), "The number of samples must be divisible by the number of steps per episode."

    @override(BaseEstimator)
    def estimate_weighted_rewards(self) -> np.ndarray:
        """Estimate the weighted rewards using the Trajectory-wise Importance Sampling estimator.

        :return: the weighted rewards, or here the policy value per trajectory.
        """
        self.check_parameters()

        return self.compute_weighted_rewards(
            target_policy_action_probabilities=self.target_policy_action_probabilities,
            behavior_policy_action_probabilities=self.behavior_policy_action_probabilities,
            rewards=self.rewards,
            steps_per_episode=self.steps_per_episode,
            discount_factor=self.discount_factor,
            is_per_decision=True,
        )

    @override(BaseEstimator)
    def estimate_policy_value(self) -> float:
        """Estimate the value of the target policy using the Trajectory-wise Importance Sampling
        estimator."""
        return np.mean(self.estimate_weighted_rewards())


class SelfNormalizedPerDecisionImportanceSampling(PerDecisionImportanceSampling):
    r"""Self-Normalized Per-Decision Importance Sampling (PDIS) estimator.

    .. math::
        V_{PDIS} (\pi_e, D) = \frac {1}{n} \sum_{i=1}^n \sum_{t=0}^{T-1}
            \gamma^t \frac {w^{(i)}_{t}} {\frac {1}{n} \sum_{j=1}^n w^{(j)}_{t}} r_t^{(i)}

    Where:

    - :math:`D` is the offline collected dataset.
    - :math:`w^{(i)}_{t}` is the importance weight of the decision :math:`t` of trajectory :math:`i` defined as :math:`w_{t} = \frac {\pi_e(a_t|s_t)} {\pi_b(a_t|s_t)}`
    - :math:`\pi_e` is the target policy and :math:`\pi_b` is the behavior policy.
    - :math:`n` is the number of trajectories.
    - :math:`T` is the length of the trajectory.
    - :math:`\gamma_t` is the discount factor at time :math:`t`.
    - :math:`r_t^{(i)}` is the reward at time :math:`t` of trajectory :math:`i`.

    SNPDIS is a variance reduction technique for PDIS.

    .. rubric:: References

    https://arxiv.org/abs/1906.03735
    """

    @override(TrajectoryPerDecisionMixin)
    def normalize(self, weights: np.ndarray) -> np.ndarray:
        """Normalize the importance weights using the self-normalization strategy.

        It uses self-normalization to reduce the variance of the estimator, using the mean
        of the importance weights over the trajectories.

        :param weights: the importance weights to normalize.
        :return: the normalized importance weights.
        """
        return weights / (np.mean(weights) + 1e-10)
