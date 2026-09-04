Title: Categorisation
Heading: Topics and reading guide
Summary: Find a starting point in machine learning, explore the blog by topic, and understand how tasks, learning methods, and models fit together.

<div class="topic-guide" markdown="1">

This blog explores how machine-learning methods work and what research papers tell us about them. Start with a topic below, or follow a short reading path from the fundamentals to a particular method.

## Browse by topic

- **[Computer vision](/category/computer-vision.html)**: learning from images, with articles on visual representations, vision transformers, and self-supervised learning.
- **[Sequence models](/category/sequence-models.html)**: language modelling, attention, and transformers for processing and generating sequences.
- **[Reinforcement learning](/category/reinforcement-learning.html)**: learning to make decisions, from rewards and value functions to policies learned from recorded experience.
- **[ML Dojo](/category/ml-dojo.html)**: introductions and practical explanations for building a foundation in machine learning.
- **[Applications](/category/applications.html)**: examples of machine learning applied to problems beyond benchmark datasets.

Categories group articles by their main subject. [Tags](/tags.html) connect ideas across those groups: a transformer can process text or images, and self-supervised learning can be used in either domain. General machine learning, deep learning, optimisation, and fine-tuning are cross-cutting topics rather than separate branches of a single hierarchy.

## Where to start

**Neural networks and language.** Begin with the [Neural Networks Primer]({filename}/articles/2017/Sep/01/2017_09_01_PrimerNN.md), then read [Neural Language Modelling]({filename}/articles/2017/Nov/30/2017_11_30_Explaining-Language-Modeling.md). Continue to [Attention Is All You Need]({filename}/articles/2017/Sep/12/2017_09_12_Transformer-Attention-is-all-you-need.md) for the transformer architecture.

**Learning visual features without manual labels.** With neural-network basics in place, compare [DINO]({filename}/articles/2021/May/03/2021_05_03_Dino.md), which learns by matching predictions across image views, with [Masked Autoencoders]({filename}/articles/2021/Nov/14/2021_11_14_Masked-Autoencoders-Saclable-Vision-Learnenrs.md), which learn by reconstructing missing image content. Then read [DINOv2]({filename}/articles/2023/Apr/18/2023_04_18_Dinov2.md) to see how this line of work scales to reusable visual features.

**Learning to make decisions.** Start with the [Reinforcement Learning Primer]({filename}/articles/2021/May/01/RL_primer.md). Once rewards, policies, and value functions are familiar, [Decision Transformer]({filename}/articles/2021/Jun/01/2021_06_01_DecisionTransformer_RL2seq.md) introduces an approach that models sequences of returns, states, and actions.

## How the ideas fit together

A method is easier to understand when we separate four questions:

1. **What is the task?** Classification predicts a category; regression predicts a numerical value; clustering groups similar examples. Other tasks include detecting anomalies, ranking results, generating content, and predicting structured outputs such as a sequence of labels.
2. **Where does the learning signal come from?** Supervised learning uses supplied targets. Unsupervised learning looks for structure without supplied target labels. Self-supervised learning creates training targets from the data itself, for example by hiding part of an image and predicting it. Semi-supervised learning combines labelled and unlabelled examples. Reinforcement learning uses rewards to learn decisions over time.
3. **What kind of model is used?** Linear models, decision trees, probabilistic models, and neural networks provide different ways to represent relationships in data. Within neural networks, fully connected layers, convolutions, recurrence, and attention are building blocks, not separate definitions of learning.
4. **How is it trained or adapted?** Optimisation determines how parameters are updated. Online learning updates a model as examples arrive; fine-tuning adapts a pretrained model. Feature engineering designs the input representation, while representation learning learns useful features from data.

For example, DINOv2 uses a **vision transformer** as its model and **self-supervision** for pretraining. Its features can then support different tasks, including **classification** and **segmentation**, with supervised training of a task-specific predictor. These labels describe different parts of the same system.

## Methods and terminology

<details class="topic-reference" markdown="1">
<summary>Prediction, clustering, and anomaly detection</summary>

**Prediction.** Common methods include linear regression, logistic regression, naive Bayes, nearest-neighbour methods (k-NN), decision trees, support vector machines (SVMs), relevance vector machines (RVMs), and neural networks. Their variants support different tasks; logistic regression, for example, is a classification method despite its name. Ensembles combine predictors through approaches such as bagging and boosting; random forests are ensembles of decision trees.

