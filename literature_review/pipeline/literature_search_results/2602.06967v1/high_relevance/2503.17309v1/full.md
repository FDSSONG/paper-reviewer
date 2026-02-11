# LLM+MAP: Bimanual Robot Task Planning using Large Language Models and Planning Domain Definition Language

Kun Chu∗, Xufeng Zhao, Cornelius Weber, and Stefan Wermter

Abstract— Bimanual robotic manipulation provides significant versatility, but also presents an inherent challenge due to the complexity involved in the spatial and temporal coordination between two hands. Existing works predominantly focus on attaining human-level manipulation skills for robotic hands, yet little attention has been paid to task planning on long-horizon timescales. With their outstanding in-context learning and zeroshot generation abilities, Large Language Models (LLMs) have been applied and grounded in diverse robotic embodiments to facilitate task planning. However, LLMs still suffer from errors in long-horizon reasoning and from hallucinations in complex robotic tasks, lacking a guarantee of logical correctness when generating the plan. Previous works, such as $\mathbf { L L M + P } ,$ extended LLMs with symbolic planners. However, none have been successfully applied to bimanual robots. New challenges inevitably arise in bimanual manipulation, necessitating not only effective task decomposition but also efficient task allocation. To address these challenges, this paper introduces $\mathbf { L L M + M A P }$ a bimanual planning framework that integrates LLM reasoning and multi-agent planning, automating effective and efficient bimanual task planning. We conduct simulated experiments on various long-horizon manipulation tasks of differing complexity. Our method is built using GPT-4o as the backend, and we compare its performance against plans generated directly by LLMs, including GPT-4o, V3 and also recent strong reasoning models o1 and R1. By analyzing metrics such as planning time, success rate, group debits, and planning-step reduction rate, we demonstrate superior performance of LLM+MAP, while also providing insights into robotic reasoning. Code is available at https://github.com/Kchu/LLM-MAP.

# I. INTRODUCTION

Humans effortlessly perform bimanual tasks, from tying shoelaces to flipping a book’s pages while holding a coffee cup, often without conscious thought. Our brain orchestrates complex spatial and temporal synchronizations, dynamically adjusting to external feedback in real time. In contrast, robots struggle with such dexterity. Even simple bimanual tasks require planning, synchronization, and complex computations. Bridging this gap is an inherent challenge in robotics [1], [2], highlighting the intricate interplay of perception, control, and adaptation.

With the development of deep learning techniques, there have been some advances in dexterous bimanual manipulations, like folding shirts [3], cutting vegetables [4], scooping food [5], etc. However, most existing works concentrate on learning human-level operational skills as a whole and overlook high-level task planning. This oversight stems from the

The authors are with the Knowledge Technology Group, Department of Informatics, University of Hamburg, 22527 Hamburg, Germany. E-mail: {kun.chu, xufeng.zhao, cornelius.weber, stefan.wermter}@uni-hamburg.de

∗Corresponding author.

significant challenges of effectively allocating long-horizon tasks between dual robotic arms, such as task understanding and decomposition, subtask assignment, and proper execution sequencing.

Large language models (LLMs) have shown remarkable reasoning and planning abilities in diverse fields [6] due to their training on massive textual data. Recent works have prompted LLMs in robotic task planning [7], [8], [9], [10]. LLM planning requires appropriate prompting to guide LLM to generate appropriate plans for specific embodiments and ground the plans to executable actions within the task environment. This is, however, especially challenging when dealing with complex tasks. LLMs suffer from their weakness in long-horizon reasoning and hallucinations [11], especially in spatial scenarios. Some works have explored the combination of LLMs with classical symbolic planners [12], [13] to alleviate the challenge. With LLMs serving as translators to formalize the natural language problems into some declarative language like PDDL (Planning Domain Definition Language, [14]) and ASP (Answer Set Programming, [15]), a plan is generated with logical correctness guarantee [16], [17]. Building on prior successes in integrating LLMs with symbolic planning and considering the emerging challenges in bimanual robotic scenarios, we pose the following research question: How can LLMs be integrated with multi-agent planning to achieve efficient spatial and temporal coordination in long-horizon bimanual robotic tasks?

To address the question, we propose the LLM+MAP (LLM $^ +$ Multi-Agent Planning with PDDL) framework, which utilizes LLMs to transform the bimanual robotic domain and problem into PDDL representation, and generates a partial-order plan through classical symbolic planners, allowing for efficient spatial and temporal coordination in bimanual manipulations. Specifically, we first define the bimanual robotic domain in PDDL, following the spatiotemporal control patterns introduced in the LABOR agent [9] for the control of NICOL, a semi-humanoid robot [18]. Based on the task description in natural language with the spatial scene information from the vision-models, the LLM is then prompted to transform task configuration into PDDL representation, compatible with the domain definition we provided. Based on the planning by symbolic solvers, a partial-order plan is generated with logical correctness and executed on the bimanual robot. We conduct extensive experiments to evaluate LLM+MAP against both large-scale coding models, GPT-4o and DeepSeek-V3 [19], and the state-

of-the-art reasoning models, OpenAI-o11 and DeepSeek-R12 [20], on three task domains in the NICOL bimanual robot environment. Experimental results show that, compared to directly generating task plans with even strong reasoning models, our approach significantly outperforms in terms of reduced plan generation time, higher success rates, and more efficient task allocation.

# II. RELATED WORKS

