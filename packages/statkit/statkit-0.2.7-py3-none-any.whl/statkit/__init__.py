r"""Statistics for machine learning.

Brings traditional (frequentistic) statistical concepts to your sci-kit learn models.
Examples:
    - Hypothesis testing of model scores with \(p\)-values (see, e.g.,
        `statkit.non_parametric.unpaired_permutation_test`),
    - Estimate 95 % confidence intervals around test scores (see, e.g.,
        `statkit.non_parametric.bootstrap_score`).
    - Decision curve analysis to compare models in terms of consequences of actions
        (see, e.g., `statkit.decision.NetBenefitDisplay`).
    - Downsample a dataset while stratifying for continuous variables (see, e.g.,
      `statkit.dataset.stratified_downsample`).
    - Univariate feature selection with multiple hypothesis testing correction (see,
      e.g.,
        `statkit.feature_selection.StatisticalTestFilter`),
"""

__version__ = "0.2.7"
