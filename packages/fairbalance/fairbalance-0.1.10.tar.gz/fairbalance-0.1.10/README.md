# FairBalance

## Overview

FairBalance is a Python package that provides a suite of tools for evaluating and enhancing fairness in datasets. It includes a variety of fairness evaluation metrics and resampling methods to help address and mitigate bias in your data. This package is designed to be easily integrated into your machine learning pipeline, ensuring that your models are built on fair and balanced datasets.

## Installation

You can install FairBalance using pip:

```bash
pip install fairbalance
```

## Features
- **Easily load fairness datasets**: Load ready-to-use famous datasets such as adult to test fairbalance features 
- **Fairness Evaluation Metrics**: Compute various fairness metrics to evaluate the fairness of your dataset.
- **Resampling Methods**: Implement resampling techniques to mitigate bias in your dataset.
- **Balanced train test split**: split your dataset and rebalance your training data with one line
- **Easy Integration**: Seamlessly integrate FairBalance into your existing machine learning pipeline.

## Quick Start

Here is a quck example to get started with FairBalance:

### Evaluating the balance of your dataset
```python
from fairbalance.metrics import FairnessAnalysis
from fairbalance.datasets import load_adult

data, target, _, _ = load_adult()
FA = FairnessAnalaysis(data, target, 1, ["sex","race"], {"sex": "Male", "race": "White"})
FA.get_fairness_analysis()
```

### Applying rebalancing strategies
```python
from fairbalance.mitigation_strategies import balanceOutputForAttributes
from fairbalance.processors import RandomOverSamplerProcessor
from fairbalance.datasets import load_adult

data, target, cont_columns, cat_columns = load_adult()
mitigation = balanceOutputForAttributes(processor = RandomOverSamplerProcessor())
X_balanced, y_balanced = mitigation.resample(data, target, ["sex","race"], cont_columns, cat_columns)
```

### Creating a balanced train/test split
Fairbalance balances only the training set, to be able to test your model on real, untransformed data

```python
from fairbalance.utils import balanced_train_test_split
from fairbalance.mitigation_strategies import balanceOutputForAttributes
from fairbalance.processors import RandomOverSamplerProcessor
from fairbalance.datasets import load_adult

data, target, cont_columns, cat_columns = load_adult()
mitigation = balanceOutputForAttributes(processor = RandomOverSamplerProcessor())
X_train, X_test, y_train, y_test = balanced_train_test_split(data, target, ["sex", "race"], mitigation, cont_columns, cat_columns)
```
