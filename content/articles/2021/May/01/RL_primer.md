Title: RL Primer
Subtitle: Explaining the fundamental concepts of Reinforcement Learning
Status: published
Category: Reinforcement learning
Date: 2021-05-01 19:30
Modified: 2021-05-01 19:30
Tags: Reinforcement Learning, RL, MDP, Markov Decision Process
Slug: RL-Primer
Related_posts: Decision-Transformer-Reinforcement-Learning-via-Sequence-Modeling-RL-as-sequence
Cover: articles/2021/May/01/img/RL-primer-Cover.jpg
Summary: The objective of RL is to maximize the reward of an agent by taking a series of actions in response to a dynamic environment. Breaking it down, the process of Reinforcement Learning involves these simple steps: Observation of the environment, deciding how to act using some strategy, acting accordingly
Receiving a reward or penalty, learning from the experiences and refining our strategy, iterate until an optimal strategy is found. RL by itself is quite complex area of AI and by this requires some terms to be explained.


### Prerequisite RL knowledge
Here are explained some of the main terms that this paper uses to motivate its goal. Form more details please refer to free online book from [Richard S. Sutton
and Andrew G. Barto Second _Reinforcement Learning: An Introduction_ Edition MIT Press, Cambridge, MA, 2018](http://incompleteideas.net/book/the-book.html)

#### What is _Model-free_ RL?
A “policy”, is a strategy that an agent uses to pursue a goal.

> **TL;DR**
>
> Model-free algorithm:
> estimates the optimal policy without using or estimating the dynamics (transition and reward functions) of the environment.

> Model-based algorithm:
> uses the transition function (and the reward function) in order to estimate the optimal policy.

In an **online RL** there is an *Agent* and the *Environment*. Agent $A$ performs actions $a$ in environment $E$, and the $E$ response with the *reward* $r$ and _observation_ $o$ (or a _state_ $s$ if it is not partially observable environment). Additionally a _policy_ (network) is the algorithm used by the agent to decide its actions. This is the part that can be _model-based_ or _model-free_. Hence, agents gets to actively (interactively) interact with environment to maximize the reward with policy.

Policy can be model-based or model-free. Question is how to optimize the policy network via _policy gradient_ (PG)?

PG algorithms directly try to optimize the policy to increase rewards, however this directly needs correction from environment in online fashion.

#### Markov decision processes (MDP).
MDP is a process with a fixed number of states, and it randomly evolves from one state to another at each step. The probability for it to evolve from state A to state B is fixed.

#### What is _Offline_ RL?
In **offline** RL there is an agent and (instead of interactive environment) a limited, fixed dataset. The dataset contains experience (trajectory rollouts of arbitrary policies) from other scenarios where agents were learning a _policy_ to gain a good _reward_. In contrast to online RL, such setup is more challenging as there is no dynamic environment to test hypothesis, and all is left is to have a set of _trajectories_ without live feedback. By observing historical episodes of interaction from other agents, an offline agent needs to learn a good policy to achieve a high reward.

#### Reward /return

**Reward**
Reward is the quantity received from the environment in a given timestep as a result of an action

**Return**:
Return is defined as a function of reward sequence, which can be:

* simple sum of rewards (also called cumulative reward), or a
* sum of _discounted_ rewards (also called _cumulative future discounted reward_):

<a name="tdr">
$$R_t=r_{t+1}+\gamma r_{t+2}+ \gamma^2 r_{r+3}+\ldots = \sum\limits_{k=0}^{\infty}\gamma^kr_{t+k+1}, \gamma \in [0,1]$$

</a>

* "Cumulative" refers to the summation.
* "Future" refers to the fact that it's an expected value of all the future timesteps values until the end of the episode with respect to the present quantity.
* "Discounted" refers to the "gamma" $\gamma$ _discount rate_ factor, which is a way to adjust the importance of how much we value rewards at future time steps, i.e. starting from $t+1$.
* "Reward" refers to the main quantity of interest, i.e. the reward received from the environment.

The goal of an RL algorithm is to select actions that maximize the expected cumulative reward (the return) of the agent.

#### What is _Credit Assignment_?
In real world RL the state (and action) space usually needs to be very fine to cover all possibly relevant situations. This leads to the combinatorial explosion of states and actions which is referred as _curse of dimensionality_.
As an agent interacts with an environment in discrete timesteps, agent takes an action for current state and the environment emits a perception in form of a _reward_ and an _observation_. In case of fully observable Markov Decision Process (MDP) it is the next state (of the environment and the agents). Agent's goal is to maximize the reward. In such **fine grained** state-action spaces the reward occur terribly temporally delayed.

The (temporal) _credit assignment problem_ (CAP) is the problem of determining the actions that lead to a certain outcome. The problem of determining the contribution of each agent to the result of the training is the (temporal) CAP. In order to maximize the reward in the long run, the agent needs to determine which actions will lead to such outcome, which is essentially the temporal CAP. This way, an action that leads to a higher final cumulative reward should have more _credit_ (value) than an action that lead to a lower final reward. For instance, in Q-learning (the _off-policy_ algorithm) agents attempts to determine actions that will lead to the highest value in each state.

In RL, due to CAP, reward signals will only very weakly affect all temporally distant states that have preceded it. The influence of a reward gets more and more diluted over time and this can lead to bad convergence properties of the RL mechanism. Many steps must be performed by an iterative RL algorithm to propagate the influence of delayed reinforcement to all states and actions that have an effect on that reinforcement.

#### Value functions
Q-Learning is about learning Q-function that takes state and action conditioned on the history to predict future rewards.
VF are state-action pair functions that estimate how good a particular action will be in a given state, or what the return for that action is expected to be.

* **V-function** (State-Value) $v^\pi (s)=  \mathbb{E_\pi} [\sum_{k=0}^T \gamma^k R_{t+k+1} | S_t = s]$ <br > **Value**   of state $s$ under policy/strategy $\pi$. The expected **return** while starting at $s$ and following the $\pi$ thereafter. Shows how good a certain state is, in terms of expected cumulative reward, for an agent following a certain policy. The $\mathbb{E}[.]$ because environment state transition function might act in a stochastic way.
* **Q-function**  (State-Action) $q^\pi (s,a) = \mathbb{E_\pi}[\sum_{k=0}^T \gamma^k R_{t+k+1} | S_t = s, A_t = a]$  <br >**Quality**  of taking action $a$ in state $s$ with policy/strategy $\pi$.  The expected **return** while starting at $s$ while taking action $a$ and following the $\pi$ thereafter. Shows how good action $a$ is, given a state for agent following a policy. The $\mathbb{E}[.]$ because environment state transition function might act in a stochastic way.
* **Q-Value** - value in state-action table.  The Q-function is implemented as a table of states and actions and Q-values for each s,a pair are stored there.

**Estimating** VF for a particular policy, helps to accurately choose an action that will provide the best total reward possible, after being in that given state.

#### Temporal Difference (TD) Learning
_Temporal Difference_ (TD) (aka _bootstrapping_ method) solves the problem of **estimating** [value function](#value-functions). If the value functions were to be calculated **without estimation**, the agent would need to wait until the final reward was received before any state-action pair values can be updated. Once the final reward was received, the path taken to reach the final state would need to be traced back and each value updated accordingly. TD address this issue.

TD learning is a unsupervised, RL model-free method learning by bootstrapping from current estimate of value function. In TD, agent is learning from an environment through episodes with no prior knowledge of the environment. TD methods adjust predictions to match later, more accurate, predictions about the future before the final outcome is known.

Instead of calculating the total future reward, at each step, TD tries to predict the combination of immediate reward and its own reward prediction at the next moment in time.

TD method is called a "bootstrapping" method, because the value is updated partly using an existing estimate and not a final reward.

#### On/Off-policy algorithm
Off-policy algorithm - evaluate and improve a (target) policy that is different from (current) policy which is used for action selection. When passing the reward from the next state to the current state, it takes the maximum possible reward of the new state and ignores whatever policy we are using. Eg. Q-learning is off-policy as it updates its Q-values using the Q-value of the next state and the _greedy_ action. In other words, it estimates the **return** (cumulative/total  [discounted return](#tdr) future reward, starting from current timestep) for state-action pairs assuming a greedy policy were followed, despite the fact that it's not following a greedy policy.

On-policy algorithm - evaluate and improve the same policy which is being used to select actions, Eg. Sarsa  updates its Q-values using the Q-value of the next state and the current policy's action. It estimates the return for state-action pairs assuming the current policy continues to be followed.

#### Action Selection Policies

There are three common policies used for action selection. The aim of these policies is to balance the trade-off between **exploitation** and **exploration**, by not always exploiting what has been learned so far.

* greedy - Will lock on one action that happened to have good results at one point of time but it is not in reality the optimal action. So Greedy will keep exploiting this action while ignoring the others which might be better. It Exploits too much.
* $\epsilon$-greedy - most of the time the action with the highest estimated reward is chosen, called the greediest action. Every once in a while, say with a small probability $\epsilon$, an action is selected at random. The action is selected uniformly, independently of the action-value estimates. This method ensures that if enough trials are done, each action will be tried an infinite number of times, thus ensuring optimal actions are discovered. Explores too much because even when one action seem to be the optimal one, the methods keeps allocating a fixed percentage of the time for exploration, thus missing opportunities and increasing total regret.
* $\epsilon$-soft - very similar to $\epsilon$-greedy. The best action is selected with probability $1 - \epsilon$ and the rest of the time a random action is chosen uniformly.
* softmax - one drawback of $\epsilon$-greedy and $\epsilon$-soft is that they select random actions uniformly. The worst possible action is just as likely to be selected as the second best. Softmax remedies this by assigning a rank, or weight to each of the actions, according to their action-value estimate. A random action is selected with regards to the weight associated with each action, meaning the worst actions are unlikely to be chosen. This is a good approach to take where the worst actions are very unfavorable.

It is not clear which of these policies produces the best results overall. The nature of the task will have some bearing on how well each policy influences learning. If the problem we are trying to solve is of a game playing nature, against a human opponent, human factors may also be influential.


#### Expl**oit**ation vs explo**r**ation
Exploitation - keep the current approach. Chooses the greedy action to get the most reward by exploiting the agent’s current action-value estimates. But by being greedy with respect to action-value estimates, may not actually get the most reward and lead to sub-optimal behaviour.

Exploration - Try new approach.  Allows an agent to improve its current knowledge about each action, hopefully leading to long-term benefit. Improving the accuracy of the estimated action-values, enables an agent to make more informed decisions in the future.

When an agent explores, it gets more accurate estimates of action-values. And when it exploits, it might get more reward. It cannot, however, choose to do both simultaneously, which is also called the exploration-exploitation dilemma.
