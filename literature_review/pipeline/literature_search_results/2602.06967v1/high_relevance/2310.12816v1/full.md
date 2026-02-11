# Multi-Robot Local Motion Planning Using Dynamic Optimization Fabrics

Saray Bakker*1, Luzia Knoedler*1, Max Spahn1, Wendelin Bohmer ¨ 2 and Javier Alonso-Mora1

Abstract— In this paper, we address the problem of real-time motion planning for multiple robotic manipulators that operate in close proximity. We build upon the concept of dynamic fabrics and extend them to multi-robot systems, referred to as Multi-Robot Dynamic Fabrics (MRDF). This geometric method enables a very high planning frequency for high-dimensional systems at the expense of being reactive and prone to deadlocks. To detect and resolve deadlocks, we propose Rollout Fabrics where MRDF are forward simulated in a decentralized manner. We validate the methods in simulated close-proximity pickand-place scenarios with multiple manipulators, showing high success rates and real-time performance.

Code, video: https://github.com/tud-amr/multi-robot-fabrics

# I. INTRODUCTION

In several domains, such as manufacturing, medicine, and agriculture, it is common to have multiple manipulators operating in close proximity to each other. This arrangement improves efficiency and enables the successful execution of complex tasks [1]. However, when operating in dynamic environments, where conditions and obstacles can change, determining viable trajectories for multiple robots becomes challenging. Unlike static environments where all information can be pre-computed, dynamic environments require real-time planning to operate robots safely and efficiently.

Multi-robot motion planning can be addressed using two main approaches: coupled and decoupled methods. Coupled approaches can provide optimal solutions, but they often suffer from high computational costs, especially when dealing with large numbers of robots with many degrees of freedom (DOF) [2]. On the other hand, decoupled approaches offer more scalability but cannot guarantee optimality. In dynamic environments, the ability to adapt online in realtime becomes essential.

However, even decoupled motion planning becomes challenging for complex systems. While optimization-based approaches such as Model Predictive Control (MPC) have been widely adopted for mobile robots, their high computational

*These authors contributed equally.

This paper has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No. 101017008, from the European Union through ERC, INTERACT, under Grant 101041863, and from Ahold Delhaize. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council Executive Agency. Neither the European Union nor the granting authority can be held responsible for them.

The authors are associated with the department of 1. Cognitive Robotics and 2. Electrical Engineering, Mathematics & Computer Science, Delft University of Technology, The Netherlands, {s.bakker-7, l.knoedler, m.spahn, j.w.bohmer j.alonsomora}@tudelft.nl

![](images/b015ed1eb906435f4f9a5ec1dc9cc19654665549e30dfb8a6d908ab8f2af8e6b.jpg)  
Fig. 1: Multi-robot pick-and-place scenario in close proximity. Franka Emika Pandas pick cubes avoiding collisions.

costs make them less suitable for high-dimensional configuration spaces [3], [4], [5]. Data-driven approaches can be utilized to speed up the optimization process [5], however, they often lack generalization capabilities and necessitate costly data acquisition processes [6].

In contrast, geometric approaches to local motion planning, such as Riemannian Motion Policies [7], [8] and optimization fabrics [9], offer superior scalability and thus high reactivity [10]. With optimization fabrics, or fabrics for short, different components, such as collision avoidance and joint limit avoidance, are combined using Riemannian metrics, allowing for an iterative behavior design. Because fabrics parse local motion planning into a differential equation of second order, the solution can be computed before runtime in a symbolic way [10], thus saving computational costs during execution. This enables higher replanning frequencies making them advantageous for complex systems in dynamic environments. Furthermore, fabrics inherently promote asymptotic stability, which adds to their appeal as a framework for reactive motion planning.

Fabrics, but also their predecessor Riemannian Motion Policies, have shown impressive results in several manipulator applications, including dynamic and crowded environments [11], [12]. Recently, fabrics have been generalized to dynamic scenarios, referred to as dynamic fabrics [10]. As a drawback to highly reactive behavior, fabrics are prone to local minima [10], this is especially harmful in multi-robot scenarios where deadlocks are even more common than in single-robot applications.

This work focuses on the development of an online local motion planning algorithm to facilitate the simultaneous operation of multiple high DOF manipulators within a shared workspace. Our particular investigation revolves around the utilization of dynamic fabrics in multi-robot systems, specifi-

cally in the context of close-proximity pick-and-place scenarios. To the best of the authors’ knowledge, fabrics have not yet been employed within the context of multi-robot systems. To tackle the challenges associated with close-proximity manipulation scenarios, we introduce a concept called Rollout Fabrics (RF). This approach involves simulating the forward motion of multi-robot fabrics over a prediction horizon, enabling the detection of potential deadlocks. We propose a heuristic method to address the identified deadlocks, which involves adapting the goal-reaching parameters of the fabric formulation. To this end, our contributions are as follows:

• Extension of dynamic fabrics to multi-robot systems for high-DOF manipulators, referred to as Multi-Robot Dynamic Fabrics (MRDF),   
• RF, an approach to forward simulate MRDF enabling detection of future deadlocks or other undesired states,   
• A heuristic approach for the resolution of deadlocks,   
• Validation in simulation in close-proximity pick-andplace scenarios with high-DOF manipulators.

# II. RELATED WORK

# A. Multi-Robot Motion Planning

Regardless of the specific employed local motion planning algorithm, methods for multi-robot motion planning can be classified into two categories: coupled approaches and decoupled approaches. Coupled approaches compute the plans of all robots simultaneously and often provide guarantees regarding feasibility and optimality at the expense of a high computational burden. Decoupled planners solve a subproblem in isolation enabling rapid computation of feasible plans and relaxing communication requirements. However, they lack guarantees of completeness and optimality [13].