In this section, we first describe task planning methods in robotics, including symbolic planners, LLM planners, and their combined applications. Then, we present a brief overview of the works in bimanual manipulation and multiagent planning.

# A. Task Planning in Robotics

Task planning aims at generating plans, i.e., sequences of actions from a given action set, to achieve specific goals in given scenarios [21], [22].

Planning with Symbolic Planners. To yield a generalpurpose automated planning system, classical planners rely on a certain type of declarative language to formalize the domains and problems. Since the introduction of STRIPS [23] in early AI research, several types of language have been proposed and widely used, including answer set programming (ASP, [15]) and planning domain definition language (PDDL, [14]). Previous works have applied symbolic planning methods in diverse tasks [22], [24], [25], [26], [27]. Task and motion planning approaches employ a high-level task planner to generate symbolic actions in discrete spaces and a low-level motion planner to generate motion trajectories in continuous space [28], [29]. Most of the planners developed in these works would generate plans with guaranteed logical correctness, yet requiring domain-specific programming languages as domain, problem, and solution representations. Inspired by these features and recent works in [12], [13], we apply PDDL to a bimanual robot scenario interacting with a human, using LLM to transform the scenario information and natural language task descriptions into PDDL representations to construct a partial-order plan using classical planners.

Planning with LLMs. With the rapid developments in recent years, using natural language instructions as a prompt for LLMs to directly generate task plans has become an emergent trend in robotics. Several recent methods have leveraged LLMs as planners in diverse robotic scenarios [7], [30], [16], [9]. For instance, SayCan [7] explored utilizing LLMs to propose feasible solutions to complex tasks based on their common-sense knowledge about the world, and then ground them to specific embodiments and environments through value functions. However, LLMs suffer from their shortcomings in long-horizon reasoning and frequent hallucinations in complex tasks [31], [32], [11]. Despite some work on iterative querying LLMs by providing feedback or error messages [33], [8], [34], [9], such a strategy requires effort

in careful prompt and system design to handle the feedback with LLMs.

With LLMs’ extraordinary in-context learning capabilities, some works investigate using LLMs to translate natural language descriptions about a task and the setting to a PDDL-readable representation, enabling classical planners to generate guaranteed solutions [12], [13], [17], [35]. Existing approaches that integrate LLMs with symbolic planning, such as ViLaIn [17], focus exclusively on scenarios requiring sequential planning, without considering the requirements of parallel execution or multi-agent planning. In contrast, our work systematically examines the distinctions between sequential and parallel planning, introducing dedicated metrics to rigorously evaluate these differences.

# B. Bimanual Manipulation and Multi-Agent Planning

Bimanual Manipulation. With the development of deep learning techniques, some progress [2] has been made in learning dexterous manipulation skills using two grippers [4] or human-like hands [36], like scooping food [5], folding clothes [37], zipping zippers [4], etc. However, these works focus on designing learning-based systems to perform human-level operation skills, neglecting the explicit planning abilities in complex long-horizon tasks. As illustrated in these works, the high complexity associated with the variety of bimanual patterns suggests that high-level planning should be considered as well for an integrated control system design [1], [38].

Bimanual and Multi-Agent Planning. Early works explored using symbolic methods for designing multi-agent systems to generate an efficient plan for complex tasks in a textual world [25], [39], [40]. Recent works have leveraged LLMs for multi-agent collaboration, where either a centralized or distributed LLM analyzes, decomposes, and assigns tasks to agent candidates in both textual [41] and robotic environments [42]. A bimanual robot can be viewed as a specialized multi-agent system, typically comprising homogeneous agents (arms) operating within a confined workspace (space around the robot body). Unlike many multi-agent systems where robots handle subtasks with varying degrees of independence, bimanual planning involves tightly coupled interactions between two arms, making it uniquely constrained in both spatial and temporal dimensions. For bimanual task planning, recent work DAG-Plan [10] employs LLMs to decompose tasks into directed acyclic graphs, assigning them to the left and right arms based on predefined rules that account for availability. However, existing approaches heavily depend on the reasoning and coding capabilities of LLMs for accurate planning, overlooking the need for computational search in an abstract space to optimize coordination. Additionally, integrating abstract representations could enhance self-verification before execution.

To obtain robust and efficient bimanual plans, we format the spatial scene information for the task with linguistic task descriptions into PDDL definitions, enabling a partial-order plan to be generated for bimanual tasks, with guaranteed logical correctness and higher efficiency.

![](images/3afcd8fffb86d7bf8eb612fc6247fb80d8769234a1b5e1a3782997ddf5629a2e.jpg)  
Fig. 1: Illustrative partial-order plan for bimanual manipulation (cf. Section III), where $C$ , $A$ and $P$ indicate cup, area and point respectively. Actions for the left and right hands are colored in light blue and red respectively. Two boxes shown horizontally side by side represent two actions executed in parallel.

# III. METHOD

Given a task description in natural language, we aim to generate a valid and efficient plan for a bimanual robot based on the initial task configurations, e.g., spatial information about the objects with respect to the robot. In this sense, this section introduces the three elements of $\mathbf { L L M + M A P }$ : spatial scene description, PDDL definitions with a multiagent solver for the bimanual robotic scenario, and the LLM as a PDDL writer.

# A. Spatial Scene Understanding in Bimanual Robots

Based on spatio-temporal control patterns introduced in previous work [9], we define the manipulation areas for the hands based on the reachable areas:

