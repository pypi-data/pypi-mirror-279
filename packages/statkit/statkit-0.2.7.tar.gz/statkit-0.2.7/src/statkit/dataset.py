"""Various methods for partitioning the dataset, such as downsampling and splitting."""

from functools import partial

import numpy as np
from sklearn.linear_model import LogisticRegression  # type: ignore
from sklearn.preprocessing import LabelBinarizer  # type: ignore


def _as_categories(x_multinomial):
    """Convert multinomial sample to long vector of categorical draws."""
    #  Line up all draws in one long vector (of size `n_samples`), indicating which
    # feature was drawn.
    # Use Numpy instead of JAX implementation because it is faster.
    return np.repeat(np.arange(len(x_multinomial)), x_multinomial)  # type: ignore


def _as_multinomial(x_categorical, n_features: int):
    """Convert string of categorical draws to multinomial representation."""
    x_test = np.zeros(n_features)
    np.add.at(x_test, x_categorical, 1)  # In place change.
    return x_test  # type: ignore


def _single_multinomial_train_test_split(
    random_state, x_i, test_size: float = 0.2
) -> tuple:
    """Make train-test split for a single multinomial draw.

    Args:
        random_state: Instance of NumPy pseudo random number state.
        x_i: A single multinomial observation.
        test_size: Proportion of draws for test set.
    """
    x_i = x_i.astype(int)
    x_draws = _as_categories(x_i)
    # Take, on average, `n_test` draws from test set (i.e., without replacement).
    u = random_state.uniform(size=len(x_draws))
    selected = u <= test_size
    x_test_draws = x_draws[selected]
    # Go back to multinomial representation.
    x_test = _as_multinomial(x_test_draws, n_features=len(x_i))  # type: ignore
    # Remainder is train set.
    x_train = x_i - x_test
    return x_train, x_test


def multinomial_holdout_split(X, test_size=0.5, random_state=None):
    """Partition each row, containing multiple observations, in a train-test split.

    Args:
        X: A dataset of with multiple independent (multinomial) observations per row.
        test_size: Proportion of draws to reserve for the test set.
        random_state: Seed for numpy pseudo random number generator state.

    Returns:
        A pair `X_train`, `X_test` both with same shape as `X`.
    """
    random_state = np.random.default_rng(random_state)

    _single_split = partial(_single_multinomial_train_test_split, test_size=test_size)
    x_as = []
    x_bs = []
    for x_i in X:
        x_a, x_b = _single_split(random_state, x_i)
        x_as.append(x_a)
        x_bs.append(x_b)
    return np.stack(x_as), np.stack(x_bs)


def stratified_downsample(
    X, y, ratio: int = 1, replace: bool = False, verbose: bool = False
):
    r"""Downsample majority class while stratifying for continuous/discrete variables.

    This method uses propensity score matching to subsample the majority class so that
    both groups have similar distributions of the covariates.
    Concretely, a logistic regression model is trained on the classes to adjusting for
    features `X`. The logits are then used to find the best match in the control
    group. This ensure that after downsampling both groups are equally likely to be in
    the case and control group (according to the features `X`).

    Warning: In the worst case scenario, this method has a time complexity of
    \( O(m^2) \), where \( m \) is the number of samples.

    Args:
        X: Features/covariates/exogeneous variables to control (stratify) while
        downsampling.
        y: Binary classes to match (e.g., y=1 case, y=0 is control).
        ratio: Downsample majority class to achieve this majority:minority ratio.
        replace: By default, subsample without replacement.
        verbose: If True, print progress.

    Returns: Indices of the matched majority class (control group).
    """
    if replace:
        raise NotImplementedError("Downsampling with replacement is not implemented.")

    if ratio != 1:
        raise NotImplementedError("Downsampling with ratio != 1 is not implemented.")

    y_ = LabelBinarizer().fit_transform(y)
    y_ = np.squeeze(y_)
    # Swap classes if y=1 is the majority class.
    if sum(y_) > sum(1 - y_):
        y_ = 1 - y_

    # 1) Compute logits.
    model = LogisticRegression(penalty=None).fit(X, y_)
    logits = model.decision_function(X)

    # 2) Match the case with controls using propensity scores.
    control_indices = _find_nearest_matches_greedily(logits, y_, verbose)
    return control_indices


def _find_nearest_matches_greedily(logits, y, verbose):
    # Split cases and controls.
    case = y == 1
    control = y == 0

    # Select without replacement: we keep track of previously selected controls.
    not_selected = np.ones_like(y, dtype=bool)
    for idx_case in np.nonzero(case)[0]:
        idx_controls = np.nonzero(control & not_selected)[0]
        k = np.argmin(np.abs(logits[idx_controls] - logits[idx_case]))
        idx_match = idx_controls[k]
        not_selected[idx_match] = False
        if verbose:
            print(".", end="")

    if verbose:
        print()

    return np.nonzero(control & (~not_selected))[0]
