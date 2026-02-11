---
标题: Learning Optimal Topology for Ad-hoc Robot Networks
作者: Matin Macktoobian, Zhan Shu, Qing Zhao
发布日期: 2022-01-30
arXiv ID: 2201.12900v2
PDF: https://arxiv.org/pdf/2201.12900v2.pdf
---

# 对比摘要

In this paper, we synthesize a data-driven method to predict the optimal topology of an ad-hoc robot network. This problem is technically a multi-task classification problem. However, we divide it into a class of multi-class classification problems that can be more efficiently solved. For this purpose, we first compose an algorithm to create ground-truth optimal topologies associated with various configurations of a robot network. This algorithm incorporates a complex collection of optimality criteria that our learning model successfully manages to learn. This model is an stacked ensemble whose output is the topology prediction for a particular robot. Each stacked ensemble instance constitutes three low-level estimators whose outputs will be aggregated by a high-level boosting blender. Applying our model to a network of 10 robots displays over 80% accuracy in the prediction of optimal topologies corresponding to various configurations of the cited network.