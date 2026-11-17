"""Statistical testing and paired inference routines for G4 experimental protocol."""

import random
from typing import Dict, List, Tuple
import numpy as np


class StatisticalAnalysis:
    """Nonparametric permutation testing and bootstrap confidence intervals."""

    @staticmethod
    def paired_permutation_test(
        diffs_by_graph: List[float],
        num_permutations: int = 10000,
        seed: int = 42
    ) -> Tuple[float, float]:
        """Perform a two-sided paired permutation test on graph-level mean differences.

        H0: mu_diff = 0 vs H1: mu_diff != 0.
        Returns:
            Tuple[float, float]: (observed_mean, two_sided_p_value)
        """
        if not diffs_by_graph:
            return 0.0, 1.0

        diffs = np.array(diffs_by_graph)
        obs_mean = float(np.mean(diffs))
        abs_obs = abs(obs_mean)

        rng = np.random.RandomState(seed)
        n = len(diffs)
        # Random sign flip under null hypothesis of exchangeability
        signs = rng.choice([-1, 1], size=(num_permutations, n))
        perm_means = np.mean(signs * diffs, axis=1)

        p_value = float(np.mean(np.abs(perm_means) >= abs_obs))
        return obs_mean, p_value

    @staticmethod
    def bootstrap_confidence_interval(
        diffs_by_graph: List[float],
        num_bootstrap: int = 10000,
        ci_level: float = 0.95,
        seed: int = 42
    ) -> Tuple[float, float]:
        """Calculate graph-clustered percentile bootstrap confidence interval."""
        if not diffs_by_graph:
            return 0.0, 0.0

        diffs = np.array(diffs_by_graph)
        n = len(diffs)
        rng = np.random.RandomState(seed)

        indices = rng.randint(0, n, size=(num_bootstrap, n))
        boot_means = np.mean(diffs[indices], axis=1)

        alpha = 1.0 - ci_level
        lower = float(np.percentile(boot_means, 100 * (alpha / 2.0)))
        upper = float(np.percentile(boot_means, 100 * (1.0 - alpha / 2.0)))
        return lower, upper