• Uncoordinated Areas: areas that only one hand can reach, whereas the other one cannot, i.e., the left area and right area respectively. In those two areas, the two hands can act independently and do not influence each other; thus, manipulations can naturally occur in parallel.   
• Coordinated Area: the area that both hands can reach, i.e., the overlap area in the middle. The two hands act and manipulate dependently in spatial and temporal relations. They can collaborate either asynchronously or synchronously – an asynchronous type of control involves one hand constructing pre-conditions for the

other, while a synchronous control indicates a, usually precise, mutual dependency between them.

Based on this operational paradigm, for a bimanual task, we first need to figure out the areas in which the task-relevant objects and positions are located. To do this, we marked black lines on the edges of the work area to visualize and distinguish different areas. When receiving a task description, we use object-detection models like OWLv2 [43] to locate objects on the desktop according to the task-related text queries. Then, based on the object bounding box information compared with the black lines on the image, a rule-based recognizer is used to determine the area in which each object is located.

# B. Partial-order Plan Generation with LLMs and PDDL

We formalize the bimanual manipulation scenario as a special case of multi-agent task planning problems. In this section, we will first informally introduce the preliminaries of PDDL, and then define the bimanual domain in PDDL. We refer the reader to other references [44], [25] for a formal treatment.

# 1) Planning Domain Definition Language

Planning Domain Definition Language (PDDL, [14]) is a declarative language for standardizing the formalization of planning problems. In general, a planning problem is characterized as a tuple $\tau$ :

$$
\mathcal {T} = <   \mathcal {O}, \mathcal {P}, \mathcal {A}, \mathcal {S}, \mathcal {G} >,
$$

where $\mathcal { O }$ is the set of objects, $\mathcal { P }$ is the set of predicates, $\mathcal { A }$ is the set of actions, $s$ is the initial state, and $\mathcal { G }$ is the goal state. A state is defined as a list of predicates applied to objects and agents, that hold. Each action is defined with parameters specifying input types and describes the pre-conditions and effects of executing such action, in terms of a series of predicates for the object inputs. The PDDL presentation of a planning problem consists of two files, 1) a domain, which defines objects, predicates, and actions with pre-condition and effect specifications that describe the task world, and 2) a problem, which includes an initial state and a desired goal state which are the sets of several specific predicates.

# 2) Multi-agent Planning

In multi-agent problems, there can be a set of agents from the set of agents, $\mathcal { R } \ : = \ : \{ R _ { 1 } , . . . , R _ { N } \}$ . For an agent $R _ { i } \in \mathcal { R }$ , it can have its own set of actions $\mathcal { A } ^ { i }$ , predicates ${ \mathcal { P } } ^ { i }$ , initi states $S ^ { i }$ , and goal states $\mathcal { G } ^ { i }$ . In the cooperative multi-agent problems, the goal of each agent remains the same, i.e., ${ \mathcal { G } } ^ { i } = { \mathcal { G } }$ , and only by cooperating can the goal be accomplished. In ${ \mathcal { P } } ^ { i }$ , there are public predicates from $\mathcal { P }$ and a certain number of private predicates, i.e., environmentcommon and agent-specific properties. When executing an action inside one’s own action set, one needs to consider if the value of the predicate from ${ \mathcal { P } } ^ { i }$ and the environment’s predicate $\mathcal { P }$ meet the action’s pre-conditions. Besides, a cooperative action among agent $i$ and $j$ can only be executed if the value for several predicates from ${ \mathcal { P } } ^ { i }$ , $\mathcal { P } ^ { j }$ and $\mathcal { P }$ are hold. In this sense, the common goal can be distributed to different agents and accomplished through their cooperation

![](images/e5e01e5820892fa9ca0930828fddbb55020c0d83708515f642063312759ce2a7.jpg)  
Fig. 2: Overview of our framework. According to the spatial description of the scene, with the bimanual domain knowledge and task description, LLM+MAP generates a PDDL representation that is used for multi-agent symbolic planning. Then, a valid partial-order plan is generated and executed by the NICOL bimanual robot (see Figure 3 for scenario setting).

via interactions. To this end, the plan generated is a partialorder plan, which is a sequence of actions with dependencies but also flexibilities in execution orders, enabling parallel processes in multi-agent systems [40]. A dominant method for such type of problems is FMAP (Forward MultiAgent Planning, [25]), which effectively handles both cooperative and independent planning problems, outperforming existing multi-agent planning systems.

Inspired by the above works, we formalize a bimanual robot to a multi-agent system, with LEFT and RIGHT as two separate agents. With private predicate control, each of them has their exclusive right to control the left and right hand respectively. With a cooperative goal, they will have operations in their areas, and an overlap area in between for interactions.

# 3) PDDL for Bimanual Robotic Scenario

In the bimanual robotic scenario, to specify the spatiotemporal patterns we introduced and fundamental logics about manipulations, we design a list of predicates, shown in Table I. We define object types in $\mathcal { O }$ as: hand, area, object and point, and define a list of predicates for them, including their properties and relationships between them. Based on these definitions, we can define symbolic actions with parameter inputs and their pre-conditions and effects descriptions. We design atomic and fundamental skills for the homogenous robotic hand, catering for both independent (single-hand) and joint operations, shown in Table II. For a joint operation involving both hands, the action is not defined with specific hand(s) as input parameters (since only one hand can be controlled through the agent’s private predicate). Instead, the precondition requires both hands to be in an available state. Therefore, joint operations are a unique class of actions executed by both hands, despite being initiated by a single agent.

