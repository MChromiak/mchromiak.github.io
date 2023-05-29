Title:  NLP: Explaining Neural Language Modeling
Status: published
Category: Sequence Models
Date: 2017-11-30 19:30
Modified: 2017-11-30 19:30
Tags: NLP, language model, ngram, perplexity,  smoothing
Slug: Explaining-Neural-Language-Modeling
Related_posts: Transformer-Attention-is-all-you-need
Cover: articles/2017/Nov/30/img/nlp-cover.png
Summary: Language modeling (LM) is the essential part of Natural Language Processing (NLP) tasks such as  Machine Translation, Spell Correction Speech Recognition, Summarization, Question Answering, Sentiment analysis etc. Goal of the Language Model is to compute the probability of sentence considered as a word sequence. This article explains how to model the language using probability and n-grams. It also discuss the language model evaluation with  use of *perplexity*.

**Read before:**
* [Get started with NLP (Part I)](https://medium.com/@gon.esbuyo/get-started-with-nlp-part-i-d67ca26cc828)

**Key Takeaways:**

* The goal of a language model is to compute a probability of a token (e.g. a sentence or a sequence of words).
* Language Model (LM) actually a grammar of a language as it gives the probability of word that will follow

* Dictionary:
	* **Corpus** - Body of text, singular. Corpora is the plural of this. Example: A collection of medical journals.
	* **Token**- Each "entity" that is a part of whatever was split up based on rules. For examples, each word is a token when a sentence is "tokenized" into words. Each sentence can also be a token, if you tokenized the sentences out of a paragraph.
	* **Lexicon** - Words and their meanings. Example: English dictionary. Consider, however, that various fields will have different lexicons. For example: To a financial investor, the first meaning for thef word "Bull" is someone who is confident about the market, as compared to the common English lexicon, where the first meaning for the word "Bull" is an animal. As such, there is a special lexicon for financial investors, doctors, children, mechanics, and so on.

### Intro

*Language Modeling (LM)* is one of the most important parts of modern Natural Language Processing (NLP). There are many sorts of applications for  Language Modeling, like: Machine Translation, Spell Correction Speech Recognition, Summarization, Question Answering, Sentiment analysis etc. Each of those tasks require use of *language model*. Language model is required to represent the text to a form understandable from the machine point of view.

Below I have elaborated on the means to model a corpus of text to use in multiple machine learning NLP tasks.    

### Motivation
Each part of natural language has to assume some representation. Written text in natural way is composed out of sentences that consist of words that in turn contains letters. Each of those pieces of  text sentence can be a subject for analysis. Of course we can also use morphemes [ref]Small meaningful units that make up words. [\ref] or n-grams of the text.

One way or another, the text needs to be normalized.  Normalized mean that indexed text and query terms must have same form. For example, *U.S.A.* and *u.s.a.* are to be considered same (remove dots and case fold - lowercase) and return same result while querying any of them.  Thus, an implicit word classes equivalence must be defined.

#### Tokenizing
Choosing which text segmentation (aka tokenizing) technique will be used is arbitrary, but depends strictly on the undergoing tasks, their specification, heuristics and preconditions. For instance, if we are after a single character statistics of text task we will probably choose to operate on letters not on n-grams or words. The result for text fragmentation is called **token**. So by referring to a token in general one actually refers to the fragmentation technique outcome in form of a sentence, word, n-gram, morpheme, letter etc.  

However, even word-oriented tokens might give a different set of distinct tokens. For instance in a lemma based tokens the *cat* and plural *cats* would count as one word having same stem (core meaning-bearing unit). On the other hand, if we make more strict distinctions, that would e.g. differentiate *word form*, we would get two distinct tokens. It all depends how you define a token.

To make things more clear, lets settle three terms:

* **vocabulary** set of different types
* **type**  an element of vocabulary, and a
* **token** as an instance of a *type*.

Additionally, language modeling must consider the correlated ordering of tokens. This is because every language is based on some grammar, where order has a lot of influence on the meaning of a text.  

To complete the NLP tasks we must provide a measure to enable comparison operations and thus assessment method for grading our model. This measure is probability. This involves all kinds of tasks, for example:

* **Machine translation:** translating a sentence saying about height it would probably state that $ P(tall\ man) > P(large\ man)$ as the ‘*large*’ might also refer to weight or general appearance thus, not as probable as ‘*tall*’

* **Spelling Correction:**  Spell correcting sentence: “Put you name into form”, so that $P(name\ into\ \textbf{form}) > P(name\ into\ \textbf{from})$

* **Speech Recognition:** Call my nurse: $P(Call\ my\ nurse.) \gg P(coal\ miners)$, I have no idea. $P(no\ idea.) \gg P(No\ eye\ deer.)$
* **Summarization, question answering, sentiment analysis** etc.

### The probabilistic language modeling

The probability of a sentence $S$ (as a sequence of *words* $w_i$) is : $P(S) = P(w_1,w_2, w_3,\ldots,w_n)$. Now it is important to find the probability of upcoming word. It is an everyday task made e.g. while typing  your mobile keyboard. We will settle the *conditional probability*  of $w_4$ depending on all previous words. For a 4 word sentence this conditional probability is:

$$ P(S)=P(w_1, w_2, w_3, w_4) \equiv P(w_4 |w_1, w_2, w3) $$

This way we can actually represent the language grammar, however, in NLP it is accustomed to use the LM term.

To calculate the joint probability  of a sentence (as a word sequence) $P(W)$ the chain rule of probability will be used.

**Probability Chain Rule:**

$$P(A|B) = \frac{P(A\cap B)}{P(B)} \implies P(A\cap B)=P(A|B)P(B)$$

so in general for a token sequence we get:

$$P(S)=P(w_1,\ldots,w_n) = P(w_1)P(w_2|w_1) P(w_3)P(w_1,w_2)\ldots P(w_n|w_1,\ldots w_{n-1}) ={\displaystyle \prod_{i} P(w_i|w_1,\ldots w_{i-1})}$$

To estimate each probability a straightforward solution could be to use simple counting.

$$P(w_5|w_1,w_2,w_3,w_4)= \frac{count(w_1,w_2,w_3,w_4,w_5)}{count(w_1,w_2,w_3,w_4)}$$

but this gives us to many possible sequences to ever estimate. Imagine how much data (occurrences of each sentence) we would have to get to make this *count*s meaningful.

To cope with this issue we can simplify by applying the **Markov Assumption**, which states that it is enough to pick only one, or a couple of previous words as a prefix:

$$P(w_1,\ldots,w_n) \approx {\displaystyle \prod_{i} P(w_i|w_{i-k},\ldots P(w_{i-1}))}$$

where $k$ is the number of previous tokens (*prefix* size) that we consider.

### N-grams
An N-gram is a contiguous (order matters) sequence of items, which in this case is the words in text. The n-grams depends on the size of the *prefix*. The simplest case is the *Unigram mode*.

** (Uni-) 1-gram model**
The simplest case of *Markov assumption* is case when the size of prefix is one.
$P(w_1,\ldots,w_n) \approx {\displaystyle \prod_{i} P(w_i)}$

This will provide us with grammar that only consider one word. As a result it produces a set of unrelated words. It actually would generate sentences with random word order.

** Bigram **
However, if we consider a 2-word (tandem) bigrams correlations where we condition each word on previous one we get some sens of meaning between couples of words.

$$P(w_1,\ldots,w_n) \approx {\displaystyle \prod_{i} P(w_i|w_{i-1})}$$

This way we get a sequence of tandems that have meaning tandem-wise. This still is not enough to face a long range dependencies from natural languages, like English. This would be difficult even in case of n-grams as there can be very long sentences with dependencies. However, a 3-gram can get us a pretty nice [approximation](http://tetration.xyz/Ngram-Tutorial/).
```
and how he probably more easily believe me i never see how much as that he and pride and unshackled
```

#### Estimate n-gram probabilities

Estimation can be done with **Maximum Likelihood Estimate (MLE)**:

$$P(w_i|w_{i-1})=\frac{count(w_{i-1},w_i)}{count(w_{i-1	})}$$

<!-- z jupytera:
Z google ngram raw bigram count table
normalize by unigrams -->

So the 2-gram estimate  of sentence probability would be the product of all component tandems ordered as in the sentence.

$$P(w_1,\ldots,w_n) \approx {\displaystyle \prod_{i} P(w_i|w_{i-1})}$$

In practice, the outcome should be represented in *log* form. There are two reasons for this. Firstly, if the sentence is long and the probabilities are really small, then such product might end in arithmetic underflow.  Secondly, adding is faster - and when we use logarithm we know that: $log(a*b) = log(a)+log(b)$, thus:

$log(P(w_1,\ldots,w_n)) \approx {\displaystyle \sum_{i} log(P(w_i|w_{i-1}))}$

This is why the Language Model is stored in logarithmic values.

### Publicly available corpora
There is available [Gutenberg Project](http://www.gutenberg.org/ebooks/search/) providing with text format of some books.

Google also released a publicly available corpus trillion word corpus with over 13 million unique words. It is nice corpus from Google Books with already implemented [N-Gram viewer](https://books.google.com/ngrams) that enables to plot word counts. It includes number of corpora for multiple languages. See the below chart an example of unigram, 2-gram and 3-gram occurrences.

<iframe name="ngram_chart" src="https://books.google.com/ngrams/interactive_chart?content=machine+learning%2Cdeep+learning%2Cnlp%2Cnatural+language+processing&year_start=1982&year_end=2008&corpus=0&smoothing=3&share=&direct_url=t1%3B%2Cmachine%20learning%3B%2Cc0%3B.t1%3B%2Cdeep%20learning%3B%2Cc0%3B.t1%3B%2Cnlp%3B%2Cc0%3B.t1%3B%2Cnatural%20language%20processing%3B%2Cc0" width=860 height=300 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=no></iframe>

Such a large scale text analysis can be done by downloading [each dataset](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html) using the [Ngram Viewer API](https://books.google.com/ngrams/info).

I have created a project to collect and analyze those datasets locally with custom configuration. See the [GitHub repo](https://github.com/MChromiak/MC_Utils) for the source code.

### Language Model evaluation – Perplexity

The good LM should calculate higher probabilities to “real” and “frequently observed” sentences than the ones that are wrong accordingly to natural language grammar or those that are rarely observed.

To make such assumption, we first train the language model on one set and test it on completely new dataset. Then we can compare the results of our model on the new dataset and evaluate, how good (how accurate in terms of a task e.g. translation, spell check etc) **on average** it works on this new, previously unseen dataset. For instance how many words it translates correctly. This way one can compare and decide which language model fits the best to a task. This is called *extrinsic evaluation*.

The extrinsic evaluation approach however, requires multiple tests on models which are expensive. An alternative is the *intrinsic evaluation* which is about testing the LM itself not some particular task or application. The popular intrinsic evaluation is **perplexity**.

As **perplexity** is a bad approximation to an extreme extrinsic evaluation, in cases where the test dataset does NOT look just like the training set. Thus, it is useful only at the early stages of experiment. So later in experiment extrinsic evaluation should also be used.

Best model is the one that best predicts an unseen test set, or assigns on average the probability to all sentences that is sees.

Perprexity metric is the probability of the test set, normalized for the length of the probability by the number of words.

$$ PP(S) = P(w_1,\ldots, w_N)^{-\frac{1}{N}} =\sqrt[\leftroot{0}\uproot{3}N]{\frac{1}{P(w_1,\ldots, w_N)}} = $$

This way the longer the sentence the less probable it will be. Then again by the chain rule:

$$ = \sqrt[N]{{\displaystyle \prod_{i}^{N}\frac{1}{P(w_i|w_1,\ldots, w_{i-1})}}} $$

In case of 2-gram using Markov approximation of the chain rule:

$$ PP(S) =  \sqrt[N]{{\displaystyle \prod_{i}^{N}\frac{1}{P(w_i|w_{i-1})}}}$$

So *perplexity* is a function of probability of the sentence. The meaning of the inversion in perplexity means that whenever we minimize the perplexity we maximize the probability.

Perplexity is weighted equivalent branching factor.

To be continued...
