Title: Language models: From n-gram counts to neural next-token prediction
Subtitle: Probability, smoothing, cross-entropy, perplexity, and the assumptions behind the numbers
Status: published
Category: Sequence Models
Date: 2017-11-30 19:30
Modified: 2018-01-15 12:00
Tags: NLP, Language Model, N-gram, Perplexity, Smoothing, Neural Networks
Slug: Explaining-Neural-Language-Modeling
Related_posts: Transformer-Attention-is-all-you-need, ernie-2-0
Cover: articles/2017/Nov/30/img/nlp-cover.png
Summary: A language model assigns probabilities to token sequences by predicting each token from its context. This guide derives the chain rule, explains n-gram estimation and smoothing, connects cross-entropy to perplexity, and shows what changes when a neural Transformer replaces the count table.

---

When a phone suggests the next word, a speech recognizer chooses between similar sounds, or a generative model continues a prompt, each system needs a way to judge which token sequence is plausible. A **language model** supplies that judgment by assigning probabilities to sequences.

The modern implementation may contain billions of neural-network parameters, but the underlying probabilistic question is simple:

> Given the tokens observed so far, what distribution should we assign to the next token?

This article starts with count-based n-gram models because they make the assumptions visible. It then connects the same probability factorization to neural language models and Transformers.

## The short version

- A language model estimates $P(w_t\mid w_{<t})$, the probability of the next token given its preceding context.
- The chain rule turns those conditional probabilities into a probability for the complete sequence.
- An n-gram model deliberately shortens the context to the previous $n-1$ tokens.
- Counts alone assign zero probability to unseen sequences, so practical n-gram models redistribute probability through smoothing or backoff.
- Neural language models replace count tables with learned vector representations and functions that can generalize across contexts.
- Cross-entropy is the average negative log-probability of the observed tokens. Perplexity is its exponential.
- Perplexity comparisons are meaningful only when tokenization, test data, and probability conventions are compatible.

## Tokens, types, vocabulary, and corpus

A **corpus** is the collection of text used for training or evaluation. **Tokenization** divides that text into units. A token may be a word, subword, byte, or character; the choice changes both the model and its reported metrics.

A **token** is one occurrence in a sequence. A **type** is a distinct token value, and the set of possible types is the **vocabulary**. In the sentence “a model models text,” there are four word tokens but three types if capitalization and punctuation have already been normalized.

Normalization choices also matter. Lowercasing may merge “Polish” and “polish,” while removing punctuation can destroy useful sentence boundaries. There is no universally correct preprocessing pipeline; it must match the task and the model.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: Why modern models often use subwords or bytes</summary>

A word vocabulary must decide what to do with unseen words, spelling variants, and productive morphology. Subword tokenizers represent a rare word as several reusable pieces. Byte-level models go further and can represent any UTF-8 text without an unknown-token symbol.

The trade-off is sequence length. Smaller units reduce vocabulary problems but create more prediction steps. This is why a perplexity reported for a byte model cannot be compared directly with one reported for a word or subword model.

</details>

## From next-token probabilities to sequence probability

Let a sequence be $w_1,w_2,\ldots,w_N$. The probability chain rule gives an exact factorization:

$$
P(w_1,\ldots,w_N)
= \prod_{t=1}^{N} P(w_t\mid w_1,\ldots,w_{t-1}).
$$

The first factor is unconditional, or conditioned on a start-of-sequence symbol. Later factors condition on progressively longer histories. The equation is not an approximation and does not prescribe a neural network. It only says that a joint probability can be decomposed into conditional probabilities.

This formulation supports several applications. A speech recognizer can prefer a probable sentence among acoustically plausible candidates. A spelling corrector can compare alternative sequences. A generative model samples a token from the predicted distribution, appends it to the context, and repeats.

## The n-gram approximation

Estimating a separate probability for every possible history is impossible: most sequences never occur in a finite corpus. An n-gram model uses a Markov approximation and retains only the previous $n-1$ tokens:

$$
P(w_t\mid w_1,\ldots,w_{t-1})
\approx P(w_t\mid w_{t-n+1},\ldots,w_{t-1}).
$$

A unigram model ignores context. A bigram model uses one preceding token. A trigram model uses two. Increasing $n$ captures longer local patterns but makes each context rarer, increasing the data and memory required for reliable estimates.

For a bigram model, maximum-likelihood estimation uses relative frequency:

$$
\widehat P(w_t\mid w_{t-1})
= \frac{C(w_{t-1},w_t)}{C(w_{t-1})}.
$$

Here $C(\cdot)$ denotes a corpus count. The estimate answers: among occurrences of the previous token, what fraction were followed by the candidate next token?

### Why raw counts are not enough

If a valid bigram never appears in training, the maximum-likelihood estimate assigns it probability zero. Because sequence probability is a product, one unseen n-gram makes the entire sequence probability zero.