# 4) LLMs as a PDDL Writer

Under the above PPDL definition principles, we prompt the LLM to generate the initial state definition according to scene descriptions from the camera image, and the goal state definition based on the input of natural language task descrip-

TABLE I: Definition of PDDL predicates for the bimanual robot scenario. By abstracting hand, area, and object, the predicates capture affordance properties and relationships, enabling solutions that generalize across diverse task domains.   

<table><tr><td>Properties</td><td>Relationships</td></tr><tr><td>control (hand)</td><td>arm_at (hand, area)</td></tr><tr><td>available (hand)</td><td>arm_access (hand, area)</td></tr><tr><td>is_graspale (object)</td><td>lifting (object, hand)</td></tr><tr><td>is_free (object)</td><td>object_at_area (object, area)</td></tr><tr><td>is_releasable (point)</td><td>object_at_point (object, point)</td></tr><tr><td>isAccessible (point)</td><td>point_at (point, area)</td></tr></table>

TABLE II: Bimanual skills design. Single skills are designed independently for single hands, whereas joint skills are designed for two-hand symmetric manipulations with cooperation. Additional verification parameters are for PDDL definition to maintain appropriate pre-condition verification.   

<table><tr><td>Type</td><td>Skill(Parameters)</td><td>Verif. Param.</td></tr><tr><td rowspan="7">Single</td><td>grasp(hand, object)</td><td>area</td></tr><tr><td>move_to(hand, object, point)</td><td>area</td></tr><tr><td>release(hand, object)</td><td>point, area</td></tr><tr><td>push(hand, object, target_area)</td><td>source_area</td></tr><tr><td>pour(hand)</td><td>object1,object2</td></tr><tr><td>move_above(hand, source_object, target_object)</td><td>area</td></tr><tr><td>place(hand, source_object, target_object)</td><td>area</td></tr><tr><td rowspan="2">Joint</td><td>co_hold(object)</td><td>-</td></tr><tr><td>co_move_to(point)</td><td>-</td></tr></table>

tions. Since LLMs can effectively understand and generate Python code with minimal errors, we utilize the Unified-Planning Python library [45], which streamlines problem definition and simplifies the invocation of built-in symbolic solvers, including the well-known Fast-Downward [24] and FMAP ([25]) solvers. To reduce coding errors generated by the LLM, we re-prompt it with error messages from the Python interpreter when an error occurs, enabling iterative improvements through regeneration.

![](images/0cf346fa03e4fef45e11fc2784e4284718c0739da5b915a01500977183b4fb3d.jpg)  
(a) ServeWater

![](images/54622397ef966e3ada33c4b54d24c4e29637c5d9aaf0f7d87de2f3f49e33fc57.jpg)  
(b) ServeFruit

![](images/65c60bfd76679d931d71973482a7f511c5b852faa93fea986c2ad6cfb50ed40e.jpg)  
(c) StackBlock   
Fig. 3: A visualization of the three task domains. In ServeWateer, the brown box is placed either in the left or right area to store the blue cup, while the cups and the human user are in random areas. In ServeFruit, the human stands exclusively in front of the overlap area to receive the bowl, while the fruits and the bowl are in random areas. In StackBlock, the blocks are distributed at random positions over the three areas, while the human user stands in front of a random area.

# IV. EXPERIMENTS

We conduct the following experiments to evaluate to what extent our method can achieve efficient bimanual control in robotic tasks. Specifically, we evaluate the success and efficiency of the proposed LLM+MAP in three task domains. We built LLM+MAP on GPT-4o as the backend. As a baseline, GPT-4o is prompted with bimanual domain knowledge to generate executable plans directly. The complexity of the task necessitates stronger reasoning ability for direct plan generation. Therefore, given recent advancements in reasoningcapable LLMs, we additionally conduct experiments with o1 and R1 model as two strong baselines. Besides, we include the V3 model as a counterpart to R1, as it has the same size but lacks reasoning capabilities.

# A. Environment Setup

The experiments are conducted in the CoppeliaSim3 simulator4 on the NICOL robot [18], [8], which is designed to blend social interaction with reliable object manipulation capabilities. We use one of the two cameras at its eye positions for visual perception. At the manipulation level, it is equipped with two arms, each with six degrees of freedom, and an adult-sized, five-fingered manipulator attached to it for precise manipulation of everyday objects.

Three bimanual task domains are designed in a humanrobot environment: ServeWater, ServeFruit, and StackBlock. Such a setting closely resembles the real-world interaction, and also brings about the complexity and diversity of tasks through the spatial relationship between the human and the task-related objects.

In the ServeWater task domain, there are two cups on the work table, an empty yellow cup and a water-filled blue cup, and the task requires the robot to serve the water in the yellow cup to the human, while putting the blue cup to a

