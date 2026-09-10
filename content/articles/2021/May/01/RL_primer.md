Title: Reinforcement learning: A practical primer on agents, returns, values, and policies
Subtitle: The concepts and equations needed to reason about online, offline, model-free, and model-based RL
Status: published
Category: Reinforcement learning
Date: 2021-05-01 19:30
Modified: 2021-06-15 12:00
Tags: Reinforcement Learning, RL, MDP, Value Functions, Temporal-Difference Learning, Offline RL
Slug: RL-Primer
Related_posts: Decision-Transformer-Reinforcement-Learning-via-Sequence-Modeling-RL-as-sequence, Transformer-Attention-is-all-you-need
Cover: articles/2021/May/01/img/RL-primer-Cover.jpg
Summary: Reinforcement learning trains an agent to make sequential decisions whose consequences may arrive much later. This primer builds the essential vocabulary, derives return and value functions, explains Bellman and temporal-difference learning, and distinguishes online from offline and model-free from model-based RL.

---

In supervised learning, each training example normally comes with a target. Reinforcement learning (RL) poses a different problem: an **agent** acts, observes the consequences, and must discover which decisions produce good long-term outcomes.

That delay changes everything. A move can look harmless now but determine success many steps later. RL therefore needs a language for trajectories, return, value, uncertainty, and exploration.

## The short version

- At time $t$, an agent observes a state or observation, chooses an action, and receives a reward from the environment.
- A **policy** maps the information available to the agent to a distribution over actions.
- The goal is to maximize expected **return**, not necessarily the next immediate reward.
- Value functions estimate future return from a state or state-action pair.
- Model-free methods learn values or policies without using an explicit transition model; model-based methods use such a model for prediction or planning.
- Online RL gathers new experience while learning. Offline RL learns from a fixed dataset and cannot repair poor coverage by exploring.
- Temporal-difference methods learn before an episode ends by using one estimate to update another.

## The interaction loop

At each time step, the environment is in state $S_t$. The agent selects action $A_t$ according to its policy $\pi$. The environment then emits reward $R_{t+1}$ and moves to state $S_{t+1}$:

$$
S_t \xrightarrow{A_t} (R_{t+1}, S_{t+1}).
$$

A **policy** may be deterministic, $a=\pi(s)$, or stochastic, $\pi(a\mid s)=P(A_t=a\mid S_t=s)$. It is the agent's decision rule. The policy itself is not an environment model.

<details class="dinov2-background" markdown="1">
<summary><strong>State or observation?</strong></summary>

A state contains the information needed to predict the next transition, given an action. In a fully observed Markov decision process, the agent receives that state directly. In a partially observed problem, it receives an observation $O_t$ that may omit relevant information. The agent may then need a history or learned memory to estimate the hidden state.

</details>

## Markov decision processes

A discounted Markov decision process (MDP) is commonly written as

$$
\mathcal{M}=(\mathcal{S},\mathcal{A},p,r,\gamma),
$$

where $\mathcal{S}$ is the state space, $\mathcal{A}$ the action space, $p(s'\mid s,a)$ the transition distribution, $r$ the reward rule, and $\gamma\in[0,1]$ the discount factor.

The **Markov property** says that the present state is sufficient for predicting the next state and reward:

$$
P(S_{t+1},R_{t+1}\mid S_0,A_0,\ldots,S_t,A_t)
=P(S_{t+1},R_{t+1}\mid S_t,A_t).
$$

This does not require deterministic transitions. The same state-action pair may lead to several outcomes with different probabilities.

## Reward is local; return is cumulative

A reward $R_{t+1}$ is the scalar feedback received after action $A_t$. The **return** $G_t$ combines rewards from the remainder of the trajectory:

$$
G_t=R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\cdots
=\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}.
$$

The discount factor controls how strongly distant rewards contribute. In continuing tasks, $\gamma<1$ also keeps a bounded reward sequence from producing an infinite return. In finite episodic tasks, $\gamma=1$ may be appropriate.

Maximizing immediate reward can be shortsighted. An agent may need to accept a small cost now to reach a much better outcome later. RL usually seeks a policy that maximizes expected return.

## The credit-assignment problem

Suppose a long sequence ends with one success signal. Which earlier decisions deserve credit? This is **temporal credit assignment**: connecting delayed outcomes to the actions that helped cause them.

Long delays make learning difficult because the useful signal must propagate across many steps. They should not be confused with the **curse of dimensionality**, which concerns the rapid growth of a problem's state or action space. A task can suffer from either or both.

## Value functions

For a policy $\pi$, the state-value function is the expected return after starting in state $s$ and then following $\pi$:

$$
v_\pi(s)=\mathbb{E}_\pi[G_t\mid S_t=s].
$$

The action-value function additionally fixes the first action:

$$
q_\pi(s,a)=\mathbb{E}_\pi[G_t\mid S_t=s,A_t=a].
$$

These are mathematical functions, not necessarily tables. Small discrete problems can store one value per state or state-action pair; larger problems approximate them with linear models or neural networks.

