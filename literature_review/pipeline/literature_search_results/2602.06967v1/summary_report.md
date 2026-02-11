# 文献综述综合报告

生成时间: 2026-02-11 11:09:25

## 源论文信息

- **标题**: Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models
- **作者**: Siqi SongXuanbing XieZonglin Yuqiang Shijie WangBiqing
- **摘要**: Multi-robot collaboration tasks often require heterogeneous robots to work together over long horizons under spatial constraints and environmental uncertainties. Although Large Language Models (LLMs) ...

---

## 高相关度文献 (15 篇)

### 1. Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models

**相关度**: 1.000 | **arXiv ID**: 2602.06967v1 | **完整MD**: ❌

Multi-robot collaboration tasks often require heterogeneous robots to work together over long horizons under spatial constraints and environmental uncertainties. Although Large Language Models (LLMs) excel at reasoning and planning, their potential for coordinated control has not been fully explored. Inspired by human teamwork, we present CLiMRS (Cooperative Large-Language-Model-Driven Heterogeneous Multi-Robot System), an adaptive group negotiation framework among LLMs for multi-robot collaboration. This framework pairs each robot with an LLM agent and dynamically forms subgroups through a general proposal planner. Within each subgroup, a subgroup manager leads perception-driven multi-LLM discussions to get commands for actions. Feedback is provided by both robot execution outcomes and environment changes. This grouping-planning-execution-feedback loop enables efficient planning and robust execution. To evaluate these capabilities, we introduce CLiMBench, a heterogeneous multi-robot benchmark of challenging assembly tasks. Our experiments show that CLiMRS surpasses the best baseline, achieving over 40% higher efficiency on complex tasks without sacrificing success on simpler ones. Overall, our results demonstrate that leveraging human-inspired group formation and negotiation principles significantly enhances the efficiency of heterogeneous multi-robot collaboration. Our code is available here: https://github.com/song-siqi/CLiMRS.

---

### 2. Enhancing the LLM-Based Robot Manipulation Through Human-Robot Collaboration

**相关度**: 0.882 | **arXiv ID**: 2406.14097v2 | **完整MD**: ❌

Large Language Models (LLMs) are gaining popularity in the field of robotics. However, LLM-based robots are limited to simple, repetitive motions due to the poor integration between language models, robots, and the environment. This paper proposes a novel approach to enhance the performance of LLM-based autonomous manipulation through Human-Robot Collaboration (HRC). The approach involves using a prompted GPT-4 language model to decompose high-level language commands into sequences of motions that can be executed by the robot. The system also employs a YOLO-based perception algorithm, providing visual cues to the LLM, which aids in planning feasible motions within the specific environment. Additionally, an HRC method is proposed by combining teleoperation and Dynamic Movement Primitives (DMP), allowing the LLM-based robot to learn from human guidance. Real-world experiments have been conducted using the Toyota Human Support Robot for manipulation tasks. The outcomes indicate that tasks requiring complex trajectory planning and reasoning over environments can be efficiently accomplished through the incorporation of human demonstrations.

---

### 3. LLM+MAP: Bimanual Robot Task Planning using Large Language Models and Planning Domain Definition Language

**相关度**: 0.880 | **arXiv ID**: 2503.17309v1 | **完整MD**: ❌

Bimanual robotic manipulation provides significant versatility, but also presents an inherent challenge due to the complexity involved in the spatial and temporal coordination between two hands. Existing works predominantly focus on attaining human-level manipulation skills for robotic hands, yet little attention has been paid to task planning on long-horizon timescales. With their outstanding in-context learning and zero-shot generation abilities, Large Language Models (LLMs) have been applied and grounded in diverse robotic embodiments to facilitate task planning. However, LLMs still suffer from errors in long-horizon reasoning and from hallucinations in complex robotic tasks, lacking a guarantee of logical correctness when generating the plan. Previous works, such as LLM+P, extended LLMs with symbolic planners. However, none have been successfully applied to bimanual robots. New challenges inevitably arise in bimanual manipulation, necessitating not only effective task decomposition but also efficient task allocation. To address these challenges, this paper introduces LLM+MAP, a bimanual planning framework that integrates LLM reasoning and multi-agent planning, automating effective and efficient bimanual task planning. We conduct simulated experiments on various long-horizon manipulation tasks of differing complexity. Our method is built using GPT-4o as the backend, and we compare its performance against plans generated directly by LLMs, including GPT-4o, V3 and also recent strong reasoning models o1 and R1. By analyzing metrics such as planning time, success rate, group debits, and planning-step reduction rate, we demonstrate the superior performance of LLM+MAP, while also providing insights into robotic reasoning. Code is available at https://github.com/Kchu/LLM-MAP.

