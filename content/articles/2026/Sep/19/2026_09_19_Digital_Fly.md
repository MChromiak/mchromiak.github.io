Title: From a fly connectome to a digital fly: what the experiments show
Subtitle: What the 2026 male-CNS map reveals, what experiments test, and what digital-fly demos add
Status: published
Category: Machine Learning / Neuroscience
Date: 2026-09-19 12:00
Modified: 2026-09-19 12:00
Tags: Connectomics, Drosophila, Brain Simulation, Computational Neuroscience, FlyWire, NeuroMechFly
Slug: From-Fly-Connectome-to-Digital-Behavior
Related_posts: Dragon-Hatchling-I-Paper-Notes, Atlas-World-Model-for-Spatial-Intelligence
Cover: articles/2026/Sep/19/From-Fly-Connectome-to-Digital-Behavior/img/fly-model-evidence.svg
Summary: The 2026 male fruit fly connectome links brain and nerve cord in one open map. New studies compare male and female circuits, trace vision and taste pathways, and test social-behavior predictions. Here is how those results differ from digital-fly game demos.

---

A fruit fly can now be represented by a remarkably complete wiring map, and versions of that map have been put inside virtual worlds. The two achievements are easy to conflate. A connectome records which neurons connect; a digital fly also needs rules for how those neurons respond, a way to turn inputs into neural signals, and a controller that turns outputs into movement.