In an MDP, $q_\pi(s,a)$ need not condition on the full history because the state already carries the information required by the Markov property. History or memory becomes relevant when observations are partial.

## Bellman equations: one step plus the future

Value functions have a recursive structure. For example, the Bellman expectation equation for $v_\pi$ is

$$
v_\pi(s)=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma v_\pi(s')\right].
$$

The value of the current state equals the expected immediate reward plus the discounted value of the next state. Dynamic programming uses this relation with a known model. Temporal-difference learning estimates the same structure from sampled transitions.

## Temporal-difference learning

Monte Carlo methods wait for an episode to finish and use the observed return as a target. **Temporal-difference (TD) learning** can update after one transition. The TD(0) update is

$$
V(S_t)\leftarrow V(S_t)+\alpha
\left[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\right],
$$

where $\alpha$ is the learning rate. The expression in brackets is the **TD error**. The target $R_{t+1}+\gamma V(S_{t+1})$ contains another estimate, so TD is described as **bootstrapping**.

TD learning is not unsupervised learning in the usual representation-learning sense. It is an RL method whose training signal comes from rewards and successive predictions rather than externally supplied class labels.

## Model-free and model-based RL

A **model** predicts aspects of the environment, typically transitions and rewards. The distinction concerns how an algorithm uses environment dynamics:

- **Model-free RL** learns a policy or value function without using an explicit transition model for planning. Q-learning and many policy-gradient methods are model-free.
- **Model-based RL** uses a known or learned model to evaluate possible futures, plan actions, create synthetic experience, or improve a policy.

A learned policy can be a neural network in either family. Likewise, learning a model does not help unless the algorithm uses it effectively, and model errors can compound during long imagined rollouts.

## Online and offline RL

In **online RL**, the learner gathers new transitions by interacting with the environment. Its choices affect the data it will see next, so exploration is part of learning.

In **offline RL**, learning uses a fixed dataset of transitions or trajectories produced earlier by one or more behavior policies. The learner cannot request new examples. The central difficulty is **distribution shift**: a learned policy may choose actions that are poorly represented in the dataset, where value estimates are unreliable.

Offline RL is therefore not simply supervised imitation. A dataset may contain mixed-quality behavior, and the objective is usually to find a high-return policy without deploying exploratory actions during training.

## On-policy and off-policy learning

The **behavior policy** generates experience. The **target policy** is the policy being evaluated or improved.

- An **on-policy** method learns about the same policy that produces its data. SARSA updates toward the next action actually selected by that policy.
- An **off-policy** method can learn about a target policy from data generated by another policy. Q-learning updates toward the greedy next action even when its behavior includes exploration.

For tabular control, their one-step targets make the distinction concrete:

$$
\text{SARSA target}=R_{t+1}+\gamma Q(S_{t+1},A_{t+1}),
$$

$$
\text{Q-learning target}=R_{t+1}+\gamma\max_a Q(S_{t+1},a).
$$

## Exploration and exploitation

**Exploitation** selects actions that currently appear best. **Exploration** gathers information that may reveal a better choice. Pure exploitation can lock onto an early mistake; indiscriminate exploration can waste reward.

Common action-selection rules include:

- **Greedy:** choose an action with the highest estimated value.
- **$\epsilon$-greedy:** with probability $1-\epsilon$, choose a greedy action; with probability $\epsilon$, choose uniformly from all actions. This is an $\epsilon$-soft policy because every action has nonzero probability.
- **Softmax or Boltzmann exploration:** sample actions with probabilities derived from their estimated values and a temperature parameter.

There is no universally best exploration rule. The right mechanism depends on the cost of mistakes, uncertainty, horizon, and whether the learner is allowed to interact at all.

## How this connects to sequence modeling

An RL trajectory is an ordered sequence of states, actions, and rewards. The [Decision Transformer](/articles/2021/Jun/01/Decision-Transformer-Reinforcement-Learning-via-Sequence-Modeling-RL-as-sequence/) uses that representation to turn offline policy learning into conditional sequence modeling: given a desired return and recent trajectory context, it predicts the next action.

That perspective is useful, but it does not remove the RL problem. Dataset coverage, return conditioning, and evaluation in the environment still determine what behavior can be learned.

## A compact mental model

1. The environment defines what transitions and rewards are possible.
2. The policy defines how the agent chooses actions.
3. Return specifies the long-term quantity to optimize.
4. Value functions predict that return before the future is known.
5. Bellman relations connect present estimates to the next step.
6. The learning setting determines what evidence is available: live interaction online or fixed experience offline.

## Primary references

- Richard S. Sutton and Andrew G. Barto. [*Reinforcement Learning: An Introduction*, second edition](http://incompleteideas.net/book/the-book-2nd.html), 2018.
- Sergey Levine et al. [*Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems*](https://arxiv.org/abs/2005.01643), 2020.
- Lili Chen et al. [*Decision Transformer: Reinforcement Learning via Sequence Modeling*](https://arxiv.org/abs/2106.01345), 2021.
