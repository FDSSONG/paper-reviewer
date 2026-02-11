# Robot Inner Attention Modeling for Task-Adaptive Teaming of Heterogeneous Multi Robots

Chao Huang1 and Rui Liu1∗

Abstract— Attracted by team scale and function diversity, a heterogeneous multi-robot system (HMRS), where multiple robots with different functions and numbers are coordinated to perform tasks, has been widely used for complex and large-scale scenarios, including disaster search and rescue, site surveillance, and social security. However, due to the variety of the task requirements, it is challenging to accurately compose a robot team with appropriate sizes and functions to dynamically satisfy task needs while limiting the robot resource cost to a low level. To solve this problem, in this paper, a novel adaptive cooperation method, inner attention (innerATT), is developed to flexibly team heterogeneous robots to execute tasks as task types and environment change. innerATT is designed by integrating a novel attention mechanism into a multi-agent actorcritic reinforcement learning architecture. With an attention mechanism, robot capability will be analyzed to flexibly form teams to meet task requirements. Scenarios with different task variety (”Single Task”, ”Double Task”, and ”Mixed Task”) were designed. The effectiveness of the innerATT was validated by its accuracy in flexible cooperation.

# I. INTRODUCTION

A heterogeneous multi-robot system (HMRS) consists of multiple robots with various shapes, sizes, and capabilities to perform tasks together. With the advantages of functional diversity, team scalability, and control robustness, HMRS has been widely used for large-scale tasks. For example, in natural disaster search and rescue [1]–[3], a larger area is searched, and multiple victims are rescued because robots in HMRS can operate in parallel. In traffic condition control, such as traffic flow control, public transportation scheduling [4]–[6], it is cost-effective to deploy multiple robots with particular capabilities to form a strong team instead of deploying one robot with numerous functions to perform the entire mission. As for area coverage and search with complex tasks [7]–[9], HMRS can resolve task complexity by allocating the mission across robot team members.

However, influenced by task varieties, teaming of heterogeneous robots in the real world is challenging. First, Due to the changing of task requirements across different environments, it is difficult to assess assistance type and scale [10], [11], and it is also challenging to accurately map the robot team capability to various task needs [14]. Second, real-world factors, such as motor degradation, sensor failure, and robot working status, influence robot availability to deliver assistance [12], [13]. Faulty robots in the robot team may share incorrect information with other members of the team leading the whole team unqualified to the assigned

![](images/bfdea97210b2927332be9098225e798e7d1fafd43d5a18fc95a3fc5751a75118.jpg)  
Fig. 1. The architecture of innerATT. The inner attention mechanism determines the attention weights between robots. As the left figure shows, the input is a robot’s observations, status, and actions, and cooperability related information from the robot’s teammates. The output is the $Q$ -value network for cooperation strategy selection, in which a robot pays differentlevel attention to others to form a team for a given task. In the right figure, multiple attention heads are used to evaluate different aspects of the cooperability between a robot and its potential teammates.

task. The unpredictable nature and negative impacts of these real-world faults limit the number of qualified team members, making it challenging to deploy a qualified robot team with expected capability and team size to satisfy task needs. Third, influenced by both the dynamics in task needs, robot availability, and environment constraints, it is challenging to accurately map robot team capability to task needs [14]. Assistance needs are dynamic as tasks vary; obstacles and weather conditions influence the time and feasibility of robot participation in assistance; available robots are with different distances to the requested location. The above task variety impedes an accurate alignment between robot capability and task needs, limiting the deployment of HMRS in the real world. Therefore, there is an urgent need to flexibly compose heterogeneous robot teams for mission deployments. In [15]– [19], human pre-defined robot utility functions, including teaming strategies, time efficiency, and robot resource (robot types, numbers, and heading speed) consumption, were used to flexibly team robots. However, the pre-optimized allocation strategies ignore the general relation between

