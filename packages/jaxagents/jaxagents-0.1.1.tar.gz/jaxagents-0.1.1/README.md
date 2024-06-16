# Jaxagents

[comment]: <> ([![License: MIT]&#40;https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg&#41;]&#40;/LICENSE&#41;)

[comment]: <> (![PyPI]&#40;https://img.shields.io/pypi/v/PACKAGE?label=pypi%20package&#41;)

Jaxagents is a Python implementation of Reinforcement Learning agents built upon JAX. The PyPI page of the project can be found [here](https://pypi.org/project/jaxagents/).

## Installation
You can install the latest version of jaxagents from PyPI via:

```sh
pip install jaxagents
```

## Content

So far, the project includes the following agents:
* Deep Q Networks (DQN)
* Double Deep Q Networks (DDQN) 
* Categorical Deep Q Networks (often known as C51)
* Quantile Regression Deep Q Networks (QRDQN) 

## Background

Research and development in Reinforcement Learning can be computationally cumbersome. Utilizing JAX's high computational performance, Jaxagents provides a framework for applying and developing Reinforcement Learning agents that offers benefits in:
* computational speed
* easy control of random number generation
* hyperparameter optimization (via parallelized calculations)