**Clustering.** Examples include k-means, hierarchical clustering, BIRCH, DBSCAN, OPTICS, and mean shift. They differ in how they define a group, from proximity to a centre to connected regions of high density. Gaussian mixture models, including multivariate ones, describe data through a weighted combination of distributions; categorical mixtures serve a similar role for categorical observations. Expectation-maximisation (EM) is a fitting procedure used for mixture models, not a model in its own right.

**Anomaly detection.** Neighbour-distance scores and Local Outlier Factor identify observations that are unusual relative to a reference dataset or their local neighbourhood.

**Related tasks.** Association-rule mining looks for recurring co-occurrences; learning to rank orders candidates by relevance; grammar induction seeks grammatical structure from examples. Pattern recognition is a broader term covering the discovery and use of regularities in data.

For implementations and examples, see the scikit-learn guides to [supervised learning](https://scikit-learn.org/stable/supervised_learning.html), [clustering](https://scikit-learn.org/stable/modules/clustering.html), and [mixture models](https://scikit-learn.org/stable/modules/mixture.html).

</details>

<details class="topic-reference" markdown="1">
<summary>Representations, neural networks, and structured models</summary>

**Representations and dimensionality reduction.** Principal component analysis (PCA), independent component analysis (ICA), factor analysis, non-negative matrix factorisation (NMF), and sparse coding offer different ways to express data through a smaller or more structured set of components. Slow feature analysis (SFA) learns features that vary slowly over time. Canonical correlation analysis (CCA) finds correlated projections of paired variable sets. Linear discriminant analysis (LDA) uses class labels when finding discriminative projections. t-SNE is commonly used for low-dimensional visualisation.

**Neural networks.** Examples range from the perceptron and multilayer perceptron (MLP) to convolutional neural networks (CNNs), recurrent neural networks (RNNs), and transformers. Long short-term memory (LSTM) and gated recurrent unit (GRU) networks are recurrent variants; vision transformers (ViTs) apply transformer models to visual inputs. Deep learning refers to learning with multilayer neural networks, not just fully connected networks.

Autoencoders learn through reconstruction. Generative adversarial networks (GANs) train a generator against a discriminator. Restricted Boltzmann machines are probabilistic models, and self-organising maps (SOMs) learn a topology-preserving mapping. Hebbian learning describes a family of connection-update rules rather than one architecture.

**Structured models.** Bayesian networks, conditional random fields (CRFs), and hidden Markov models (HMMs) represent dependencies among variables. They can support structured prediction when outputs are related, as in sequence labelling.

The scikit-learn documentation gives further examples of [decomposition methods](https://scikit-learn.org/stable/modules/decomposition.html), [CCA](https://scikit-learn.org/stable/modules/cross_decomposition.html#canonical-correlation-analysis), and [supervised dimensionality reduction with LDA](https://scikit-learn.org/stable/modules/lda_qda.html#dimensionality-reduction-using-linear-discriminant-analysis).

</details>

<details class="topic-reference" markdown="1">
<summary>Reinforcement learning and learning theory</summary>

**Reinforcement learning.** Temporal-difference (TD) learning updates value estimates using rewards and other value estimates. Q-learning and SARSA are TD control methods: they learn action values that help determine which action to take. The [Reinforcement Learning Primer]({filename}/articles/2021/May/01/RL_primer.md) introduces the underlying concepts.

**Learning theory.** Statistical and computational learning theory study what can be learned, from how much data, and under which assumptions. Topics include the bias-variance trade-off, empirical risk minimisation, Occam-style arguments for simpler explanations, probably approximately correct (PAC) learning, and Vapnik-Chervonenkis (VC) theory. These are tools for reasoning about learning and generalisation, rather than application categories.

</details>

## Follow the research

[NeurIPS](https://neurips.cc/), [ICML](https://icml.cc/), and [ICLR](https://iclr.cc/) are major machine-learning conferences. [JMLR](https://www.jmlr.org/) is a research journal. The [machine-learning listings on arXiv](https://arxiv.org/list/cs.LG/recent) provide access to preprints; an arXiv posting alone does not indicate peer review.

</div>