Commonly used motion planning algorithms are samplingbased and optimization-based approaches, or combinations of both methods [14]. Sampling-based planners are well-suited for high-dimensional configuration spaces, making them a suitable choice for multi-robot systems. Rapidly exploring random trees (RRT) [15] and the probabilistic roadmap method (PRM) [16] can be extended to multi-robot systems by considering the robots as a single multi-arm robot or planning for each robot individually and adapting the velocities to avoid collisions [17]. Further extensions improving efficiency are dRRT [13] which considers an implicit representation of a tensor product of roadmaps for the individual robots and its informed extension dRRT* [18]. Sampling-based methods are primarily used for static environments, where trajectories are initially planned for a specific task and then executed and thus mainly employed for offline motion planning.

Optimization-based planners [19] commonly take into account dynamic feasibility as well as static and dynamic collision avoidance as constraints. Since an increasing number of constraints can lead to a significant increase in computational cost, it is crucial to efficiently implement constraints. One commonly utilized optimization-based motion planner is MPC [20] which solves the optimization problem in a receding horizon manner, thereby continuously updating and

optimizing the plan as new information becomes available. For multi-robot motion planning, MPC can be applied in a centralized [21] or distributed [22], [23] fashion. Since the centralized MPC solves a coupled optimization problem, it has limited scalability [2]. This motivates the development of distributed MPC formulations where each robot optimizes its own motion while considering the predicted behavior of the other robots. For instance, [23] present a distributed MPC approach formulated as a non-cooperative game that focuses on collision avoidance between multiple manipulators. However, their approach requires communication of the (extrapolated) predicted joint states of all neighbor robots at each time instance. To avoid the costly solution of a constrained optimization problem, the planning problem can be phrased as a purely geometric problem. Such methods fall into the field of geometric control. In a comparative study, it was shown that fabrics, a form of geometric control, outperform MPC in terms of collision avoidance and computation time for mobile manipulators [10].

Thus, in this work, we make use of the lightweight structure of optimization fabrics in a multi-robot setting. The fabrics formulation of the other robots only needs to be communicated once at the beginning of each task. Then at each time step, only the current configuration, velocity and goal information of the other robots must be communicated among the robots. We further present approximations that can be used to reduce communication.

# B. Geometric Control for Single-Robot Scenarios

Operational space control, a control method applied to robotic systems, enables natural control of kinematically redundant robots [24], [25]. It was formalized in geometric control, which utilizes differential geometry to achieve stable and converging behavior [26]. Recently, Riemannian Motion Policies (RMP) introduced a trajectory generation method for manipulation tasks, allowing composability by separating the importance metric and forcing term [7], [8]. Optimization fabrics were later introduced to fully decouple the importance metrics and defining geometry, ensuring guaranteed convergence with simple construction rules [9], [12], [27], [28]. In [10], optimization fabrics are extended towards Dynamic Fabrics (DF) which incorporate path following and collision avoidance with moving obstacles. By proposing dynamic pullback operations, relative coordinate frames are explored introducing relative task positions, velocities, and accelerations. Convergence is guaranteed if the reference is bounded. Here we build upon optimization fabrics and DF and extend them to multi-robot environments.

# III. PRELIMINARIES

In this section, we provide a concise introduction to the fundamental concepts necessary for trajectory generation using fabrics. We first specify the required notations III-A, then we present spectral semi-sprays III-B and their operations III-C which build the foundations for optimization fabrics III-D and DF III-E. For a more detailed overview of fabrics and their theoretical foundations in differential

geometry, we refer to [9], [11] and for DF to [10]. We further state the problem formulation for multi-robot fabrics III-F.

# A. Notations

We use $\mathbf { \Psi } \mathbf { { q } } _ { t } ~ \in ~ \mathcal { C }$ to denote the configuration of a robot at time $t$ . Here, $\mathcal { C }$ is the robot’s configuration space of dimension $n = D O F$ . Similarly, $\dot { \pmb q } _ { t }$ and $\ddot { \pmb q } _ { t }$ define the corresponding instantaneous derivatives. To improve readability we will neglect the subscript $t$ in the following.

We define a set of $M$ task variables $\mathbf { \pmb { x } } _ { j } ~ \in ~ \mathcal { X } _ { j }$ for $j \in$ $[ M ]$ with variable dimension $m _ { j } \leq n$ . We use the shorthand notation $[ M ]$ to denote $\{ j \in \mathbb { N } : j \leq M \}$ . A differential map $\phi _ { j } : { \mathcal { C } }  { \mathcal { X } } _ { j } $ with ${ \pmb x } _ { j } = \phi _ { j } ( { \pmb q } )$ relates the configuration space of a robot to the $j$ -th task space. For instance, if a task variable is defined as the end-effector position, then $\phi _ { j }$ is the positional part of the forward kinematics (fk). If a task variable is defined as the joint position, then $\phi _ { j }$ is the identity function. We assume that $\phi _ { j }$ is smooth and twice differentiable and denote the map’s Jacobian as $J _ { \phi _ { j } } = \frac { \partial \phi _ { j } } { \partial { \bf q } }$ ∂ϕj or $\begin{array} { r } { J _ { \phi _ { j } } = \partial _ { q } \phi _ { j } } \end{array}$ for short. Thus, we can write the time derivatives of $\mathbf { \Delta } _ { \mathbf { \mathcal { X } } _ { j } }$ as ${ \dot { \pmb { x } } } _ { j } = { \pmb { J } } _ { \phi _ { j } } { \dot { \pmb { q } } }$ and $\ddot { \pmb { x } } = J _ { \phi _ { j } } \ddot { \pmb { q } } + \dot { J } _ { \phi _ { j } } \dot { \pmb { q } }$ . In the following, the subscript $j$ is dropped to improve readability.

# B. Spectral Semi-Sprays