specified store point on the brown box, which is randomly located in the left or right area. In the ServeFruit task domain, there is a banana, an apple, and a big red bowl, and the task requires serving the fruits with a bowl to the human. It should be noted that the bowl is not graspable with one single hand, and the symmetric manipulations for two hands can only be done in the overlap area. In this sense, the bowl should be pushed to the overlap area so that it can be held by both hands. In the StackBlock task domain, there are several blocks with different colors randomly located on the table, and the task goal is to stack one or two piles with specific blocks in a certain order. We design the task’s configurations in two aspects: the total number of blocks to be stacked, and the number of cubes in each pile. Specifically, the task requires the robot to stack the selected four or five blocks into a specific pile in terms of $\left[ ( 2 , 2 ) , ( 3 , 1 ) , ( 4 , 0 ) \right]$ or $[ ( 2 , 3 ) , ( 4 , 1 ) , ( 5 , 0 ) ]$ , respectively. An example of a task goal with $( 4 , 1 )$ in natural language is, the task is to stack the selected five blocks in two piles on the tray right in front of the human, where one pile is yellow over red over purple over black and one pile is green.

# B. Metrics

To examine the efficacy and efficiency of generated plans, we compare our proposed methods with baselines along the following three metrics:

• Planning Time (PT). For LLM-direct task planning, the time cost depends solely on the inference time of certain LLMs, while the planning time of our method is composed of LLM inference time and symbolic planning time.   
• Success Rate (SR), which reveals the overall ability for task completion.   
• Group Debits (GD), a metric to compare the planning efficiency of models.5 Specifically, we set the debits of the “champion” model (the one that uses the fewest

planning steps) to 0. Other models are assigned debits according to the number of planning steps exceeding those of the champion (higher debits mean worse performance).

# C. Results

Planning Time. As is shown in Table III, we have several immediate observations: (1) the PT of GPT-4o, V3 direct and LLM+MAP are dramatically shorter than the other two advanced reasoning models, o1 and R1. (2) The LLM inference time increases across all models as task complexity grows. (3) In analyzing the PT distribution for LLM+MAP, the LLM inference time remains relatively stable, while the symbolic planning time for simpler tasks is sufficiently small (smaller than the LLM inference time), but increases considerably for more complex tasks with a larger search space. In practice,

TABLE III: Task Planning Time (s) for different models. For LLM+MAP, we also provide the time spent on each module, including LLM inference time for code generation and PDDL planning time.   

<table><tr><td>Model</td><td>ServeWater</td><td>ServeFruit</td><td>StackBlock-4</td><td>StackBlock-5</td></tr><tr><td>gpt-4o direct</td><td>5.33 ±6.70</td><td>4.17 ±1.35</td><td>7.82 ±2.46</td><td>11.17 ±20.65</td></tr><tr><td>V3 direct</td><td>10.80 ±1.90</td><td>10.41 ±2.03</td><td>14.00 ±2.41</td><td>17.20 ±2.78</td></tr><tr><td>R1 direct</td><td>122.42 ±40.16</td><td>144.42 ±70.94</td><td>220.85 ±72.68</td><td>168.28 ±38.59</td></tr><tr><td>o1 direct</td><td>104.29 ±71.69</td><td>77.68 ±31.62</td><td>96.85 ±51.00</td><td>66.38 ±17.96</td></tr><tr><td>LLM+MAP</td><td>11.34 ±6.73</td><td>7.75 ±0.91</td><td>34.97 ± 21.53</td><td>62.75 ±26.05</td></tr><tr><td>∈ LLM</td><td>9.55 ±6.70</td><td>6.00 ±0.91</td><td>13.08 ±4.19</td><td>18.23 ±8.11</td></tr><tr><td>∈ MAP</td><td>1.80 ±0.49</td><td>1.74 ±0.25</td><td>21.89 ±20.97</td><td>44.52 ±23.40</td></tr></table>

multi-agent planning can be time-consuming with the FMAP solver, so we set a timeout to avoid excessively long computation times. As an alternative, we convert it to a singlerobot task, allowing for a feasible solution with the BFWS solver [46]. According to the bimanual characteristics, the generated plan is then post-processed as a partial-order plan using automated graph tools.

Success Rate. From the experimental results presented in Table IV, we have the following findings: (1) It is clear that our proposed method achieves the highest performance out of all tasks, thanks to the integration of LLM coding and multi-agent planning. This result is impressive because the original performance of GPT-4o, as a base LLM with specifically tuning in the pursuit of strong reasoning ability, performs poorly while our method – built on top of this base model – outperforms. GPT-4o’s strength in in-context understanding minimizes errors during the generation of PDDL definitions. In the StackBlock domain, such errors primarily result from GPT-4o defining the task goal with an incorrect block order, which consequently leads to execution failures in the actual task configuration. (2) Long-horizon robotic tasks require strong reasoning ability for correct task completions, specifically tuned reasoning LLMs, o1 and R1, trade inference time compute (indicating both higher cost in both time and expense) with a better reasoning competence, resulting in higher SR in our experiments. (3) Comparing the results of V3 and R1, it is enlightening that,

despite having the same parameter scale, R1 dramatically outperforms V3. This suggests that strong reasoning ability is crucial for solving long-horizon tasks, particularly when the base language model is not integrated with a planning mechanism like LLM+MAP.

TABLE IV: Success rate $( \% )$ of plan execution across the task domains.   

<table><tr><td>Model</td><td>ServeWater</td><td>ServeFruit</td><td>StackBlock-4</td><td>StackBlock-5</td></tr><tr><td>gpt-4o direct</td><td>2</td><td>13</td><td>2</td><td>0</td></tr><tr><td>V3 direct</td><td>2</td><td>6</td><td>6</td><td>1</td></tr><tr><td>R1 direct</td><td>67</td><td>63</td><td>94</td><td>77</td></tr><tr><td>o1 direct</td><td>84</td><td>82</td><td>95</td><td>88</td></tr><tr><td>LLM+MAP</td><td>100</td><td>100</td><td>96</td><td>97</td></tr></table>

