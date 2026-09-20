Title: Typed Decision Models: Jev and Laya in Agentic AI
Subtitle: How bounded questions turn text into usable probabilities, and where this approach fits beside LLMs
Status: published
Category: Machine Learning / AI Systems
Date: 2026-09-17 12:00
Modified: 2026-09-20 12:00
Tags: Decision Models, Jev, Laya, Agentic AI, Enterprise AI, Calibration, Structured Outputs
Slug: Typed-Decision-Models-Jev-and-Laya-in-Agentic-AI
Related_posts: Transformer-Attention-is-all-you-need, Explaining-Neural-Language-Modeling, RL-Primer
Cover: articles/2026/Sep/17/Typed-Decision-Models-Jev-and-Laya-in-Agentic-AI/img/jev-cover.svg
Summary: Some AI tasks need a bounded judgment, not generated prose. Jev and Laya illustrate how decision models turn textual state and defined answer spaces into probability distributions. This guide explains the shared pattern, where the implementations differ, what their benchmarks establish, and how to evaluate them in an agentic workflow.

---

Imagine a customer writes: “I was charged twice. Please refund the duplicate today.” An AI system may need to draft a reply, but the application first needs narrower judgments: Which team owns the case? Does the policy appear to cover it? How urgent is the message?

Each judgment has an answer space we can define before seeing this particular ticket. That suggests a different interface from asking a language model to write a paragraph: give a model the relevant text, ask a bounded question, and receive a distribution over the permitted answers. **The model interprets language; code decides what to do with the result.**

[Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) and [Laya](https://github.com/NandhaKishorM/laya) are two current examples. They share the broad idea of returning typed decisions rather than prose, but they are different products with different disclosed internals, training evidence, deployment choices, and limits. “Typed decision model” is a useful description of this *task and interface*, not the name of one established neural architecture.

![Editorial cover showing textual state entering a decision model and emerging as bounded probability distributions.]({attach}img/jev-cover.svg)

Figure 1. Shared textual state and defined answer spaces turn a vague automation request into explicit judgments that software can inspect.
{: align=center }

## The decision pattern

The application supplies three things: **state** (the evidence), **questions** (the judgments needed), and **answer spaces** (the allowed outcomes). A model returns answers and probability distributions. Code then checks permissions, applies thresholds and hard rules, and chooses whether to act, ask an LLM, or send the case to a person.

For a choice question, the intended object is a distribution such as $p(y\mid x,q,C)$: the probability of answer $y$ given state $x$, question $q$, and allowed choices $C$. That notation describes the *interface*. It does not imply that every model estimates well-calibrated probabilities or uses the same internal architecture.

Jev names its three question types **Noul**, **Choice**, and **Score**. Laya exposes similarly named typed questions. [TypeSafe primitives](https://docs.typesafe.ai/primitives); [Laya API](https://github.com/NandhaKishorM/laya#decision-primitives).

| Question shape | Example | What the application receives |
| --- | --- | --- |
| **Yes/no (Noul)** | Did the customer request a refund? | A probability for “yes” |
| **Choice** | Which team owns the case? | A selected option and a distribution over the declared options |
| **Ordinal Score** | How urgent is the message? | A position on an ordered rubric and a distribution over its levels |

The word *bounded* matters. A Choice model cannot name a team outside the list we supplied. That is a useful type guarantee, not a correctness guarantee: if `fraud` is missing from the list, the model may confidently choose `billing`. Include `other` or `none_of_the_above` where the list may be incomplete.

<a href="/articles/2026/Sep/17/Typed-Decision-Models-Jev-and-Laya-in-Agentic-AI/" aria-label="Open the canonical typed decision models article by Michał Chromiak"><picture><source media="(max-width: 600px)" srcset="/articles/2026/Sep/17/Typed-Decision-Models-Jev-and-Laya-in-Agentic-AI/img/jev-parallel-flow-mobile.svg?v=20260920" width="720" height="1080"><source media="(prefers-reduced-motion: reduce)" srcset="../img/jev-parallel-flow-static.png?v=20260920" width="1200" height="675"><source media="(min-width: 601px)" srcset="../img/jev-parallel-flow.webp?v=20260920" width="1200" height="675"><img src="{attach}img/jev-parallel-flow-mobile.svg?v=20260920" width="720" height="1080" loading="lazy" decoding="async" alt="A support case and three bounded questions enter a decision model; probability distributions return together, while code keeps the refund rule and action permissions."></picture></a>

Figure 2. The common workflow: reuse relevant state for several bounded judgments, then compose the results in ordinary code. Jev and Laya expose comparable question types, although their implementations are not interchangeable. Sources: [TypeSafe introduction](https://docs.typesafe.ai/introduction) and [Laya README](https://github.com/NandhaKishorM/laya).
{: align=center }

For our duplicate-charge ticket, illustrative outputs might be `billing: 0.94`, `policy appears to permit refund: 0.97`, and an urgency score of `1.7 / 3` with its full level distribution. These are example numbers, not a measured response from either model. Neither model has authorized a refund. Code must still verify the charges, identity, refund limits, and permissions.

Questions sharing the same state can be batched, but dependencies still belong in the workflow. If question B needs the answer to question A, put that answer into a later request or compute the dependency in code. The useful rule is **one semantic judgment per question; composition and side effects in code**.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: Choice, Score, and Noul are not interchangeable</summary>

A **Noul** value of `0.5` means that “yes” and “no” receive equal probability. It does not mean that the underlying property has medium intensity. To represent intensity, use a Score with explicit ordered levels.

A **Choice** assumes the valid outcomes form a fixed set. If the listed options may be incomplete, include `other` or `none_of_the_above`; otherwise the model must select the least-wrong declared option.

A **Score** is a probability-weighted position across two to ten ordered levels. With three zero-indexed levels and probabilities `0.25`, `0.50`, and `0.25`, the returned score is `0×0.25 + 1×0.50 + 2×0.25 = 1.0`. Different distributions can produce that same value, so inspect the distribution when the shape matters. A Score is not a reconstructed dollar amount, duration, or probability of loss.

TypeSafe currently documents up to 255 Choice options, two to ten Score levels, a 64k-token combined request limit, and a 32k-token limit for the state plus the longest question. Those are product limits, not properties of the general idea.

</details>

## Two implementations, one task shape

The shared contract does not make Jev and Laya the same model. TypeSafe calls Jev a **System One Model** and says it uses a new architecture, a parallel sampler, and post-training called Reinforcement Learning for Calibrated Decisions (RLCD). It has not published the neural topology, parameter count, training recipe, or loss. We can describe its documented behavior, not draw its hidden layers. [TypeSafe launch](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

Laya is open-source and more inspectable. Its English and typed-decision checkpoints use a 421-million-parameter ModernBERT-large encoder; its multilingual checkpoint uses a 322-million-parameter mmBERT-base encoder. A question-and-option head scores declared answers without writing a response token by token. The project supplies code, weights, a router, and benchmark scripts. Those assets make local deployment and task-specific fine-tuning possible, but the published results depend strongly on the checkpoint and the task. [Laya repository](https://github.com/NandhaKishorM/laya).

| Design choice | Jev | Laya |
| --- | --- | --- |
| Deployment | TypeSafe's managed API | Open weights and code; run and maintain it yourself |
| Disclosed internals | Parallel sampling and RLCD are described; network architecture is not published | ModernBERT/mmBERT encoder with a typed-option head is documented |
| Typical input budget | TypeSafe documents a 64k-token combined request limit | Default checkpoints use 512 or 1,024 tokens; configuration and encoder capacity differ |
| Adaptation | Versioned provider model | Fine-tune a checkpoint and fit calibration to the target domain |
| Main operational trade-off | Less infrastructure to own, but provider dependence | More control over data and deployment, but model serving and evaluation are yours |

These are **product and deployment differences**, not a verdict about which is universally more accurate. Laya's author published earlier work on fast probability estimates for sales conversations in [2025](https://arxiv.org/abs/2503.23303). That is relevant intellectual history, but it is not evidence that the current Laya checkpoints or Jev's undisclosed architecture existed then.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: What differs inside Laya's checkpoints?</summary>

The `laya` English checkpoint and `laya-typed-decisions` share an encoder family but serve different roles. The latter was fine-tuned on the training split of the typed-decisions benchmark; the base English and multilingual checkpoints perform much worse on that test without specialization. The multilingual checkpoint can handle more scripts, but its quality is not uniform across languages. The router selects a checkpoint before inference rather than trusting a confidently wrong out-of-language answer. [Laya README and benchmark report](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md).

The context figures in the table are documented defaults, not absolute architectural ceilings. Raising a configured limit consumes memory and computation and does not guarantee reliable long-document decisions. Jev's larger advertised request limit likewise says little by itself about accuracy on long, noisy state.

</details>

## Why this differs from asking an LLM

Think of two forms. A generative LLM receives a mostly blank page and writes an answer. A decision model receives a scorecard whose boxes and permitted values are already defined. The distinction concerns the requested output and the work needed to produce it; it does not prove that all decision models share one architecture.

### A conventional LLM generates a sequence

A decoder-style language model assigns probabilities to the next token given the tokens already present. It selects a token, appends it to the sequence, and repeats until the response is complete. This autoregressive process is powerful because a sequence can represent almost anything: prose, code, a plan, a tool call, or structured data.

The flexibility has a cost. Output length adds sequential decoding work. If the result must drive software, the system also needs a contract around the generated sequence. Modern structured-output APIs can constrain an LLM to valid JSON, so malformed output is not inevitable. But the model is still being used as a generator, and application-level uncertainty over the business choices is usually not the native output.

### A decision model scores declared answers

The caller declares yes/no, Choice, or Score answer spaces before inference. Jev says it returns several independent distributions through a parallel sampler; Laya uses a bidirectional encoder and an option-scoring head. Neither has to generate an explanatory paragraph for a bounded judgment. This contrasts with autoregressive output, but not with every possible classifier or structured-output system.

[![Comparison of an autoregressive LLM decoding a token sequence and a bounded decision model scoring declared answers.]({attach}img/jev-vs-llm.svg)]({attach}img/jev-vs-llm.svg)

Figure 3. The visible contrast is sequence generation versus distributions over declared answer spaces. Jev's internals are not public; Laya documents its encoder and head. Sources: [TypeSafe launch](https://typesafe.ai/blog/introducing-system-one-models-and-jev) and [Laya repository](https://github.com/NandhaKishorM/laya).
{: align=center }

The resulting advantages follow from specialization:

- **Less sequential output work.** The model is not decoding a paragraph or JSON document token by token.
- **A bounded result by construction.** Choice cannot invent an option outside the supplied set; Noul remains a yes/no probability; Score remains on the declared rubric.
- **Several questions can share prepared state.** This avoids sending the same evidence in separate sequential calls when the implementation supports batching.
- **Uncertainty is available to policy.** Code can inspect the complete distribution rather than only the winning label.
- **Control flow stays visible.** Thresholds, deterministic rules, permissions, and side effects remain in ordinary software.

These benefits appear when the answer space is known in advance. A narrow interface gives up the ability to write arbitrary strings. It does not automatically give better accuracy, calibration, or latency than a well-built classifier or LLM on a particular workload.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: Why structured-output LLMs are still different</summary>

Constrained decoding can make an LLM emit JSON that conforms to a schema. That solves an important engineering problem, and it means “LLMs always require fragile parsing” is no longer accurate.

The proposed distinction is deeper than JSON syntax: Jev and Laya aim to score bounded answers directly, while a structured-output LLM remains a generator even when decoding is constrained. The LLM remains useful when a schema contains generated strings or the task requires flexible reasoning before filling it.

Compare the complete workload rather than the interface label: quality, latency, cost, stability, usefulness of the probabilities, and integration effort.

</details>

## What the probabilities mean

Both products return numbers that look like probabilities. To **calibrate** them, we need a population of cases with known outcomes. Think of a weather forecast: among days labelled “80% chance of rain,” rain should occur roughly 80% of the time. The analogous test groups model decisions assigned probability `0.8` and checks their observed frequency.

Calibration says nothing certain about a single case. A ticket routed to `billing` with probability `0.8` can still belong to `fraud`. The schema only guarantees that the answer is one of the declared choices; it does not guarantee that the chosen answer is correct.

Jev's Choice and Score responses also include `confidence`, a scalar derived from the distribution's shape. A concentrated distribution has higher confidence than a flat one; Noul already supplies a yes/no probability. Laya uses comparable field names, but equal-looking fields do not establish equal calibration across providers. [TypeSafe confidence semantics](https://docs.typesafe.ai/confidence); [Laya API](https://github.com/NandhaKishorM/laya#decision-primitives).

Compare two Choice results:

```text
A: billing 0.94 | technical 0.05 | other 0.01
B: billing 0.40 | technical 0.35 | other 0.25
```

Both select `billing`, but they tell different stories. Result A is concentrated around one answer. Result B is almost a three-way contest and should be treated more cautiously. Looking only at the winning label would hide that difference.

Four related quantities are easy to confuse:

- **Probability** belongs to an outcome, such as `P(refund permitted) = 0.83`.
- **Confidence** may summarize how concentrated a multi-option distribution is; inspect each provider's definition.
- **Correctness** is established only by comparing the prediction with an appropriate reference outcome.
- **Calibration** asks whether probability estimates match frequencies over many cases.

TypeSafe describes RLCD as post-training for calibrated decisions but did not publish a cross-domain calibration study with its launch. Laya reports calibration tests and also says its base checkpoints are overconfident as shipped; its stronger expected-calibration-error result follows temperature fitting on held-out data. That fitting is a deployment step, not an intrinsic guarantee. [TypeSafe's RLCD primer](https://docs.typesafe.ai/introduction/machine-learning-primer); [Laya benchmark report](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md).

Treat either product's probabilities as estimates to validate on representative labelled traffic. Recheck them after changing the model, prompt/schema, language, or application domain. If the cost of a false positive is high, compare decisions and uncertainty at the threshold that actually controls the workflow, not only overall accuracy.

## What the comparisons actually show

There is no single “Jev versus Laya” number. A vendor workflow, a fine-tuned checkpoint on a matching training split, and a fresh third-party task set answer different questions. Read each result with its task, model version, hardware, and reference labels attached.

### Jev against LLM workflows

TypeSafe publishes four workflow evaluations: security incidents, agent-trace observability, invoice processing, and customer service. Each one turns a business policy into narrow model questions plus deterministic code, then runs the same workflow with Jev and several LLMs. [Interactive workflow evaluations](https://evals.typesafe.ai/).

In Figure 4, moving right means spending more per case and moving up means agreeing more often with TypeSafe's reference. The most attractive region is therefore the upper-left corner.

[![Scatterplot of agreement with TypeSafe's model-derived reference versus reported cost per case. Jev is far left at 67.8 percent and 0.0004 dollars, while several LLM workflows show similar or higher agreement at higher cost.]({attach}img/jev-workflow-eval-replot.svg)]({attach}img/jev-workflow-eval-replot.svg)

Figure 4. Jev reports 67.8% mean agreement at $0.0004 and 0.4 seconds per case. GPT-5.6 Terra reports 67.9% at $0.0304 and 10.1 seconds; GPT-5.6 Sol reports 74.1% at $0.0836 and 23.3 seconds. Data: [TypeSafe workflow evals](https://evals.typesafe.ai/), accessed September 17, 2026.
{: align=center }

Jev sits far to the left while remaining close to several LLM configurations on the vertical axis. The clearest pair is Jev and GPT-5.6 Terra: their reported agreement differs by only 0.1 percentage point, while Terra costs about 76 times more and takes about 25 times longer per case using the rounded values shown. That comparison applies to these four bounded decision workflows, not to the open-ended generation and reasoning tasks that Jev cannot perform.

The vertical axis is **agreement**, not independently annotated accuracy. TypeSafe constructs its reference by averaging answers from GPT-6 Astra and Claude Fable 5.1 at high thinking. Its own model-capabilities team wrote the workflows, and each non-reference model uses its provider's default reasoning setting. Laya was not part of this evaluation. These choices make the plot a useful Jev-versus-LLM vendor demonstration, not a Jev-versus-Laya leaderboard.

<details class="dinov2-background" markdown="1">
<summary>Optional detail: Per-workflow results and methodology</summary>

The aggregate gives all four workflows equal weight. Jev's displayed per-workflow results are:

| Workflow | Reference agreement | Reported cost per case | Reported time per case |
| --- | ---: | ---: | ---: |
| Security incidents | 61.7% | $0.0001 | 0.3 s |
| Agent-trace observability | 71.6% | $0.0003 | 0.5 s |
| Invoice processing | 61.8% | $0.0011 | 0.5 s |
| Customer service | 76.0% | $0.0001 | 0.4 s |

The spread matters. Invoice processing, for example, is a case where several LLM workflows score materially higher than Jev. An aggregate should not become a service-level promise for a different domain.

Latency was measured by TypeSafe from laptops on the US West Coast, where its service was hosted. Costs use provider prices at evaluation time. TypeSafe acknowledges possible workflow bias and that its largest advertised gains are likely at the high end of real-world results. Its homepage multipliers also depend on the selected comparator and workload, so the per-model values above are more informative than one universal speedup claim.

</details>

### What Laya adds, and what it does not establish

The Laya project reports `0.766` top-label accuracy on 2,000 typed decisions for a checkpoint **fine-tuned on that benchmark's training split**, compared with a published Jev result of `0.727`. Its base English and multilingual checkpoints score `0.362` and `0.342` on the same test, below the reported `0.461` majority-class baseline. The improvement is evidence that specialization matters, not that any Laya checkpoint beats Jev out of the box. The Jev figure was imported from another run, so prompts and sample conditions were not identical. [Laya results and caveats](https://github.com/NandhaKishorM/laya/blob/main/README.md#benchmarks).

The distribution-level picture differs from the winning-label picture. On that typed-decisions comparison, Jev has higher reported *soft accuracy* against the reference distributions (`0.580` versus `0.471`), while Laya's fine-tuned checkpoint has better reported top-label accuracy. Laya's raw calibration error on this set is higher (`0.213` versus Jev's published `0.144`); the stronger Laya calibration headline uses additional temperature fitting. These figures should not be collapsed into “better probabilities.” [Laya benchmark report](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md).

An independent check points the other way on broader tasks. [JevBench v1.2](https://github.com/fstandhartinger/jevbench/blob/main/RESULTS-v1.2.md) ranks Jev above the tested base Laya English checkpoint on its mixed decision suite. That Laya run used default 512-token question budgets and CPU inference, so it neither measures the specialized typed-decisions checkpoint nor fairly compares local GPU latency with Jev's hosted API. It does show why a result on one trained task should not be generalized to long policies and unfamiliar questions.

Laya also reports short local GPU inference times; Jev reports end-to-end hosted latency. Those are different measurement boundaries. A decision between them needs a same-task test at your own serving boundary, including network, batch size, cold starts, model hosting cost, and human-review volume.

## Where decision models fit in an agent stack

A bounded decision model is not an agent: it does not own a goal, generate a plan, write a customer message, or operate tools. Its role is a **semantic decision layer** between unstructured evidence and code that controls a workflow. Jev and Laya are candidates for this layer, not a reason to replace every existing rule or classifier.

Consider a support agent. The LLM may need to synthesize a conversation, retrieve evidence, draft a response, and propose an approved tool call. A decision model can sit at narrower boundaries:

- before the LLM, classify intent and choose the appropriate specialist;
- after retrieval, score passages for relevance, contradiction, or prompt injection;
- before a tool call, judge whether the request matches policy and whether review is needed;
- after generation, verify that a response addresses the request or that cited evidence supports a claim;
- after the run, triage the trace for silent failures and prioritize human review.

<a href="/articles/2026/Sep/17/Typed-Decision-Models-Jev-and-Laya-in-Agentic-AI/" aria-label="Open the canonical typed decision models article by Michał Chromiak"><picture><source media="(max-width: 600px)" srcset="/articles/2026/Sep/17/Typed-Decision-Models-Jev-and-Laya-in-Agentic-AI/img/jev-enterprise-routing-mobile.svg?v=20260920" width="720" height="1130"><source media="(prefers-reduced-motion: reduce)" srcset="../img/jev-enterprise-routing-static.png?v=20260920" width="1200" height="675"><source media="(min-width: 601px)" srcset="../img/jev-enterprise-routing.webp?v=20260920" width="1200" height="675"><img src="{attach}img/jev-enterprise-routing-mobile.svg?v=20260920" width="720" height="1130" loading="lazy" decoding="async" alt="Enterprise workflow: code prepares relevant state, a bounded decision model supplies judgments, and explicit risk rules route work to code, an LLM, or human review before controlled tools act and outcomes are logged."></picture></a>

Figure 5. Code owns state preparation, policy, permissions, and side effects. A decision model supplies bounded judgments; LLMs generate and reason; people handle uncertain or high-impact exceptions. The layout is a conceptual application pattern, not a claim about either model's internals. Sources: TypeSafe's [system-design guidance](https://docs.typesafe.ai/concepts/how-to-build-with-system-one) and [intent-routing pattern](https://docs.typesafe.ai/patterns/intent-routing).
{: align=center }

Follow one request through the diagram. Code first retrieves the customer record and relevant policy, calculates exact values such as dates and amounts, and removes unrelated history. The model then scores intent, policy fit, risk, and urgency. A routine order-status request can go to deterministic code only after hard checks; a product question can go to a specialist LLM; an uncertain complaint can go to a person. The thresholds remain visible in code rather than buried in an agent prompt.

Batching can also reduce sequential agent loops. As one product-specific example, TypeSafe's regulatory-document cookbook reports that one Jev call with 13 independent questions was 12.2 times cheaper and 10.0 times faster than thirteen sequential calls, with similar outputs across five repeats. Concurrent calls would narrow that latency comparison. Laya also batches questions, but its throughput must be measured separately on the chosen hardware. [TypeSafe cookbook](https://docs.typesafe.ai/cookbooks/parallel_questions); [Laya speed measurements](https://github.com/NandhaKishorM/laya#speed-tesla-t4-measured).

## Which tool should do which job?

| Need | Best starting point | Reason |
| --- | --- | --- |
| Exact arithmetic, date comparison, database lookup, authorization, hard policy | **Code** | Deterministic, testable, auditable, and usually cheaper |
| Bounded semantic classification, scoring, routing, or verification over text | **Decision model candidate** | Typed distributions over declared outcomes; compare Jev, Laya, and conventional classifiers on your task |
| Explanation, conversation, synthesis, planning, code, or any open-ended output | **LLM** | Generative flexibility is the requirement, not overhead |
| Ambiguous, novel, regulated, or high-impact exception | **Human review** | Accountability and contextual judgment outweigh automation speed |
| A real enterprise process | **A deliberate combination** | Different stages have different accuracy, latency, control, and accountability needs |

A useful test is: **Can I enumerate the valid answer space before seeing the case?** If yes, and the hard part is a semantic judgment over text, test a decision model against a conventional classifier and a structured-output LLM. If the output must contain new language, a novel plan, or a chain of reasoning, use an LLM. If code can calculate the answer exactly, do not call a model.

## The same task through two APIs

The two APIs are not drop-in replacements. The Jev SDK expresses each question with a Python class; Laya takes a dictionary and can run locally. Both can provide judgments to the *same application-owned* policy. Here is the Jev form, using the official Python SDK:

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

state = {
    "message": "I was charged twice. Please refund the duplicate today.",
    "charges": [
        {"amount_usd": 49, "status": "captured"},
        {"amount_usd": 49, "status": "captured"},
    ],
    "policy": "Verified duplicate charges are eligible for a refund.",
}

with TypeSafeClient() as client:
    result = client.system_one(
        state=state,
        questions={
            "owner": Choice(
                instructions="Which team owns the primary issue?",
                criteria={
                    "billing": "Charges, invoices, refunds, or subscriptions.",
                    "technical": "Product failures or errors.",
                    "account": "Login, permissions, or account security.",
                    "other": "None of the listed teams fits.",
                },
            ),
            "refund_allowed": Noul(
                instructions="Does `policy` permit the refund requested in `message`, given `charges`?"
            ),
            "urgency": Score(
                instructions="How urgent is the request expressed in `message`?",
                criteria=[
                    "Routine: no stated deadline or ongoing harm.",
                    "Time-sensitive: the customer asks for prompt resolution.",
                    "Urgent: delay is causing material harm.",
                    "Critical: immediate intervention is required.",
                ],
            ),
        },
    )

owner = result.answers["owner"]
refund_probability = result.answers["refund_allowed"].noul

if owner.choice == "billing" and refund_probability > 0.90:
    queue_duplicate_refund_for_policy_checks(state)
else:
    route_to_review(state, result)
```

The model interprets language. Code still verifies identity, compares charge amounts, enforces authorization, applies refund limits, records the action, and makes it idempotent. A high model probability must never become a substitute for transaction controls.

Laya expresses a similar request with dictionary schemas. This abbreviated example shows the interface rather than a validated refund policy: [Laya quickstart](https://github.com/NandhaKishorM/laya#quickstart-route-mode-recommended).

```python
from laya import Router

router = Router()
decision = router.predict(
    state,
    {
        "owner": {
            "type": "choice",
            "instructions": "Which team owns the primary issue?",
            "criteria": {
                "billing": "charges, invoices, refunds, or subscriptions",
                "technical": "product failures or errors",
                "account": "login, permissions, or account security",
                "other": "none of the listed teams fits",
            },
        },
        "refund_requested": {
            "type": "noul",
            "instructions": "Does the customer explicitly request a refund?",
        },
    },
)
owner = decision["answers"]["owner"]["choice"]
```

The snippets ask related, not byte-identical, questions. A fair production comparison would normalize both providers' outputs, use one frozen question set and policy, and evaluate the resulting decisions against the same labelled cases.

## Failure modes that matter in production

The shared interface brings shared engineering hazards, while each model adds its own. TypeSafe's [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) and Laya's [documented limits](https://github.com/NandhaKishorM/laya#honest-limits) suggest five boundaries:

1. **Keep exact work in code.** Jev documents weaknesses in numerical precision, counting, and date comparison; a small encoder is not a substitute for exact computation either. Parse timestamps, calculate amounts, check authorization, and enforce hard limits deterministically.
2. **Prepare focused, untrusted state.** Retrieve only the evidence needed for the question. Test adversarial content and prompt injection because text inside the state can influence the result.
3. **Leave room for “none of the above.”** A closed Choice with an incomplete option list forces the model to select the least-wrong answer.
4. **Validate and version the decision boundary.** Measure precision, recall, coverage, calibration, and business cost. Pin the Jev model version or Laya checkpoint and record any local calibration fit used to set a threshold.
5. **Engineer the surrounding service.** A hosted API needs timeouts, retries, and fallback behavior; a local checkpoint needs serving capacity, cold-start planning, and monitoring. Both need human queues and reversible side effects. Log state and schema versions, distributions, routes, overrides, tool outcomes, and eventual business results.

Neither model returns a natural-language rationale. That avoids mistaking fluent prose for evidence, but it does not make a system auditable by itself. The audit trail comes from versioned inputs, explicit criteria, probabilities, policy code, and observed outcomes.

## How to evaluate a decision model in your workflow

Begin with one decision, not an entire agent. Define its allowed outputs, the business cost of each error, and which cases must always reach a person. Build a labelled set that includes common traffic, rare classes, ambiguity, missing evidence, and adversarial examples.

Next, compare complete implementations: deterministic rules, a conventional classifier, a structured-output LLM, Jev, a suitable Laya checkpoint, and any useful hybrid. Use the same held-out inputs and downstream policy for each. Alongside per-class precision and recall, measure calibration, latency percentiles, infrastructure and API cost, and the share of cases sent to human review. Separate zero-shot tests from tests after task-specific fine-tuning; report both if both matter.

Run the preferred design in shadow mode before it can act. Compare its decisions with real outcomes and reviewer choices. When it goes live, begin with reversible, low-impact actions and continue monitoring input drift, confidence distributions, overrides, provider errors, version changes, and downstream outcomes.

Low-cost decision calls could make per-item checks practical across retrieved passages, proposed tool calls, generated outputs, and completed traces. Their value still depends on explicit policy, domain evaluation, observability, and safe fallbacks.

## The practical takeaway

The useful idea is broader than either product: many steps in an AI workflow need a bounded judgment, not another paragraph. Jev packages that as a managed decision API; Laya offers an inspectable, adaptable local route. Both make the answer space explicit and expose distributions to code. Neither should be selected from a single vendor graph or a mismatched benchmark.

Give each part of the system the job it handles best: code performs exact work and controls actions, a tested decision model interprets text into bounded answers, LLMs generate and reason, and people resolve consequential uncertainty. The model at the decision step can change without handing it authority over the rest of the workflow.

## Related reading

For the mechanism bounded decision models avoid at output time, [Transformer: Attention Is All You Need]({filename}../../../2017/Sep/12/2017_09_12_Transformer-Attention-is-all-you-need.md) explains the architecture underlying modern sequence models, while [Explaining neural language modelling]({filename}../../../2017/Nov/30/2017_11_30_Explaining-Language-Modeling.md) develops next-token prediction from first principles.

For a different view of decision-making systems, [Reinforcement learning: a practical primer]({filename}../../../2021/May/01/RL_primer.md) explains states, actions, rewards, values, and policies. A bounded judgment model is not itself an RL agent: it does not own goals, environmental actions, or long-horizon credit assignment.

## Primary sources

- Diogo Almeida. [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), TypeSafe AI, September 15, 2026. Primary launch description, disclosed components, company benchmarks, and caveats.
- TypeSafe AI. [Introduction](https://docs.typesafe.ai/introduction), [System One](https://docs.typesafe.ai/concepts/system-one), and [Primitives](https://docs.typesafe.ai/primitives). Public interface and answer semantics.
- TypeSafe AI. [AI primer: RLCD and calibrated decisions](https://docs.typesafe.ai/introduction/machine-learning-primer) and [Confidence](https://docs.typesafe.ai/confidence). Definitions of calibration, probability, and confidence.
- TypeSafe AI. [Workflow evals](https://evals.typesafe.ai/). Interactive aggregate and per-workflow measurements, methodology, and reference construction.
- TypeSafe AI. [How to build with System One](https://docs.typesafe.ai/concepts/how-to-build-with-system-one), [Intent routing](https://docs.typesafe.ai/patterns/intent-routing), and [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions). Official workflow patterns and batching example.
- TypeSafe AI. [Jev 1.13 known limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) and [Models and pricing](https://docs.typesafe.ai/models). Version-specific failure modes, aliases, limits, and dated pricing.
- TypeSafe AI. [Official Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) and [JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js). MIT-licensed client implementations and public request/response types.
- Nandakishor Mukkunnoth and Convai Innovations. [Laya repository](https://github.com/NandhaKishorM/laya), [benchmarks and reproduction notes](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md), and [model checkpoints](https://huggingface.co/convaiinnovations/laya). Primary documentation for the open implementation, its training-specific results, limits, and code.
- Nandakishor Mukkunnoth. [SalesRLAgent](https://arxiv.org/abs/2503.23303), March 2025. Earlier, domain-specific probability-prediction work; not a paper describing the current Laya architecture.
- Benchmark Heaven. [JevBench v1.2 results](https://github.com/fstandhartinger/jevbench/blob/main/RESULTS-v1.2.md). Independent, versioned decision-task comparison; its CPU Laya run is not a matched GPU serving test.