Drawing inspiration from fundamental mechanics, optimization fabrics formulate motion policies as second-order dynamical systems, denoted by $\ddot { \pmb x } = \pi ( \pmb x , \dot { \pmb x } )$ [8], [9]. The motion policies are described by the differential equation $M ( { \pmb x } , \dot { \pmb x } ) \ddot { \pmb x } + { \pmb f } ( { \pmb x } , \dot { \pmb x } ) = 0$ , where the matrix $M ( { \pmb x } , { \dot { \pmb x } } )$ is symmetric and invertible, and $M ( { \pmb x } , { \dot { \pmb x } } )$ and ${ f } ( { \pmb x } , { \dot { \pmb x } } )$ depend on position and velocity variables. These secondorder dynamical systems are referred to as spectral semisprays or simply specs $\boldsymbol { \mathcal { S } } = ( M , f ) _ { \mathcal { X } }$ . We drop the specsubscript if the task manifold is clear from the context.

# C. Operations on Spectral Semi-Sprays

The generation of complex trajectories involves various components, including collision avoidance and joint limits avoidance. In order to address these aspects, optimization fabrics utilize a weighted summation of metrics, enabling the integration of multiple components originating from different manifolds. The following operations, derived from operations on specs, play a crucial role in this process:

Energization: A spec can be energized by incorporating Lagrangian energy, effectively equipping the spec with a metric. This process involves a spec of the form $S _ { h } = ( I , h )$ with identity matrix $\pmb { I }$ , a geometry defining term $^ { h }$ , and an energy Lagrangian $\mathcal { L } _ { e }$ with the derived equations of motion $M _ { \mathcal { L } _ { e } } \ddot { \pmb { x } } + \pmb { f } _ { \mathcal { L } _ { e } } = 0$ . The operation of energization can be defined as follows:

$$
\begin{array}{l} S _ {h} ^ {\mathcal {L} _ {e}} = \operatorname {e n e r g i z e} _ {\mathcal {L} _ {e}} S _ {h} \tag {1} \\ = \left(M _ {\mathcal {L} _ {e}}, f _ {\mathcal {L} _ {e}} + P _ {\mathcal {L} _ {e}} \left[ M _ {\mathcal {L} _ {e}} h - f _ {\mathcal {L} _ {e}} \right]\right), \\ \end{array}
$$

Here, $\begin{array} { l } { P _ { \mathcal { L } _ { e } } ~ = ~ M _ { \mathcal { L } _ { e } } \left( M _ { \mathcal { L } _ { e } } ^ { - 1 } - \frac { \dot { x } \dot { x } ^ { T } } { \dot { x } ^ { T } M _ { \mathcal { L } _ { e } } \dot { x } } \right) } \end{array}$ x˙ x˙ T represents an orthogonal projector. The resulting energy-conserving spec is referred to as an energized spec, the operation itself is known as energization. The energized system follows the same path

and differs only by an acceleration along the direction of motion.

Pullback: Given a differential map $\phi : { \mathcal { C } }  { \mathcal { X } }$ and a spec $( M , f ) _ { \chi }$ , the pullback is defined as

$$
\operatorname {p u l l} _ {\phi} (\boldsymbol {M}, \boldsymbol {f}) _ {\mathcal {X}} = \left(\boldsymbol {J} _ {\phi} ^ {T} \boldsymbol {M} \boldsymbol {J} _ {\phi}, \boldsymbol {J} _ {\phi} ^ {T} (\boldsymbol {f} + \dot {\boldsymbol {J}} _ {\phi} \dot {\boldsymbol {q}})\right) _ {\mathcal {C}}. \tag {2}
$$

The pullback allows conversion between two distinct manifolds. For example, a spec defined in the robot’s workspace can be pulled into the robot’s configuration space using the pullback with $\phi$ representing the forward kinematics.

Summation: For two specs, $S _ { 1 } = ( M _ { 1 } , f _ { 1 } ) _ { \cal C }$ and ${ \cal S } _ { 2 } = $ $( M _ { 2 } , f _ { 2 } ) _ { \cal C }$ , their summation is defined as:

$$
\mathcal {S} _ {1} + \mathcal {S} _ {2} = \left(M _ {1} + M _ {2}, f _ {1} + f _ {2}\right) _ {\mathcal {C}}. \tag {3}
$$

We denote the combined spec as $\tilde { \cal S } = ( \tilde { M } , \tilde { f } ) _ { \cal C }$ .

By leveraging spectral semi-sprays and the aforementioned operations, joint limit avoidance, collision avoidance, or selfcollision avoidance can be achieved.

# D. Optimization Fabrics

Above, we discussed the combination of tasks that can be used for combining different avoidance behaviors. Additionally, spectral semi-sprays can be influenced by a potential, where $S _ { \psi } = ( M , f + \partial _ { x } \psi )$ is known as the forced spec. The solution ${ \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf { } } { \mathbf } { \mathbf { } } { \mathbf { } } { \mathbf } { } \mathbf { }  { \mathbf { } \mathbf { } } { \mathbf { } \mathbf { } } { \mathbf { } \mathbf { } } { \mathbf } { \mathbf { } } { \mathbf } { \mathbf } { } \mathbf { } \mathbf { } \mathbf { } \mathbf { }  { \mathbf } { \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } } { \mathbf } { \mathbf } { \mathbf } { \mathbf } { \mathbf } { \mathbf } { \mathbf } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf { } \mathbf \mathbf { } \mathbf $ of the forced spec $S _ { \psi }$ converges to the minimum of the potential $\psi ( { \pmb x } )$ if constructed via the guidelines of optimization fabrics. The construction of optimization fabrics involves the following steps:

1) Creation: The initial spec representing an avoidance component is formulated in the form ${ \ddot { \pmb x } } + \pmb h ( \pmb x , { \dot { \pmb x } } ) = 0$ . In this formulation, $^ { h }$ is homogeneous of degree 2, meaning that $h ( { \pmb x } , \alpha \dot { \pmb x } ) = \alpha ^ { 2 } h ( { \pmb x } , \dot { \pmb x } )$ .   
2) Energization: The spec’s geometry is energized using a Finsler structure [9, Definition 5.4] through the energization operation in Eq. 1. The combination of homogeneity of degree 2 and energization with the Finsler structure guarantees, as stated in [9, Theorem 4.29], that the energized spec forms a frictionless fabric. A frictionless fabric is defined as optimizing the forcing potential $\psi$ while being damped by a positive definite damping term [9, Definition 4.4]. As a result, the trajectory converges to a local minima if damped. 3) Combination: All avoidance components are combined in the configuration space of the robot using the pullback and summation operations. Note that both operations are closed under the algebra designed by these operations. In other words, every pulled optimization fabric or the sum of two optimization fabrics is itself an optimization fabric.   
4) Forcing: In the final step, the combined spec is forced by the potential $\psi$ to the desired minimum with attractor weight $\gamma$ and damped with a positive definite constant damping matrix $\textbf {  { B } }$ . This results in a system of the form

$$
\tilde {M} (\boldsymbol {q}, \dot {\boldsymbol {q}}) \ddot {\boldsymbol {q}} + \tilde {\boldsymbol {f}} (\boldsymbol {q}, \dot {\boldsymbol {q}}) + \gamma \partial_ {\boldsymbol {q}} \psi + B \dot {\boldsymbol {q}} = 0. \tag {4}
$$

Solving Eq. (4) yields to the trajectory generation policy in acceleration form $\ddot { \pmb q } = \tilde { \pi } ( \pmb q , \dot { \pmb q } )$ . In the following, we will refer to optimization fabrics by [9] as Static Fabrics (SF)

since the formulation relies on the assumption that obstacles are static at each time step.

# E. Dynamic Fabrics

Recently, DF have been proposed to handle dynamic environments, such as moving obstacles and reference path tracking [10]. By introducing a dynamic pull-back operation, relative coordinate systems, ${ \pmb x } _ { r e l } = { \pmb x } - { \bar { \pmb x } }$ , can be exploited to integrate the velocity and acceleration of moving obstacles. This operation is defined as

$$
\operatorname {p u l l} _ {\phi_ {d}} \left(M _ {d}, \boldsymbol {f} _ {d}\right) _ {\chi_ {\text {r e l}}} = \left(M _ {d}, \boldsymbol {f} _ {d} - M _ {d} \ddot {\bar {x}}\right) _ {\chi}, \tag {5}
$$

where $\mathcal { X } _ { \mathrm { r e l } }$ is the relative task manifold and $\ddot { x }$ is the acceleration of the moving obstacle. This dynamic pull-back alongside the dynamic energization effectively renders the spec $( M _ { d } , \pmb { f } _ { d } ) _ { \pmb { \chi } _ { \mathrm { r e l } } }$ dependent on $\bar { \pmb x }$ and $\dot { \bar { \mathbf { x } } }$ . For clarity, we will refer to $( { \bar { \pmb x } } , { \dot { \bar { \pmb x } } } , { \ddot { \bar { \pmb x } } } )$ as $( \pmb { x } _ { o b s } , \dot { \pmb { x } } _ { o b s } , \ddot { \pmb { x } } _ { o b s } )$ to indicate the position, velocity, and acceleration of the moving obstacles. For simplicity, acceleration dependency is often disregarded.

# F. Multi-Robot Problem Formulation

In previous works, SF and DF were presented for singlerobot scenarios. Here, we formulate the multi-robot case as a decentralized collision avoidance problem. Consider a multirobot scenario with $N$ robots with possibly different DOF, moving in close proximity in a shared workspace $\mathcal { W } \subseteq \mathbb { R } ^ { 3 }$ . We introduce the superscript $i$ to refer to the $i$ -th robot.

# Problem 1: (Decentralized Multi-Robot Fabrics)

In the decentralized case, each robot $i$ minimizes its own acceleration based on the states of the other robots $\neg i$ ,

$$
\tilde {\pi} ^ {i} \left(\boldsymbol {q} ^ {i}, \dot {\boldsymbol {q}} ^ {i}\right) = \ddot {\boldsymbol {q}} ^ {i} = \left(\tilde {\boldsymbol {M}} ^ {i}\right) ^ {- 1} \left(\tilde {\boldsymbol {f}} ^ {i} + \gamma^ {i} \partial_ {\boldsymbol {q} ^ {i}} \psi^ {i} + \beta \dot {\boldsymbol {q}} ^ {i}\right), \tag {6}
$$

where $\tilde { M } ^ { i }$ and $\tilde { f } ^ { i }$ are dependent on the current configuration and velocity of the robot as well as the states of the other robots $\neg i$ . In the following section, decentralized multi-robot fabrics are discussed in more detail and multi-robot collision avoidance is defined.

# IV. METHOD

In this section, we address multi-robot motion planning using fabrics as stated in Problem 1. We first derive the collision avoidance formulation and present Multi-Robot Dynamic Fabrics (MRDF) in Section IV-A. In Section IV-B Rollout Fabrics (RF) are introduced to detect future deadlocks. Lastly, we present a heuristic approach to resolve the deadlocks in Section IV-C.

# A. Multi-Robot Dynamic Fabrics

We first derive the collision-avoidance formulation for MRDF which requires the configurations and velocities of the other robots. These can be determined using a perception pipeline or through communication. Below, we only describe collision avoidance between robots, as the integration of static obstacles, dynamic obstacles, and joint limit avoidance were presented in [10] and [9].

We approximate each robot using collision spheres, see Fig. 1, with a center $\pmb { x } _ { o b s , l } ^ { i }$ and radius $r _ { o b s , l } ^ { i }$ for $l \in [ L ^ { i } ]$

where $L ^ { i }$ is the number of collision spheres per robot. The collision obstacles for robot $i$ are thus all collision spheres of the other robots, which is a total number of $\begin{array} { r } { \dot { O } ^ { i } ~ = ~ \sum _ { p = 1 , p \neq i } ^ { N } L ^ { p } } \end{array}$ . For each collision avoidance task $j \in$ $[ L ^ { i } O ^ { i } ]$ with relative task variable $\begin{array} { r } { \pmb { x } _ { r e l , j } ^ { i } = \pmb { x } _ { o b s , l } ^ { i } - \pmb { x } _ { o b s , l } ^ { p } } \end{array}$ for $p \neq i$ , we consider a geometry $\ddot { { \pmb x } } _ { r e l , j } + h ( { \pmb x } _ { r e l , j } , \dot { { \pmb x } } _ { r e l , j } ) = 0$