The major new result in September 2026 is the [first complete map of a male fly's central nervous system](https://pubmed.ncbi.nlm.nih.gov/42691995/): brain, optic lobes, and ventral nerve cord together. Its value is already visible in peer-reviewed studies of sex differences, vision, taste, and social behavior. The Minecraft and Doom projects that followed are a different kind of experiment: they test software interfaces built around the open map. **The question throughout this article is what each layer actually establishes.**

[![Four stages of digital-fly research: reconstruct the wiring, simulate neural dynamics, test circuit predictions, and close a sensory-motor loop in a virtual body.]({attach}img/fly-model-evidence.svg)](/articles/2026/Sep/19/From-Fly-Connectome-to-Digital-Behavior/)

Figure 1. Four steps often compressed into "digital fly": map connections, simulate activity, test predictions, and close a loop with a body. Editorial synthesis of the [2026 MaleCNS map](https://pubmed.ncbi.nlm.nih.gov/42691995/), the [2024 FlyWire and simulation studies](https://www.nature.com/articles/s41586-024-07558-y), and the [embodiment work](https://www.nature.com/articles/s41592-024-02497-y); not a figure from those papers.
{: align=center }

## The 2026 map: brain to nerve cord

The [MaleCNS reconstruction](https://pubmed.ncbi.nlm.nih.gov/42691995/) contains **166,700 neurons** assigned to **11,710 types**. It follows connections through the male fly's brain, optic lobes, and ventral nerve cord, where many pathways toward the body continue. [Janelia released the dataset in June 2026](https://www.janelia.org/project-team/flyem/male-cns-connectome); the main paper and companion studies appeared in September. Researchers can inspect individual cells and trace candidate routes from sensation toward movement, rather than assembling those routes from separate, incomplete maps.

This is a map of *connections*, not a record of thoughts or movements. Electron microscopy reveals the fine structure from which neurons and synapses are reconstructed. It does not directly measure how strongly each connection acts in a behaving fly, or how its strength changes with context. Those unknowns matter when a map is turned into a simulation.

<details class="dinov2-background" markdown="1">
<summary>What is a connectome?</summary>

A connectome is a network description: neurons are the nodes and their anatomical connections are the edges. Multiple observed synapses between two neurons give a useful estimate of their anatomical connection strength, but not a measured electrical weight. A digital-fly model must supply additional rules for neural activity, sensory input, and motor output.

</details>

## What the new papers found

The main MaleCNS study makes a comparison that was not possible with a female brain map alone. It matches cell types across male and female connectomes at synaptic resolution. Of the types it compares, **8,069 have corresponding forms in both sexes**, while **138 are structurally different**, **289 are male-specific**, and **71 are female-specific**. Much of the sensory and motor periphery is shared; the more pronounced differences are concentrated in higher brain centers. The implication is specific: some sex-dependent behavior may arise from *different routes through otherwise partly shared circuitry*, not from replacing the entire sensory or motor system. [Berg et al., *Cell* 2026](https://pubmed.ncbi.nlm.nih.gov/42691995/).

<div style="position:relative;width:100%;padding-top:56.25%;margin:1.5em 0 0.5em;">
  <iframe src="https://www.youtube.com/embed/mNV_ypFXKwg" title="Janelia animation comparing a sexually dimorphic fly neuron and its connections" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>
</div>

Animation 1. Janelia's reconstruction of the AOTU012 neuron type, present in both sexes but connected differently. It illustrates anatomical differences, not neural activity. Source: [Janelia MaleCNS media gallery](https://male-cns.janelia.org/media/) ([watch on YouTube](https://www.youtube.com/watch?v=mNV_ypFXKwg)).
{: align=center }

Three companion studies show how researchers can use the map:

- **Vision:** [Hoeller et al.](https://pubmed.ncbi.nlm.nih.gov/42691997/) trace visual pathways from the eyes through the optic lobes into the brain. Their network analysis predicts how different routes collect and combine visual information; predicted response properties agree with available physiological measurements. This is a test of circuit organization, not a simulation of a whole fly seeing and acting.
- **Taste:** [Tastekin et al.](https://pubmed.ncbi.nlm.nih.gov/42691996/) connect taste inputs with pathways for feeding, movement, endocrine regulation, and courtship across the brain and nerve cord. A complete route on a diagram gives a concrete hypothesis about how a taste can influence an action; it does not by itself show that each route causes the predicted behavior.
- **Social behavior:** [Rubin et al.](https://pubmed.ncbi.nlm.nih.gov/42692022/) identify **48 related cell types** in a sexually differentiated network, make tools to target them, and test their roles in social signaling and male-male interactions. Here the anatomical map leads to interventions in living animals, making this a stronger behavioral test than a traced pathway alone.

These studies share the same resource but answer different questions. The map establishes *where connections go*. Analysis proposes *what a circuit may compute*. Recordings and targeted interventions test whether those proposals resemble the living animal.

<div style="position:relative;width:100%;padding-top:56.25%;margin:1.5em 0 0.5em;">
  <iframe src="https://www.youtube.com/embed/TQ0T4C7noMo" title="Janelia animation tracing a visual-to-motor pathway through the male fly central nervous system" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>
</div>

Animation 2. An example route from R1-R6 visual neurons toward DNg13. The clip follows reconstructed connections; it does not show a recorded signal traveling along them. Source: [Janelia MaleCNS media gallery](https://male-cns.janelia.org/media/) ([watch on YouTube](https://www.youtube.com/watch?v=TQ0T4C7noMo)).
{: align=center }

## How the field got here

The [FlyWire paper](https://www.nature.com/articles/s41586-024-07558-y) published in 2024 reconstructed an adult **female brain**, with roughly **139,000 neurons and 50 million chemical synapses**. That is a different specimen and a different anatomical scope from the 2026 male brain-plus-nerve-cord map. The counts should not be read as a simple male-versus-female neuron comparison.

[![FlyWire Figure 1: reconstructed neurons across the central brain and optic lobes, with examples of the microscopy, segmentation, annotations, and synapse data behind the map.]({attach}img/flywire-fig1.png)]({attach}img/flywire-fig1.png)

Figure 2. In the original FlyWire figure, panel **a** shows the reconstructed brain; panels **b-f** show how microscopy, segmentation, annotation, and synapse detection make the map usable. Source: [Dorkenwald et al., *Nature* 2024, Figure 1](https://www.nature.com/articles/s41586-024-07558-y/figures/1) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); reproduced unmodified).
{: align=center }

<video controls preload="none" playsinline width="960" poster="/articles/2026/Sep/19/From-Fly-Connectome-to-Digital-Behavior/img/flywire-fig1.png" aria-label="FlyWire rendering of the reconstructed neurons in an adult fruit fly brain">
  <source src="https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-024-07558-y/MediaObjects/41586_2024_7558_MOESM6_ESM.mp4" type="video/mp4">
  <a href="https://www.nature.com/articles/s41586-024-07558-y">Watch the FlyWire reconstruction on the publisher's site</a>.
</video>

Video 1. The FlyWire team's 3D rendering shows the reconstructed neurons, not neural activity. [Open the original MP4](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-024-07558-y/MediaObjects/41586_2024_7558_MOESM6_ESM.mp4). Source: [Dorkenwald et al., *Nature* 2024, Supplementary Video 1](https://www.nature.com/articles/s41586-024-07558-y) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
{: align=center }

The same map supported an important simulation test. [Shiu et al.](https://www.nature.com/articles/s41586-024-07763-9) built a **leaky integrate-and-fire** model of about 127,400 central-brain neurons: each modeled neuron accumulates input, loses some over time, and emits a spike at a threshold. The map specifies which neurons can influence which; the model supplies simplified dynamics. The researchers stimulated sugar-sensing cells in the model and predicted which intermediate cell types could drive a feeding movement. In living flies, **10 of 11 predicted positives** evoked the movement, while **four of 95 predicted negatives** did. A shuffled-wiring control performed far worse, supporting the value of the measured connection pattern for this particular test.

[![Shiu and colleagues' Figure 2: predicted MN9 activation for 106 tested cell types, measured rostrum extension in real flies, and a confusion matrix comparing predictions with observations.]({attach}img/shiu-fig2.png)]({attach}img/shiu-fig2.png)

Figure 3. The model ranks 106 cell types by predicted MN9 activation (**a**); optogenetic tests measure rostrum extension in real flies (**b**); the matrix compares predicted and observed outcomes (**c**). Source: [Shiu et al., *Nature* 2024, Figure 2](https://www.nature.com/articles/s41586-024-07763-9/figures/2) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); reproduced unmodified).
{: align=center }

<details class="dinov2-background" markdown="1">
<summary>Why use a leaky integrate-and-fire neuron?</summary>

It is a compact way to turn a static graph into activity over time. A modeled voltage rises under input, decays toward a baseline, and resets after a threshold crossing. That is enough to test whether a mapped circuit can carry a stimulus to an output. It leaves out much of a real neuron's biophysics, so success on one circuit does not validate every simulated activity pattern.

</details>

Another 2024 study asked a complementary question. [Lappalainen et al.](https://www.nature.com/articles/s41586-024-07939-3) constrained a visual-motion network with measured wiring, then optimized its remaining parameters for a motion task. Some predicted responses of identified cell types resembled recordings from living flies, although models with the same wiring could still arrive at different internal responses. The lesson carries into 2026: a map narrows the possibilities; physiology helps select among them.

## From a map to a moving fly

To test behavior, a simulated brain needs a body, sensors, and an environment that reacts to movement. [NeuroMechFly v2](https://www.nature.com/articles/s41592-024-02497-y) supplies a physics-based fly body and simulated sensory inputs. Its 2024 experiments include navigation and a fly-following example with a connectome-constrained **visual** network. The body and its controllers are substantial research tools, but this was not an entire connectome driving every muscle.

[Watch the authors' Supplementary Video 14](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41592-024-02497-y/MediaObjects/41592_2024_2497_MOESM17_ESM.mp4) to see the following fly, its visual inputs, and simulated visual-neuron activity together. This is a publisher-hosted video of the NeuroMechFly experiment described above.

In March 2026, [Eon Systems reported an integration](https://eon.systems/updates/embodied-brain-emulation) that puts a connectome-based brain model into a NeuroMechFly-derived body. Selected sensory signals update the model; selected neural outputs feed trained body controllers; the resulting movement changes the next sensory input. [The demonstration video](https://eon.systems/updates/first-multi-behavior-brain-upload) shows a closed loop, not a fully autonomous reconstruction of fly behavior. The company's own technical note identifies hand-selected interfaces, trained locomotion controllers, and a visual model that does not yet substantially determine the shown actions. This is a useful engineering demonstration, but it has not undergone the same experimental scrutiny as the papers above.

## What the game demos actually test

Public projects have begun wiring the open MaleCNS graph to virtual worlds. [NeuroCraft Fly](https://github.com/evnsnclr/neurocraft-fly-public) maps Minecraft events into modeled neural inputs, reads out selected activity, then invokes scripted movement programs. [DOOMFLY](https://github.com/nftechie/doomfly) similarly defines its own visual mapping, neural dynamics, and assignments from neural activity to game buttons. These systems test whether developers can build usable *interfaces around a large connectome*. They do not test whether a fly would perceive a game screen or choose the demonstrated actions. DOOMFLY's public validation notes also report that its current visual and survival-learning tests have not yet passed.

The earlier [fly-chess project](https://github.com/cesp99/fly-chess) is a different kind of demo: it trains a network constrained by fly-derived topology to choose chess moves. Its learned weights and chess-specific input and output mappings make it a machine-learning experiment, not evidence of chess ability in a biological fly. These projects are valuable prompts for controls: compare them with other graph topologies while keeping training, interfaces, and output programs fixed.

## The next decisive experiment

The 2026 advance is not that a fly has been "uploaded." It is that a far more complete, open map now supports specific questions across the full central nervous system. The vision and taste papers extract pathways from that map; the social-circuit study goes further by testing targeted cells in living flies. The 2024 simulation work shows that simplified dynamics can already make useful predictions. The embodied and game projects show what is technically possible when a model is connected to an environment.

The remaining challenge is to make a digital fly predict **both neural activity and behavior** under new stimuli, then repeat the comparison after targeted perturbations. The model should be tested against alternative wiring and interface choices, with its training fixed before those tests. That matters because [theory shows](https://www.nature.com/articles/s41593-025-02080-4) that the same measured connections can support different activity when unmeasured parameters change. A convincing digital fly will succeed where a plausible-looking animation could fail: it will forecast what a real fly does, and where its neurons become active, in experiments it has not seen.

## Original papers and technical sources

- [Berg et al., "Sexual dimorphism in the complete Drosophila male central nervous system connectome" (*Cell*, 2026)](https://pubmed.ncbi.nlm.nih.gov/42691995/): the male brain-and-nerve-cord map and comparison with female circuits.
- [Hoeller et al., "The organization of visual pathways in the Drosophila brain" (*Cell*, 2026)](https://pubmed.ncbi.nlm.nih.gov/42691997/): visual pathways and predicted response organization.
- [Tastekin et al., "The complete gustatory connectome of adult Drosophila reveals how taste guides feeding, foraging, and social behavior" (*Cell*, 2026)](https://pubmed.ncbi.nlm.nih.gov/42691996/): taste pathways through the central nervous system.
- [Rubin et al., "Networks of sexually dimorphic neurons that regulate social behaviors in Drosophila" (*Current Biology*, 2026)](https://pubmed.ncbi.nlm.nih.gov/42692022/): mapped cell types and behavioral tests.
- [Janelia FlyEM MaleCNS project and data release (2026)](https://www.janelia.org/project-team/flyem/male-cns-connectome): the public resource and viewers.
- [Dorkenwald et al., "Neuronal wiring diagram of an adult brain" (*Nature*, 2024)](https://www.nature.com/articles/s41586-024-07558-y): the earlier FlyWire female-brain reconstruction.
- [Shiu et al., "A Drosophila computational brain model reveals sensorimotor processing" (*Nature*, 2024)](https://www.nature.com/articles/s41586-024-07763-9): the spiking whole-brain model and feeding/grooming tests.
- [Lappalainen et al., "Connectome-constrained networks predict neural activity across the fly visual system" (*Nature*, 2024)](https://www.nature.com/articles/s41586-024-07939-3): a task-optimized visual circuit model checked against neural recordings.
- [Wang-Chen et al., "NeuroMechFly v2: simulating embodied sensorimotor control in adult Drosophila" (*Nature Methods*, 2024)](https://www.nature.com/articles/s41592-024-02497-y): the virtual body and control experiments.
- [Beiran and Litwin-Kumar, "Prediction of neural activity in connectome-constrained recurrent networks" (*Nature Neuroscience*, 2025)](https://www.nature.com/articles/s41593-025-02080-4): why identical wiring does not uniquely fix neural dynamics.
- [Eon Systems, "How the Eon Team Produced a Virtual Embodied Fly" (2026)](https://eon.systems/updates/embodied-brain-emulation): a company technical account of its integration.
- [NeuroCraft Fly](https://github.com/evnsnclr/neurocraft-fly-public), [DOOMFLY](https://github.com/nftechie/doomfly), and [fly-chess](https://github.com/cesp99/fly-chess): creators' repositories for the community demos, not peer-reviewed biological experiments.