---

### 4. CE-MRS: Contrastive Explanations for Multi-Robot Systems

**相关度**: 0.873 | **arXiv ID**: 2410.08408v1 | **完整MD**: ❌

As the complexity of multi-robot systems grows to incorporate a greater number of robots, more complex tasks, and longer time horizons, the solutions to such problems often become too complex to be fully intelligible to human users. In this work, we introduce an approach for generating natural language explanations that justify the validity of the system's solution to the user, or else aid the user in correcting any errors that led to a suboptimal system solution. Toward this goal, we first contribute a generalizable formalism of contrastive explanations for multi-robot systems, and then introduce a holistic approach to generating contrastive explanations for multi-robot scenarios that selectively incorporates data from multi-robot task allocation, scheduling, and motion-planning to explain system behavior. Through user studies with human operators we demonstrate that our integrated contrastive explanation approach leads to significant improvements in user ability to identify and solve system errors, leading to significant improvements in overall multi-robot team performance.

---

### 5. RoboBallet: Planning for Multi-Robot Reaching with Graph Neural Networks and Reinforcement Learning

**相关度**: 0.872 | **arXiv ID**: 2509.05397v1 | **完整MD**: ❌

Modern robotic manufacturing requires collision-free coordination of multiple robots to complete numerous tasks in shared, obstacle-rich workspaces. Although individual tasks may be simple in isolation, automated joint task allocation, scheduling, and motion planning under spatio-temporal constraints remain computationally intractable for classical methods at real-world scales. Existing multi-arm systems deployed in the industry rely on human intuition and experience to design feasible trajectories manually in a labor-intensive process. To address this challenge, we propose a reinforcement learning (RL) framework to achieve automated task and motion planning, tested in an obstacle-rich environment with eight robots performing 40 reaching tasks in a shared workspace, where any robot can perform any task in any order. Our approach builds on a graph neural network (GNN) policy trained via RL on procedurally-generated environments with diverse obstacle layouts, robot configurations, and task distributions. It employs a graph representation of scenes and a graph policy neural network trained through reinforcement learning to generate trajectories of multiple robots, jointly solving the sub-problems of task allocation, scheduling, and motion planning. Trained on large randomly generated task sets in simulation, our policy generalizes zero-shot to unseen settings with varying robot placements, obstacle geometries, and task poses. We further demonstrate that the high-speed capability of our solution enables its use in workcell layout optimization, improving solution times. The speed and scalability of our planner also open the door to new capabilities such as fault-tolerant planning and online perception-based re-planning, where rapid adaptation to dynamic task sets is required.

---

### 6. Human-Aware Physical Human-Robot Collaborative Transportation and Manipulation with Multiple Aerial Robots

**相关度**: 0.866 | **arXiv ID**: 2210.05894v3 | **完整MD**: ❌