Group Debits. As is discussed in Subsection IV-B, GD is a metric to compare the planning efficiency of models. From Figure 4, we find that (1) LLM+MAP almost dominates the competitions, especially in easier tasks, with mass mainly distributed around 0 debits (relative optimal, i.e. winner with minimal planning steps among competitors). (2) With the growth of task complexity, the GD of reasoning models is comparable to the multi-agent planning results, indicating that stronger reasoning ability helps a comprehensive understanding of the temporal and spatial resilience of dual hands. However, for easier tasks, plans generated by those strong reasoning models are far from being efficient, we hypothesize that this non-efficiency may stem from the overthink [47] of current reasoning models, especially of the R1 model, which takes excessive reasoning time (cf. Table III) and outputs wordy content.

Discussion. The combination of the above metrics provides additional insights. Although the SR of the R1 model is lower than that of the o1 model, its GD scores higher, indicating greater efficiency in terms of bimanual coordination and suggesting a superior temporal understanding. In contrast, the o1 model appears to have a stronger spatial understanding, which is crucial for successful task completion. The decoupling of temporal and spatial dimensions, along with the corresponding investigation, is left as a direction for future work.

# D. Ablation Study

To investigate the efficacy of multi-agent PDDL planning in comparison to traditional planning, which treats configurations of both hands as a unified collection of presets of a single agent, we conduct an ablation study by removing MAP component and only use BFWS [46] as its solver to generate sequential plan, resulting in an adapted6 implementation of $\mathrm { L L M + P }$ [12]. We compute the Planning Step Reduction Rate (PSRR) as

$$
\mathrm{PSRR} = \frac{N_{+P} - N_{+MAP}}{N_{+P}}\times 100\% ,
$$

![](images/e94adf43a1b5b5a2e381e2da5f423924daeb2e7c3c6cb98e4362fedda7f2dfa0.jpg)  
(a) ServeWater

![](images/b14648afc1554ce02bc0389b09c3ebec2a06d5f8b728c4582cf728f7b9624ab5.jpg)  
(b) ServeFruit

![](images/1054ff9809789c877d3fd5b919ad67f52bf6fa0af53e424571ea53854180594c.jpg)  
(c) StackBlock-4

![](images/16cf86d284862ccff3c3f43aa30358c374b55206f9d9667bfdfd0a6123a6fd45.jpg)  
(d) StackBlock-5   
Fig. 4: The Group Debits statistics among successful tasks in three domains, the smaller the better.

where $N _ { + \mathrm { P } }$ and $N _ { + \mathrm { M A P } }$ are the number of planning steps for $\mathrm { L L M + P }$ and LLM+MAP respectively. As shown in Figure 5 (across successful tasks in 100 runs), compared to the sequential plans generated by $\mathrm { L L M + P } ,$ our method facilitates more parallel task allocation for both hands, resulting in a significant improvement in overall efficiency.

![](images/2eeeed4eb015cd84142d678e7c5d4dc2879c213a13ebf0e8feabd3364f5a20fa.jpg)  
Fig. 5: Planning Step Reduction Rate $( \% )$ of $\mathbf { L L M + M A P }$ over LLM+P, showcasing the improved efficiency of Multiagent planning.

# V. CONCLUSION

We propose $\mathbf { L L M + M A P } ,$ , which formulates the bimanual robot task planning problem as a special form of multiagent planning, leveraging the coding and reasoning ability of LLMs and formalized language representations for efficient multi-agent planning. Specifically, vision models transform spatial information and task descriptions into PDDL representations in bimanual robot scenarios, achieving efficient spatial and temporal coordination with guaranteed correctness and optimality by symbolic planners. Extensive experiments on three task domains showcase that our framework outperforms planning results with GPT-4o, V3 and even strong reasoning models o1 and R1, in terms of higher success rate and efficiency with less plan generation time.

Limitations and Future Work. While our main focus in this paper is not on the acquisition and design of bimanual skills, the execution of the underlying task assumes that existing motion primitives serve the purpose well, raising a certain gap when transferring to the real world. Integrating with learning-based bimanual robotic skills will be our main focus in the future. We have used the LLM+MAP framework for merely two agents, i.e., the robot’s hands, while the feasibility and effectivity of extending our framework to control a larger number of agents are still to be investigated.

Hierarchical planning with LLM bootstrapping can be a viable direction to explore for task planning in large-scale multi-robot tasks. Additionally, considering the dynamic nature of the world, future work includes incorporating action durations or costs for more fine-grained bimanual planning, enabling adaptive re-planning in response to action failures or unexpected environmental changes, and improving the verification of action preconditions and effects, etc.

# ACKNOWLEDGMENT

The authors gratefully acknowledge support from the Horizon Europe project TERAIS and the MSCA Doctoral Network TRAIL. Additionally, they express their gratitude to OpenAI’s Researcher Access Program for generously providing API tokens.

# REFERENCES