**Smoothing** reserves or redistributes probability mass for unseen events. Simple add-one smoothing is useful pedagogically but performs poorly for serious language modeling. Strong classical systems use methods such as interpolation, backoff, and modified Kneser-Ney smoothing, which combine evidence from several context lengths and reason more carefully about how words appear in new contexts.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: Backoff versus interpolation</summary>

A backoff model uses the longest available context and falls back to a shorter one when the longer n-gram lacks reliable evidence. An interpolated model always combines several estimates, for example trigram, bigram, and unigram probabilities, with weights that sum to one.

Both approaches address data sparsity. They differ in when and how shorter-context evidence participates.

</details>

## Why computations use logarithms

Multiplying many probabilities smaller than one quickly underflows floating-point arithmetic. Taking logarithms turns the product into a sum:

$$
\log P(w_1,\ldots,w_N)
= \sum_{t=1}^{N}\log P(w_t\mid w_{<t}).
$$

The log-probability is typically negative. A better prediction assigns the observed token a larger probability and therefore a less negative log-probability.

Training usually minimizes the average **negative** log-probability, also called cross-entropy loss:

$$
H
= -\frac{1}{N}\sum_{t=1}^{N}\log P(w_t\mid w_{<t}).
$$

With natural logarithms, $H$ is measured in nats; with base-2 logarithms, it is measured in bits.

## Perplexity

Perplexity exponentiates the average negative log-probability:

$$
\operatorname{PPL}
= \exp\left(-\frac{1}{N}\sum_{t=1}^{N}\log P(w_t\mid w_{<t})\right)
= P(w_1,\ldots,w_N)^{-1/N}.
$$

Lower perplexity means the model assigned more probability to the observed test sequence. A rough intuition is an effective branching factor: a perplexity of 20 resembles choosing among 20 equally likely options at each step. Real distributions are not uniform, so this is an interpretation rather than a literal count.

Perplexity must be evaluated on data not used for parameter fitting. It is an **intrinsic** metric: it measures predictive fit to that token stream. An **extrinsic** evaluation measures performance on the task that ultimately matters, such as transcription errors, translation quality, retrieval accuracy, or human preference.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: When perplexity comparisons are invalid</summary>

Perplexity depends on the prediction units. A word model, a 32k-subword model, and a byte model produce different numbers of decisions with different vocabularies. Their raw perplexities are not directly comparable.

The test corpus must also match. A model can obtain low perplexity on text similar to its training distribution and perform poorly on another domain. Tokenization, casing, handling of unknown tokens, context length, and whether boundary tokens are scored must be held compatible before interpreting a difference.

</details>

## What a neural language model changes

An n-gram table treats contexts as discrete entries. A neural language model maps tokens to learned vectors and uses a parameterized function to predict the next-token distribution. Similar contexts can therefore share statistical strength even when the exact sequence was not observed.

Early neural language models used a fixed context window. Recurrent networks summarized a variable-length prefix in a hidden state. A [Transformer](/articles/2017/Sep/12/Transformer-Attention-is-all-you-need/) lets each position combine information from earlier positions through causal self-attention.

Despite these architectural differences, autoregressive training still uses the same factorization:

$$
P(w_1,\ldots,w_N)=\prod_{t=1}^{N}P_\theta(w_t\mid w_{<t}),
$$

where $\theta$ denotes learned parameters. The model is trained by minimizing token cross-entropy, usually over many sequences in parallel.

Masked-language-model systems such as BERT and [ERNIE 2.0](/articles/2019/Jul/30/ernie-2-0/) use a related but different objective: they reconstruct selected hidden tokens using context on both sides. That produces useful encoders but is not the same causal distribution used for left-to-right generation.

## What language-model probability does not mean

A high probability does not imply truth. A model estimates regularities in its data and training objective. Common misconceptions, stereotypes, and fluent falsehoods can all receive high probability.

Likewise, a low perplexity does not by itself establish reasoning ability, factual accuracy, safety, or usefulness. Those properties require targeted evaluations. Language modeling is the predictive foundation, not a complete definition of intelligence.

## A practical reading path

1. Use n-grams to understand conditional probability, sparsity, smoothing, and perplexity.
2. Read the [Transformer guide](/articles/2017/Sep/12/Transformer-Attention-is-all-you-need/) to see how attention builds a context-dependent predictor.
3. Study [ERNIE 2.0](/articles/2019/Jul/30/ernie-2-0/) for an example of enriching pre-training with several objectives.
4. Continue to [LoRA](/articles/2023/Mar/18/LoRA-Low-Rank-Adaptation-of-Large-Language-Models/) and [QLoRA](/articles/2023/May/26/QLoRA-Efficient-Finetuning-of-Quantized-LLMs/) to separate pre-training from efficient downstream adaptation.

## Primary references

- Daniel Jurafsky and James H. Martin. [*Speech and Language Processing*, Chapter 3: N-gram Language Models](https://web.stanford.edu/~jurafsky/slp3/), third-edition draft.
- Yoshua Bengio et al. [*A Neural Probabilistic Language Model*](https://www.jmlr.org/papers/v3/bengio03a.html), JMLR, 2003.
- Ashish Vaswani et al. [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762), 2017.
