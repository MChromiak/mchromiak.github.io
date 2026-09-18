# Jev by TypeSafe AI: primary-source research note

**Research date:** 2026-09-17
**Scope:** TypeSafe AI's official website, documentation, evaluation site, and official GitHub repositories only.
**Status:** Jev was announced on 2026-09-15 and is in early access. Treat current model names, prices, limits, and measurements as a dated snapshot.

## Executive assessment

Jev is a hosted, text-input decision model. A caller supplies application state and one or more typed questions; Jev returns bounded, machine-readable judgments and probability distributions rather than generated prose. TypeSafe calls this model class **System One Models** and describes Jev as its first public example. The most defensible shorthand is:

> **Textual state + predefined questions in; typed probabilistic judgments out. Code remains responsible for control flow, exact computation, and actions.**

This is not merely an LLM API wrapped in JSON mode according to TypeSafe: the company says it developed a new model architecture, a parallel sampler, and a training method called Reinforcement Learning for Calibrated Decisions (RLCD). However, it has **not disclosed the neural architecture, parameter count, base model, training objective, RL algorithm, training-set composition, hardware, or an architecture paper**. The article must not invent an encoder, classification heads, a one-forward-pass mechanism, or any other internal diagram. A diagram can show the documented interface and parallel evaluation behavior, with the model interior explicitly marked **undisclosed**.

TypeSafe's four company-authored workflow evaluations show a strong speed/cost result, but they are not independent benchmarks or human-labeled ground truth. The reference labels are averages of GPT-6 Astra and Claude Fable 5.1 at high thinking. TypeSafe itself says the workflows were made by its model-capabilities team, acknowledges possible bias, and calls the advertised `193.6x faster` and `444.6x cheaper` figures the high end of likely real-world gains. The correct presentation is therefore **"TypeSafe reports... on its workflow evals"**, followed immediately by the methodology and caveats.

## 1. What Jev does

### Verified public interface