We derive the positions and velocities of thespheres using the forward kinematics and Jacobians, $\boldsymbol { x } _ { o b s , l } ^ { p } =$ $f k _ { l } ( { \pmb q } ^ { p } ) , \dot { \pmb x } _ { o b s , l } ^ { p } = J _ { l } \dot { \pmb q } ^ { p }$ . Thus, Eq. (6) becomes dependent on the state of all other robots resulting in

$$
\tilde {\pi} ^ {i} \left(\boldsymbol {q} ^ {i}, \dot {\boldsymbol {q}} ^ {i}, \boldsymbol {q} ^ {\neg i}, \dot {\boldsymbol {q}} ^ {\neg i}, \boldsymbol {\theta} ^ {i}, \boldsymbol {\theta} ^ {\neg i}\right). \tag {7}
$$

With a slight abuse of notation compared to Eq. (6) we explicitly add the dependency of $\tilde { \pi }$ to parameter vectors $\pmb { \theta } ^ { i }$ and $\pmb { \theta } ^ {  i }$ , e.g., the goal position $\pmb { p } _ { \mathrm { g o a l } }$ and attractor weight $\gamma$ .

We refer to this equation as MRDF which is solved by every robot given that the configuration and velocity of the other robots are communicated, observed, or estimated. In the following, we describe our proposed method to overcome deadlocks that are likely to occur in this naive approach.

# B. Rollout Fabrics

In this section, we introduce the notion of RF, an approach to forward propagate MRDF over a prediction horizon enabling the detection of deadlocks by forward propagating MRDF. Since fabrics are a lightweight representation that can easily be communicated, each robot can transmit its symbolic fabrics policy $\tilde { \pi } ^ { i }$ in the beginning of the interaction. We first assume that the current configuration and velocity, and goal configuration of all other robots are available at run-time. As mentioned before, this can be either observed or communicated. Later, we will relax this assumption. Without loss of generality, we refer to the current time step as $k = 0$ . Each robot $i \in [ N ]$ propagates its own MRDF and the MRDF formulation of the other robots $\neg i$ forward over $K$ discrete steps covering the horizon $T = K \Delta t$ .

To enhance clarity, we will now outline the approach from the perspective of the ego-robot $i$ . At each step $k$ , the egorobot $i$ computes its action $\ddot { q } _ { k } ^ { i }$ using Eq. 7. The actions of the other robots ${ \ddot { q } } _ { k } ^ { \lnot i }$ are derived using the communicated MRDF formulations. Then, the configurations and velocities of each robot $i \in [ N ]$ at $k + 1$ are computed given the configuration and velocities at step $k$ , the action $\ddot { q } _ { k } ^ { i }$ and their respective goal configuration. To avoid the need for simulating the complex dynamics of each robot, we approximate future configurations and velocities using a second-order integrator:

$$
\left[ \begin{array}{l} \boldsymbol {q} _ {k + 1} ^ {i} \\ \dot {\boldsymbol {q}} _ {k + 1} ^ {i} \end{array} \right] = \underbrace {\left[ \begin{array}{c c} \boldsymbol {I} _ {n} & \Delta t \boldsymbol {I} _ {n} \\ \boldsymbol {0} _ {n} & \boldsymbol {I} _ {n} \end{array} \right]} _ {\boldsymbol {A}} \left[ \begin{array}{l} \boldsymbol {q} _ {k} ^ {i} \\ \dot {\boldsymbol {q}} _ {k} ^ {i} \end{array} \right] + \underbrace {\left[ \begin{array}{c} \boldsymbol {0} _ {n} \\ \Delta t \boldsymbol {I} _ {n} \end{array} \right]} _ {\boldsymbol {B}} \ddot {\boldsymbol {q}} _ {k} ^ {i}, \tag {8}
$$

with identity matrix ${ { I } _ { n } }$ of size $n \times n$ and time-step $\Delta t$ . The proposed approach is summarized in Algorithm 1.

Instead of communicating the goal configuration every time the goal has changed, it can constantly be estimated by assuming a constant velocity for the end effector,

$$
\tilde {\boldsymbol {p}} _ {\text {g o a l}} = \boldsymbol {x} _ {\mathrm {e e}} + H \Delta t \boldsymbol {v} _ {\mathrm {e e}}, \tag {9}
$$

where $\scriptstyle { \pmb x } _ { \mathrm { e e } }$ and ${ \pmb v } _ { \mathrm { e e } }$ are the end effector position and velocity, respectively. The integer scaling factor $H$ determines the duration for which the constant velocity model predicts the future goal. RF considering the estimated goal $\tilde { p } _ { \mathrm { g o a l } }$ are in the following referred to as RF-CV.

The rollouts provide us with a set of configuration, velocity, and acceleration estimates along $T$ , which can be used to detect deadlocks. We apply a heuristic that detects deadlocks where at least two robots have average velocities along the prediction horizon $\begin{array} { r } { \bar { v } ^ { i } = \frac { 1 } { K } \sum _ { k = 0 } ^ { K } \lVert \dot { \pmb q } _ { k } ^ { i } \rVert _ { 2 } } \end{array}$ below the threshold $v _ { d , m i n }$ . An additional condition for a deadlock is that the position of the end-effectors $\mathbf { \Delta } \mathbf { x } _ { e e }$ of the robots have to be within a distance $d _ { e e , c }$ from each other. Thus, a deadlock is detected if the following condition holds for any $p \neq i$ :