Human-robot interaction will play an essential role in various industries and daily tasks, enabling robots to effectively collaborate with humans and reduce their physical workload. Most of the existing approaches for physical human-robot interaction focus on collaboration between a human and a single ground or aerial robot. In recent years, very little progress has been made in this research area when considering multiple aerial robots, which offer increased versatility and mobility. This paper proposes a novel approach for physical human-robot collaborative transportation and manipulation of a cable-suspended payload with multiple aerial robots. The proposed method enables smooth and intuitive interaction between the transported objects and a human worker. In the same time, we consider distance constraints during the operations by exploiting the internal redundancy of the multi-robot transportation system. The key elements of our approach are (a) a collaborative payload external wrench estimator that does not rely on any force sensor; (b) a 6D admittance controller for human-aerial-robot collaborative transportation and manipulation; (c) a human-aware force distribution that exploits the internal system redundancy to guarantee the execution of additional tasks such inter-human-robot separation without affecting the payload trajectory tracking or quality of interaction. We validate the approach through extensive simulation and real-world experiments. These include scenarios where the robot team assists the human in transporting and manipulating a load, or where the human helps the robot team navigate the environment. We experimentally demonstrate for the first time, to the best of our knowledge, that our approach enables a quadrotor team to physically collaborate with a human in manipulating a payload in all 6 DoF in collaborative human-robot transportation and manipulation tasks.

---

### 7. Deploying and Evaluating LLMs to Program Service Mobile Robots

**相关度**: 0.865 | **arXiv ID**: 2311.11183v3 | **完整MD**: ❌

Recent advancements in large language models (LLMs) have spurred interest in using them for generating robot programs from natural language, with promising initial results. We investigate the use of LLMs to generate programs for service mobile robots leveraging mobility, perception, and human interaction skills, and where accurate sequencing and ordering of actions is crucial for success. We contribute CodeBotler, an open-source robot-agnostic tool to program service mobile robots from natural language, and RoboEval, a benchmark for evaluating LLMs' capabilities of generating programs to complete service robot tasks. CodeBotler performs program generation via few-shot prompting of LLMs with an embedded domain-specific language (eDSL) in Python, and leverages skill abstractions to deploy generated programs on any general-purpose mobile robot. RoboEval evaluates the correctness of generated programs by checking execution traces starting with multiple initial states, and checking whether the traces satisfy temporal logic properties that encode correctness for each task. RoboEval also includes multiple prompts per task to test for the robustness of program generation. We evaluate several popular state-of-the-art LLMs with the RoboEval benchmark, and perform a thorough analysis of the modes of failures, resulting in a taxonomy that highlights common pitfalls of LLMs at generating robot programs. We release our code and benchmark at https://amrl.cs.utexas.edu/codebotler/.

---

### 8. Optimal Sequential Task Assignment and Path Finding for Multi-Agent Robotic Assembly Planning

**相关度**: 0.849 | **arXiv ID**: 2006.08845v1 | **完整MD**: ❌

We study the problem of sequential task assignment and collision-free routing for large teams of robots in applications with inter-task precedence constraints (e.g., task $A$ and task $B$ must both be completed before task $C$ may begin). Such problems commonly occur in assembly planning for robotic manufacturing applications, in which sub-assemblies must be completed before they can be combined to form the final product. We propose a hierarchical algorithm for computing makespan-optimal solutions to the problem. The algorithm is evaluated on a set of randomly generated problem instances where robots must transport objects between stations in a "factory "grid world environment. In addition, we demonstrate in high-fidelity simulation that the output of our algorithm can be used to generate collision-free trajectories for non-holonomic differential-drive robots.

---

### 9. Intuitive Programming, Adaptive Task Planning, and Dynamic Role Allocation in Human-Robot Collaboration

**相关度**: 0.848 | **arXiv ID**: 2511.08732v1 | **完整MD**: ❌

Remarkable capabilities have been achieved by robotics and AI, mastering complex tasks and environments. Yet, humans often remain passive observers, fascinated but uncertain how to engage. Robots, in turn, cannot reach their full potential in human-populated environments without effectively modeling human states and intentions and adapting their behavior. To achieve a synergistic human-robot collaboration (HRC), a continuous information flow should be established: humans must intuitively communicate instructions, share expertise, and express needs. In parallel, robots must clearly convey their internal state and forthcoming actions to keep users informed, comfortable, and in control. This review identifies and connects key components enabling intuitive information exchange and skill transfer between humans and robots. We examine the full interaction pipeline: from the human-to-robot communication bridge translating multimodal inputs into robot-understandable representations, through adaptive planning and role allocation, to the control layer and feedback mechanisms to close the loop. Finally, we highlight trends and promising directions toward more adaptive, accessible HRC.