TypeSafe describes Jev as evaluating typed questions against a shared state without generating text or requiring response parsing. State can be a string, a JSON object, or an array containing text values. Jev currently accepts text only; it does not accept images, audio, or video. [Introduction](https://docs.typesafe.ai/introduction), [System One](https://docs.typesafe.ai/concepts/system-one), [State](https://docs.typesafe.ai/concepts/state)

The public API exposes three question/answer primitives:

| Primitive | Intended judgment | Returned data | Important semantics |
| --- | --- | --- | --- |
| **Noul** | Is a proposition true? | `noul` in `[0, 1]` | Probability assigned to "yes"; no separate confidence field. A value near `0.5` means yes/no uncertainty, not a medium amount of a property. |
| **Choice** | Which member of a fixed, unordered set fits? | selected `choice`, full `probabilities`, `confidence` | Selected choice is the highest-probability option; probabilities sum to 1; up to 255 options. Include `other`/`none` if the list may be incomplete. |
| **Score** | Where does the state lie on an ordered, descriptive rubric? | fractional `score`, `legend`, full `probabilities`, `confidence` | Supports 2-10 levels. `score` is the probability-weighted mean of zero-based level positions, so different distributions can yield the same score. It is not a reconstructed physical quantity. |

Sources: [Primitives](https://docs.typesafe.ai/primitives), [Noul](https://docs.typesafe.ai/primitives/noul), [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score).

All questions in one request see the same state, are evaluated independently, and are processed in parallel. TypeSafe says adding questions "barely changes" response time, though each extra question still consumes input tokens. Independent evaluation also means one answer cannot depend on another answer in the same call; dependent stages require a follow-up request or code composition. [Introduction](https://docs.typesafe.ai/introduction), [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out)

The documented context limits for Jev 1.13 are:

- 64,000 tokens across the state and all questions;
- 32,000 tokens for the state plus the longest single question.

Source: [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

### Minimal example for the article

The official SDKs make the contract concrete. A support system can provide a ticket as state and ask, in one request:

```python
questions = {
    "refund_requested": Noul(
        instructions="Does the customer explicitly request a refund?"
    ),
    "owner": Choice(
        instructions="Which team should handle the primary issue?",
        criteria={
            "billing": "Charges, invoices, refunds, subscriptions",
            "technical": "Product failures or errors",
            "account": "Login, permissions, or security",
            "other": "None of the listed teams fits",
        },
    ),
    "frustration": Score(
        instructions="How frustrated does the customer appear?",
        criteria=[
            "Calm and matter-of-fact",
            "Frustrated but civil",
            "Very angry or threatening to leave",
        ],
    ),
}
```

The application then thresholds probabilities, inspects confidence, and executes deterministic policy in ordinary code. Official implementation references: [Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python), [JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js), [HTTP API](https://docs.typesafe.ai/api).

## 2. Architecture: what is disclosed and what is not

### Disclosed by TypeSafe

TypeSafe says Jev uses:

1. a **new model architecture** focused on automation;
2. a **parallel sampler** that returns all requested outputs/probabilities rather than autoregressively generating tokens;
3. **RLCD**, a training method optimized for calibrated decisions;
4. a typed output space fixed by the caller's questions and criteria.

Sources: [launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer).

TypeSafe explicitly says Jev is "neither small nor an LLM" in its launch FAQ. That is a first-party characterization, not an independently verifiable architectural description. [Launch article FAQ](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

### Not publicly disclosed

As of the research date, the primary sources do not disclose:

- parameter count or model dimensions;
- whether the network uses transformers, state-space layers, diffusion, or another core architecture;
- whether it is encoder-only, decoder-based, or a multi-head classifier;
- how runtime-defined questions/options are represented internally;
- the number of forward passes or exact parallel-sampling algorithm;
- RLCD's loss, reward construction, optimization algorithm, calibration metric, or ablation studies;
- pretraining corpus composition or scale;
- training compute, inference hardware, batching, or serving topology;
- independently replicated calibration curves or expected calibration error;
- a peer-reviewed paper or technical report.

The launch FAQ says TypeSafe makes all training data itself and does not train on user data, but declines to describe its data process. The legal documentation reiterates a no-training-on-user-data commitment and says zero data retention is available for enterprise customers. [Launch article FAQ](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [Legal docs](https://docs.typesafe.ai/legal)

### Safe architecture comparison for a diagram

The following comparison stays within disclosed facts:

| Stage | Conventional autoregressive LLM call | Jev / System One call |
| --- | --- | --- |
| Input contract | Messages/prompts, sometimes with a requested JSON schema | Textual application state plus typed atomic questions and bounded criteria |
| Inference output | A token sequence, each token conditioned on the preceding sequence | Typed judgments and distributions for the questions, evaluated in parallel |
| Output contract | Free-form text or constrained structured text that must be validated | Values constrained to Noul, supplied Choice options, or supplied Score levels |
| Native job | Generate language, explanations, code, plans, or open-ended content | Detect, classify, score, rank, verify, and route within a bounded answer space |
| Uncertainty | Token probabilities exist internally, but application-level confidence is not generally calibrated by default | Application-level probabilities are part of the API; TypeSafe says RLCD optimizes their calibration |
| Control flow | Often delegated to an agent prompt | Kept in ordinary code, with model judgments as inputs |

Do not draw a transformer block on the Jev side. Use a visually opaque block labeled `Jev (internal architecture undisclosed)`.

## 3. RLCD and calibration

### TypeSafe's documented claim

RLCD stands for **Reinforcement Learning for Calibrated Decisions**. TypeSafe describes its intended result as probabilities whose frequency matches outcomes over groups of predictions: events assigned `0.8` should occur about 80% of the time. This is a population property, not a guarantee that a particular 0.8 prediction is correct. [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [System One](https://docs.typesafe.ai/concepts/system-one)

For Choice and Score, `confidence` is a scalar from 0 to 1 derived from the shape of the returned probability distribution: peaked distributions have higher confidence and flat distributions lower confidence. TypeSafe does not publish the exact statistic in the confidence documentation. Noul has no separate confidence because its single probability already expresses the yes/no split. [Confidence](https://docs.typesafe.ai/confidence)

### Required qualification

**Calibration is not correctness.** Jev can return the wrong valid option, assign the wrong score distribution, or be confidently wrong. Schema constraints eliminate malformed or out-of-set output, not semantic error.

The phrase **"zero hallucinations"** should not appear unqualified. A precise formulation is:

> Jev guarantees schema-conforming output: it cannot invent an undeclared Choice or return malformed prose in place of an answer. It can still make an incorrect judgment within the schema.

TypeSafe's own known-limitations page documents literal readings, weak numeric precision, unreliable counting/date comparison, degraded performance with indirection or irrelevant context, susceptibility to adversarial content, confusion from contradictory criteria, and inability to generate text. [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

The public primary sources define calibration and claim RLCD optimizes it, but they do not publish a reliability diagram, expected calibration error, Brier score, or third-party calibration study. Therefore the article should say **"TypeSafe describes/claims Jev as calibrated"**, and advise readers to validate probability and confidence thresholds on their own labeled traffic and pin a model version after validation.

## 4. Benchmark evidence

### Official workflow-eval design

TypeSafe publishes four workflow evaluations:

1. Security Incidents
2. Agent Trace Observability
3. Invoice Processing
4. Customer Service

The same domain workflow/harness is run with each model. Each workflow decomposes a policy into narrow Noul, Choice, and Score questions plus deterministic code. TypeSafe also compares an alternative in which the policy is supplied as one standalone prompt. Aggregate points give the four workflows equal weight. Models other than the two reference models run at their providers' default reasoning settings. [Workflow evals](https://evals.typesafe.ai/)

The labels are **not conventional ground truth**. TypeSafe states that it assumes the workflow code is correct and constructs reference probabilities from the average of GPT-6 Astra and Claude Fable 5.1 at high thinking, answering every question in the harness. Accuracy is then reported against those consensus labels. This makes the eval useful as a vendor demonstration of workflow fit, but it does not establish correctness against independently annotated outcomes. [Workflow evals methodology](https://evals.typesafe.ai/)

### Published aggregate results

The following values are rendered in the official aggregate chart; they are rounded display values and reflect the workflow implementation, not the standalone-prompt variant:

| Model configuration | Mean accuracy | Mean cost/case | Mean time/case |
| --- | ---: | ---: | ---: |
| **Jev workflow** | **67.8%** | **$0.0004** | **0.4 s** |
| GPT-5.6 Terra workflow | 67.9% | $0.0304 | 10.1 s |
| GPT-5.6 Luna workflow | 66.8% | $0.0033 | 12.9 s |
| GPT-5.6 Sol workflow | 74.1% | $0.0836 | 23.3 s |
| Claude Haiku 4.5 workflow | 53.6% | $0.0195 | 12.5 s |
| Claude Sonnet 5 workflow | 67.8% | $0.1174 | 78.1 s |
| Claude Opus 5 workflow | 73.1% | $0.1761 | 37.8 s |
| DeepSeek v4 Flash workflow | 64.4% | $0.0059 | 51.9 s |
| DeepSeek v4 Pro workflow | 65.5% | $0.0413 | 86.5 s |

Source: [TypeSafe workflow-eval overview](https://evals.typesafe.ai/). Model names above follow labels on the official plot; the chart abbreviates GPT-5.6 variants to Luna, Terra, and Sol.

The Jev per-workflow values visible on the official pages are:

| Workflow | Accuracy | Cost/case | Time/case |
| --- | ---: | ---: | ---: |
| Security Incidents | 61.7% | $0.0001 | 0.3 s |
| Agent Trace Observability | 71.6% | $0.0003 | 0.5 s |
| Invoice Processing | 61.8% | $0.0011 | 0.5 s |
| Customer Service | 76.0% | $0.0001 | 0.4 s |

Sources: [Security Incidents](https://evals.typesafe.ai/security_incidents.html), [Agent Trace Observability](https://evals.typesafe.ai/agent_trace_observability.html), [Invoice Processing](https://evals.typesafe.ai/invoice_processing.html), [Customer Service](https://evals.typesafe.ai/customer_service.html).

These numbers support three limited conclusions:

- Jev is much cheaper and faster on these four **System One-shaped, company-authored workflows**.
- Jev's average agreement with the model-derived reference is near Terra and Sonnet, lower than Sol and Opus, and higher than some configurations.
- Jev does not win quality on every workflow; invoice processing is a conspicuous case where several LLM workflows score materially higher.

### Headline multipliers and caveats

TypeSafe's homepage advertises `193.6x faster` and `444.6x cheaper`. Its launch article says these come from the workflow evals and are likely at the high end of real-world gains. The official aggregate chart's rounded values are broadly compatible with comparisons to different frontier configurations, but the public page does not show the exact calculation or comparator behind each multiplier. The simultaneously displayed homepage example (`0.114 s` vs `8.566 s`; `$0.000081` vs `$0.013880`) implies about `75.1x` faster and `171.4x` cheaper, not the two headline multipliers. Do not reproduce the multipliers as a universal speedup; link to the eval and explain the comparator/method ambiguity. [Homepage](https://typesafe.ai/), [launch caveats](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [workflow evals](https://evals.typesafe.ai/)

TypeSafe additionally discloses:

- the workflows were created by people on its model-capabilities team, so bias may exist;
- they were not deliberately created to favor Jev and are claimed not to be in its training distribution;
- using Astra/Fable consensus biases the reference toward OpenAI and Anthropic behavior;
- LLMs use TypeSafe's structured [System One adapter](https://github.com/typesafe-ai/system-one-adapter-python), which returns compatible probability-bearing decisions but may be slower/more expensive than requesting decisions without probabilities;
- published latency runs are generally made from laptops on the US West Coast, where the service is hosted;
- price sustainability cannot yet be proven and could be subsidized;
- TypeSafe deliberately does not publish standard public-benchmark scores.

Sources: [launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [benchmark philosophy](https://typesafe.ai/blog/antibenchmaxxing).

### Current price and service limits

As of 2026-09-17, the docs list `jev-1.13.0` at `$42` per billion input tokens (`$0.042`/million), with output tokens free. Published standard limits are 250,000 tokens/second and 1,200 requests/minute, marked as dynamically changing. `jev-latest` and `jev-preview` both point to `jev-1.13.0`. TypeSafe warns that aliases move, so production systems with tuned thresholds should pin the version and upgrade deliberately. [Models and pricing](https://docs.typesafe.ai/models)

## 5. When Jev helps, and when an LLM or code is better

| Need | Best default | Why |
| --- | --- | --- |
| Exact arithmetic, dates, database state, policy tables, hard authorization | **Code** | Deterministic, testable, and auditable; TypeSafe explicitly says Jev is weak at counting, numbers, and date comparison. |
| A bounded semantic judgment over text: detect, classify, score, rank, route, verify | **Jev candidate** | Native typed distributions; many independent questions can run in parallel; inexpensive enough for per-item checks. |
| Open-ended writing, explanations, plans, code, synthesis, multi-step reasoning | **LLM** | Jev does not generate text or reasoning and struggles with multiple levels of indirection. |
| High-stakes or ambiguous case | **Human and/or stronger reasoning model** | Confidence can gate escalation, but confidence does not guarantee correctness. |
| Mixed enterprise process | **Code + Jev + LLM + human** | Code owns policy/control flow; Jev supplies bounded judgments; LLM handles generation/reasoning; humans handle exceptional or high-risk decisions. |

This four-part composition is more defensible than presenting Jev as an LLM replacement.

## 6. Enterprise agentic workflow impact

### Strong patterns supported by official docs

1. **Intent and model routing.** Jev classifies a request and estimates complexity; code routes to deterministic logic, a specialist LLM, or a human. [Intent routing](https://docs.typesafe.ai/patterns/intent-routing)
2. **Confidence-gated automation.** High-confidence, low-risk cases can proceed; medium-confidence cases gather more information; low-confidence or high-risk cases escalate. Thresholds must be validated per action and domain. [Confidence](https://docs.typesafe.ai/confidence), [confidence routing](https://docs.typesafe.ai/patterns/confidence-routing)
3. **Speculative fan-out.** Ask all potentially useful independent questions once and let code ignore irrelevant answers, reducing sequential model round trips. [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out)
4. **Composite scoring.** Split a vague judgment into explicit dimensions and combine them with reviewable weights in code. [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring)
5. **Agent guardrails.** Screen prompts, retrieved passages, tool calls, and generated outputs for injection, policy violations, sensitive data, relevance, contradiction, or unsupported claims. [LLM guardrails](https://docs.typesafe.ai/cookbooks/llm_guardrails), [RAG passage classification](https://docs.typesafe.ai/cookbooks/classifying_rag_passages), [citation checking](https://docs.typesafe.ai/cookbooks/citation_check)
6. **Trace triage and observability.** Classify completed agent traces, detect errors or silent failures, and prioritize human review. [Agent trace eval](https://evals.typesafe.ai/agent_trace_observability.html)
7. **Large-scale semantic feature extraction.** Turn unstructured records into typed probabilistic features for downstream analytics or classical supervised models. [Use-case map](https://docs.typesafe.ai/concepts/use-case-map)

### A sound reference workflow

```text
request / event / document
            |
            v
  deterministic preprocessing
  (parse, retrieve, compute, validate)
            |
            v
  Jev: parallel bounded judgments
  intent | risk | relevance | confidence
            |
            v
  policy in code
     |          |             |
     v          v             v
 deterministic  specialist    human review
 handler        LLM/tool      or approval
     |          |             |
     +----------+-------------+
                |
                v
       optional Jev verification
       of output / action / citation
```

Expected benefits are reduced LLM calls, lower latency for routine decisions, explicit uncertainty, deterministic policy ownership, and more observable decision boundaries. Expected costs are additional question/rubric engineering, domain-specific evaluation, threshold monitoring, version pinning, error handling, and another hosted dependency.

### Operational limits and risks to include

- **Semantic errors remain.** Typed output guarantees shape, not truth.
- **Calibration is domain-dependent in practice.** Validate thresholds on representative labeled data; monitor drift after model/version changes.
- **Prompt injection remains possible.** TypeSafe says Jev 1.13 does not treat state as hostile by default.
- **Context rot remains.** Accuracy falls with irrelevant state; retrieve/filter before calling.
- **No explanations.** A returned distribution does not provide a rationale or evidence trail. Store inputs, question definitions, model version, outputs, and downstream policy decisions for auditability.
- **Early product.** Jev is a closed hosted service in early access; architecture and training are not independently reproducible.
- **Data governance.** TypeSafe states it does not train on user data and offers enterprise zero-data-retention, but an enterprise still needs to review the DPA, retention configuration, data residency, security controls, service levels, and regulatory obligations. [Legal docs](https://docs.typesafe.ai/legal)
- **Failure isolation.** The workflow needs timeouts, retries, a circuit breaker, and a deterministic/human fallback. The SDKs retry selected errors by default, but business behavior during provider failure belongs in application code. [Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python), [JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js)

## 7. Official graphics and reuse guidance

### High-value official assets found

| Asset | Direct official URL | What it shows | Recommended article treatment |
| --- | --- | --- | --- |
| Workflow quality/cost plot | [PNG](https://framerusercontent.com/images/z4Uu1YpJeEZPBSMTCMI0CN2PX0.png) | Vendor aggregate Pareto plot | Prefer linking to the interactive [evaluation site](https://evals.typesafe.ai/) and drawing an original chart from cited values. |
| Example decomposed workflow | [PNG](https://framerusercontent.com/images/ih1bFwZGYJxlnijbTuXx3f9NeM.png) | The simplest of TypeSafe's four workflow harnesses | Redraw conceptually with original styling and cite TypeSafe; the original is not openly licensed. |
| Type-error / hallucination plot | [PNG](https://framerusercontent.com/images/KEoJ6ZaJkOZG6mcjBsOlB3NCqek.png) | Vendor comparison of schema/type errors | Avoid as primary evidence: Jev's zero is guaranteed by schema rather than empirically measured, and LLM data comes from OpenRouter with acknowledged routing bias. |
| Training-path diagram | [light WebP](https://mintcdn.com/ts-docs/aFVnpmCIX68NpsV1/images/ai-primer/training-paths-light.webp?fit=max&auto=format&n=aFVnpmCIX68NpsV1&q=85&s=61898215ac31388d3be15bf583b743ee) | RLHF / RLVR / RLCD conceptual branches | Useful context, but safer to redraw and link to the [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer). |
| Mode-dropping diagram | [light WebP](https://mintcdn.com/ts-docs/aFVnpmCIX68NpsV1/images/ai-primer/mode-dropping-light.webp?fit=max&auto=format&n=aFVnpmCIX68NpsV1&q=85&s=d51758a6212b526fc243cc9a81572cc7) | TypeSafe's conceptual account of RLHF mode dropping | Optional; it is a vendor framing, not direct evidence about Jev. |

### Licensing warning

TypeSafe's website terms say the site's visual interfaces, graphics, designs, compilations, data, and other materials are TypeSafe's or its licensors' property and may not be reproduced or publicly displayed unless expressly authorized. Attribution alone is not a license. [TypeSafe Terms of Use, sections 3-4](https://typesafe.ai/legal/terms)

Therefore:

- do **not** copy the launch-page PNGs into the blog repository without written permission;
- link to the official interactive evals rather than hotlinking or republishing their graphics;
- create original diagrams for Jev's documented interface and workflow composition;
- if plotting official numeric results, label them `Data: TypeSafe AI workflow evals (accessed 2026-09-17)` and explain the methodology/caveats in the caption;
- TypeSafe's SDK repositories are MIT-licensed, but that license covers those repositories' code, not the website's graphics.

## 8. Recommended article visuals

1. **Animated "state to decisions" diagram.** A support ticket enters; Noul, Choice, and Score questions fan out simultaneously; probability bars animate; code takes one of three routes: automate, call an LLM, or ask a human. This directly answers what Jev does.
2. **Animated LLM versus Jev inference contract.** LLM side emits tokens serially into a JSON/text response; Jev side reveals bounded probability distributions together. Put `internal architecture undisclosed` inside Jev. This explains the known difference without inventing internals.
3. **Original benchmark scatterplot.** Replot the official aggregate workflow values with cost or time on a log axis and accuracy on the vertical axis. Add a prominent `Vendor-authored eval; labels derived from Astra + Fable, not human ground truth` caption.
4. **Enterprise hybrid architecture.** Code in the center as control plane; Jev handles routing/verification; an LLM handles open-ended generation/reasoning; humans handle uncertain/high-risk cases. Animate a request taking different paths as confidence changes.
5. **"Typed is not true" calibration explainer.** First panel shows schema guarantee; second shows a wrong but valid answer; third shows calibration bins and explains that 0.8 means about 80% accuracy across similar predictions, not certainty for one case.

## 9. Writing guardrails for the final article

Use:

- "TypeSafe reports" for performance and calibration claims.
- "The public interface returns" for API facts.
- "TypeSafe has not disclosed" for model internals.
- "schema-conforming" instead of unqualified "hallucination-free".
- "parallel questions/outputs" rather than "one forward pass".
- "a specialized decision model that complements LLMs" rather than "an LLM replacement".

Avoid:

- calling Jev a world model, agent, reasoning model, classifier with a fixed label set, or small LLM;
- drawing a speculative neural architecture;
- treating confidence as correctness or a calibrated guarantee on the user's domain;
- presenting the vendor workflow eval as independent evidence;
- using the `193.6x` and `444.6x` figures without their workflow-specific and vendor-reported qualification;
- saying Jev cannot hallucinate without defining the claim as an output-schema guarantee;
- implying Jev supports image/audio/video input;
- claiming cost savings before measuring the full workflow, including engineering, evaluation, fallback, and monitoring costs.

## Primary-source index

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [TypeSafe homepage](https://typesafe.ai/)
- [Workflow evals](https://evals.typesafe.ai/)
- [Documentation introduction](https://docs.typesafe.ai/introduction)
- [System One](https://docs.typesafe.ai/concepts/system-one)
- [Primitives](https://docs.typesafe.ai/primitives)
- [AI primer / RLCD](https://docs.typesafe.ai/introduction/machine-learning-primer)
- [Confidence](https://docs.typesafe.ai/confidence)
- [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)
- [Known Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [Models, pricing, and aliases](https://docs.typesafe.ai/models)
- [Official Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python)
- [Official JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js)
- [Official System One LLM adapter](https://github.com/typesafe-ai/system-one-adapter-python)
- [Legal and data-use documentation](https://docs.typesafe.ai/legal)
- [Website terms governing graphics/materials](https://typesafe.ai/legal/terms)