[1] F. Krebs and T. Asfour, “A bimanual manipulation taxonomy,” IEEE Robotics and Automation Letters, vol. 7, no. 4, pp. 11 031–11 038, 2022.   
[2] M. Drolet, S. Stepputtis, S. Kailas, A. Jain, J. Peters, S. Schaal, and H. B. Amor, “A comparison of imitation learning algorithms for bimanual manipulation,” IEEE Robotics and Automation Letters, vol. 9, no. 10, pp. 8579–8586, 2024.   
[3] K. Shaw, Y. Li, J. Yang, M. K. Srirama, R. Liu, H. Xiong, R. Mendonca, and D. Pathak, “Bimanual dexterity for complex tasks,” in The 8th Annual Conference on Robot Learning (CoRL), 2024.   
[4] J. Grannen, Y. Wu, B. Vu, and D. Sadigh, “Stabilize to act: Learning to coordinate for bimanual manipulation,” in The 7th Conference on Robot Learning (CoRL). PMLR, 2023, pp. 563–576.   
[5] J. Grannen, Y. Wu, S. Belkhale, and D. Sadigh, “Learning bimanual scooping policies for food acquisition,” in Proceedings of The 6th Conference on Robot Learning, ser. Proceedings of Machine Learning Research, K. Liu, D. Kulic, and J. Ichnowski, Eds., vol. 205. PMLR, 14–18 Dec 2023, pp. 1510–1519. [Online]. Available: https://proceedings.mlr.press/v205/grannen23a.html   
[6] W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, et al., “A survey of large language models,” arXiv preprint arXiv:2303.18223, vol. 1, no. 2, 2023.   
[7] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, R. Julian, et al., “Do as I can, not as I say: Grounding language in robotic affordances,” in Proceedings of The 6th Conference on Robot Learning (CoRL). PMLR, 2023, pp. 287–318.   
[8] X. Zhao, M. Li, C. Weber, M. B. Hafez, and S. Wermter, “Chat with the environment: Interactive multimodal perception using large language models,” in 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2023, pp. 3590–3596.   
[9] K. Chu, X. Zhao, C. Weber, M. Li, W. Lu, and S. Wermter, “Large language models for orchestrating bimanual robots,” in 2024 IEEE-RAS 23rd International Conference on Humanoid Robots (Humanoids), 2024, pp. 328–334.

[10] Z. Gao, Y. Mu, J. Qu, M. Hu, L. Guo, P. Luo, and Y. Lu, “DAGplan: Generating directed acyclic dependency graphs for dual-arm cooperative planning,” arXiv preprint arXiv:2406.09953, 2024.   
[11] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen, J. Tang, X. Chen, Y. Lin, et al., “A survey on large language model based autonomous agents,” Frontiers of Computer Science, vol. 18, no. 6, p. 186345, 2024.   
[12] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone, “LLM+P Empowering large language models with optimal planning proficiency,” arXiv preprint arXiv:2304.11477, 2023.   
[13] Y. Xie, C. Yu, T. Zhu, J. Bai, Z. Gong, and H. Soh, “Translating natural language to planning goals with large-language models,” arXiv preprint arXiv:2302.05128, 2023.   
[14] C. Aeronautiques, A. Howe, C. Knoblock, I. D. McDermott, A. Ram, M. Veloso, D. Weld, D. W. Sri, A. Barrett, D. Christianson, et al., “PDDL— the planning domain definition language,” Technical Report, Tech. Rep., 1998.   
[15] V. Lifschitz, “Answer set programming and plan generation,” Artificial Intelligence, vol. 138, no. 1-2, pp. 39–54, 2002.   
[16] Y. Ding, X. Zhang, C. Paxton, and S. Zhang, “Task and motion planning with large language models for object rearrangement,” in 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2023, pp. 2086–2092.   
[17] K. Shirai, C. C. Beltran-Hernandez, M. Hamaya, A. Hashimoto, S. Tanaka, K. Kawaharazuka, K. Tanaka, Y. Ushiku, and S. Mori, “Vision-language interpreter for robot task planning,” in 2024 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2024, pp. 2051–2058.   
[18] M. Kerzel, P. Allgeuer, E. Strahl, N. Frick, J.-G. Habekost, M. Eppe, and S. Wermter, “NICOL: A neuro-inspired collaborative semihumanoid robot that bridges social interaction and reliable manipulation,” IEEE Access, vol. 11, pp. 123 531–123 542, 2023.   
[19] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, et al., “Deepseek-v3 technical report,” arXiv preprint arXiv:2412.19437, 2024.   
[20] DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, et al., “DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning,” 2025. [Online]. Available: https://arxiv.org/abs/2501.12948   
[21] A. E. Gerevini, “An introduction to the planning domain definition language (PDDL): Book review,” Artificial Intelligence, vol. 280, p. 103221, 2020.   
[22] Y.-q. Jiang, S.-q. Zhang, P. Khandelwal, and P. Stone, “Task planning in robotics: an empirical comparison of PDDL-and ASP-based systems,” Frontiers of Information Technology & Electronic Engineering, vol. 20, pp. 363–373, 2019.   
[23] R. E. Fikes and N. J. Nilsson, “STRIPS: A new approach to the application of theorem proving to problem solving,” Artificial Intelligence, vol. 2, no. 3-4, pp. 189–208, 1971.   
[24] M. Helmert, “The fast downward planning system,” Journal of Artificial Intelligence Research, vol. 26, pp. 191–246, 2006.   
[25] A. Torreno, E. Onaindia, and O. Sapena, “FMAP: Distributed cooperative multi-agent planning,” Applied Intelligence, vol. 41, pp. 606–626, 2014.   
[26] Y. Ding, X. Zhang, X. Zhan, and S. Zhang, “Task-motion planning for safe and efficient urban driving,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020, pp. 2119– 2125.   
[27] Y. Jiang, H. Yedidsion, S. Zhang, G. Sharon, and P. Stone, “Multi-robot planning with conflicts and synergies,” Autonomous Robots, vol. 43, no. 8, pp. 2011–2032, 2019.   
[28] L. P. Kaelbling and T. Lozano-Perez, “Integrated task and motion ´ planning in belief space,” The International Journal of Robotics Research, vol. 32, no. 9-10, pp. 1194–1227, 2013.   
[29] Z. Jiao, Z. Zhang, W. Wang, D. Han, S.-C. Zhu, Y. Zhu, and H. Liu, “Efficient task planning for mobile manipulation: a virtual kinematic chain perspective,” in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2021, pp. 8288–8294.   
[30] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents,” in International Conference on Machine Learning (ICML). PMLR, 2022, pp. 9118–9147.