teaming and task needs. When task requirements change, which is common in real-world situations, predefined teaming strategies cannot satisfy the assistance needs along the mission timeline. To overcome the above-mentioned limits, in [20]–[25], a deep reinforcement learning algorithm was used to dynamically model the highly nonlinear relation between situation constraints and task needs to flexibly team robots together. Although reinforcement learning methods can perform real-time teaming guidance by considering key elements related to robot status, task type and location, these methods cannot resist robot faults, which will mislead the teaming strategies and cause mission failures. To reduce the influence of robot failures on HMRS performance, research of self-healing was conducted. [26], [27] investigated methods for mobile robot networks to maintain the logical and physical topology of the network when robots fail and must be replaced within a formation. However, these researches mainly focused on replacing broken robots, which ignores partial failures such as direction deviation and slowed speed that are likely to be encountered in real-world deployments. Recently, [28]–[32] limited the negative influence of robot failures on team performance by restricting unreliable information sharing among robots. However, the influence limits were predefined so that they cannot adapt to real-world dynamic situations where the robot performance and task requirement change all the time.

This paper addresses above issues by designing a novel flexible teaming method, inner attention (innerATT), which is developed by integrating a novel attention mechanism into a multi-agent actor-critic reinforcement learning architecture, as shown in Figure 1. innerATT enables a robot to pay attention to the communication with its available teammates and capture the cooperation-related factors during teaming; the robots flexibly select cooperators to form a team to adapt to environment dynamics. The attention mechanism in innerATT is automatically obtained during deployment training. This paper mainly has three contributions:

1) A novel multi-robot teaming method, innerATT, has been developed to guide the flexible cooperation among heterogeneous robots as the task complexity varies in target number, target type, and robot work status.   
2) A theoretical analysis has been conducted to validate the robustness of innerATT in guiding flexible cooperation, providing a theoretical foundation for implementing innerATT in general disturbance-involved multi-robot teaming in future similar research.   
3) A deep reinforcement learning based simulation framework, which integrates the simulation platform of multi-agent particle environment, the multi-agent deep reinforcement learning algorithms, and robot models, has been developed to provide standard pipelines for simulating the flexible robot teaming.

# II. INNER ATTENTION SUPPORTED ADAPTIVE COOPERATION

With the innerATT supported by the inner attention mechanism, a robot assesses the function compensation and cooperation likelihood of its surrounding teammates, estimating a teaming plan based on the available robot sources. As shown in Figure 1, given the inputs are robots’ motion status and observations of the surrounding environment, innerATT automatically determines the amount of attention paid to different robots to form a mission team.

# A. Robot Inner Attention for Team Adaptability Modeling

The basic framework of robot teaming is established based on a multi-agent actor-critic deep reinforcement learning (MAAC) algorithm defined by robot number, $N$ ; motion state space, $S$ ; robot action sets, $A = \{ A _ { 1 } , . . . A _ { N } \}$ ; transition probability function over the next possible states, $T$ : $S \times A _ { 1 } \times . . . \times A _ { N } \to P ( S )$ ; a set of observations for all robots, $O = \{ O _ { 1 } , . . . O _ { N } \}$ ; and reward function for each robot $R _ { i }$ : $S \times A _ { 1 } \times . . . \times A _ { N } \to R$ . By using extended actorcritic reinforcement learning to guide robot cooperation, each robot learns an individual policy function, $\pi _ { i } \colon O _ { i } \to P ( A _ { i } )$ , which is a probability distribution on potential cooperation actions. The goal of multi-agent reinforcement learning is to learn an optimal cooperation strategy for each robot that can maximize their expected discounted returns:

$$
J _ {i} \left(\pi_ {i}\right) = E _ {a _ {*} \sim \pi_ {*}; s \sim T} \left[ \sum_ {t = 0} ^ {\infty} \gamma^ {t} r _ {i t} \left(s _ {t}, a _ {1 t}, \dots , a _ {N t}\right) \right], \tag {1}
$$

where * represent $\{ 1 , . . . N \}$ ; $\gamma \in [ 0 , 1 ]$ is the discount factor that determines the degree to which the cooperation policy favors immediate reward over long-term gain.

In the extended actor-critic framework consisting of centralized training with decentralized execution, to calculate the $Q$ -value function $Q _ { i } ( o , a )$ for the robot $i$ , the critic receives the observations, $\boldsymbol { o } ~ = ~ \left( o _ { 1 } , . . . , o _ { N } \right)$ , and actions, $a = ( a _ { 1 } , . . . , a _ { N } )$ , for all robots, which will take redundant information into account. With an attention mechanism, each robot actively explores cooperation-relevant information from its surrounding robots to assess their compatibility and potential collaboration, and therefore selectively choose robots to team together.

