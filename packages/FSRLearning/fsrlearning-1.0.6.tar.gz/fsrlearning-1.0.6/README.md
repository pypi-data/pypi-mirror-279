# FSRLeaning - Python Library

[![Downloads](https://static.pepy.tech/badge/FSRLearning)](https://pepy.tech/project/FSRLearning)
[![Downloads](https://static.pepy.tech/badge/FSRLearning/month)](https://pepy.tech/project/FSRLearning)

FSRLeaning is a Python library for feature selection using reinforcement learning. It's designed to be easy to use and efficient, particularly for selecting the most relevant features from a very large set.

## Installation

Install FSRLearning using pip:

```bash
pip install FSRLearning
```

## Example usage

### Data Pre-processing

#### The Dataset

In this example, we're using the Australian credit approval dataset. It has 14 features that have been intentionally anonymized. The goal is to predict whether the label is 0 or 1. We're using this dataset to demonstrate how to use the library, but the model can work with any dataset. You can find more details about the dataset [here](https://archive.ics.uci.edu/dataset/143/statlog+australian+credit+approval).

#### The process

The first step is a pre-processing of the data. You need to give as input to the method for feature selection a X and y pandas DataFrame. X is the dataset with all the features that we want to evaluate and y the label to be predicted. **It is highly recommended to create a mapping between features and a list of number.** For example each feature is associated with a number. Here is an example of the data pre-processing step on a data set with 14 features including 1 label.
```python
import pandas as pd

# Get the pandas DataFrame
australian_data = pd.read_csv('australian_data.csv', header=None)

# Get the dataset with the features
X = australian_data.drop(14, axis=1)

# Get the dataset with the label values
y = australian_data[14]
```

After this step we can simply run a feature selection and ranking process that maximises a metric. 

```python
from FSRLearning import FeatureSelectorRL

# Create the object of feature selection with RL
fsrl_obj = FeatureSelectorRL(14, nb_iter=200)

# Returns the results of the selection and the ranking
results = fsrl_obj.fit_predict(X, y)
results
```

The feature_Selector_RL has several parameters that can be tuned. Here is all of them and the values that they can take.

- feature_number (integer) : number of features in the DataFrame X

- feature_structure (dictionary, optional) : dictionary for the graph implementation
- eps (float [0; 1], optional) : probability of choosing a random next state, 0 is an only greedy algorithm and 1 only random
- alpha (float [0; 1], optional): control the rate of updates, 0 is a very not updating state and 1 a very updated
- gamma (float [0, 1], optional): factor of moderation of the observation of the next state, 0 is a shortsighted condition and 1 it exhibits farsighted behavior
- nb_iter (int, optional): number of sequences to go through the graph
- starting_state ("empty" or "random", optional) : if "empty" the algorithm starts from the empty state and if "random" the algorithm starts from a random state in the graph 

The output of the selection process is a 5-tuple object.

- Index of the features that have been sorted

- Number of times that each feature has been chosen
- Mean reward brought by each feature
- Ranking of the features from the less important to the most important
- Number of states visited


## Existing methods

- Compare the performance of the FSRLearning library with RFE from Sickit-Learn :

```python
fsrl_obj.compare_with_benchmark(X, y, results)
```
Returns some comparisons and plot a graph with the metric for each set of features selected. It is useful for parameters tuning. 

- Get the evolution of the number of the visited states for the first time and the already visited states :

```python
fsrl_obj.get_plot_ratio_exploration()
```
Returns a plot. It is useful to get an overview of how the graph is browse and to tune the epsilon parameter (exploration parameter).

- Get an overview of the relative impact of each feature on the model :

```python
fsrl_obj.get_feature_strengh(results)
```

Returns a bar plot.

- Get an overview of the action of the stop conditions :

```python
fsrl_obj.get_depth_of_visited_states()
```

Returns a plot. It is useful to see how deep the Markovian Decision Process goes in the graph. 

## Your contribution is welcomed !

- Automatise the data processing step and generalize the input data format and type
- Distribute the computation of each reward for making the algorithm faster
- Add more vizualization and feedback methods

## References

This library has been implemented with the help of these two articles :
- Sali Rasoul, Sodiq Adewole and Alphonse Akakpo, FEATURE SELECTION USING REINFORCEMENT LEARNING (2021)
- Seyed Mehdin Hazrati Fard, Ali Hamzeh and Sattar Hashemi, USING REINFORCEMENT LEARNING TO FIND AN OPTIMAL SET OF FEATURES (2013)