[31] X. Zhao, M. Li, W. Lu, C. Weber, J. H. Lee, K. Chu, and S. Wermter, “Enhancing zero-shot chain-of-thought reasoning in large language models through logic,” in Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024). ELRA and ICCL, May 2024, pp. 6144–6166.   
[32] K. Stechly, K. Valmeekam, and S. Kambhampati, “On the selfverification limitations of large language models on reasoning and planning tasks,” arXiv preprint arXiv:2402.08115, 2024.   
[33] Z. Wang, S. Cai, G. Chen, A. Liu, X. Ma, Y. Liang, and T. CraftJarvis, “Describe, explain, plan and select: interactive planning with large language models enables open-world multi-task agents,” in Proceedings of the 37th International Conference on Neural Information Processing Systems (NeurIPS), ser. NIPS ’23. Red Hook, NY, USA: Curran Associates Inc., 2023.   
[34] K. Rana, J. Haviland, S. Garg, J. Abou-Chakra, I. Reid, and N. Suenderhauf, “SayPlan: Grounding large language models using 3D scene graphs for scalable robot task planning,” in 7th Annual Conference on Robot Learning (CoRL), 2024.   
[35] Y. Chen, J. Arkin, C. Dawson, Y. Zhang, N. Roy, and C. Fan, “AutoTAMP: Autoregressive task and motion planning with LLMs as translators and checkers,” in 2024 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2024, pp. 6695–6702.   
[36] Y. Chen, T. Wu, S. Wang, X. Feng, J. Jiang, Z. Lu, S. McAleer, H. Dong, S.-C. Zhu, and Y. Yang, “Towards human-level bimanual dexterous manipulation with reinforcement learning,” Advances in Neural Information Processing Systems (NeurIPS), vol. 35, pp. 5150– 5163, 2022.   
[37] Y. Avigal, L. Berscheid, T. Asfour, T. Kroger, and K. Goldberg, ¨ “Speedfolding: Learning efficient bimanual folding of garments,” in 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2022, pp. 1–8.   
[38] C. Smith, Y. Karayiannidis, L. Nalpantidis, X. Gratal, P. Qi, D. V. Dimarogonas, and D. Kragic, “Dual arm manipulation—a survey,” Robotics and Autonomous systems, vol. 60, no. 10, pp. 1340–1353, 2012.   
[39] J. Cox and E. Durfee, “Efficient and distributable methods for solving the multiagent plan coordination problem,” Multiagent and Grid Systems, vol. 5, no. 4, pp. 373–408, 2009.   
[40] M. Ghallab, D. Nau, and P. Traverso, Automated Planning: theory and practice. Elsevier, 2004.   
[41] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, J. Wang, C. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, “MetaGPT: Meta programming for a multi-agent collaborative framework,” in The Twelfth International Conference on Learning Representations (ICLR), 2024.   
[42] S. S. Kannan, V. L. N. Venkatesh, and B.-C. Min, “SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models,” in 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), Oct. 2024, pp. 12 140–12 147.   
[43] M. Minderer, A. Gritsenko, and N. Houlsby, “Scaling open-vocabulary object detection,” Advances in Neural Information Processing Systems (NeurIPS), vol. 36, pp. 72 983–73 007, 2023.   
[44] D. L. Kovacs et al., “A multi-agent extension of PDDL3.1,” in ICAPS 2012 Proceedings of the 3rd Workshop on the International Planning Competition (WS-IPC 2012), 2012, pp. 19–37.   
[45] A. Micheli, A. Bit-Monnot, G. Roger, E. Scala, A. Valentini,¨ L. Framba, A. Rovetta, A. Trapasso, L. Bonassi, A. E. Gerevini, L. Iocchi, F. Ingrand, U. Kockemann, F. Patrizi, A. Saetti, I. Serina, ¨ and S. Stock, “Unified planning: Modeling, manipulating and solving AI planning problems in python,” SoftwareX, vol. 29, p. 102012, 2025. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S2352711024003820   
[46] G. Frances, H. Geffner, N. Lipovetzky, and M. Ramirez, “Best-first ´ width search in the IPC 2018: Complete, simulated, and polynomial variants,” IPC-9 Planner Abstracts, pp. 23–27, 2018.   
[47] X. Chen, J. Xu, T. Liang, Z. He, J. Pang, D. Yu, L. Song, Q. Liu, M. Zhou, Z. Zhang, et al., “Do NOT think that much for $2 + 3 { = } ?$ On the overthinking of o1-like LLMs,” arXiv preprint arXiv:2412.21187, 2024.