$$
\left(\bar {v} ^ {i} <   v _ {\mathrm {d}, \min } \wedge \bar {v} ^ {p} <   v _ {d, \min }\right) \wedge \left(\left\| \boldsymbol {x} _ {\mathrm {e e}} ^ {i} - \boldsymbol {x} _ {\mathrm {e e}} ^ {p} \right\| _ {2} <   d _ {\mathrm {e e , c}}\right). \tag {10}
$$

If no deadlock is present, the ego-robot’s action is the acceleration $\ddot { q } _ { 0 } ^ { i }$ . A deadlock is assumed to be resolved when the predicted velocities are above the velocity minimum, $v _ { d , m i n }$ and a time of $t _ { d , m i n }$ has passed, or when one of the robots has reached its goal. The time requirement is introduced to avoid the robots from switching between normal and deadlock-resolving behavior.

Since we can approximate the current configurations and velocities of the other robots with RF, it is not required for each robot to communicate this at each time step. Instead, these can be communicated at a lower frequency and approximated using forward propagation if no current information is available.

Algorithm 1 Rollout Fabrics   
Input: $(\pmb{q}_0^i,\dot{\pmb{q}}_0^i) = (\pmb{q}_t^i,\dot{\pmb{q}}_t^i),\forall i\in [N]$ ▷Initialization for $k = 0:K$ do $\pmb{x}_{\mathrm{obst}}^{i} = f k(\pmb{q}_{k}^{i},\dot{\pmb{q}}_{k}^{i}),\forall i\in [N]$ obstacle positions $\dot{\pmb{x}}_{\mathrm{obst}}^{i} = J_{l}(\pmb{q}_{k}^{i},\dot{\pmb{q}}_{k}^{i}),\forall i\in [N]$ obstacle velocities $\ddot{\pmb{q}}_k^i = \tilde{\pi}^i (\pmb {q}^i,\dot{\pmb{q}}^i,\pmb {q}^{-i},\dot{\pmb{q}}^{-i},\pmb {\theta}^i,\pmb {\theta}^{-i}),\forall i\in [N]$ MRDF $\begin{bmatrix}\pmb{q}_{k + 1}^{i}\\ \dot{\pmb{q}}_{k + 1}^{i}\end{bmatrix} = \pmb {A}\begin{bmatrix}\pmb{q}_k^i\\ \dot{\pmb{q}}_k^i\end{bmatrix} + \pmb {B}\ddot{\pmb{q}}_k^i,\forall i\in [N]$ Model end for deadlock $= \operatorname {Eq.}10$ Detect deadlock

# C. Resolving Deadlocks

Here, we describe how the detected deadlocks can be addressed using a heuristic approach, which is summarized in Algorithm 2 for the two-robot case. If a deadlock is detected, a hierarchy is defined and communicated, based on the proximity of the robots to their respective goal or at random for a perfectly symmetric scenario. With this method, we do not claim completeness to resolve all possible deadlocks. Note that if all robots apply the same heuristic and the configurations and desired goals of the other robots are known, the hierarchy does not need to be communicated.

To resolve a deadlock, the lower-priority robot’s goal is set opposite to the higher-prioritized robot’s goal, $g o a l \_ l o w ( )$ . Additionally, the weight for goal-reaching $\gamma$ of the higherprioritized robot is increased to $\gamma _ { h i g h }$ .

Algorithm 2 Resolving deadlocks   
if deadlock then $g_{\mathrm{low\_priority}} = \mathrm{goal\_low}(\mathbf{q}),$ ▷Change goal $\gamma_{\mathrm{priority}} = \gamma_{\mathrm{high}},$ ▷Change weight $\ddot{\pmb{q}}_t = \tilde{\pi} (\pmb {q}_t^i,\dot{\pmb{q}}_t^i,\pmb {q}_t^{-i},\dot{\pmb{q}}_t^{-i},\pmb {\theta}^i,\pmb {\theta}^{-i}),\forall i\in [N]$ MRDF else $\ddot{\pmb{q}}_t = \ddot{\pmb{q}}_0,$ ▷Apply first action end if

# V. RESULTS

Here, we assess the performance of RF with deadlock resolution heuristics and compare them against MRDF. For a comparison between fabrics and MPC, we refer to [10].

# A. Experimental Setup and Performance Metrics

We consider multi-robot close-proximity pick-and-place scenarios as illustrated in Figure 1 and 2 and the video. Specifically, we apply multiple 7 DOF Franka Emika Pandas that are tasked to pick up their assigned cubes from a table and place them in a tray. Simulations are performed using the Pybullet physics simulation [29] and the open source toolbox urdfenvs. In the experiments, besides multi-robot collision avoidance, collision avoidance between each robot and the table is considered, as well as joint limit avoidance. The robots each have to pick and place two cubes. To evaluate the performance we consider the below metrics for a tworobot scenario with randomized initial cube positions:

• Success Rate: The ratio of successfully grasped and placed cubes within the time window $T _ { m a x }$ over the total number of cubes.   
• Time-to-Success: Time to complete the pick-and-place scenario for all robots successfully.   
• Collision Rate: Ratio of scenarios where at least one collision has occurred over all runs. A collision is registered if any collision sphere of a robot collides with either the environment or the collision spheres of the other robot.   
• Minimum Clearance: Minimum distance between the collision spheres of the robots.   
• Computation Time: The time to compute an action via the local motion planner at each time step.

Note, the above performance metrics, excluding the success rate and computation time, are only evaluated if the concerned motion planner succeeds. We execute our planner on a standard laptop (i7-12700H) without parallelization. All parameters are summarized in Table I. Joint velocities are provided as inputs to the robots by integrating $\ddot { q } ^ { i }$ , $\forall i \in [ N ]$ .

# B. Simulation Experiments

Table II displays the performance across 50 scenarios with randomized cube positions for MRDF, RF, and RF-CV. The

TABLE I: Parameters   