To generate the attention weights, the embedded information is fed into the innerATT to get the $Q$ -value function $Q _ { i } ( o ; a )$ for robot $i$ , which is a function:

$$
Q _ {i} (o; a) = w ^ {2 T} \sigma \left(w ^ {1}, <   e _ {i}, x _ {i} >\right), \tag {2}
$$

where $\sigma$ is rectified linear units (ReLU), $w ^ { 1 }$ and $w ^ { 2 }$ are the parameters of critics. The inner attention mechanism has shared query $( w _ { q } )$ , key $( w _ { k } )$ , and value $( w _ { v } )$ matrixes. Each robot’s embedding $e _ { i }$ can be linearly transformed into qi, $k _ { i }$ , and $v _ { i }$ separately. The contribution from other robots, $x _ { i }$ , is a weighted sum of other robots’ value:

$$
x _ {i} = \sum_ {j \neq i} \alpha_ {i j} v _ {j} = \sum_ {j \neq i} \alpha_ {i j} \sigma (v _ {j}). \tag {3}
$$

The attention weight $\alpha _ { i j }$ compares the similarity between $k _ { j }$ and $q _ { i }$ , and the similarity value can be obtained from a softmax function:

$$
\alpha_ {i j} = \frac {S _ {i j}}{\sum_ {k = 1} ^ {N} S _ {i k}} = \frac {e _ {j} w _ {k} ^ {T} w _ {q} e _ {i}}{\sum_ {k = 1} ^ {N} e _ {k} w _ {k} ^ {T} w _ {q} e _ {i}}. \tag {4}
$$

To better analyze the effectiveness of the innerATT method, a baseline method without the inner attention mechanism has also been designed. In the baseline method, the attention weights $\alpha$ are simply fixed to $\frac { 1 } { ( N _ { - } 1 ) }$ . Given that only the values of attention weights are changed to a fixed value, both innerATT and baseline methods are implemented with an approximately equal number of parameters.

# B. Theoretical analysis of innerATT’s robustness

To simply explain whether inner attention mechanism works in supporting flexible teaming, the output of the $Q$ - value neural network with inner attention mechanism, when the input is $x$ , can be written as:

$$
f (x) = w ^ {2 T} \sigma \left(w ^ {1}, x\right), x = <   e _ {i}, x _ {i} >, \tag {5}
$$

the robots can be more robust to other robots’ failure or a sensor failure [33]. Consider that a small perturbation is added to a particular robot $j$ ’s embedding, such that $e _ { j }$ is changed to $e _ { j } + \triangle e$ while all the other robots’ embeddings remain unchanged. How much will this perturbation affect the attention weights $\alpha _ { i j }$ ? For a particular $i ( i \neq j )$ , the

$$
S _ {i j} = e _ {j} w _ {k} ^ {T} w _ {q} e _ {i} \tag {6}
$$

is only changed by one term since:

