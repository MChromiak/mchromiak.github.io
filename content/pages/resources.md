Title: Resources
Status: published

Interesting articles and research papers form DL/ML area are exponentially flourishing. Here I will link to some interesting articles online that I find interesting. My blog articles are [here](../../)

##### **2021-06**
* ##### [NLP Course from huggingFace](https://huggingface.co/course/chapter1/2?fw=pt)
* ##### [Google:Machine Learning Crash Course with TensorFlow APIs](https://developers.google.com/machine-learning/crash-course)


##### **2017-11**
* ##### [An introduction to Generative Adversarial Networks (with code in TensorFlow)](http://blog.aylien.com/introduction-generative-adversarial-networks-code-tensorflow/)
* ##### [Deep Image Prior](https://dmitryulyanov.github.io/deep_image_prior)
"Deep Image Prior": super-resolution, inpainting, denoising without learning on a dataset and pretrained networks. Comparable results to learned methods.
* ##### [Distilling a Neural Network Into a Soft Decision Tree](https://arxiv.org/abs/1711.09784)
G. Hinton  describe a way of using a trained neural net to create a type of soft decision tree that generalizes better than one learned directly from the training data.
* ##### [Are GANs Created Equal? A Large-Scale Study](https://arxiv.org/abs/1711.10337)
This study shows that many papers over the last year or so were just observing sampling error, not true improvement. Some totally new GAN structures like StackGAN, Progressive GAN, CycleGAN, etc., are real advances, but this exhaustive empirical study shows that several of the new loss functions for basic GANs perform about the same as the original GAN loss.
* ##### [StarGAN ](https://github.com/yunjey/StarGAN)
StarGAN: learning one model that translates between *multiple* domains without supervision (previous works were about translating between two domains without supervision)
* ##### [Career-- How to build a Portfolio as a Machine Learning/Data Science Engineer in industry ?](https://www.reddit.com/r/MachineLearning/comments/7dzh87/d_how_to_build_a_portfolio_as_a_machine/)
* ##### [Basics-- An overview of gradient descent optimization algorithms](http://ruder.io/optimizing-gradient-descent/)
GD variants, challenges, GD optimization algorithms, SGD Parallelizing and distributing, SGD optimizations
* ##### [Business questions engineers should ask when interviewing at ML/AI companies](https://medium.com/@danielgross/seven-questions-to-ask-when-interviewing-for-an-ml-job-1963ccee3a19)
* ##### [On the State of the Art of Evaluation in Neural Language Models](https://arxiv.org/abs/1707.05589)
"Regularisation methods with large-scale automatic black-box hyperparameter tuning and arrive at surprising conclusion that standard LSTM architectures, when properly regularised, outperform more recent models"
* ##### [A Regularized Framework for Sparse and Structured Neural Attention](https://arxiv.org/abs/1705.07704) [GitHub code](https://github.com/vene/sparse-structured-attention)
Framework for sparse and structured attention, building upon a smoothed max operator
* ##### What's wrong with convolutional neural networks? By Geoffrey Hinton [Reddit](https://www.reddit.com/r/MachineLearning/comments/6upe7d/r_what_is_wrong_with_convolutional_neural_nets/),[Quora](https://www.quora.com/Whats-wrong-with-convolutional-neural-networks)
* ##### [Dynamic Routing Between Capsules](https://arxiv.org/abs/1710.09829), [Matrix capsules with EM routing](https://openreview.net/forum?id=HJWLfGWRb&noteId=HJWLfGWRb), [A Keras implementation of CapsNet in NIPS2017 paper "Dynamic Routing Between Capsules](https://github.com/XifengGuo/CapsNet-Keras)
A **capsule** is a group of neurons whose outputs represent different properties of the same entity.
* ##### [Regularizing Neural Networks by Penalizing Confident Output Distributions](https://arxiv.org/abs/1701.06548)
Penalizing low entropy output distributions, acts as a strong regularizer in supervised learning.
* ##### [Don't Decay the Learning Rate, Increase the Batch Size](https://arxiv.org/abs/1711.00489)
* ##### [Layer Normalization](https://arxiv.org/abs/1607.06450)
One way to reduce the training time is to normalize the activities of the neurons.

##### **2017-10**
* ##### [One pixel attack for fooling deep neural networks](https://arxiv.org/abs/1701.06548)
Authors prove that single pixel change can induce DNN to classify image incorrectly.

* ##### [Efficient Processing of Deep Neural Networks: A Tutorial and Survey](https://arxiv.org/abs/1703.09039) Rate:[4/5]
Recommended by A.Karpathy, comprehensive tutorial and survey about the recent advances towards the goal of enabling efficient processing of DNNs.

* ##### [Learning to Optimize with Reinforcement Learning](http://bair.berkeley.edu/blog/2017/09/12/learning-to-optimize-with-rl/)
Can we learn ML algorithms instead instead designing manually?

* ##### [Introducing Hybrid lda2vec Algorithm](http://multithreaded.stitchfix.com/blog/2016/05/27/lda2vec/#topic=38&lambda=1&term=),[When word2vec is enough. Part 1](http://multithreaded.stitchfix.com/blog/2017/10/18/stop-using-word2vec/), [Part 2](http://multithreaded.stitchfix.com/blog/2017/10/25/word-tensors/)
**Lda2vec** algorithm. A neural network is not always required to find word vectors. ([lda2vec: Tools for interpreting natural language](https://github.com/cemoody/lda2vec),[tensor decompositions](https://github.com/ahwillia/tensortools), [lda2vec-tf](https://github.com/meereeum/lda2vec-tf))

* ##### [Learning a Hierarchy](https://blog.openai.com/learning-a-hierarchy/)
Learning a hierarchical policy to solve mazes by [OpenAI](https://www.openai.com/) [@GitHub](https://github.com/openai/mlsh) [ArXiv](https://arxiv.org/abs/1710.09767)

* ##### [Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation](https://arxiv.org/abs/1609.08144)

* ##### [AutoML - deeper than deep?](https://research.googleblog.com/2017/05/using-machine-learning-to-explore.html)

* ##### [Deep Learning (DLSS) and Reinforcement Learning (RLSS) Summer School, Montreal 2017](http://videolectures.net/deeplearning2017_montreal/)
    * Good introduction videos + slides for DL and RL

##### **2017-09**

* ##### **Information bottleneck:** [New Theory Cracks Open the Black Box of Deep Learning](https://www.quantamagazine.org/new-theory-cracks-open-the-black-box-of-deep-learning-20170921/?utm_campaign=Revue%20newsletter&utm_medium=Newsletter&utm_source=The%20Wild%20Week%20in%20AI)
    * Paper: [ArXiv](https://arxiv.org/abs/1703.00810)
    * Parameterizing the Bottleneck [Google DeepVIB](https://research.google.com/pubs/pub45903.html)

* ##### Pointer Networks