<table><tr><td>Max time Tmax</td><td>70 s</td><td>Time step Δt</td><td>0.01 s</td></tr><tr><td># of collision spheres Li</td><td>32</td><td>Pred. steps K</td><td>10</td></tr><tr><td>Min vel deadlock vd,min</td><td>0.03 rad/s</td><td>Radius robj</td><td>8 cm</td></tr><tr><td>Min time deadlock td,min</td><td>3.0 s</td><td>Weight γhigh</td><td>3</td></tr><tr><td>Min distance deadlock dee,c</td><td>0.35 m</td><td>Weight γlow</td><td>2</td></tr></table>

![](images/1c3cffc25b0ee76b5d53e05cd674debba9e39866d01fc5b4fed6a472cceb6a54.jpg)  
(a) Initial pose

![](images/38a61b3167fd2bfeed98b8325b088ffcaeeae3abcdb25ad3fbfd2237674eb1f1.jpg)  
(b) Deadlock detected

![](images/935fd05712f6e1e7b3d0b39ca4993b745f393cf7dd426a68ba30da94ed97a000.jpg)  
(c) Deadlock resolving

![](images/889bfcb2677519c41db9f7175b1f059e935266ef9e60013b9e2f32a1f95c378d.jpg)  
(d) Deadlock resolved

![](images/e1dd3d430993b71ae1d9c7355113d20a1c77155cf3f67f414a1a5a6421a15dae.jpg)  
(e) Block delivered   
Fig. 2: Selected time frames of RF resolving deadlocks

TABLE II: Statistics for 50 scenarios of our proposed methods RF and RF-CV compared to 50 scenarios of MRDF.   

<table><tr><td></td><td>Success-Rate</td><td>Time-to-Success [s]</td><td>Collision-rate</td><td>Min Clearance [m]</td><td>Computation Time [ms]</td></tr><tr><td>MRDF</td><td>0.73 ± 0.40</td><td>36.4 ± 15.8</td><td>0.31</td><td>0.004 ± 0.004</td><td>4 ± 0.9</td></tr><tr><td>RF</td><td>0.97 ± 0.11</td><td>25.0 ± 4.0</td><td>0.04</td><td>0.022 ± 0.013</td><td>20.5 ± 0.8</td></tr><tr><td>RF-CV</td><td>0.98 ± 0.09</td><td>24.7 ± 2.8</td><td>0.04</td><td>0.024 ± 0.015</td><td>29 ± 1.0</td></tr></table>

![](images/deccc76f98185a3ea11f1752044682198e770f36031868156427b45fae6586a7.jpg)  
Fig. 3: Scaling of computation times with horizon length $K$ .

benefits of RF combined with a heuristic approach to resolve deadlocks are clearly illustrated by a success rates of $9 7 \%$ compared to $73 \%$ for MRDF. The minimum clearance and collision-rate are also improved for RF compared to MRDF, since the deadlocks in MRDF cause close-to-collision configurations. Due to the rollouts being efficiently implemented using a symbolic Casadi function [30] defined beforehand and called during operation, the computation time of 20.5 ms is realistic for real-time local motion planning. Although a longer prediction horizon results in earlier detection of a deadlock, it comes with the drawback of increased computation times, see Fig. 3.

While RF assume that the goal configurations of the other robots are known, RF-CV removes this assumption by estimating the goal of the other robots. Figure 4 illustrates the joint angles of two robots that have reached a deadlock according to Eq. (10). For this specific scenario, the robots detect the deadlock with a time difference of 0.2 s when using goal estimation and deviate from RF with known goals. The success-rate, minimum clearance, collision-rate, and time-to-success for RF-CV are similar to RF, as can be seen in Table II. Applying RF-CV improved collision avoidance when compared to MRDF without requiring additional communication. Therefore, the goal estimation is beneficial in set-ups where communication is challenging or unreliable.

![](images/c81bbbddf83e1d927f9d0c67de29d1010b21e08b67fa59df038982132d5116f5.jpg)  
Fig. 4: Robot joint angles and identified deadlock instances. Panda 1 and Panda 2 apply Rollout Fabrics with an estimated goal for the other robot, respectively. Furthermore, the deadlock identified with full knowledge of the other robot’s goal is displayed.

# VI. CONCLUSIONS

In this work, we showcased the applicability of dynamic fabrics to multi-robot scenarios. Additionally, dynamic fabrics are extended to Rollout Fabrics (RF), where dynamic fabrics are propagated forward in time. These future predictions are used to detect and resolve deadlock scenarios. Simulation experiments are performed with multiple manipulators where each robot performs a pick-and-place task in close proximity to the other robots. Analyzing the scenarios with two manipulators, the success rate of the proposed RF in combination with the proposed deadlock resolution is increased compared to multi-robot dynamic fabrics. Additionally, we analyze RF with goal estimation which removes the requirement for communicating updated goals. For future research, we want to explore the applicability of RF to human-centered environments and analyze how the strategy of rollouts can be used for manipulation tasks involving physical interaction. Our approach would thereby benefit from advances in environment and robot representation. Furthermore, we intend to show the applicability of RF in real-world experiments.

# REFERENCES

