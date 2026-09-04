Title: Resources
Heading: Papers and research notes
Summary: An annotated collection of machine-learning papers, technical articles, and implementations, organised by research topic.
Status: published

<div class="resource-notes" markdown="1">

Papers and technical articles worth returning to, with short notes on the ideas they introduce. Most of this collection comes from 2015–2018: a useful record of developments in deep learning, rather than a list of today's best-performing methods.

For a broad selection of courses, books, and tools, visit [Learning and research links]({filename}/pages/links.md). For explanations on this blog, start with the [topic guide]({filename}/pages/categorisation.md).

[Training](#training-and-evaluation) · [Vision](#vision-and-generative-models) · [Language](#language-and-attention) · [Learning algorithms](#learning-algorithms-and-hierarchies) · [Interpretability](#interpretability-and-information) · [Tutorials](#tutorials-and-lectures) · [Career perspectives](#career-perspectives)

## Training and evaluation

- **[An overview of gradient descent optimization algorithms](https://arxiv.org/abs/1609.04747)** (2016). Sebastian Ruder explains gradient-descent variants, momentum, adaptive learning rates, and parallel training. A starting point for understanding what an optimiser changes about the learning process.
- **[Layer Normalization](https://arxiv.org/abs/1607.06450)** (2016). Computes normalisation statistics across a layer's activations for an individual example, rather than across a minibatch. The paper develops the method for recurrent networks as well as other settings.
- **[Regularizing Neural Networks by Penalizing Confident Output Distributions](https://arxiv.org/abs/1701.06548)** (2017). Adds a penalty for overly concentrated output probabilities. Useful for understanding how confidence penalties and label smoothing can regularise a classifier.
- **[Don't Decay the Learning Rate, Increase the Batch Size](https://arxiv.org/abs/1711.00489)** (2017). Studies increasing batch size as an alternative to reducing the learning rate. The reported experiments achieve similar learning curves with fewer parameter updates, connecting optimisation noise with opportunities for parallel computation.
- **[On the State of the Art of Evaluation in Neural Language Models](https://arxiv.org/abs/1707.05589)** (2017). Carefully tuned and regularised LSTMs outperform several newer recurrent architectures in the study. The lasting lesson is about experimental design: architecture comparisons need comparable tuning effort and strong baselines.
- **[Are GANs Created Equal? A Large-Scale Study](https://arxiv.org/abs/1711.10337)** (2017 preprint; 2018 conference paper). Many of the tested generative adversarial networks reach similar scores with sufficient tuning and random restarts. The comparison shows why evaluation metrics and tuning budgets belong in any report of model quality.
- **[Efficient Processing of Deep Neural Networks: A Tutorial and Survey](https://arxiv.org/abs/1703.09039)** (2017). Explains how computation, data movement, memory, and hardware design affect neural-network efficiency. A foundation for understanding performance beyond a model's parameter count.

## Vision and generative models

- **[Deep Image Prior](https://arxiv.org/abs/1711.10925)** (2017). Fits a randomly initialised convolutional network to a single image for tasks including denoising, super-resolution, and inpainting. It needs neither a separate training dataset nor pretrained weights, but it still optimises the network for each image. The architecture itself supplies a useful bias towards image structure. [Project page and examples](https://dmitryulyanov.github.io/deep_image_prior).
- **[StarGAN](https://arxiv.org/abs/1711.09020)** (2017). Uses one model to translate images among multiple domains, such as facial attributes or expressions. Training uses unpaired images together with domain or attribute labels; unpaired translation is not the same as learning without supervision. [Official implementation](https://github.com/yunjey/stargan).
- **[Dynamic Routing Between Capsules](https://arxiv.org/abs/1710.09829)** (2017). Represents an entity, such as an object part, with a vector of properties. Routing strengthens connections when lower-level capsules agree about a higher-level entity. [Matrix capsules with EM routing](https://openreview.net/forum?id=HJWLfGWRb) (2018) develops a related approach using pose matrices. A [community Keras implementation](https://github.com/XifengGuo/CapsNet-Keras) accompanies the earlier dynamic-routing paper.
- **[One pixel attack for fooling deep neural networks](https://arxiv.org/abs/1710.08864)** (2017). Uses differential evolution to search for single-pixel changes that alter an image classifier's prediction. The experiments demonstrate adversarial vulnerability under a tightly constrained perturbation budget.

## Language and attention

- **[Google's Neural Machine Translation System](https://arxiv.org/abs/1609.08144)** (2016). Describes a large-scale translation system built around deep LSTMs, attention, and wordpiece units. A useful account of neural translation before transformers, including the engineering needed to make the system practical.
- **[A Regularized Framework for Sparse and Structured Neural Attention](https://arxiv.org/abs/1705.07704)** (2017). Builds attention mechanisms that can concentrate on a subset of inputs or on structured groups, such as contiguous text segments. It connects attention to regularised optimisation. [Authors' implementation](https://github.com/vene/sparse-structured-attention).
- **[Pointer Networks](https://arxiv.org/abs/1506.03134)** (2015). Uses attention to select positions in an input sequence as outputs, instead of choosing from a fixed vocabulary. This lets the output choices vary with input length, as needed in ordering and combinatorial problems.
- **[Introducing our Hybrid lda2vec Algorithm](https://multithreaded.stitchfix.com/blog/2016/05/27/lda2vec/)** (2016). Chris Moody combines word embeddings with interpretable document-topic mixtures. Supporting code includes the [original lda2vec repository](https://github.com/cemoody/lda2vec) and a [community TensorFlow port](https://github.com/meereeum/lda2vec-tf).
- **[Stop Using word2vec](https://multithreaded.stitchfix.com/blog/2017/10/18/stop-using-word2vec/)** and **[Word Tensors](https://multithreaded.stitchfix.com/blog/2017/10/25/word-tensors/)** (2017). Explore count-based word representations, matrix factorisation, and higher-order co-occurrence structure. They offer alternatives to neural embedding training, not a universal rule against word2vec. For a separate implementation reference on tensor decomposition, see [tensortools](https://github.com/ahwillia/tensortools).

## Learning algorithms and hierarchies

- **[Learning to Optimize](https://arxiv.org/abs/1606.01885)** (2016) and **[Learning to Optimize Neural Nets](https://arxiv.org/abs/1703.00441)** (2017). Ke Li and Jitendra Malik treat an optimiser as a policy that can be learned through reinforcement learning. The second paper explores this approach for training shallow neural networks. These papers provide the technical background for the [BAIR article on learning to optimise](https://bair.berkeley.edu/blog/2017/09/12/learning-to-optimize-with-rl/).
- **[Meta Learning Shared Hierarchies](https://arxiv.org/abs/1710.09767)** (2017). Learns reusable behaviours shared across tasks, with a task-specific policy choosing among them. The aim is to adapt to new tasks using those behaviours rather than learning every action from scratch. [Authors' code](https://github.com/openai/mlsh).
- **[Using Machine Learning to Explore Neural Network Architecture](https://research.google/blog/using-machine-learning-to-explore-neural-network-architecture/)** (2017). Google Research's explanation of early neural architecture search: a controller proposes architectures and learns from their evaluated performance. Useful context for separating the search procedure from the networks it produces.

## Interpretability and information

- **[Distilling a Neural Network Into a Soft Decision Tree](https://arxiv.org/abs/1711.09784)** (2017). Nicholas Frosst and Geoffrey Hinton transfer predictions from a trained network into a tree with probabilistic decisions. The tree offers a more inspectable decision structure; its predictions approximate the teacher rather than exposing the teacher's internal reasoning.
- **[Opening the Black Box of Deep Neural Networks via Information](https://arxiv.org/abs/1703.00810)** (2017). Investigates learning through the information that intermediate representations retain about inputs and targets. Its proposed fitting-and-compression account prompted substantial debate. Pair it with [Saxe and colleagues' follow-up analysis](https://research.ibm.com/publications/on-the-information-bottleneck-theory-of-deep-learning--1), which challenges the generality of the compression explanation. The original [Quanta article](https://www.quantamagazine.org/new-theory-cracks-open-the-black-box-of-deep-learning-20170921/) provides an accessible account of the proposal.
- **[Deep Variational Information Bottleneck](https://arxiv.org/abs/1612.00410)** (2016). Turns the information-bottleneck principle into a trainable objective using a variational approximation. This is a method for learning representations that balance prediction and compression, distinct from the claim that ordinary neural-network training necessarily follows such a process.

## Tutorials and lectures

- **[Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)**: an introduction to core concepts, model evaluation, and practical machine learning.
- **[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)**: the expanded successor to the NLP course originally linked here. Covers transformer models, tokenisation, datasets, and fine-tuning; assumes Python knowledge and some deep-learning background.
- **[TensorFlow's DCGAN tutorial](https://www.tensorflow.org/tutorials/generative/dcgan)**: a worked example of training a generator and discriminator to produce images. Replaces the unavailable AYLIEN introduction to GANs.
- **[Montreal Deep Learning and Reinforcement Learning Summer School, 2017](https://videolectures.net/deeplearning2017_montreal/)**: a historical collection of lectures and presentations. Software examples should be read in the context of their original versions.

## Career perspectives

- **[Building a machine-learning portfolio](https://www.reddit.com/r/MachineLearning/comments/7dzh87/d_how_to_build_a_portfolio_as_a_machine/)**: a 2017 community discussion about presenting projects and demonstrating practical skills.
- **[Seven questions to ask when interviewing for an ML job](https://medium.com/@danielgross/seven-questions-to-ask-when-interviewing-for-an-ml-job-1963ccee3a19)**: Daniel Gross's perspective on evaluating an employer's use of machine learning. These are discussion prompts, separate from the research evidence above.

</div>