---

### 10. Learning Optimal Topology for Ad-hoc Robot Networks

**相关度**: 0.844 | **arXiv ID**: 2201.12900v2 | **完整MD**: ❌

In this paper, we synthesize a data-driven method to predict the optimal topology of an ad-hoc robot network. This problem is technically a multi-task classification problem. However, we divide it into a class of multi-class classification problems that can be more efficiently solved. For this purpose, we first compose an algorithm to create ground-truth optimal topologies associated with various configurations of a robot network. This algorithm incorporates a complex collection of optimality criteria that our learning model successfully manages to learn. This model is an stacked ensemble whose output is the topology prediction for a particular robot. Each stacked ensemble instance constitutes three low-level estimators whose outputs will be aggregated by a high-level boosting blender. Applying our model to a network of 10 robots displays over 80% accuracy in the prediction of optimal topologies corresponding to various configurations of the cited network.

---

### 11. State-of-the-art in Robot Learning for Multi-Robot Collaboration: A Comprehensive Survey

**相关度**: 0.843 | **arXiv ID**: 2408.11822v1 | **完整MD**: ❌

With the continuous breakthroughs in core technology, the dawn of large-scale integration of robotic systems into daily human life is on the horizon. Multi-robot systems (MRS) built on this foundation are undergoing drastic evolution. The fusion of artificial intelligence technology with robot hardware is seeing broad application possibilities for MRS. This article surveys the state-of-the-art of robot learning in the context of Multi-Robot Cooperation (MRC) of recent. Commonly adopted robot learning methods (or frameworks) that are inspired by humans and animals are reviewed and their advantages and disadvantages are discussed along with the associated technical challenges. The potential trends of robot learning and MRS integration exploiting the merging of these methods with real-world applications is also discussed at length. Specifically statistical methods are used to quantitatively corroborate the ideas elaborated in the article.

---

### 12. A Survey of Robot Manipulation in Contact

**相关度**: 0.839 | **arXiv ID**: 2112.01942v3 | **完整MD**: ❌

In this survey, we present the current status on robots performing manipulation tasks that require varying contact with the environment, such that the robot must either implicitly or explicitly control the contact force with the environment to complete the task. Robots can perform more and more manipulation tasks that are still done by humans, and there is a growing number of publications on the topics of 1) performing tasks that always require contact and 2) mitigating uncertainty by leveraging the environment in tasks that, under perfect information, could be performed without contact. The recent trends have seen robots perform tasks earlier left for humans, such as massage, and in the classical tasks, such as peg-in-hole, there is a more efficient generalization to other similar tasks, better error tolerance, and faster planning or learning of the tasks. Thus, in this survey we cover the current stage of robots performing such tasks, starting from surveying all the different in-contact tasks robots can perform, observing how these tasks are controlled and represented, and finally presenting the learning and planning of the skills required to complete these tasks.

---

### 13. Task Adaptation in Industrial Human-Robot Interaction: Leveraging Riemannian Motion Policies

**相关度**: 0.837 | **arXiv ID**: 2406.17333v1 | **完整MD**: ❌

In real-world industrial environments, modern robots often rely on human operators for crucial decision-making and mission synthesis from individual tasks. Effective and safe collaboration between humans and robots requires systems that can adjust their motion based on human intentions, enabling dynamic task planning and adaptation. Addressing the needs of industrial applications, we propose a motion control framework that (i) removes the need for manual control of the robot's movement; (ii) facilitates the formulation and combination of complex tasks; and (iii) allows the seamless integration of human intent recognition and robot motion planning. For this purpose, we leverage a modular and purely reactive approach for task parametrization and motion generation, embodied by Riemannian Motion Policies. The effectiveness of our method is demonstrated, evaluated, and compared to \remove{state-of-the-art approaches}\add{a representative state-of-the-art approach} in experimental scenarios inspired by realistic industrial Human-Robot Interaction settings.