[1] Z. Feng, G. Hu, Y. Sun, and J. Soon, “An overview of collaborative robotic manipulation in multi-robot systems,” Annual Reviews in Control, vol. 49, pp. 113–127, 2020.   
[2] P. D. Christofides, R. Scattolini, D. M. de la Pena, and J. Liu, “Distributed model predictive control: A tutorial review and future research directions,” Computers & Chemical Engineering, vol. 51, pp. 21–41, 2013.   
[3] M. Spahn, B. Brito, and J. Alonso-Mora, “Coupled mobile manipulation via trajectory optimization with free space decomposition,” in 2021 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2021, pp. 12 759–12 765.   
[4] W. Edwards, G. Tang, G. Mamakoukas, T. Murphey, and K. Hauser, “Automatic tuning for data-driven model predictive control,” in 2021 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2021, pp. 7379–7385.   
[5] J. Nubert, J. Kohler, V. Berenz, F. Allg ¨ ower, and S. Trimpe, “Safe and ¨ fast tracking on a robot manipulator: Robust mpc and neural network control,” IEEE Robotics and Automation Letters, vol. 5, no. 2, pp. 3050–3057, 2020.   
[6] L. Hewing, K. P. Wabersich, M. Menner, and M. N. Zeilinger, “Learning-based model predictive control: Toward safe learning in control,” Annual Review of Control, Robotics, and Autonomous Systems, vol. 3, pp. 269–296, 2020.   
[7] N. D. Ratliff, J. Issac, D. Kappler, S. Birchfield, and D. Fox, “Riemannian motion policies,” arXiv preprint arXiv:1801.02854, 2018.   
[8] C.-A. Cheng, M. Mukadam, J. Issac, S. Birchfield, D. Fox, B. Boots, and N. Ratliff, “Rmp flow: A computational graph for automatic motion policy generation,” in Algorithmic Foundations of Robotics XIII: Proceedings of the 13th Workshop on the Algorithmic Foundations of Robotics 13. Springer, 2020, pp. 441–457.   
[9] N. D. Ratliff, K. Van Wyk, M. Xie, A. Li, and M. A. Rana, “Optimization fabrics,” arXiv preprint arXiv:2008.02399, 2020.   
[10] M. Spahn, M. Wisse, and J. Alonso-Mora, “Dynamic Optimization Fabrics for Motion Generation,” IEEE Transactions on Robotics, pp. 1–16, 2023.   
[11] K. Van Wyk, M. Xie, A. Li, M. A. Rana, B. Babich, B. Peele, Q. Wan, I. Akinola, B. Sundaralingam, D. Fox et al., “Geometric fabrics: Generalizing classical mechanics to capture the physics of behavior,” IEEE Robotics and Automation Letters, vol. 7, no. 2, pp. 3202–3209, 2022.   
[12] M. Xie, K. Van Wyk, A. Li, M. A. Rana, Q. Wan, D. Fox, B. Boots, and N. Ratliff, “Geometric fabrics for the acceleration-based design of robotic motion,” arXiv preprint arXiv:2010.14750, 2020.   
[13] K. Solovey, O. Salzman, and D. Halperin, “Finding a needle in an exponential haystack: Discrete rrt for exploration of implicit roadmaps in multi-robot motion planning,” The International Journal of Robotics Research, vol. 35, no. 5, pp. 501–513, 2016.   
[14] V. N. Hartmann, A. Orthey, D. Driess, O. S. Oguz, and M. Toussaint, “Long-horizon multi-robot rearrangement planning for construction assembly,” IEEE Transactions on Robotics, vol. 39, no. 1, pp. 239– 252, 2022.   
[15] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in 2000 IEEE International Conference on Robotics and Automation (ICRA), vol. 2. IEEE, 2000, pp. 995– 1001.

[16] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” IEEE Transactions on Robotics and Automation, vol. 12, no. 4, pp. 566–580, 1996.   
[17] G. Sanchez and J.-C. Latombe, “Using a prm planner to compare centralized and decoupled planning for multi-robot systems,” in 2002 IEEE International Conference on Robotics and Automation (ICRA), vol. 2. IEEE, 2002, pp. 2112–2119.   
[18] R. Shome, K. Solovey, A. Dobson, D. Halperin, and K. E. Bekris, “drrt*: Scalable and informed asymptotically-optimal multi-robot motion planning,” Autonomous Robots, vol. 44, no. 3-4, pp. 443–467, 2020.   
[19] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “Chomp: Gradient optimization techniques for efficient motion planning,” in 2009 IEEE international conference on robotics and automation. IEEE, 2009, pp. 489–494.   
[20] D. Q. Mayne, J. B. Rawlings, C. V. Rao, and P. O. Scokaert, “Constrained model predictive control: Stability and optimality,” Automatica, vol. 36, no. 6, pp. 789–814, 2000.   
[21] A. Tika, N. Gafur, V. Yfantis, and N. Bajcinca, “Optimal scheduling and model predictive control for trajectory planning of cooperative robot manipulators,” IFAC-PapersOnLine, vol. 53, no. 2, pp. 9080– 9086, 2020.   
[22] A. Tika and N. Bajcinca, “Synchronous minimum-time cooperative manipulation using distributed model predictive control,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2020, pp. 7675–7681.   
[23] N. Gafur, G. Kanagalingam, and M. Ruskowski, “Dynamic collision avoidance for multiple robotic manipulators based on a noncooperative multi-agent game,” arXiv preprint arXiv:2103.00583, 2021.   
[24] O. Khatib, “Real-time obstacle avoidance for manipulators and mobile robots,” The international journal of robotics research, vol. 5, no. 1, pp. 90–98, 1986.   
[25] ——, “A unified approach for motion and force control of robot manipulators: The operational space formulation,” IEEE Journal on Robotics and Automation, vol. 3, no. 1, pp. 43–53, 1987.   
[26] F. Bullo and A. D. Lewis, Geometric control of mechanical systems: modeling, analysis, and design for simple mechanical control systems. Springer, 2019, vol. 49.   
[27] A. Li, C.-A. Cheng, M. A. Rana, M. Xie, K. Van Wyk, N. Ratliff, and B. Boots, “Rmp2: A structured composable policy class for robot learning,” arXiv preprint arXiv:2103.05922, 2021.   
[28] X. Meng, N. Ratliff, Y. Xiang, and D. Fox, “Neural autonomous navigation with riemannian motion policy,” in 2019 International Conference on Robotics and Automation (ICRA). IEEE, 2019, pp. 8860–8866.   
[29] E. Coumans and Y. Bai, “Pybullet, a python module for physics simulation for games, robotics and machine learning,” http://pybullet.org, 2016.   
[30] J. A. Andersson, J. Gillis, G. Horn, J. B. Rawlings, and M. Diehl, “Casadi: a software framework for nonlinear optimization and optimal control,” Mathematical Programming Computation, vol. 11, pp. 1–36, 2019.