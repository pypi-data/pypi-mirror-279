from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
from scipy.stats import binom, ks_2samp
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle

from statkit.dataset import (
    _as_categories,
    _as_multinomial,
    _single_multinomial_train_test_split,
    multinomial_holdout_split,
    stratified_downsample,
)


class TestHoldOutSplit(TestCase):
    def setUp(self):
        self.random_state = np.random.default_rng(42)

    def test_as_mulitnomial_and_categories(self):
        """Test that multinomial and categorical representations are inverse."""
        n_features = 10
        x_sample = self.random_state.integers(0, high=10, size=[n_features])
        x_draws = _as_categories(x_sample)
        x_test = _as_multinomial(x_draws, n_features=n_features)
        assert_array_equal(x_sample, x_test)

    def assert_number_of_draws(self, n_observed, n_draws, fraction):
        """Assert that the number of draws is within the expected range."""
        n_observed = int(n_observed)
        n_draws = int(n_draws)
        # On average, the size of the test set, `n_test`, contains `fraction` of the
        # draws. The actual number is binomially distributed around the mean with a
        # variance of:
        #  p (1 - p) n.

        # Check that `n_test` falls within the 90% quantile range of the binomial
        # distribution.
        n_lower = int(binom.ppf(0.05, n_draws, fraction))
        n_upper = int(binom.ppf(0.95, n_draws, fraction))
        error_message = (
            f"The number of draws {n_observed}/{n_draws} is outside the 90% "
            f"quantile range {n_lower}-{n_upper} for a fraction of {fraction*100:.0f}%."
        )
        self.assertTrue(n_lower < n_observed, error_message)
        self.assertTrue(n_upper > n_observed, error_message)

    def test_single_train_test_split(self):
        """Test train-test split of a single multinomial."""
        fraction = 1 / 6
        x_sample = self.random_state.integers(0, high=10, size=[10])
        x_train, x_test = _single_multinomial_train_test_split(
            self.random_state, x_sample, test_size=fraction
        )
        # On average, the size of the test set, `n_test`, contains 1/6 of the draws. The
        # actual number is binomially distributed around the mean with a variance of 1/6
        # * 5/6 * n.
        self.assert_number_of_draws(
            n_observed=x_test.sum(), n_draws=x_sample.sum(), fraction=fraction
        )
        self.assertEqual(x_train.sum() + x_test.sum(), x_sample.sum())
        assert_array_equal(x_train + x_test, x_sample)

    def test_holdout_split(self):
        """Test train-test split of a dataset of multinomials."""
        fraction = 1 / 3
        n_features = 10
        n_samples = 20
        x_sample = self.random_state.integers(0, high=10, size=[n_samples, n_features])
        # Triple number of observations to take out a third (=fraction).
        x_sample = x_sample * 3

        x_train, x_test = multinomial_holdout_split(
            x_sample, test_size=fraction, random_state=43
        )
        assert_array_equal(x_train + x_test, x_sample)
        self.assert_number_of_draws(
            n_observed=x_test.sum(), n_draws=x_sample.sum(), fraction=fraction
        )
        # assert_array_equal(x_test.sum(axis=1), x_sample.sum(axis=1) * fraction)
        self.assertEqual(x_train.sum() + x_test.sum(), x_sample.sum())
        assert_array_equal(
            x_train.sum(axis=1) + x_test.sum(axis=1), x_sample.sum(axis=1)
        )

        # Check if the function is deterministic.
        x_train2, x_test2 = multinomial_holdout_split(
            x_sample, test_size=fraction, random_state=43
        )
        assert_array_equal(x_train, x_train2)
        assert_array_equal(x_test, x_test2)

    def test_sparse_holdout_split(self):
        """Test edge cases where the data are sparse categorical observations."""
        x_sparse = np.zeros([1_000, 2], dtype=int)
        x_sparse[:, 1] = 1
        x_train, x_test = multinomial_holdout_split(
            x_sparse, test_size=0.5, random_state=42
        )
        # Some of the observations are in the test set.
        self.assertTrue(x_test.sum() > 0)
        self.assertTrue(x_train.sum() > 0)

        # Check that the sum is close to 50%.
        assert_allclose(x_test.mean(axis=0), [0.0, 0.5], atol=0.01)
        assert_allclose(x_train.mean(axis=0), [0.0, 0.5], atol=0.01)


class TestDownSampling(TestCase):
    """Test on a toy dataset with confounded samples."""

    def setUp(self):
        self.random_state = np.random.default_rng(42)

        # The following dataset contains a set of confounded samples:
        # Those with x_1 = 1 are all in the y=0 class.
        y_case = np.ones(5)
        y_control = np.zeros(10)
        y = np.concatenate([y_case, y_control])

        x1_case = np.zeros(5)
        x1_control = np.concatenate([np.ones(5), np.zeros(5)])
        x1 = np.concatenate([x1_case, x1_control])

        # And a non informative variable.
        x2 = np.random.normal(size=15)

        X = np.column_stack([x1, x2])

        self.X, self.y = shuffle(X, y, random_state=43)

    def test_remove_confounders(self):
        """Test that confounded samples are removed."""
        indices = stratified_downsample(self.X, self.y)
        # Check that all indices are from the control group.
        self.assertTrue(all(self.y[indices] == 0))
        # Since samples with x_1 = 1 are all in the y=0 class, they should be removed.
        self.assertTrue(all(self.X[indices, 0] == 0))

    def test_matched_logits(self):
        """Test that after downsampling the logits are similar."""
        # Compute logits for the entire dataset.
        model = LogisticRegression(penalty=None).fit(self.X, self.y)
        logits = model.decision_function(self.X)

        # Downsampled controls and compare with logits of cases.
        indices = stratified_downsample(self.X, self.y)
        logits_case = logits[self.y == 1]
        logits_controls = logits[indices]

        _, p_value = ks_2samp(logits_case, logits_controls)
        false_alarm_rate = 0.1
        self.assertGreater(p_value, false_alarm_rate)