---

### 14. CLIPSwarm: Converting text into formations of robots

**相关度**: 0.833 | **arXiv ID**: 2311.11047v1 | **完整MD**: ❌

We present CLIPSwarm, an algorithm to generate robot swarm formations from natural language descriptions. CLIPSwarm receives an input text and finds the position of the robots to form a shape that corresponds to the given text. To do so, we implement a variation of the Montecarlo particle filter to obtain a matching formation iteratively. In every iteration, we generate a set of new formations and evaluate their Clip Similarity with the given text, selecting the best formations according to this metric. This metric is obtained using Clip, [1], an existing foundation model trained to encode images and texts into vectors within a common latent space. The comparison between these vectors determines how likely the given text describes the shapes. Our initial proof of concept shows the potential of this solution to generate robot swarm formations just from natural language descriptions and demonstrates a novel application of foundation models, such as CLIP, in the field of multi-robot systems. In this first approach, we create formations using a Convex-Hull approach. Next steps include more robust and generic representation and optimization steps in the process of obtaining a suitable swarm formation.

---

### 15. MAPS-X: Explainable Multi-Robot Motion Planning via Segmentation

**相关度**: 0.829 | **arXiv ID**: 2010.16106v3 | **完整MD**: ❌

Traditional multi-robot motion planning (MMP) focuses on computing trajectories for multiple robots acting in an environment, such that the robots do not collide when the trajectories are taken simultaneously. In safety-critical applications, a human supervisor may want to verify that the plan is indeed collision-free. In this work, we propose a notion of explanation for a plan of MMP, based on visualization of the plan as a short sequence of images representing time segments, where in each time segment the trajectories of the agents are disjoint, clearly illustrating the safety of the plan. We show that standard notions of optimality (e.g., makespan) may create conflict with short explanations. Thus, we propose meta-algorithms, namely multi-agent plan segmenting-X (MAPS-X) and its lazy variant, that can be plugged on existing centralized sampling-based tree planners X to produce plans with good explanations using a desirable number of images. We demonstrate the efficacy of this explanation-planning scheme and extensively evaluate the performance of MAPS-X.

---

## 低相关度文献 (24 篇)

<details>
<summary>点击展开查看</summary>

### 1. Automated Generation of MDPs Using Logic Programming and LLMs for Robotic Applications

**相关度**: 0.828 | **arXiv ID**: 2511.23143v1

We present a novel framework that integrates Large Language Models (LLMs) with automated planning and formal verification to streamline the creation and use of Markov Decision Processes (MDP). Our system leverages LLMs to extract structured knowledge in the form of a Prolog knowledge base from natur...

---

### 2. Egocentric Robots in a Human-Centric World? Exploring Group-Robot-Interaction in Public Spaces

**相关度**: 0.826 | **arXiv ID**: 2407.18009v1

The deployment of social robots in real-world scenarios is increasing, supporting humans in various contexts. However, they still struggle to grasp social dynamics, especially in public spaces, sometimes resulting in violations of social norms, such as interrupting human conversations. This behavior...

---

### 3. Robotic Motion Planning using Learned Critical Sources and Local Sampling

**相关度**: 0.825 | **arXiv ID**: 2006.04194v1

Sampling based methods are widely used for robotic motion planning. Traditionally, these samples are drawn from probabilistic ( or deterministic ) distributions to cover the state space uniformly. Despite being probabilistically complete, they fail to find a feasible path in a reasonable amount of t...

---

### 4. Infusing model predictive control into meta-reinforcement learning for mobile robots in dynamic environments

**相关度**: 0.822 | **arXiv ID**: 2109.07120v3

The successful operation of mobile robots requires them to adapt rapidly to environmental changes. To develop an adaptive decision-making tool for mobile robots, we propose a novel algorithm that combines meta-reinforcement learning (meta-RL) with model predictive control (MPC). Our method employs a...