$$
S _ {i j} ^ {\prime} = \left\{ \begin{array}{l l} S _ {i j} + \triangle e w _ {k} ^ {T} w _ {q} e _ {i}, & i f (i \neq j) \\ S _ {i j}, & o t h e r w i s e \end{array} , \right. \tag {7}
$$

where $S _ { i j } ^ { \prime }$ denotes the value after the perturbation. Therefore, ij with the perturbed input, each set of $\{ S _ { i j } \} _ { j = 1 } ^ { N }$ will only have one term being changed. For the perturbation part, assume $\| \triangle e \| \le \delta _ { 1 }$ and $\lVert e _ { i } \rVert \leq \delta _ { 2 }$ , then the expected value is

$$
E \left[ S _ {i j} ^ {\prime} - S _ {i j} \right] \leq \| w _ {q} \| \| w _ {k} \| \delta_ {1} \delta_ {2}. \tag {8}
$$

Then, the probability results can be obtained by using Markov inequality:

$$
P \left(\left| S _ {i j} ^ {\prime} - S _ {i j} \right| \geq \varepsilon\right) \leq \frac {\left\| w _ {q} \right\| \left\| w _ {k} \right\| \delta_ {1} \delta_ {2}}{\varepsilon}. \tag {9}
$$

Therefore, as the norm of $w _ { q } , w _ { k }$ are not too large (usually regularized by $L _ { 2 }$ during training), there will be a significant amount of $i$ such that $S _ { i j } ^ { \prime }$ is perturbed negligibly. Therefore, with the inner attention mechanism, innerATT method is robust to the robot unavailability caused by either mission occupation or system failures.

![](images/36cef4104c12064d25618417731421264690736398da2ba180b846d00ab0f0df.jpg)  
Fig. 2. Simulated environment scenario illustration. In the flood disaster, there are trapped victims with different injury levels. For the victims with high injury level (Task 1), they need rescue robots providing them with food, water, and emergency medical treatment; While for the victims with low injury level (Task 2), they will need other kinds rescue robots providing food, water, and useful information to guide them to safer places. The main robot team is expected to split into different sub-teams that can rescue these victims effectively.

TABLE I THE CONFIGURATIONS OF ROBOTS   

<table><tr><td>Type</td><td>Speed</td><td>Mass</td><td>Ability</td></tr><tr><td>Food Delivery</td><td>1.0 m/s</td><td>1.0 kg</td><td>Food</td></tr><tr><td>Navigation</td><td>1.5 m/s</td><td>0.5 kg</td><td>Information</td></tr><tr><td>Medical Assistance</td><td>1.5 m/s</td><td>0.5 kg</td><td>Medicine</td></tr></table>

# III. EXPERIMENT SETTINGS

To validate innerATT’s effectiveness in improving HMRS adaptability, a task environment with three variety situations (”Single Task”, ”Double Task”, and ”Mixed Task”) were designed. These scenarios are typical task situations in realworld mission deployment, therefore being used here to evaluate the general effectiveness of the proposed method in mission support.

The environment shown in Figure 2 was implemented based on the open-source multi-agent particle environment (MPE) framework [34]. The size of the artificial environment was set to $2 \times 2$ . The parameters of robots, shown in Table I, were set according to real-world robots. Two types of victims and four types of rescue robots are involved to simulate the rescuing process. For the rescue robots, two of them are food delivery robots providing living supplies such as food and water; one is a navigation robot providing victims with useful location information, directing them to safer places. The remaining robots are medical assistance robots to provide medical treatments to heavily injured victims. For victims, one type is heavily injured, requiring both food and medical assistance for survival, defined as ”Task 1”; while another is trapped but in good health, needing food as well as navigation, defined as ”Task $2 ^ { \circ }$ .

To analyze the effectiveness of the innerATT method, three situations - from simple to complex - for each scenario were designed, shown in Figure 3. In $^ { \small , \mathparagraph } ( S _ { 1 } )$ Single Task” situation, only one task, ”Task 1” or ”Task 2”, appeared at random locations. In $^ { , , } ( S _ { 2 } )$ Double Task”, ”Task $1 ^ { \circ }$ and

![](images/746b17d26062e4643fded593b568b4bbc6f27be2361f0a748ce9214e99b913d4.jpg)  
Fig. 3. Simulated environment situations illustration. (a) $^ { \ ' } ( S _ { 1 } )$ Single Task” in which only one kind of task popup. (b) ” $\ " ( S _ { 2 } )$ Double Task” in which always popup two kind of tasks. Robot team will always deal with Task1 and Task2. (c) $^ { \circ } ( S _ { 3 } )$ Mixed Task” which is the combination of situation one and two.

”Task $2 ^ { \circ }$ will always present together in each time at random locations. In $\overrightarrow { \mathbf { \nabla } } ( S _ { 3 } )$ Mixed Task” is a combination of $S _ { 1 }$ and $S _ { 2 }$ , that is an unpredictable number of tasks appear at a random location each time. In addition, two deep reinforcement learning algorithms with (simplified as PPO) and without (simplified as TD) proximal policy optimization have also been used. In the method without inner attention, the attention weights $\alpha$ are simply fixed to $\frac { 1 } { ( N - 1 ) }$ . Given that only the values of attention weights are changed to a fixed value, both innerATT and methods without inner attention are implemented with an approximately equal number of parameters.

As for the training procedure, the extended actor-critic method for maximum entropy reinforcement learning was used in the training progress of 25,000 episodes. There were 12 threads to process training data in parallel and a replay buffer to store experience tuples of $\left( o _ { t } , a _ { t } , r _ { t } , o _ { t + 1 } \right)$ for each time step. In detail, sample 1024 tuples from the replay buffer and update the parameters of the $Q$ -function and the policy objective through policy gradients. Adam optimizer was used, and the initial learning rate was set as 0.001 and the discount factor $\gamma$ was 0.99. The embedded information function used a hidden dimension of 128, and four attention heads were used in the inner attention mechanism.

![](images/b6f7dd3e6bc7a2133e5d79bbd6fa8c40f55eb962f7a6c3220a80953d5eb05a4a.jpg)

![](images/0aa1730c39de3a47dd53349ff31f131dd6401c9339fa31af606052008dcfd2b0.jpg)  
Fig. 4. Attention entropy of each attention head during the training phase for the robots in the multi-robot cooperation environment. A lower entropy value indicates that the robots have learned to selectively pay attention to another specific team member.

# IV. RESULTS

# A. Adapting to Task Varieties

In the typical ”task variety” scenario, robots’ flexibility, the cooperation rate between food delivery robots and other rescue robots, was calculated in a period of time (80 episodes) by using the following formulation:

$$
\operatorname {r a t e} _ {i j} = \frac {\operatorname {N u m} _ {i j}}{\sum_ {k = 1} ^ {N} \operatorname {N u m} _ {i k}}, \tag {10}
$$

where $\sum _ { k = 1 } ^ { N } N u m _ { i k }$ is the total number of victims rescued by robot $i$ ; $N u m _ { i j }$ is the total number of victims rescued by the cooperation of robot $i$ and robot $j$ . The results are shown in Table II. In Task 1, the cooperation rates of food delivery robots trained by innerATT are 0.52 and 0.48 respectively, which is similar to the uniform distribution with $9 5 \%$ confidence; while the cooperation rates of food delivery robots trained by baseline method are 0.90 and 0.10, which doesn’t have enough evidence to prove that it is similar to the uniform distribution. Similar results have been shown for task 2, that the robots trained by innerATT are more flexible than those trained by the baseline method. As suspected, the baseline model’s critics use all information non-selectively, while innerATT can learn which robot to pay more attention to through the inner attention mechanism. Thus, innerATT method is more flexible and sensitive to dynamically changed tasks. Besides that, Figure 4 demonstrates the effect of the attention head on the robot during the training process by showing the entropy of the attention weights for each robot. From the results shown in Figure 4, the entropy of all robot attention heads is continually decreasing to 1.02 around, which indicates that innerATT can train the robots to selectively pay attention to a specific team member through the inner attention mechanism.

To further prove that the inner attention mechanism is beneficial to robot’s flexible adaptation to different tasks, the relationship between robot behaviors and their inner attention weights was analyzed to illustrate attention supports

![](images/807ebc2369923c3635af04f7e6ad2d462ad67c4cba26b897616be6454bcd9f21.jpg)  
(A) Stages of transferring situations   
(i) Pre-Stage

![](images/84ff7217d2e256564e4895387e3217d37f5001a2143b3c07189a476ad46b94e0.jpg)  
(ii) Middle-Stage

![](images/07e40a2e6cfa19febb2c2ddf454d7099d2d8db058b2d43b6f727ddff2e86663c.jpg)  
(ii) Post-Stage

![](images/ceed6c8b78ada48777ec83c1639799f5b254976426e8b801bfc861f8f93b978b.jpg)  
(B) Total attention weights

![](images/81060787fc49c90670638384f744d7274ad406f8617f6558d598c05b016384d9.jpg)  
(C) Attention weights of each head

![](images/3b0c77d5accced8ba74594e7a581b311560175ae4358db041a5dbb0b3fd15434.jpg)

![](images/88c277aa5683ef28dabbd57171b6d391cc4d226854f9fa4450a920ef720012e1.jpg)

![](images/7bc49bb977d8ce539eaddd014917d9bcbe52eb48780efa2dd6c1e3ef0b86e6c2.jpg)  
food delivery 2

![](images/9feef1a25a5cea46ae71301fcdc6e2125acc3186f3978aefc04b2808ed8a1bbf.jpg)

![](images/70e33a8d1dccc4e29b760a0478c923801a552efb0ec3a83832dcb17dee38678c.jpg)

![](images/16f3da9546869265304abece0fa8a7be0c8444c53e1bcead8ae49b2455ae2f9d.jpg)  
medical assistance

![](images/1c943a87683962db99d8acad099b40b6dfa3d21692dcc1d420c36d99529f9ae4.jpg)  
Fig. 5. Relationships between food delivery 1 robot’s behavior and its inner attention weights in adaptive teaming. (A) three stages of food delivery 1 robot’s flexible teaming. In pre-stage (i), food delivery 1 robot is cooperating with medical assistance robot. In middle-stage (ii), food delivery 1 robot is changing its behavior based on inner attention mechanism. In post-stage (iii), food delivery 1 robot is cooperating with a navigation robot. (B) food delivery 1 robot’s total attention weight paid to other robots. (C) food delivery 1 robot’s attention weights obtained from each attention head.

TABLE II UAVS PARTICIPATE RATE COMPARISON   

<table><tr><td colspan="2"></td><td>UAV food delivery1</td><td>UAV food delivery2</td><td>\( \chi_1^2 \) (a = 0.05)</td></tr><tr><td rowspan="2">Task1</td><td>TD-innerATT</td><td>0.47</td><td>0.53</td><td>0.36 &lt; 3.84</td></tr><tr><td>TD</td><td>0.82</td><td>0.18</td><td>81.9 &gt; 3.84</td></tr><tr><td rowspan="2">Task2</td><td>TD-innerATT</td><td>0.56</td><td>0.44</td><td>1.44 &lt; 3.84</td></tr><tr><td>TD</td><td>0.18</td><td>0.82</td><td>81.9 &gt; 3.84</td></tr><tr><td rowspan="2">Task1</td><td>PPO-innerATT</td><td>0.48</td><td>0.52</td><td>0.16 &lt; 3.84</td></tr><tr><td>PPO</td><td>0.32</td><td>0.68</td><td>25.9 &gt; 3.84</td></tr><tr><td rowspan="2">Task2</td><td>PPO-innerATT</td><td>0.45</td><td>0.55</td><td>1.00 &lt; 3.84</td></tr><tr><td>PPO</td><td>0.73</td><td>0.27</td><td>42.3 &gt; 3.84</td></tr></table>

in adjusting robot behaviors for flexible teaming. Figure 5 (A) is an illustration of a specific scenario occurring during the experiment. In the pre-stage, food delivery 1 robot is firstly cooperating with medical assistance robot to rescue the heavily injured victim (Task 1). At this moment, food delivery 1 robot needs to pay more attention to medical assistance robot. After finishing Task 1, in the middle-stage and post-stage, it will change to cooperate with a navigation robot to rescue the trapped victim in good health (Task 2). At this time, food delivery 1 robot needs to pay more attention to navigation robot. Figure 5 (B) is the curves of food delivery 1 robot’s total attention weights over the other three robots. In the pre-stage, the curve of total attention weights paid on medical assistance robot has the highest values, which supports the food delivery 1 robot to selectively cooperate with medical assistance robot. In the middle-stage and post-

stage, the curves of total attention weights paid on medical assistance robot and navigation robot are decreasing and increasing separately, which supports food delivery 1 robot to transfer its attention from medical assistance robot to navigation robot. Therefore, the inner attention mechanism can support robot flexible teaming behaviors to different tasks. Figure 5 (C) are the curves of food delivery 1 robot’s attention weights, generated by each attention head, over other rescue robots.

# V. CONCLUSION AND FUTURE WORK

This paper developed a novel inner attention model, innerATT, to enable multi heterogeneous robots to cooperate flexibly according to task needs. With scenarios of different task varieties, including ”a single task, double task, and dynamically mixed tasks”, the effectiveness of the innerATT model for guiding flexible teaming has been validated. This model essentially addressed the question of allocating limited available robot sources into dynamic task situations. This theoretical model can also be extended to guide flexible teaming between the ground and aerial vehicles, and even the teaming between vehicles and human units. Therefore, this attention-based flexible teaming model bears a huge potential for real-world multi-robot implementations, from disaster research, to wildlife protection, and to airport traffic control.

Notes that, in this work, the primary focus is validating the feasibility of using attention for flexible heterogeneous teaming. The simulated environment is different from the real-world environment, so the model trained in our research cannot achieve the same performance in real-world applications; but the trained model will be a helpful initial learner for further training in the real-world. In the future, the research

of robot behavior understanding and human trust modeling will be an option to improve the performance of HMRS in the real world.

# REFERENCES

[1] A. Matos, A. Martins, A. Dias, B. Ferreira, J. M. Almeida, H. Ferreira, G. Amaral, A. Figueiredo, R. Almeida and F. Silva, ”Multiple robot operations for maritime search and rescue in euRathlon 2015 competition,” OCEANS 2016-Shanghai, pp. 1-7, 2016.   
[2] C. Mouradian, S. Yangui and R. H. Glitho, ”Robots as-a-service in cloud computing: search and rescue in large-scale disasters case study,” 2018 15th IEEE Annual Consumer Communications and Networking Conference (CCNC), pp. 1-7, 2018.   
[3] Z. Beck, Teacy, N. R. Jennings and A. C. Rogers, ”Online planning for collaborative search and rescue by heterogeneous robot teams,” Association of Computing Machinery, 2016.   
[4] E. T. S. Alotaibi, H. Al-Rawi, ”Multi-robot path-planning problem for a heavy traffic control application: A survey,” International Journal of Advanced Computer Science and Applications, vol. 7, no. 6, pp. 10, 2016.   
[5] V. Digani, L. Sabattini, C. Secchi and C. Fantuzzi, ”Towards decentralized coordination of multi robot systems in industrial environments: A hierarchical traffic control strategy,” 2013 IEEE 9th International Conference on Intelligent Computer Communication and Processing (ICCP), pp. 209-215, 2013.   
[6] V. Digani, L. Sabattini, C. Secchi and C. Fantuzzi, ”Hierarchical traffic control for partially decentralized coordination of multi agv systems in industrial environments,” IEEE International Conference on Robotics and Automation, pp. 6144-6149, 2014.   
[7] B. Broecker, I. Caliskanelli, K. Tuyls, E. I. Sklar and D. Hennes, ”Hybrid insect-inspired multi-robot coverage in complex environments.” Conference Towards Autonomous Robotic Systems, pp. 56-68, 2015.   
[8] A. Kolling and S. Carpin, ”Multi-robot surveillance: an improved algorithm for the graph-clear problem,” IEEE International Conference on Robotics and Automation, pp. 2360-2365, 2008.   
[9] K. Easton and J. Burdick, ”A coverage algorithm for multi-robot boundary inspection,” IEEE International Conference on Robotics and Automation, pp. 727-734, 2005.   
[10] D. Q. Zhu, H. Huang and S. X. Yang, ”Dynamic task assignment and path planning of multi-AUV system based on an improved selforganizing map and velocity synthesis method in three-dimensional underwater workspace,” IEEE Transactions on Cybernetics, vol. 43, no. 2, pp. 504-514, 2013.   
[11] A. M. Zhu and S. X. Yang, ”An improved SOM-based approach to dynamic task assignment of multi-robot,” World Congress on Intelligent Control and Automation, pp. 2168-2173, 2010.   
[12] A. Prorok, M. A. Hsieh and V. Kumar, ”Fast redistribution of a swarm of heterogeneous robots,” Proceedings of the 9th EAI International Conference on Bio-inspired Information and Communications Technologies (formerly BIONETICS), pp. 249-255, 2016.   
[13] Z. G. Saribatur, V. Patoglu and E. Erdem, ”Finding optimal feasible global plans for multiple teams of heterogeneous robots using hybrid reasoning: an application to cognitive factories,” Autonomous Robots, vol. 43, no. 1, pp. 213-238, 2019.   
[14] A. Vergnano, C. Thorstensson, B. Lennartson, P. Falkman, M. Pellicciari, F. Leali and S. Biller, ”Modeling and optimization of energy consumption in cooperative multi-robot systems,” IEEE Transactions on Automation Science and Engineering, vol. 9, no. 2, pp. 423-428, 2012.   
[15] N. Atay and B. Bayazit, ”Mixed-integer linear programming solution to multi-robot task allocation problem,” 2006.   
[16] M. Darrah, W. Niland and B. Stolarik, ”Multiple UAV dynamic task allocation using mixed integer linear programming in a SEAD mission,” Infotech at Aerospace, pp. 7165, 2005.   
[17] A. R. Mosteo and L. Montano, ”Simulated annealing for multi-robot hierarchical task allocation with flexible constraints and objective functions,” Workshop on Network Robot Systems: Toward Intelligent Robotic Systems Integrated with Environments, 2006.   
[18] D. Juedes, F. Drews, L. Welch and D. Fleeman, ”Heuristic resource allocation algorithms for maximizing allowable workload in dynamic, distributed real-time systems,” International Parallel and Distributed Processing Symposium, pp. 117, 2004.

[19] W. Kmiecik, M. Wojcikowski, L. Koszalka and A. Kasprzak, ”Task allocation in mesh connected processors with local search metaheuristic algorithms,” Asian Conference on Intelligent Information and Database Systems, pp. 215-224, 2010.   
[20] N. Iijima, A. Sugiyama, M. Hayano and T. Sugawara, ”Adaptive task allocation based on social utility and individual preference in distributed environments,” Procedia computer science, vol. 112, pp. 91-98, 2017.   
[21] D. Lope, Javier, D. Maravall and Y. Quinonez, ”Response threshold ˜ models and stochastic learning automata for self-coordination of heterogeneous multi-tasks distribution in multi-robot systems,” Robotics and Autonomous Systems, 2012.   
[22] A. Elfakharany, R. Yusof, Z. Ismail, ”Towards multi-robot Task Allocation and Navigation using Deep Reinforcement Learning,” Journal of Physics: Conference Series, vol. 1447, no. 1, pp. 012045, 2020.   
[23] T. X. Fan, P. X. Long, W. X. Liu, J. Pan, ”Fully distributed multi-robot collision avoidance via deep reinforcement learning for safe and efficient navigation in complex scenarios,” arXiv preprint arXiv:1808.03841, 2018.   
[24] D. B. Noureddine, A. Gharbi and S. B. Ahmed, ”Multi-agent Deep Reinforcement Learning for Task Allocation in Dynamic Environment,” ICSOFT, pp. 17-26, 2017.   
[25] T. Z. Luo, B. Subagdja, D. Wang and A. Tan, ”Multi-Agent Collaborative Exploration through Graph-based Deep Reinforcement Learning,” 2019 IEEE International Conference on Agents (ICA), pp. 2-7, 2019.   
[26] Z. Liu, J. Ju, W. Chen, X. Y. Fu and H. Wang, ”A gradient-based self-healing algorithm for mobile robot formation,” 2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 3395-3400, 2015.   
[27] F. Zhang and W. Chen, ”Self-healing for mobile robot networks with motion synchronization,” 2007 IEEE/RSJ International Conference on Intelligent Robots and Systems, pp. 3107-3112, 2007.   
[28] N. Mathews, A. L. Christensen, R. O’Grady, F. Mondada and M. Dorigo, ”Mergeable nervous systems for robots,” Nature communications, vol. 8, no. 1, pages 1-7, 2017.   
[29] N. Mathews, A. L. Christensen, A. Stranieri, A. Scheidler and M. Dorigo, ”Supervised morphogenesis: Exploiting morphological flexibility of self-assembling multirobot systems through cooperation with aerial robots,” Robotics and autonomous systems, vol. 112, pp. 154- 167, 2019.   
[30] A. Pelc and D. Peleg, ”Broadcasting with locally bounded byzantine faults.” Information Processing Letters, vol. 93, no. 3, pp. 109-115, 2005.   
[31] K. Saulnier, D. Saldana, A. Prorok, G. J. Pappas and V. Kumar, ”Resilient flocking for mobile robot teams,” IEEE Robotics and Automation letters, vol. 2, no. 2, pp. 1039-1046, 2017.   
[32] R. Liu, F. Jia, W. H. Luo, M. Chandarana, C. J. Nam, M. Lewis and K. Sycara, ”Trust-Aware Behavior Reflection for Robot Swarm Self-Healing,” Proceedings of the 18th International Conference on Autonomous Agents and MultiAgent Systems, pp. 122-130, 2019.   
[33] Y. L. Hsieh, M. H. Cheng, D. C. Juan, W. Wei, W. L. Hsu and C. J. Hsieh, ”On the robustness of self-attentive models,” Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pp. 1520-1529, 2019.   
[34] R. Lowe, Y. I. Wu, A. Tamar, J. Harb, O. P. Abbeel and I. Mordatch, ”Multi-agent actor-critic for mixed cooperative-competitive environments,” Advances in neural information processing systems, pp. 6379- 6390, 2017.