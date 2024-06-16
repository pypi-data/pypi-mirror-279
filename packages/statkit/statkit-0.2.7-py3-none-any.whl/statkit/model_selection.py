from deprecation import deprecated  # type: ignore
import statkit
from statkit.dataset import multinomial_holdout_split


@deprecated(
    deprecated_in="0.2.7",
    removed_in="0.3.0",
    current_version=statkit.__version__,
    details="Use `multinomial_holdout_split` instead.",
)
def holdout_split(X, test_size=0.5, random_state=None):
    """Make train-test split from of a dataset of multinomial draws.

    Args:
        X: A dataset of multinomial observations, with independent samples along the
            rows.
        test_size: Proportion of draws to reserve for the test set.
        random_state: Seed for numpy pseudo random number generator state.

    Returns:
        A pair `X_train`, `X_test` both with same shape as `X`.
    """
    return multinomial_holdout_split(X, test_size, random_state)