---

### 5. Motion Planning for a Pair of Tethered Robots

**相关度**: 0.820 | **arXiv ID**: 2102.13212v1

Considering an environment containing polygonal obstacles, we address the problem of planning motions for a pair of planar robots connected to one another via a cable of limited length. Much like prior problems with a single robot connected via a cable to a fixed base, straight line-of-sight visibil...

---

### 6. LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics

**相关度**: 0.815 | **arXiv ID**: 2504.21716v1

We present an embodied robotic system with an LLM-driven agent-orchestration architecture for autonomous household object management. The system integrates memory-augmented task planning, enabling robots to execute high-level user commands while tracking past actions. It employs three specialized ag...

---

### 7. Deep Reinforcement Learning for Decentralized Multi-Robot Control: A DQN Approach to Robustness and Information Integration

**相关度**: 0.815 | **arXiv ID**: 2408.11339v1

The superiority of Multi-Robot Systems (MRS) in various complex environments is unquestionable. However, in complex situations such as search and rescue, environmental monitoring, and automated production, robots are often required to work collaboratively without a central control unit. This necessi...

---

### 8. Act, Perceive, and Plan in Belief Space for Robot Localization

**相关度**: 0.813 | **arXiv ID**: 2002.08124v3

In this paper, we outline an interleaved acting and planning technique to rapidly reduce the uncertainty of the estimated robot's pose by perceiving relevant information from the environment, as recognizing an object or asking someone for a direction.   Generally, existing localization approaches re...

---

### 9. MARL Warehouse Robots

**相关度**: 0.807 | **arXiv ID**: 2512.04463v2

We present a comparative study of multi-agent reinforcement learning (MARL) algorithms for cooperative warehouse robotics. We evaluate QMIX and IPPO on the Robotic Warehouse (RWARE) environment and a custom Unity 3D simulation. Our experiments reveal that QMIX's value decomposition significantly out...

---

### 10. Policies over Poses: Reinforcement Learning based Distributed Pose-Graph Optimization for Multi-Robot SLAM

**相关度**: 0.801 | **arXiv ID**: 2510.22740v1

We consider the distributed pose-graph optimization (PGO) problem, which is fundamental in accurate trajectory estimation in multi-robot simultaneous localization and mapping (SLAM). Conventional iterative approaches linearize a highly non-convex optimization objective, requiring repeated solving of...

---

### 11. Design of an Adaptive Lightweight LiDAR to Decouple Robot-Camera Geometry

**相关度**: 0.798 | **arXiv ID**: 2302.14334v2

A fundamental challenge in robot perception is the coupling of the sensor pose and robot pose. This has led to research in active vision where robot pose is changed to reorient the sensor to areas of interest for perception. Further, egomotion such as jitter, and external effects such as wind and ot...

---

### 12. Bayesian Optimization with Adaptive Kernels for Robot Control

**相关度**: 0.797 | **arXiv ID**: 2402.07021v1

Active policy search combines the trial-and-error methodology from policy search with Bayesian optimization to actively find the optimal policy. First, policy search is a type of reinforcement learning which has become very popular for robot control, for its ability to deal with complex continuous s...

---

### 13. Malleable Robots

**相关度**: 0.791 | **arXiv ID**: 2502.04012v1

This chapter is about the fundamentals of fabrication, control, and human-robot interaction of a new type of collaborative robotic manipulators, called malleable robots, which are based on adjustable architectures of varying stiffness for achieving high dexterity with lower mobility arms. Collaborat...

---

### 14. Moderating Group Conversation Dynamics with Social Robots

**相关度**: 0.790 | **arXiv ID**: 2408.00151v1

This research investigates the impact of social robot participation in group conversations and assesses the effectiveness of various addressing policies. The study involved 300 participants, divided into groups of four, interacting with a humanoid robot serving as the moderator. The robot utilized c...

---

### 15. A Tutorial on Meta-Reinforcement Learning

**相关度**: 0.789 | **arXiv ID**: 2301.08028v4

While deep reinforcement learning (RL) has fueled multiple high-profile successes in machine learning, it is held back from more widespread adoption by its often poor data efficiency and the limited generality of the policies it produces. A promising approach for alleviating these limitations is to ...

---

### 16. ViTAL: Vision-Based Terrain-Aware Locomotion for Legged Robots

**相关度**: 0.787 | **arXiv ID**: 2212.01246v1

This work is on vision-based planning strategies for legged robots that separate locomotion planning into foothold selection and pose adaptation. Current pose adaptation strategies optimize the robot's body pose relative to given footholds. If these footholds are not reached, the robot may end up in...

---

### 17. Towards Closing the Sim-to-Real Gap in Collaborative Multi-Robot Deep Reinforcement Learning

**相关度**: 0.781 | **arXiv ID**: 2008.07875v1

Current research directions in deep reinforcement learning include bridging the simulation-reality gap, improving sample efficiency of experiences in distributed multi-agent reinforcement learning, together with the development of robust methods against adversarial agents in distributed learning, am...

---

### 18. Stabilizing Extreme Q-learning by Maclaurin Expansion

**相关度**: 0.779 | **arXiv ID**: 2406.04896v2

In offline reinforcement learning, in-sample learning methods have been widely used to prevent performance degradation caused by evaluating out-of-distribution actions from the dataset. Extreme Q-learning (XQL) employs a loss function based on the assumption that Bellman error follows a Gumbel distr...

---

### 19. Assistax: A Hardware-Accelerated Reinforcement Learning Benchmark for Assistive Robotics

**相关度**: 0.774 | **arXiv ID**: 2507.21638v1

The development of reinforcement learning (RL) algorithms has been largely driven by ambitious challenge tasks and benchmarks. Games have dominated RL benchmarks because they present relevant challenges, are inexpensive to run and easy to understand. While games such as Go and Atari have led to many...

---

### 20. Causal-Paced Deep Reinforcement Learning

**相关度**: 0.766 | **arXiv ID**: 2507.02910v1

Designing effective task sequences is crucial for curriculum reinforcement learning (CRL), where agents must gradually acquire skills by training on intermediate tasks. A key challenge in CRL is to identify tasks that promote exploration, yet are similar enough to support effective transfer. While r...

---

### 21. A Hybrid Adaptive Controller for Soft Robot Interchangeability

**相关度**: 0.761 | **arXiv ID**: 2307.10838v2

Soft robots have been leveraged in considerable areas like surgery, rehabilitation, and bionics due to their softness, flexibility, and safety. However, it is challenging to produce two same soft robots even with the same mold and manufacturing process owing to the complexity of soft materials. Mean...

---

### 22. ARLBench: Flexible and Efficient Benchmarking for Hyperparameter Optimization in Reinforcement Learning

**相关度**: 0.740 | **arXiv ID**: 2409.18827v1

Hyperparameters are a critical factor in reliably training well-performing reinforcement learning (RL) agents. Unfortunately, developing and evaluating automated approaches for tuning such hyperparameters is both costly and time-consuming. As a result, such approaches are often only evaluated on a s...

---

### 23. Piezoelectric Soft Robot Inchworm Motion by Tuning Ground Friction through Robot Shape: Quasi-Static Modeling and Experimental Validation

**相关度**: 0.708 | **arXiv ID**: 2111.00944v2

Electrically-driven soft robots based on piezoelectric actuators may enable compact form factors and maneuverability in complex environments. In most prior work, piezoelectric actuators are used to control a single degree of freedom. In this work, the coordinated activation of five independent piezo...

---

### 24. Stochastic Approach for Modeling a Soft Robotic Finger with Creep Behavior

**相关度**: 0.696 | **arXiv ID**: 2306.07035v1

Soft robots have high adaptability and safeness which are derived from their softness, and therefore it is paid attention to use them in human society. However, the controllability of soft robots is not enough to perform dexterous behaviors when considering soft robots as alternative laborers for hu...

---


</details>
