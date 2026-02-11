# Human-Aware Physical Human-Robot Collaborative Transportation and Manipulation with Multiple Aerial Robots

Guanrui $\mathrm { L i ^ { * } }$ , Xinyang Liu∗, and Giuseppe Loianno

![](images/cdd6309c66f9f7a2dc7ab2fcd7ca405c744dea74721f270bb40cf95d990c9757.jpg)  
Fig. 1: A human operator collaborates with three quadrotors, transporting and manipulating a payload. On the left: The quadrotors are moving to keep a distance from the human operator without affecting payload tracking. On the right: the aerial robot team is transporting the payload using the human operator’s interactive force and moment as commands.

Abstract—Human-robot interaction will play an essential role in various industries and daily tasks, enabling robots to effectively collaborate with humans and reduce their physical workload. Most of the existing approaches for physical human-robot interaction focus on collaboration between a human and a single ground or aerial robot. In recent years, very little progress has been made in this research area when considering multiple aerial robots, which offer increased versatility and mobility. This paper proposes a novel approach for physical humanrobot collaborative transportation and manipulation of a cablesuspended payload with multiple aerial robots. The proposed method enables smooth and intuitive interaction between the transported objects and a human worker. In the same time, we consider distance constraints during the operations by exploiting the internal redundancy of the multi-robot transportation system. The key elements of our approach are (a) a collaborative payload external wrench estimator that does not rely on any force sensor; (b) a 6D admittance controller for human-aerial-robot collaborative transportation and manipulation; (c) a human-aware force distribution that exploits the internal system redundancy to guarantee the execution of additional tasks such inter-humanrobot separation without affecting the payload trajectory tracking or quality of interaction. We validate the approach through extensive simulation and real-world experiments. These include scenarios where the robot team assists the human in transporting

and manipulating a load, or where the human helps the robot team navigate the environment. We experimentally demonstrate for the first time, to the best of our knowledge, that our approach enables a quadrotor team to physically collaborate with a human in manipulating a payload in all 6 DoF in collaborative humanrobot transportation and manipulation tasks.

Index Terms—Aerial Robotics, Physical Human-Robot Interaction

# SUPPLEMENTARY MATERIAL

Video: https://youtu.be/WMev7j97fDg

# I. INTRODUCTION

As envisioned in the Industry 4.0 revolution, human-robot interaction will play an increasingly significant role in future industries and daily life [1]. While most research in humanrobot interaction has concentrated on collaborations between humans and ground robots, only a limited number of approaches have been developed for aerial robots, with the majority being confined to teleoperation. Unlike ground robots, collaborative Micro Aerial Vehicles (MAVs) show additional flexibility and maneuverability due to their 3D mobility and compact size. Moreover, a team of collaborative MAVs can provide increased adaptivity, resilience, and robustness during a task or multiple simultaneous tasks compared to a single aerial robot. For example, MAV teams can assist humans in

executing complex or dangerous tasks, including but not limited to inspection [2], [3], mapping [4], [5], environment interaction [6], [7], surveillance [8], and autonomous transportation and manipulation [9], [10]. Specifically, in autonomous aerial transportation and manipulation, there are many possible usage scenarios. For instance, in a post-disaster response task, a team of aerial robots can cooperatively deliver emergency supplies to designated rescue locations based on the first respondent’s guidance. Alternatively, on construction sites, an aerial robot team can cooperatively manipulate over-sized construction materials with human workers to expedite the installation process and reduce physical workload.

This paper proposes a novel approach that enables a team of aerial robots to transport and manipulate a cable-suspended payload in physical collaboration with a human operator, as depicted in Fig. 1. As discussed in [11], cable mechanisms stand out compared to other existing solutions, such as simple spherical joints, or robot arms [12], [13], because of their lighter weight, lower costs, simpler design requirements, and zero-actuation-energy consumption. Therefore, they are particularly suited for Size, Weight, and Power (SWaP) aerial platforms.

Cables also present a good balance among maneuverability, manipulability, and safety for physical human-aerial-robots collaboration compared to other solutions. For instance, several solutions attach the robots directly to the payloads via passive mechanisms like spherical joints [14], magnets [15] or active mechanisms like grippers [16]. However, these mechanisms offer reduced maneuverability and manipulability during a manipulation or physical interaction task compared to cables. Conversely, other complex actuated solutions based on robot arms [17]–[19] can enhance maneuverability and flexibility. However, this generally comes at the price of increased system inertia and power, potentially compromising the operator’s safety. Therefore, compared to other existing solutions, we believe that lightweight cable mechanisms can provide a good trade-off in terms of maneuverability, manipulability, and safety while concurrently offering good flexibility to execute multiple tasks.

We present an innovative control, planning, and estimation framework that enables a human operator to physically collaborate with a team of quadrotors for the transportation and manipulation of a rigid-body payload in all 6 Degrees of Freedom (DoF). A key contribution of this work is the exploitation of system redundancy, allowing for secondary tasks, such as human-aware human-robot interaction. Specifically, our approach ensures distancing between agents and the human operator during physical collaboration, enabling effective human-aware interaction, as depicted in Fig. 1 (left).

Existing approaches to human and aerial robot collaboration have largely focused on single aerial robot interactions [18], [20], [21]. When considering multiple aerial robots, teleoperation becomes a common solution [6], [22]. However, few solutions exist for human physical interaction and collaboration with several MAVs [23], [24]. However, the human operator’s physical collaboration is limited to a 2D horizontal plane. Moreover, these approaches overlook the potential of exploiting the additional DoF to enhance both the system’s

awareness of the human’s presence.

In summary, the contributions of this paper are the following

• We propose a novel control method that enables a team of quadrotors to manipulate a payload while exploiting the system’s redundancy to achieve secondary tasks (e.g., maintaining distances from the human operator or ensuring inter-robot separation). This solution facilitates the physical interaction between the quadrotor team and a human operator.

• We introduce a collaborative external wrench estimator that allows the robot team to collaboratively measure an external human force input without relying on any external force sensors. Additionally, we demonstrate that this approach outperforms existing state-of-the-art solutions.

• We complement our control solution with a 6-DoF admittance controller, which utilizes the estimated human wrench. It enables physical interaction between a human operator and a team of aerial robots for collaborative manipulation and transportation tasks.

• We experimentally demonstrate for the first time, to the best of our knowledge, that our approach enables a quadrotor team to physically collaborate with a human in manipulating a payload in all 6 DoF in collaborative human-robot transportation and manipulation tasks.

The remainder of the paper is organized as follows. In Section II, we review relevant literature on cooperative aerial manipulation and physical human-robot interaction. In Section IV, we review the nonlinear system dynamics, considering the external wrench from a human operator. In Section V, we discuss the proposed human-aware control framework that considers the nonlinear system dynamics. Section VI details the state estimation strategy and admittance control framework for intended human-aerial-robot collaborative manipulation. Section VII presents real-world experiment results validating the proposed framework. Section IX concludes the work and proposes multiple future research directions.

# II. RELATED WORKS

# A. Cooperative Aerial Manipulation

In the subsequent discussion, we focus on the existing related works on control, planning, and estimation techniques for aerial transportation and manipulation using suspended cables. This focus arises from the distinct advantages that cable mechanisms offer over other methods, as previously mentioned.

Past literature includes several control and estimation methods [11], [22], [25], [26] for autonomous aerial transportation and manipulation using multiple aerial robots equipped with cables. For example, several works [25]–[29] propose formation controllers for a team of MAVs to fly in a desired formation when carrying the suspended-payload. The carried payload is not modeled as an integrated part of the system but as an external disturbance that each MAV controller tries to compensate for. Therefore, it is expected that these solutions can struggle to transport the payload to a given position. In [30], by assuming the payload is a point-mass, the authors analyze the full nonlinear dynamics of the system. Based on

the dynamic model, the authors design a geometric controller to transport the payload to the desired position moving the quadrotor team to accommodate the desired load motions. Moreover, the previously mentioned methods [26]–[28], [30], treat the payload as a point-mass, hence restricting the manipulation capabilities to payload’s positional movements only, with no control over its orientation.

Other approaches for autonomous aerial transportation and manipulation rely on a leader-follower paradigm [31]–[35]. The leader robot follows the desired trajectory, whereas the followers maintain either a constant distance from the leader [33], or adapt to forces exerted on them when tracking their trajectory [14], [31]. However, these methods are subject to error compounding failure since they rely on the leader as a fundamental control unit for navigation. Furthermore, they cannot accurately guarantee the payload’s transportation to the desired location or manipulate its orientation.

Several works analyze the system’s complex nonlinear dynamics and mechanics and propose corresponding controllers to control the payload’s pose in 6 DoF [36]–[39]. For example, in [38], [39], the authors assume the system is in a quasi-static state and analyze the corresponding static system mechanics. A payload pose controller assigns the quadrotors’ desired position to manipulate the payload to the desired pose. In [36], [37], the complex nonlinear dynamics in the system are thoroughly analyzed using Lagrangian mechanics. Leveraging this model, nonlinear geometric controllers enable the payload to follow the desired pose trajectory. More recently, several solutions propose optimal control strategies [40], [41]. Although all these works consider the payload a rigid body, the redundant control DoF available in the system [42] are not exploited to accommodate additional tasks like obstacle avoidance or to ensure safety distance among agents.

Some recent literature starts to investigate this aspect [7], [22], [43]. However, they are specifically designed for a team of three or four quadrotors. In [44], the authors attempt to leverage system redundancy for a team with an arbitrary number of aerial robots, implementing an optimization formulation for the parallel robot that exclusively optimizes the tension magnitude in the cables, without considering cable directions. However, the methodology presented in [44] does not provide clear instructions for determining cable direction. Consequently, its applicability for secondary tasks such as obstacle avoidance or spatial separation from the human operator remains ambiguous. In this work, we formulate a human-aware controller for any $n \geq 3$ quadrotors that exploit the additional system redundancy at the control level, allowing the system to achieve some secondary tasks, such as avoiding obstacles, inter-robot separation or keeping a safe distance among robots and human operators.

However, since the above methods are designed to control the payload’s pose explicitly, it is essential to have a reasonable estimation of the payload’s states (i.e., pose and twists) to be fed back into the controller to have a good tracking performance of the payload’s pose. Some estimation approaches can recover the payload pose in [22], [45], but they rely on GPS and, therefore, cannot be employed in indoor environments or areas where the GPS signal is shadowed. Conversely, in

our previous work [11], we tackle the payload pose inference problem using onboard vision sensors and IMU to obtain closed-loop control of the payload pose.

However, the proposed vision-based estimation method might be subject to onboard visual-inertial odometry drift, leading to some constant offset errors. Although such errors will not affect the stability of the system, they will influence the task performance. For instance, consider a scenario where the system is required to transport a payload to a specific location, but due to state estimation drift, there is a 1-meter offset from the desired destination. In such cases, as shown in this paper, our proposed method enables a local human operator to guide the system and correct the payload to the desired pose, ensuring that the payload is transported to the correct final destination.

# B. Physical Human-Robot Interaction

Physical Human-Robot Interaction (pHRI) is a rapidly growing field in robotics, facilitating the collaboration between humans and robots in various scenarios such as manufacturing, healthcare, and service industry. Most of the research in this field focuses on the collaboration between a single robot and a human. For instance, this includes cooperative manipulation with a robot arm attached to a ground wheeled base [46], [47], a fixed-base robot arm [48], a humanoid robot [49], or an aerial robot with a manipulator [18], [20]. Past Researchers’ works also present approaches like admittance control [20], [50], compliance control, impedance control for single-humansingle-robot physical collaboration.

To increase payload capacity, the common strategies are either deploying a more powerful robot or utilizing a team of robots. The latter approach not only increases redundancy and provides the potential for fault tolerance, but also brings in specialized capabilities that enhance the team’s resilience and performance compared to a single robot. However, employing a team of robots demands effective coordination and collaboration across estimation, planning, and control levels.

While multiple robot-human interactions with teleoperation via haptic devices [51] or mixed reality glasses [52], [53] is a widely explored research topic, physical human-multi-robot cooperative manipulation remains mostly underexplored [54]. Recently, a handful of works started to research on direct physical interaction between a human and multiple ground robots to cooperatively manipulate or transport an object [54]– [56]. In [56], the authors demonstrate that 4 omnidirectional ground robots with robot arms can physically collaborate with a human using their proposed force-mediated controller but only simulation results were presented. In [54], the authors design an omni-robot system that can lift payloads. Then the multiple proposed omni-robots can collaborate with humans to manipulate objects toward desired locations. In [55], the authors use two robot arms with omnidirectional wheeled base to physically collaborate with a human to manipulate oversize objects. They introduce an admittance control module on both ground robots to adapt the human motion as the human leads the manipulation. However, the system dynamics for aerial robots are inherently different from ground robots as

aerial robots move in 3D. Hence, the established dynamics models and corresponding control methods for ground robots cannot be directly translated to aerial robots. Moreover, for the SWAP-constrained aerial robots, designing a lightweight, computationally efficient sensing strategy is also essential.

In [23], the authors propose a framework for physical human-robot collaborative transportation of cable-suspended payload with a team of quadrotors. The proposed approach models the payload as a point mass and assumes external forces applied on the payload to be constrained in 2D. Leveraging their previous work [33], the designed controller assigns three quadrotors as leaders and the remaining robots as followers in the team. When an external force is applied to the payload, a fixed step is given to the leaders’ positions along the estimated force direction. In [24], five quadrotors collaborate with a human operator to transport a point mass payload. The force applied by a human on the payload is estimated by summing the cable tension forces and subtracting the gravity. The human-applied force is fed into an admittance controller, which updates the desired quadrotor position and velocity in the formation. However, compared to our work, the cable tension magnitude is measured by a custom tension measurement module, and its direction by a motion capture system. Moreover, the aforementioned works present substantial limitations as they presume the payload to be a point mass and constrain the human operator to manipulate the payload in only 2D. On the contrary, in our proposed work, we widen the scope of physical interactions between the human operator and the payload to all 6 DoF. This enhancement is achieved by modeling the payload as a rigid body with 6 DoF and developing an estimator to estimate the full 6 DoF wrench acting on the payload. Furthermore, our system removes the use of any force-measuring devices on the robots or payload (except to obtain the ground truth during testing for validating our estimation approach). These are unique characteristics that increase the flexibility and applicability of our solution compared to existing ones.

# III. OVERVIEW

In this section, we present an overview of our proposed system designed to enable a team of quadrotors to collaborate with a human operator to manipulate a rigid-body payload. Depicted in Fig. 2, the system comprises $n$ quadrotors, and each quadrotor is tethered by a cable to its center of mass. The software architecture of the system encompasses couple of primary components: planning and control, and physical human-robot interaction, as shown in Fig. 3. We provide a more detailed description of each module below.

# A. Planning and Control

The planning module generates a desired trajectory for the payload, encompassing both position and orientation. The trajectory is represented by a polynomial trajectory of time. By differentiating the polynomial with respect to time, we can obtain payload state’s respective first and second derivatives. These derivatives represent the twist and acceleration of the payload pose. We use the similar planning method as the

![](images/cdbe77298334c5c1ad670039b2643712b3efa65477e11069a61fa52551e78cc1.jpg)  
Fig. 2: System convention definition: I, L, Bk denote the world frame, the payload body frame, and the $k ^ { t h }$ robot body frames, respectively, for a generic quadrotor team that’s cooperatively transporting and manipulating a cable-suspended payload.

one we used in our previous work to generate the trajectory for payload [57]. The desired values will be fed into the admittance controller. If human interaction with the payload occurs, the admittance controller will update the trajectory in response to the human inputs.

The control proposed in this paper, described in Section V, adopts a hierarchical design that comprises the payload tracking controller, dynamic force distribution, and robot controller. The hierarchical controller design offers several advantages. Firstly, it simplifies the complex task of controlling the entire system by breaking it down into several manageable subtasks. At the base of our design is the robot controller, which computes the control actions based on local information, such as cable direction and robot orientation. This strategy allows us to first test the individual robot controller with a single robot, thereby ensuring we do not risk compromising the entire system. After successfully building and testing the robot controller, we can proceed to test the higher-level modules, including the payload controller and dynamic force distribution.

Moreover, the modularity enhances the system’s maintainability and scalability, as changes or improvements to one part of the control system can be implemented without affecting other components. For example, in our case, we can introduce the adaptation module at the payload level without changing the robot controller.

In the following sections, we will provide a more detailed overview of the controllers within the control design.

1) Payload Controller: The payload controller’s function is to control the payload’s state, enabling it to track the adapted desired payload states from the admittance controller. It generates the desired manipulation force and moment on the payload to track the desired payload states.

![](images/b746a0dbcf064c7acda86e686e66f38826b3ca12cd9d5b4f85a8509ee8be1d51.jpg)  
Fig. 3: Block diagram of the system illustrating the overview of the system. It begins with a trajectory generator, which outputs the desired trajectory of the payload in all six degrees of freedom. The payload admittance controller updates this trajectory based on the estimated human input, adapting to the interaction wrench exerted by the human on the payload. The modified trajectory is then passed to the payload controller as the desired payload state to track. The payload controller calculates the desired wrench to control the payload’s motion. Subsequently, the dynamic force distribution module allocates the desired cable forces based on the human’s position and the system dynamics, and distributes the desired cable forces for each robot to track. Each robot controller will then track its corresponding desired cable force and output the corresponding thrust and moment commands to the quadrotor platform.

2) Dynamic Force Distribution: The dynamic force distribution dynamically distributes the desired cable tension forces that each quadrotor needs to exert to manipulate the payload. It consists of two parts: nominal force distribution and humanaware force modification.

Nominal Force Distribution: The nominal module processes the desired forces and moments on the payload, as computed by the payload controller. It maps the desired wrench on the payload into nominal desired cable tension forces for each quadrotor.

Human-Aware Force Distribution: This module leverages the redundancy inherent in a multi-quadrotor system to adjust the nominal cable tension forces calculated by the nominal tension distribution module. It modifies the nominal cable tension forces without impacting the overall manipulation forces and moments exerted on the payload computed by the payload controller.

3) Robot Controller: Each quadrotor runs an individual robot controller to track the desired cable tension forces assigned from the dynamic force distribution module. It commands thrust and moment to the quadrotor such that the quadrotor can track the desired cable direction as well as exert the desired tension in the cable.

# B. Physical Human-Robot Interaction

The Human Interaction module proposed in this paper in Section VI, comprises two main parts: the admittance controller and Human Input Estimation.

# C. Robot State Estimation

Each robot runs an onboard Unscented Kalman Filter(UKF) to estimate the robot’s position, velocity, orientation, angular velocity, and the cable force applied to the robot. The cable force estimated by each quadrotor will be shared among the team to collaboratively estimate the human wrench.

1) Human Wrench Estimation: This component estimates the human’s input wrench on the payload by collecting all the cable forces estimated by each quadrotor. Given the challenges associated with adding additional force sensors to the payload for real-world applications, we aim to minimize modifications to maintain cost-effectiveness. Our innovative solution, which does not require any additional force sensor, involves each quadrotor estimating its cable force. And the estimated cable force is then shared among the team to deduce the total forces and moments from all cables, further derive the human input wrench.   
2) Payload Admittance Controller: The admittance controller modifies the desired payload trajectory based on humanapplied forces and moments. This would allow the system to adapt to the human input, leading to collaborative transportation and manipulation of the payload between the human and the team of quadrotor robots.

# IV. SYSTEM DYNAMICS

This section presents the modeling of the overall system dynamics. We consider a scenario where a team of $n$ quadrotors cooperatively manipulates a rigid body payload, as illustrated in Fig. 2. We establish the world frame $\mathcal { T }$ on the ground. The payload frame $\mathcal { L }$ is located at the payload’s center of mass. The

TABLE I: Notation table   

<table><tr><td>I, L, Bk</td><td>world frame, payload frame, kthrobot frame</td></tr><tr><td>mL, mk ∈ R</td><td>mass of payload, kthrobot</td></tr><tr><td>xL, xk ∈ R3</td><td>position of payload, kthrobot in I</td></tr><tr><td>xL, xk ∈ R3</td><td>linear velocity, acceleration of payload in I</td></tr><tr><td>xk, xk ∈ R3</td><td>linear velocity, acceleration of kthrobot in I</td></tr><tr><td>RL ∈ SO(3)</td><td>orientation of payload with respect to I</td></tr><tr><td>Rk ∈ SO(3)</td><td>orientation of kthrobot with respect to I</td></tr><tr><td>Θk ∈ R3</td><td>vector of kthrobot&#x27;s yaw, pitch, roll in I</td></tr><tr><td>ΩL, ΩL ∈ R3</td><td>payload&#x27;s angular velocity, acceleration in L</td></tr><tr><td>Ωk, Πk ∈ R3</td><td>kthrobot&#x27;s angular velocity, acceleration in Bk</td></tr><tr><td>JL, Jk ∈ R3×3</td><td>moment of inertia of payload, kthrobot</td></tr><tr><td>ξk ∈ S2</td><td>unit vector from kthrobot to attach point in I</td></tr><tr><td>ωk ∈ R3, lk ∈ R</td><td>angular velocity, length of kthcable</td></tr><tr><td>μk ∈ R</td><td>tension magnitude within the kthcable</td></tr><tr><td>FH, Fk ∈ R3</td><td>external human force, net force on payload in I</td></tr><tr><td>MH ∈ R3</td><td>external human moment on payload in L</td></tr><tr><td>ML ∈ R3</td><td>net moment on payload in L</td></tr><tr><td>fk ∈ R</td><td>total thrust of kthquadrotor</td></tr><tr><td>Fk ∈ R3</td><td>control force on kthrobot in I</td></tr><tr><td>Mk ∈ R3</td><td>control moment on kthrobot in Bk</td></tr><tr><td>ρk ∈ R3</td><td>kthattach point position in L</td></tr><tr><td>pH, Patt,k ∈ R3</td><td>human position, kthattach point position in I</td></tr></table>

payload’s position and orientation relative to $\mathcal { T }$ are denoted by $\mathbf { x } _ { L }$ and $\scriptstyle { R _ { L } }$ , respectively.

The relevant variables in this paper are summarized in Table I. We denote the three elements of any 3D vector using subscripts ∗x,y,z. ${ * } _ { x , y , z }$

The system dynamics models are developed based on the following assumptions

1) Aerodynamic interactions with the ground and other effects caused by high robot velocity are ignored due to its insignificant effect at a low moving speed that’s achieved by this system;   
2) Each cable is assumed to be attached at the center of mass of each robot, each robot’s center of gravity coincides with its geometrical center, and all cables are assumed to be massless with no dynamic effects on the system;   
3) Wind disturbances are ignored, the human operator would only interact with the payload, and all external forces on the payload and each robot are considered to be exerted by a human operator.

Assumption 1 is justified by the operational velocity, and spatial separation among agents we propose in Section V-B2, which minimizes aerodynamic effects. Assumption 2 is based on the symmetrical design of the MAV and the lightweight nature of the cables. Finally, Assumption 3 is relevant due to our focus on indoor operation.

# A. Basic Geometry

As shown in Fig. 2, the $k ^ { t h }$ quadrotor attached one massless cable with length $l _ { k }$ from its center of mass to the $k ^ { t h }$ attach point on the payload. The location of the attach point $k$ with respect to $\mathcal { L }$ and $\mathcal { T }$ is represented by constant vector ${ \boldsymbol \rho } _ { k } \in \mathbb { R } ^ { 3 }$ and vector $\mathbf { p } _ { a t t , k } \in \mathbb { R } ^ { 3 }$ respectively. Hence, from the geometry, we can have

$$
\mathbf {p} _ {\text {a t t}, k} = \mathbf {x} _ {L} + \boldsymbol {R} _ {L} \boldsymbol {\rho} _ {k}. \tag {1}
$$

As we can also observe from Fig. 2, when the cable is taut, the robot’s position can be obtained by using the attach point

position and the cable as follows

$$
\mathbf {x} _ {k} = \mathbf {p} _ {\text {a t t}, k} - l _ {k} \boldsymbol {\xi} _ {k}, \tag {2}
$$

where $\mathbf { x } _ { k }$ is the $k ^ { t h }$ quadrotor’s position in $\mathcal { T }$ , and $\xi _ { k }$ is the unit vector that represents the cable direction from the robot to the corresponding attach point in $\mathcal { T }$ .

# B. Payload Dynamics

The net force $\mathbf { F } _ { L }$ in $\mathcal { T }$ and moment ${ \bf M } _ { L }$ in $\mathcal { L }$ on the payload is determined by all the cable tension forces $\mu _ { k }$ , $k = 1 , \cdots , n$ , gravitational pull g, and external wrench $\mathbf { F } _ { H } , \mathbf { M } _ { H }$ applied by the human operator

$$
\left[ \begin{array}{l} \mathbf {F} _ {L} \\ \mathbf {M} _ {L} \end{array} \right] = \left[ \begin{array}{l} \mathbf {F} _ {H} \\ \mathbf {M} _ {H} \end{array} \right] + \mathbf {P} \boldsymbol {\mu} - \left[ \begin{array}{c} m _ {L} \mathbf {g} \\ \mathbf {0} \end{array} \right], \quad \boldsymbol {\mu} = \left[ \begin{array}{c} \boldsymbol {\mu} _ {1} \\ \vdots \\ \boldsymbol {\mu} _ {n} \end{array} \right], \tag {3}
$$

where $m _ { L }$ is the payload mass, $\mathbf { g } ~ = ~ g \mathbf { e } _ { 3 }$ , $g \ : = \ : 9 . 8 1 \mathrm { m / s ^ { 2 } }$ , $\mathbf { e } _ { 3 } = \left[ 0 \quad 0 \quad 1 \right] ^ { \top }$ . In eq. (3), the matrix $\mathbf { P } \in \mathbb { R } ^ { 6 \times 3 n }$ maps tension vectors of all $n$ MAVs in $\mathcal { T }$ to the wrench on the payload with force in $\mathcal { T }$ and moments in $\mathcal { L }$

$$
\mathbf {P} = \left[ \begin{array}{c c c c} \mathbf {I} _ {3 \times 3} & \mathbf {I} _ {3 \times 3} & \dots & \mathbf {I} _ {3 \times 3} \\ \hat {\rho} _ {1} \boldsymbol {R} _ {L} ^ {\top} & \hat {\rho} _ {2} \boldsymbol {R} _ {L} ^ {\top} & \dots & \hat {\rho} _ {n} \boldsymbol {R} _ {L} ^ {\top} \end{array} \right]. \tag {4}
$$

where $\mathbf { I } _ { 3 \times 3 } \in \mathbb { R } ^ { 3 \times 3 }$ is an identity matrix and the hat map $\hat { \cdot } : \mathbb { R } ^ { 3 } \to { \mathfrak { s o } } ( 3 )$ is defined such that $\pmb { \hat { a } } \mathbf { b } = \pmb { a } \times \mathbf { b } , \forall \pmb { a } , \mathbf { b } \in \mathbb { R } ^ { 3 }$ .

By inspecting the matrix $\mathbf { P }$ , we observe that $\mathbf { P }$ has 6 rows, independent of the number of robots in the system. For $n \geq 3$ robots, the number of columns of $\mathbf { P }$ surpasses the number of rows, causing the dimension of the domain of $\mathbf { P }$ to exceed that of its image. Hence, there is an additional nullity in matrix $\mathbf { P }$ , which can be represented by the null space of the matrix P, denoted as $\mathcal { N } ( \mathbf { P } ) \subset \mathbb { R } ^ { 3 n - 6 }$ . The system can utilize the nullity to accomplish secondary tasks, such as obstacle avoidance, inter-robot separation, or keeping a distance between human and robot [58], which we will introduce in Section V.

Through standard rigid body dynamics, we can obtain the translational and rotational dynamics of the payload as

$$
m _ {L} \ddot {\mathbf {x}} _ {L} = \mathbf {F} _ {L}, \quad \mathbf {J} _ {L} \dot {\boldsymbol {\Omega}} _ {L} = \mathbf {M} _ {L} - \boldsymbol {\Omega} _ {L} \times \mathbf {J} _ {L} \boldsymbol {\Omega} _ {L}, \tag {5}
$$

where $\ddot { \bf x } _ { L } , \dot { \pmb \Omega } _ { L } \in \mathbb { R } ^ { 3 }$ is the payload linear and angular acceleration respectively, $\Omega _ { L } \ \in \ \mathbb { R } ^ { 3 }$ is the payload angular velocity and $\mathbf { J } _ { L } \in \mathbb { R } ^ { 3 \times 3 }$ is the payload’s inertia matrix.

# C. Quadrotor Dynamics

Based on assumptions 2 and 3, we consider the translational and rotational dynamics of the $k ^ { t h }$ quadrotor as follows

$$
m _ {k} \ddot {\mathbf {x}} _ {k} = \mathbf {u} _ {k} - \boldsymbol {\mu} _ {k} - m _ {k} \mathbf {g}, \tag {6}
$$

$$
\mathbf {J} _ {k} \hat {\boldsymbol {\Omega}} _ {k} = \mathbf {M} _ {k} - \boldsymbol {\Omega} _ {k} \times \mathbf {J} _ {k} \boldsymbol {\Omega} _ {k}, \tag {7}
$$

where $\mathbf { u } _ { k }$ and ${ { \bf { M } } _ { k } }$ are the control force and moment on the $k ^ { t h }$ quadrotor, $\pmb { \mu _ { k } } = - \mu _ { k } \pmb { \xi } _ { k }$ is the tension force applied on the $k ^ { t h }$ quadrotor.

When the cable is taut, the motion of $k ^ { t h }$ quadrotor is constrained to the surface of a sphere centered at the $k ^ { t h }$ attach point, with a radius equal to the cable length [42]. The dynamics of the cable direction can then be derived using the Lagrange d’Alembert principle as follows [9]:

$$
\ddot {\boldsymbol {\xi}} _ {k} = \frac {1}{m _ {k} l _ {k}} \hat {\boldsymbol {\xi}} _ {k} ^ {2} \left(\mathbf {u} _ {k} - m _ {k} \mathbf {a} _ {k}\right) - \left\| \dot {\boldsymbol {\xi}} _ {k} \right\| _ {2} ^ {2} \boldsymbol {\xi} _ {k}, \tag {8}
$$

where $\mathbf { \delta } _ { \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } } \mathbf { \alpha } _ { \mathbf { \alpha } \mathbf { \beta } \mathbf { \alpha } \mathbf { \alpha } \mathbf { \alpha } } \mathbf { \alpha } _ { \mathrm { ~ \mathrm { ~  ~ } \alpha ~ } }$ is the acceleration of the $k ^ { t h }$ attachment point

$$
\boldsymbol {a} _ {k} = \ddot {\mathbf {x}} _ {L} + \mathbf {g} - \boldsymbol {R} _ {L} \hat {\rho} _ {k} \hat {\Omega} _ {L} + \boldsymbol {R} _ {L} \hat {\Omega} _ {L} ^ {2} \rho_ {k}. \tag {9}
$$

# V. CONTROL

In this section, we introduce a hierarchical nonlinear controller that enables a team of $n$ quadrotors to manipulate a rigid-body load suspended by cables. The formulation of the controller is based on the system dynamics presented in Section IV. Fig. 3 illustrates the hierarchical structure of the controller.

The hierarchy begins with a payload controller, detailed in Section V-A, which generates the desired wrenches $\mathbf { F } _ { L , d e s } , \mathbf { M } _ { L , d e s }$ to control the position and orientation of the payload. Subsequently, the dynamic force distribution module, described in Section V-B, assigns desired cable force vectors $\mu _ { k } , k = 1 , \cdot \cdot \cdot , n$ for each robot, based on the desired payload wrench $\mathbf { F } _ { L , d e s } , \mathbf { M } _ { L , d e s }$ . The control hierarchy finishes with the robot controller at its lowest level, where the individual robot controller on each robot tracks its corresponding desired cable force vector $\mu _ { k }$ . Each robot controller, associated with the $k ^ { t h }$ robot, computes the appropriate thrust and moment commands for the robot, as further shown in Section V-C.

# A. Payload Controller

We present a payload controller that enables the load to follow the desired trajectory in a closed loop. The subscript $\ast _ { d e s }$ denotes the desired value given by the trajectory planner. The desired forces and moments acting on the payload are designed as

$$
\mathbf {F} _ {L, d e s} = m _ {L} \boldsymbol {a} _ {L, c}, \tag {10}
$$

$$
\boldsymbol {a} _ {L, c} = \mathbf {K} _ {p} \mathbf {e} _ {\mathbf {x} _ {L}} + \mathbf {K} _ {d} \mathbf {e} _ {\dot {\mathbf {x}} _ {L}} + \mathbf {K} _ {i} \int_ {0} ^ {t} \mathbf {e} _ {\mathbf {x} _ {L}} d \tau + \ddot {\mathbf {x}} _ {L, d e s} + \mathbf {g},
$$

$$
\begin{array}{l} \mathbf {M} _ {L, d e s} = \mathbf {K} _ {R _ {L}} \mathbf {e} _ {R _ {L}} + \mathbf {K} _ {\Omega_ {L}} \mathbf {e} _ {\Omega_ {L}} + \mathbf {J} _ {L} R _ {L} ^ {\top} R _ {L, d e s} \dot {\boldsymbol {\Omega}} _ {L, d e s} \\ + \left(\boldsymbol {R} _ {L} ^ {\top} \boldsymbol {R} _ {L, d e s} \boldsymbol {\Omega} _ {L, d e s}\right) ^ {\wedge} \mathbf {J} _ {L} \boldsymbol {R} _ {L} ^ {\top} \boldsymbol {R} _ {L, d e s} \boldsymbol {\Omega} _ {L, d e s}, \tag {11} \\ \end{array}
$$

where ${ \bf K } _ { p } , { \bf K } _ { d } , { \bf K } _ { i }$ ${ \bf K } _ { p } , { \bf K } _ { d } , { \bf K } _ { i } , { \bf K } _ { R _ { L } } , { \bf K } _ { \Omega _ { L } } \in \mathbb { R } ^ { 3 \times 3 }$ are constant diagonal positive definite matrices, and

$$
\mathbf {e} _ {\mathbf {x} _ {L}} = \mathbf {x} _ {L, d e s} - \mathbf {x} _ {L}, \mathbf {e} _ {\dot {\mathbf {x}} _ {L}} = \dot {\mathbf {x}} _ {L, d e s} - \dot {\mathbf {x}} _ {L},
$$

$$
\mathbf {e} _ {\boldsymbol {R} _ {L}} = \frac {1}{2} \left(\boldsymbol {R} _ {L} ^ {\top} \boldsymbol {R} _ {L, d e s} - \boldsymbol {R} _ {L, d e s} ^ {\top} \boldsymbol {R} _ {L}\right) ^ {\vee}, \tag {12}
$$

$$
\mathbf {e} _ {\Omega_ {L}} = \boldsymbol {R} _ {L} ^ {\top} \boldsymbol {R} _ {L, d e s} \boldsymbol {\Omega} _ {L, d e s} - \boldsymbol {\Omega} _ {L}.
$$

In the above equation, the vee map $\textsf { V } : { \mathfrak { s o } } ( 3 ) \to \mathbb { R } ^ { 3 }$ is the reverse of the hat map ˆ·.

# B. Dynamic Force Distribution

In this section, we will present our dynamic force distribution method that allocates the desired force ${ \bf F } _ { L , d e s }$ and moment ${ \mathbf { M } } _ { L , d e s }$ on the payload to the desired cable tension forces $\mu _ { k } , k = 1 , \cdot \cdot \cdot , n$ . The force distribution comprises two segments: the nominal force distribution and the human-aware force distribution.

The nominal force distribution, originated from nonlinear geometric control method [9], [11], distributes the desired

payload wrench to the desired cable tension forces using minimum norm solution.

On the other hand, the human-aware force distribution leverages the system redundancy, given that the robot number $n \geq 3$ , to obtain the cable forces that yield a zero effective wrench on the payload. This adjustment enables the system to modify the desired cable forces from the nominal distribution for secondary objectives, such as maintaining a distance from the robots to the human operator and between the robots themselves, without impacting the original manipulation tasks.

In the following, we will first present the nominal force distribution method in Section V-B1, followed by the humanaware force distribution method in Section V-B2.

1) Nominal Force Distribution: Once the desired payload wrench ${ \bf F } _ { L , d e s }$ , ${ \mathbf { M } } _ { L , d e s }$ is obtained, it can be distributed to the desired tension force $\bar { \mu } _ { k , d e s }$ along each cable as

$$
\bar {\boldsymbol {\mu}} _ {d e s} = \left[ \begin{array}{c} \bar {\boldsymbol {\mu}} _ {1, d e s} \\ \vdots \\ \bar {\boldsymbol {\mu}} _ {n, d e s} \end{array} \right] = \mathbf {P} ^ {\dagger} \left[ \begin{array}{c} \mathbf {F} _ {L, d e s} \\ \mathbf {M} _ {L, d e s} \end{array} \right], \tag {13}
$$

where $\mathbf { P } ^ { \dagger } = \mathbf { P } ^ { \top } ( \mathbf { P } \mathbf { P } ^ { \top } ) ^ { - 1 }$ is the Moore-Penrose inverse of P. The above solution can be directly used as the desired cable tension vector for the robot, like in our previous works [9], [11]. However, the above solution does not exploit the possibility of the quadrotor team’s needs to accomplish secondary tasks. For example, the second task can be avoiding obstacles or, as shown in this paper, spatially separating the human and the robots during physical collaboration.

2) Human-Aware Force Distribution: As we have mentioned before, the human-aware force distribution exploits the system redundancy to modify the desired cable forces from the nominal distribution for secondary tasks. The secondary tasks can be maintaining a distance from the robots to the human operator and between the robots themselves, without impacting the original manipulation tasks.

To accomplish these, we propose and discuss two distinct approaches in this section. The system aims to allocate the wrench to the desired cable tension forces with two principal goals in mind:

1) Minimize the total cable tension forces to conserve the robot’s energy.   
2) Utilize the null space of the cable distribution matrix $\mathbf { P }$ to facilitate secondary tasks, such as ensuring a safety distance between the robots and potential human operators within the team.

In the following, we introduce two methods enabling each MAV to maintain distance from an object. Concurrently, these methods allow the team to maintain the original desired load forces, ${ \bf F } _ { L , d e s }$ , and moments, ${ \mathbf { M } } _ { L , d e s }$ , as outlined in Section V-A. This approach ensures that the original objectives in load manipulation are not compromised.

The methods leverage the redundancy inherent in system configurations involving more than three MAVs, as explained in Section IV. We intend to find a desired tension force modifier, $\tilde { \mu } _ { d e s } \in \mathcal { N } ( \mathbf { P } )$ , that modifies $\bar { \mu } _ { d e s }$ in eq. (13), and

satisfies

$$
\mathbf {P} \tilde {\boldsymbol {\mu}} _ {d e s} = \mathbf {0}, \quad \tilde {\boldsymbol {\mu}} _ {d e s} = \left[ \begin{array}{c} \tilde {\boldsymbol {\mu}} _ {1, d e s} \\ \vdots \\ \tilde {\boldsymbol {\mu}} _ {n, d e s} \end{array} \right]. \tag {14}
$$

Eq. (14) means the tension modifiers result in zero wrench on the payload, which doesn’t affect the original desired manipulation wrench from eqs. (10) and (11). With the tension force modifier, we can update $k ^ { t h }$ robot’s desired cable tension force as

$$
\boldsymbol {\mu} _ {k, d e s} = \tilde {\boldsymbol {\mu}} _ {k, d e s} + \tilde {\boldsymbol {\mu}} _ {k, d e s}. \tag {15}
$$

Intuitively, $\mathcal { N } ( \mathbf { P } )$ provides all the possible combinations of $n$ cable tension vectors that can generate internal motions of the structure (i.e., variations of the cables’ directions) that do not affect the load configuration controlled by the method presented in Section V-A. This is confirmed by eq. (3) and eq. (15), as $\bar { \mu } _ { k , d e s }$ would create a nonzero net wrench on the payload while $\tilde { \mu } _ { k , d e s }$ creates zero net wrench. Moreover, $\tilde { \mu } _ { k , d e s }$ can be related to the position of each robot

$$
\mathbf {p} _ {a t t, k} + l _ {k} \tilde {\xi} _ {k, d e s} = \mathbf {x} _ {k}, \tag {16}
$$

and

$$
\tilde {\boldsymbol {\xi}} _ {k, d e s} = - \boldsymbol {\xi} _ {k, d e s} = \frac {\bar {\boldsymbol {\mu}} _ {k , d e s} + \tilde {\boldsymbol {\mu}} _ {k , d e s}}{\| \bar {\boldsymbol {\mu}} _ {k , d e s} + \tilde {\boldsymbol {\mu}} _ {k , d e s} \|}. \tag {17}
$$

The advantage is that we can exploit $\tilde { \mu } _ { k , d e s }$ to enforce the $k ^ { t h }$ robot to maintain a certain distance with respect to the other agents in the system and other objects in the environments, like a potential human operator.

Therefore, the human-aware force distribution needs to find the aforementioned tension force modifier, $\tilde { \mu } _ { d e s } \in \mathcal { N } ( \mathbf { P } )$ , and use eq. (15) to move MAVs based on eq. (16) without affecting the payload. We propose the following two approaches for finding µ˜des $\tilde { \mu } _ { d e s }$

1) Gradient-Based Method: Find a $\tilde { \mu } _ { d e s }$ such that each MAV maximizes the distance between itself and the object using a gradient ascent method.   
2) Optimization-Based Method: Find a $\tilde { \mu } _ { d e s }$ such that each MAV guarantees a predetermined minimal safe distance between all its neighboring drones and the object by using nonlinear optimization.

In the following, we can describe the obstacle or human operator as a particular object of interest in the environment. The corresponding point position with respect to $\mathcal { T }$ is denoted as $\mathbf { p } _ { O }$ in the following controller formulation.

Gradient-Based Method: Inspired by strategies used for redundant rigid link robot arms in [59], we introduce a gradient-based method to compute $\tilde { \mu } _ { d e s }$ . Specifically, a pseudo tension force modifier, $\mu _ { d e s } ^ { 0 }$ , is found by maximizing the distance between objects in the environment and each drone. $\mu _ { d e s } ^ { 0 }$ is then projected into $\mathcal { N } ( \mathbf { P } )$ to become the tension force modifier $\tilde { \mu } _ { d e s }$ . To update $\mu _ { d e s } ^ { 0 }$ , we propose

$$
\boldsymbol {\mu} _ {d e s} ^ {0} = \mathbf {Q} \frac {\partial \mathbf {w} (\tilde {\boldsymbol {\mu}} _ {d e s})}{\partial \tilde {\boldsymbol {\mu}} _ {d e s}}, \tag {18}
$$

where $\mathbf { Q } \in \mathbb { R } ^ { 3 n \times 3 n }$ is a diagonal positive-definite matrix with variable and tunable coefficients on its diagonal, and $\mathbf { w } ( \tilde { \pmb { \mu } } _ { d e s } )$ is the cost function. $\mathbf { w } ( \tilde { \pmb { \mu } } _ { d e s } )$ is defined as the squared distance

between each drone and the object from which the system is required to keep a safe distance as follow

$$
\mathbf {w} \left(\tilde {\boldsymbol {\mu}} _ {d e s}\right) = \sum_ {i = 1} ^ {k} \left\| \mathbf {p} _ {O} - \left(\mathbf {p} _ {a t t, k} + \mathbf {l} _ {k} \tilde {\boldsymbol {\xi}} _ {k, d e s}\right) \right\| ^ {2}, \tag {19}
$$

where $\mathbf { l } _ { k } ~ = ~ l _ { k } \mathbf { I } _ { 3 \times 3 }$ . Note that $\tilde { \xi } _ { k , d e s }$ points from the $k ^ { t h }$ attach point to the $k ^ { t h }$ robot. We can now compute the partial derivative of the cost function corresponding to the $k ^ { t h }$ robot by using eq. (19) and obtain the following:

$$
\begin{array}{l} \frac {\partial \mathbf {w} (\tilde {\boldsymbol {\mu}} _ {k , d e s})}{\partial \tilde {\boldsymbol {\mu}} _ {k , d e s}} = - 2 \mathbf {l} _ {k} [ \mathbf {p} _ {O} - \mathbf {p} _ {a t t, k} ] ^ {\top} \frac {\partial \tilde {\boldsymbol {\xi}} _ {d e s}}{\partial \tilde {\boldsymbol {\mu}} _ {k , d e s}} \\ = - 2 \mathbf {l} _ {k} \left[ \mathbf {p} _ {O} - \mathbf {p} _ {a t t, k} \right] ^ {\top} \frac {\left(\mathbf {I} _ {3 \times 3} - \tilde {\boldsymbol {\xi}} _ {k , d e s} \tilde {\boldsymbol {\xi}} _ {k , d e s} ^ {\top}\right)}{\| \tilde {\boldsymbol {\mu}} _ {k , d e s} + \tilde {\boldsymbol {\mu}} _ {k , d e s} \|}. \tag {20} \\ \end{array}
$$

For each control step, we update $\mu _ { d e s } ^ { 0 }$ based on eq. (18), performing gradient ascent to maximize the distance between each robot and the objects in the environment. To regulate the effect of gradient on each robot when the object is far away, we propose each element of $\mathbf { Q }$ as an exponential decay function of the robot-to-object distance

$$
\mathbf {Q} = \operatorname {d i a g} \left(\mathbf {Q} _ {1}, \dots , \mathbf {Q} _ {n}\right), \quad \mathbf {Q} _ {k} = a e ^ {- b \| \mathbf {p} _ {O} - \mathbf {x} _ {k} \|} \mathbf {I} _ {3 \times 3}, \tag {21}
$$

where, $a , b \in \mathbb { R }$ are tunable coefficients. With these varying coefficients, we can implicitly impose distance limits as the gradients will only have impact on the tension modification when $k ^ { t h }$ robot is close enough to the object. However, till now, $\mu _ { d e s } ^ { 0 }$ from eq. (18) is not yet in $\mathcal { N } ( \mathbf { P } )$ . Hence we consider the following optimization to project $\mu _ { d e s } ^ { 0 }$ into the null space of the matrix $\mathbf { P }$

$$
\begin{array}{l} \min  _ {\boldsymbol {\mu} _ {\bar {d e s}}} \left\| \boldsymbol {\mu} _ {d e s} ^ {0} - \tilde {\boldsymbol {\mu}} _ {d e s} \right\| ^ {2} \tag {22} \\ \begin{array}{l l} \text {s . t .} & \mathbf {P} \tilde {\boldsymbol {\mu}} _ {d e s} = 0. \end{array} \\ \end{array}
$$

Since the above optimization problem is a quadratic programming problem with linear equality constraints, there is a closed-form solution shown as follows [60]

$$
\tilde {\boldsymbol {\mu}} _ {d e s} = \mathbf {B} \boldsymbol {\mu} _ {d e s} ^ {0} = \left(\boldsymbol {I} - \mathbf {P} ^ {\dagger} \mathbf {P}\right) \boldsymbol {\mu} _ {d e s} ^ {0}, \tag {23}
$$

orthogonal projector that projects any where $\mathbf { P } ^ { \dagger }$ is the pseudoinverse as in eq. (13), and $\mu _ { d e s } ^ { 0 }$ orthogonally into $\mathbf { B }$ is an the null space of $\mathbf { P }$ .

Using this result, we project $\mu ^ { 0 }$ into $\mathcal { N } ( \mathbf { P } )$ with eq. (23), ensuring zero additional wrenches being applied on the payload when each robot is maximizing distance from the object. Finally, we update the desired tension vector as

$$
\boldsymbol {\mu} _ {d e s} = \bar {\boldsymbol {\mu}} _ {d e s} + \tilde {\boldsymbol {\mu}} _ {d e s} = \bar {\boldsymbol {\mu}} _ {d e s} + \mathbf {B} \boldsymbol {\mu} _ {d e s} ^ {0}. \tag {24}
$$

Optimization-Based Method: In this section, we directly formulate an optimization problem to solve for a tension force modifier $\tilde { \mu } _ { d e s }$ in $\mathcal { N } ( \mathbf { P } )$ that guarantees safety distance among the objects and the robots. The nonlinear optimization problem is to minimize the total square norm of the resulting cable tension vector. Furthermore, we formulate $n$ robot-to-object distance constraints, as well as another $\textstyle { { \binom { n } { 2 } } = { \frac { n ( n - 1 ) } { 2 } } }$ constraints are added to prevent each pair of robots from collision.

Consider the following nonlinear optimization problem

$$
\min _ {\mathbf {c}} \quad \| \bar {\boldsymbol {\mu}} _ {d e s} + \mathbf {N} \boldsymbol {\Lambda} \| ^ {2}
$$

$$
\text {s . t .} \quad \| \mathbf {p} _ {O} - \mathbf {x} _ {k} \| ^ {2} \geq^ {\mathrm {h}} r ^ {2}, \quad 0 <   k \leq n, \tag {25}
$$

$$
\left\| \mathbf {x} _ {i} - \mathbf {x} _ {j} \right\| ^ {2} \geq^ {\mathrm {r}} r ^ {2}, \quad 0 <   i <   j \leq n,
$$

where the columns of $\mathbf { N }$ spans $\mathcal { N } ( \mathbf { P } )$ and $\mathbf { c } \in \mathbb { R } ^ { 3 n - 6 }$ is the vector to be optimized. $^ { \mathrm { r } } r$ and $\mathrm { h } _ { r }$ are two scalar values denoting the predetermined safe minimum distance allowed between robots and between the object and each robot, respectively. The $k ^ { t h }$ robot’s position is expressed in terms of ${ \bf N } _ { k } \Lambda$ and µ¯ k,des $\bar { \mu } _ { k , d e s }$

$$
\mathbf {x} _ {k} = \mathbf {p} _ {a t t, k} + l _ {k} \frac {\bar {\boldsymbol {\mu}} _ {k , d e s} + \mathbf {N} _ {k} \boldsymbol {\Lambda}}{\| \bar {\boldsymbol {\mu}} _ {k , d e s} + \mathbf {N} _ {k} \boldsymbol {\Lambda} \|}, \tag {26}
$$

where ${ \bf N } _ { k }$ represents the three rows from the $k ^ { t h }$ row to the $k + 2 ^ { t h }$ row of the null space basis matrix N, which corresponds to the $k ^ { t h }$ MAV. Since eq. (25) is a nonlinear optimization problem with quadratic cost function and quadratic constraints, we use sequential quadratic programming solver for nonlinearly constrained gradient-based optimization [61] in NLOPT [62] to solve eq. (25) and obtain c. After obtaining c, the desired cable tension forces can be obtained as follows

$$
\boldsymbol {\mu} _ {d e s} = \bar {\boldsymbol {\mu}} _ {d e s} + \tilde {\boldsymbol {\mu}} _ {d e s} = \bar {\boldsymbol {\mu}} _ {d e s} + \mathbf {N} \boldsymbol {\Lambda}. \tag {27}
$$

Discussion: The proposed methods are both effective for the quadrotor team to keep a safe distance away from a given object, as we also experimentally verify in Section VII. However, considering computational aspects, the gradient-based method requires fewer resources compared to the optimization-based method. This is primarily due to the closed-form solution offered by the gradient-based approach, as demonstrated by eq. (20). On the other hand, the optimization-based method needs to solve a nonlinear optimization problem. In Section VIII, we provide a quantitative analysis of the computational complexity and resource usage for both methods based on our implementation.

# C. Robot Controller

In this section, we present the controller on each robot that enables the quadrotor to execute the desired cable tension force. The same robot controller has been used in our previous works [9], [11].

Once we obtain the desired tension forces $\mu _ { d e s }$ from eq. (24) or eq. (27), we can obtain the desired direction $\xi _ { k , d e s }$ and the desired angular velocity $\omega _ { k , d e s }$ of the $k ^ { t h }$ cable link as

$$
\boldsymbol {\xi} _ {k, d e s} = - \frac {\boldsymbol {\mu} _ {k , d e s}}{\| \boldsymbol {\mu} _ {k , d e s} \|}, \omega_ {k, d e s} = \boldsymbol {\xi} _ {k, d e s} \times \dot {\boldsymbol {\xi}} _ {k, d e s},
$$

where $\dot { \xi } _ { k , d e s }$ is the derivative of the desired cable direction $\xi _ { k , d e s }$ . After we obtain the desired cable direction $\xi _ { k , d e s }$ and cable angular velocity $\omega _ { k , d e s }$ , we can determine the desired

force vector for the robot $\mathbf { u } _ { k }$ as

$$
\mathbf {u} _ {k} = \mathbf {u} _ {k} ^ {\parallel} + \mathbf {u} _ {k} ^ {\perp},
$$

$$
\begin{array}{l} \mathbf {u} _ {k} ^ {\perp} = m _ {k} l _ {k} \boldsymbol {\xi} _ {k} \times \left[ - \mathbf {K} _ {\boldsymbol {\xi} _ {k}} \mathbf {e} _ {\boldsymbol {\xi} _ {k}} - \mathbf {K} _ {\boldsymbol {\omega} _ {k}} \mathbf {e} _ {\boldsymbol {\omega} _ {k}} - \hat {\boldsymbol {\xi}} _ {k} ^ {2} \boldsymbol {\omega} _ {k, d e s} \right. \\ \left. - \left(\boldsymbol {\xi} _ {k} \cdot \boldsymbol {\omega} _ {k, d e s}\right) \dot {\boldsymbol {\xi}} _ {k, d e s} \right] - m _ {k} \hat {\boldsymbol {\xi}} _ {k} ^ {2} \boldsymbol {a} _ {k, c}, \tag {28} \\ \end{array}
$$

$$
\mathbf {u} _ {k} ^ {\parallel} = \boldsymbol {\xi} _ {k} \boldsymbol {\xi} _ {k} ^ {\top} \boldsymbol {\mu} _ {k, d e s} + m _ {k} l _ {k} \| \omega_ {k} \| _ {2} ^ {2} \boldsymbol {\xi} _ {k} + m _ {k} \boldsymbol {\xi} _ {k} \boldsymbol {\xi} _ {k} ^ {\top} \boldsymbol {a} _ {k, c},
$$

$$
\boldsymbol {a} _ {k, c} = \boldsymbol {a} _ {L, c} - \boldsymbol {R} _ {L} \hat {\rho} _ {k} \dot {\boldsymbol {\Omega}} _ {L} + \boldsymbol {R} _ {L} \hat {\boldsymbol {\Omega}} _ {L} ^ {2} \rho_ {k},
$$

where $\mathbf { K } _ { \xi _ { k } }$ and $\mathbf { K } _ { \omega _ { k } } \in \mathbb { R } ^ { 3 \times 3 }$ are constant diagonal positive definite matrices, $\mathbf { e } _ { \xi _ { k } }$ and $\mathbf { e } _ { \omega _ { k } } \in \mathbb { R } ^ { 3 }$ are the cable direction and cable angular velocity errors respectively

$$
\mathbf {e} _ {\boldsymbol {\xi} _ {k}} = \boldsymbol {\xi} _ {k, d e s} \times \boldsymbol {\xi} _ {k}, \quad \mathbf {e} _ {\boldsymbol {\omega} _ {k}} = \boldsymbol {\omega} _ {k} + \boldsymbol {\xi} _ {k} \times \boldsymbol {\xi} _ {k} \times \boldsymbol {\omega} _ {k, d e s}.
$$

As we obtain the desired force vector of the quadrotor from eq. (28), we can follow [63] to derive the desired rotation $R _ { k , d e s }$ and angular velocity $\Omega _ { k , d e s }$ with desired yaw angle and desired yaw angular velocity from the robot’s own planner. The thrust command $f _ { k }$ and moment command ${ { \bf { M } } _ { k } }$ to the $k ^ { t h }$ quadrotor are therefore selected as

$$
\begin{array}{l} f _ {k} = \mathbf {u} _ {k} \cdot \boldsymbol {R} _ {k} \mathbf {e} _ {3}, (29) \\ \mathbf {M} _ {k} = \mathbf {K} _ {R} \mathbf {e} _ {R _ {k}} + \mathbf {K} _ {\Omega} \mathbf {e} _ {\Omega_ {k}} + \boldsymbol {\Omega} _ {k} \times \mathbf {J} _ {k} \boldsymbol {\Omega} _ {k} (30) \\ - \mathbf {J} _ {k} \left(\hat {\boldsymbol {\Omega}} _ {k} \mathbf {R} _ {k} ^ {\top} \mathbf {R} _ {k, d e s} \mathbf {\Omega} _ {k, d e s} - \mathbf {R} _ {k} ^ {\top} \mathbf {R} _ {k, d e s} \dot {\mathbf {\Omega}} _ {k, d e s}\right), \\ \end{array}
$$

where $\mathbf { K } _ { R }$ , $\mathbf { K } _ { \Omega } \in \mathbb { R } ^ { 3 \times 3 }$ are constant diagonal positive definite matrices, ${ \bf e } _ { R _ { k } } \in \mathbb { R } ^ { 3 }$ and $\mathbf { e } _ { \Omega _ { k } } \ \in \ \mathbb { R } ^ { 3 }$ are the orientation and angular velocity errors similarly defined using eq. (12). The readers can refer to [42] for stability analysis of the controller.

# VI. PHYSICAL HUMAN-ROBOT INTERACTION

This section introduces the physical human-robot interaction module that enables a human operator to physically cooperate with a team of $n$ quadrotors in manipulating a suspended rigidbody payload. The module comprises two main sub-blocks: the estimation module and the admittance controller.

The estimation module is designed to facilitate the quadrotor team in estimating the human operator’s input wrench exerted on the payload. The admittance controller takes the estimated human wrench and the desired payload state as input and generates a desired payload state to adapt the human’s action.

# A. Estimation

We present the estimator design that allows the quadrotor team to estimate the external wrench applied to the payload by the human operator. First, in Section VI-A1, we introduce a quadrotor state estimator based on Unscented Kalman Filter (UKF) that runs onboard each quadrotor in a distributed fashion. Each quadrotor can leverage the estimator to estimate the cable force applied to it, without the need for a force sensor. Subsequently, in Section VI-A2, we show how we can estimate the external wrench applied on the payload by the human operator via sharing the cable force on each quadrotor among the team.

1) Robot State Estimation: We consider the $k ^ { t h }$ MAV to have the following state $\mathbf { S } _ { k }$

$$
\mathbf {S} _ {k} = \left[ \begin{array}{l l l l l l l} \mathbf {x} _ {k} ^ {\top} & \dot {\mathbf {x}} _ {k} ^ {\top} & \boldsymbol {\Theta} _ {k} ^ {\top} & \boldsymbol {\Omega} _ {k} ^ {\top} & \boldsymbol {\xi} _ {k} & \dot {\boldsymbol {\xi}} _ {k} ^ {\top} & \mu_ {k} \end{array} \right] ^ {\top}, \tag {31}
$$

where $\Theta _ { k } \in \mathbb { R } ^ { 3 }$ is a vector of the 3 Euler angles expressed according to the ZYX convention representing the robot’s orientation. And the input is defined as

$$
\mathbf {U} _ {k} = \left[ \begin{array}{l l} f _ {k} & \mathbf {M} _ {k} ^ {\top} \end{array} \right] ^ {\top}, \tag {32}
$$

where $f _ { k }$ and ${ { \bf { M } } _ { k } }$ are obtained based on motor speed measured by the electronic speed controllers on the robot. The relationship between motor speed and the resultant thrust and moment is expressed as follows:

$$
\left[ \begin{array}{l} f _ {k} \\ \mathbf {M} _ {k} \end{array} \right] = \left[ \begin{array}{c c c c} k _ {f} & k _ {f} & k _ {f} & k _ {f} \\ d _ {x} k _ {f} & d _ {x} k _ {f} & - d _ {x} k _ {f} & - d _ {x} k _ {f} \\ - d _ {y} k _ {f} & d _ {y} k _ {f} & d _ {y} k _ {f} & - d _ {y} k _ {f} \\ k _ {m} & - k _ {m} & k _ {m} & - k _ {m} \end{array} \right] \left[ \begin{array}{l} \omega_ {m 1} ^ {2} \\ \omega_ {m 2} ^ {2} \\ \omega_ {m 3} ^ {2} \\ \omega_ {m 4} ^ {2} \end{array} \right] \tag {33}
$$

where $k _ { f }$ and $k _ { m }$ represent the motor constants corresponding to rotor force and moment, respectively. $d _ { x }$ and $d _ { y }$ denote the distances from the rotor to the body’s $\mathbf { X }$ and y axes. Additionally, $\omega _ { m j }$ signifies the motor speed of the $j ^ { t h }$ motor. We denote the current time step as $* ^ { t }$ and the previous time step as $* ^ { t - 1 }$ . Subsequently, we present the nonlinear process model and the linear measurement model of the Unscented Kalman Filter (UKF).

a) Process Model: Based on MAV equations of motion presented in eq. (7), discretizations of quadrotor states are performed by assuming each control step moves forward in time by $\delta t$ . The discrete-time nonlinear process model is

$$
\mathbf {S} _ {k} ^ {t} = g \left(\mathbf {S} _ {k} ^ {t - 1}, \mathbf {U} _ {k} ^ {t}\right) = \left[ \begin{array}{c} \mathbf {x} _ {k} ^ {t} \\ \dot {\mathbf {x}} _ {k} ^ {t} \\ \boldsymbol {\Theta} _ {k} ^ {t} \\ \boldsymbol {\Omega} _ {k} ^ {t} \\ \boldsymbol {\xi} _ {k} ^ {t} \\ \dot {\boldsymbol {\xi}} _ {k} ^ {t} \\ \mu_ {k} ^ {t} \end{array} \right] = \left[ \begin{array}{c} \mathbf {x} _ {k} ^ {t - 1} + \dot {\mathbf {x}} _ {k} ^ {t - 1} \delta t + \ddot {\mathbf {x}} _ {k} ^ {t} \frac {\delta t ^ {2}}{2} \\ \dot {\mathbf {x}} _ {k} ^ {t - 1} + \ddot {\mathbf {x}} _ {k} ^ {t} \delta t \\ \left\lfloor R _ {k} ^ {t - 1} \exp \left[ R _ {k} ^ {t - 1} \boldsymbol {\Omega} _ {k} ^ {t - 1} \delta t \right] \right\rfloor \\ \boldsymbol {\Omega} _ {k} ^ {t - 1} + \dot {\boldsymbol {\Omega}} _ {k} ^ {t} \delta t \\ \boldsymbol {\xi} _ {k} ^ {t - 1} + \dot {\boldsymbol {\xi}} _ {k} ^ {t} \delta t + \ddot {\boldsymbol {\xi}} _ {k} ^ {t} \frac {\delta t ^ {2}}{2} \\ \dot {\boldsymbol {\xi}} _ {k} ^ {t - 1} + \ddot {\boldsymbol {\xi}} _ {k} ^ {t} \delta t \\ \mu_ {k} ^ {t - 1} \end{array} \right]. \tag {34}
$$

For updating the Euler angles, a few nonlinear mappings are used as in [64]

1) $\lfloor * \rfloor$ that maps $* \in S O ( 3 )$ to $\Theta \in \mathbb { R } ^ { 3 }$ .   
2) $\mathbf { e x p } [ * ]$ that maps $* \in \mathbb { R } ^ { 3 }$ to $S O ( 3 )$ ; or maps axis-angle $\mathfrak { s o } ( 3 )$ , to rotation matrix $S O ( 3 )$ .

In eq. (34), $\Omega _ { k } ^ { t - 1 }$ is rotated into $\mathcal { T }$ . After time step $\delta t$ the robot’s angular displacement in $\mathcal { T }$ , expressed in so(3) is mapped into $S O ( 3 )$ . This new robot orientation in $S O ( 3 )$ is then added to the previous orientation and the resultant orientation is converted to Euler angle using $\lfloor * \rfloor$ . The equations of motion for unit cable direction are provided in [11], with the results presented here

$$
\ddot {\boldsymbol {\xi}} _ {k} ^ {t} = \frac {\left(\hat {\boldsymbol {\xi}} _ {k} ^ {t - 1}\right) ^ {2} \left(\mathbf {u} _ {k} - m _ {k} \boldsymbol {a} _ {k}\right)}{m _ {k} l _ {k}} - \left\| \dot {\boldsymbol {\xi}} _ {k} ^ {t - 1} \right\| _ {2} ^ {2} \boldsymbol {\xi} _ {k} ^ {t - 1}. \tag {35}
$$

In our system, we employ a $1 6 \times 1 6$ time-invariant process noise diagonal covariance matrix, operating under the assumption that the system has zero-mean, additive Gaussian process noise. For the prediction phase, the Unscented Kalman Filter (UKF) algorithm utilizes eq. (34). It’s important to note that in instances where measurements are not available at every control time step, the UKF implements a nonlinear prediction method that assumes zero process noise.

b) Measurement Model: Using an indoor MOCAP system, we can measure everything in the state except tension magnitude. The measured states for $k ^ { t h }$ robot therefore are

$$
\mathbf {Z} _ {k} = \left[ \begin{array}{l l l l l l} \mathbf {x} _ {k} ^ {\top} & \dot {\mathbf {x}} _ {k} ^ {\top} & \boldsymbol {\Theta} _ {k} ^ {\top} & \boldsymbol {\Omega} _ {k} ^ {\top} & \boldsymbol {\xi} _ {k} ^ {\top} & \dot {\boldsymbol {\xi}} _ {k} ^ {\top} \end{array} \right] ^ {\top}. \tag {36}
$$

We also want to note that using onboard Visual Inertial Odometry and vision-based methods from our previous work [11] can provide the same measurements as the motion capture does and can potentially make the entire measurement update process run fully onboard. However, this is out of the scope of this paper and we refer to it as future works.

Denoting the time step when the UKF measurement update is triggered as $m$ , the UKF finds the state prior to m, $\mathbf { S } _ { k } ^ { m - 1 }$ . A nonlinear propagation through eq. (34) is performed by propagating sigma points around Sm−1k $\mathbf { S } _ { k } ^ { m - 1 }$ through the system model in eq. (34) as shown in [65].

The linear measurement model is

$$
\mathbf {H} = \left[ \begin{array}{c c} \mathbf {I} _ {1 8 \times 1 8} & \mathbf {0} _ {1 8 \times 1} \\ \mathbf {0} _ {1 \times 1 8} & \mathbf {0} _ {1 \times 1} \end{array} \right].
$$

The system state prediction is compared to the actual measurement using the above model

$$
\mathbf {S} _ {k} ^ {m} = \mathbf {K} _ {k} \left(\mathbf {H} \bar {\mathbf {S}} _ {k} ^ {m} - \mathbf {Z} _ {k}\right), \tag {37}
$$

where $\bar { \mathbf { S } } _ { k } ^ { m }$ is the averaged state after sigma point propagation and $\mathbf { K } _ { k }$ is the Kalman gain. Kalman gain is computed based on the standard UKF update step as in [65].

2) Human Wrench Estimation: Rearranging eq. (3), we obtain

$$
\left[ \begin{array}{c} m _ {L} \ddot {\mathbf {x}} _ {L} \\ \mathbf {J} _ {L} \dot {\boldsymbol {\Omega}} _ {L} \end{array} \right] = \left[ \begin{array}{c} \mathbf {F} _ {H} \\ \mathbf {M} _ {H} \end{array} \right] + \mathbf {P} \left[ \begin{array}{c} \boldsymbol {\mu} _ {1} \\ \vdots \\ \boldsymbol {\mu} _ {n} \end{array} \right] - \left[ \begin{array}{c} m \mathbf {g} \\ \mathbf {0} _ {3 \times 1} \end{array} \right]. \tag {38}
$$

Considering quasi-static operating conditions, we can assume the payload linear and angular acceleration terms can be neglected. Therefore, leveraging this assumption and rearranging based on eq. (38) we obtain

$$
\left[ \begin{array}{l} \mathbf {F} _ {H} \\ \mathbf {M} _ {H} \end{array} \right] = - \mathbf {P} \left[ \begin{array}{c} \boldsymbol {\mu} _ {1} \\ \vdots \\ \boldsymbol {\mu} _ {n} \end{array} \right] + \left[ \begin{array}{l} m \mathbf {g} \\ \mathbf {0} _ {3 \times 1} \end{array} \right]. \tag {39}
$$

Extracting tension values from each robot’s state allows us to compute the external wrenches on the payload.

# B. Payload Admittance Controller

The admittance controller is a high-level controller that updates ${ \bf x } _ { L , d e s }$ and $R _ { L , d e s }$ in eq. (12) for the payload controller (Section V-A) based on the external force applied on the payload. When interacting with the payload, it allows the human operator to experience a virtual mass-spring-damper system rather than the actual mass. By setting the admittance controller’s tunable parameters to the desired values, the payload can be either sensitive or insensitive to external forces regardless of the payload’s actual property.

The admittance controller conceptualizes the payload as a virtual mass-spring-damper system, responding to external forces and moments from the human operator. It takes the external wrench, represented as $\begin{array} { r l } { [ \mathbf { F } _ { H } ^ { \top }  } & { { } \mathbf { \dot { M } } _ { H } ^ { \top } ] ^ { \top } \ \in \ \mathbb { R } ^ { 6 \times 1 } } \end{array}$ , as the input. The output from this controller includes the desired payload twist, denoted as $\dot { \mathcal { X } } _ { d e s } \in \mathbb { R } ^ { 6 \times 1 }$ , along with the desired

![](images/42c8b303d035cf6b3aa1361cbaa96edcd74aa12488eecd45ec1c4c29c3d8f9e9.jpg)  
Fig. 4: Wrench estimation evaluation. The human operator uses a force measurement device to measure the applied wrench on the payload, which is used to validate our wrench estimation algorithm results. On the left, we show the human operator applies force via the force measurement device, and, on the right, we show the force measurement device in detail.

linear and angular positions of the payload, $\mathcal { X } _ { d e s } ~ \in ~ \mathbb { R } ^ { 6 \times 1 }$ , where the angular position is expressed in Euler angles. Additionally, the admittance controller calculates the desired linear and angular accelerations, $\ddot { \mathcal { X } } _ { d e s } \in \mathbb { R } ^ { 6 \times 1 }$ . However, it is noteworthy that these acceleration outputs are not utilized by the lower-level payload controller.

The admittance controller assumes the following dynamics for the payload

$$
\begin{array}{l} \mathbf {M} \ddot {\mathbf {e}} _ {a d m} + \mathbf {D} \dot {\mathbf {e}} _ {a d m} + \mathbf {K} \mathbf {e} _ {a d m} = \left[ \begin{array}{c} \mathbf {F} _ {H} \\ \mathbf {M} _ {H} \end{array} \right], \\ \ddot {\mathbf {e}} _ {a d m} = \dddot {\mathcal {X}} _ {d e s} - \dddot {\mathcal {X}} _ {t r a j}, \quad \dot {\mathbf {e}} _ {a d m} = \dot {\mathcal {X}} _ {d e s} - \dot {\mathcal {X}} _ {t r a j}, \tag {40} \\ \end{array}
$$

$$
\mathbf {e} _ {a d m} = \mathcal {X} _ {d e s} - \mathcal {X} _ {t r a j},
$$

where M, D, and $\mathbf { K } \in \mathbb { R } ^ { 6 \times 6 }$ are tunable diagonal positive semidefinite matrices denoting the desired mass, damping, and spring property of the payload. Based on the initial starting condition of the payload, $\ddot { \mathcal X } _ { t r a j }$ , $\dot { \mathcal { X } } _ { t r a j }$ , and $\chi _ { t r a j }$ can be set accordingly. We choose to set them to be the planned trajectory. Closed-form solutions exist for eq. (40) with the assumption that the input wrench is a predetermined function (e.g., a linear function). However, such an assumption is not ideal for our use case. Therefore, we choose to solve $\mathcal { X } _ { d e s }$ , $\dot { \mathcal { X } } _ { d e s }$ , $\ddot { \mathcal { X } } _ { d e s }$ with Runge-Kutta $4 ^ { t h }$ order approximation.

# VII. EXPERIMENTAL RESULTS

The experiments are conducted in an indoor testbed with a flying space of $1 0 \times 6 \times 4 ~ \mathrm { m ^ { 3 } }$ of the ARPL lab at New York University. We use three quadrotors to carry a triangular payload via suspended cables. The quadrotor platform used in the experiments is equipped with a Qualcomm®SnapdragonTM 801 board for on-board computing [66]. A laptop equipped with an Intel i9-9900K CPU obtains the Vicon 1 motion capture system data via ethernet cable.

The framework has been developed in ${ \mathrm { R O S } } ^ { 2 }$ and the robots’ clocks are synchronized by Chrony3. The mass of the payload is $\mathrm { 3 1 0 ~ g }$ , which exceeds the payload capacity of every single vehicle. The pose and twist of the payload and quadrotors, the position and velocity of attachment points, and the human operator’s position are estimated using the Vicon data at a

1www.vicon.com   
2www.ros.org   
3https://chrony.tuxfamily.org/

![](images/cc812144393d33e43a8c9d92552befaa6f905a81c36b3983b0441604da994e7d.jpg)

![](images/11b8dd723efa1244e17cd8c8dc338e650bb799d159e51b5b3352c5a1942c3175.jpg)

![](images/22ce52d290e49eac4e1f370df834b13f39910dff2ef506e0c2255fb883b54849.jpg)  
Fig. 5: Cable force estimation experiment results. Comparison between the cable force estimation algorithm results and the force measurements from the force measurement device in all 3 DoF.

frequency of $1 0 0 ~ \mathrm { H z }$ . The unit vector of each cable direction $\xi _ { k }$ and the corresponding velocity $\dot { \xi } _ { k }$ are estimated by

$$
\boldsymbol {\xi} _ {k} = \frac {\mathbf {p} _ {a t t , k} - \mathbf {x} _ {k}}{\left\| \mathbf {p} _ {a t t , k} - \mathbf {x} _ {k} \right\|}, \quad \dot {\boldsymbol {\xi}} _ {k} = \frac {\dot {\mathbf {p}} _ {a t t , k} - \dot {\mathbf {x}} _ {k}}{l _ {k}}, \tag {41}
$$

where $\mathbf { p } _ { a t t , k } , \dot { \mathbf { p } } _ { a t t , k }$ are position and velocity of the $k ^ { t h }$ attach point in $\mathcal { T }$ and ${ \bf x } _ { k } , \dot { \bf x } _ { k }$ are position and velocity of the $k ^ { t h }$ robot in $\mathcal { T }$ , all of which are estimated by the motion capture system.

# A. Cable Force and External Wrench Estimation

In this section, we validate our cable force and external wrench estimation algorithm by comparing the estimation results obtained using the approach presented in Section VI-A2 with the ground truth from the wrench measurement device as shown in Fig. 4.

We can identify the ground truth force by measuring the force direction and force magnitude separately via the wrench measurement device. As the ground truth force direction is along the cable between the measurement device and the other end where the device is attached to the system, it is measured by computing the difference between the load cell’s position and the attach point position using the Vicon motion capture system. The ground truth force magnitude is measured via a Phidget micro load cell4 as shown in Fig. 4. The measured cable direction and tension magnitude are post-processed to obtain the ground truth force.

TABLE II: RMSE of wrench estimation and measurement.   

<table><tr><td rowspan="2"></td><td colspan="3">Force (N)</td><td colspan="3">Moment (N·m)</td></tr><tr><td>x</td><td>y</td><td>z</td><td>roll</td><td>pitch</td><td>yaw</td></tr><tr><td>Ours</td><td>0.0185</td><td>0.0117</td><td>0.0564</td><td>0.0088</td><td>0.0066</td><td>0.0045</td></tr><tr><td>[7]</td><td>0.0282</td><td>0.0164</td><td>0.0419</td><td>0.0148</td><td>0.0040</td><td>0.0120</td></tr></table>

![](images/538d0154e5b43d0bd6424a4698c73415aaebdbaff15a25ccfd98b0409b39f9d5.jpg)

![](images/046236c25358983600f823ef0f8d5c2fc8cc151d3575688ff84a16fe8c81ea1d.jpg)

![](images/a33ef275dd2bdc718a8e38c4dd9c9d2487744516f5629d8b2d702c71cd2d64b0.jpg)

![](images/6e814f8d123f51c72c0fe8473ff09823bb23146f0d00436ff879096abf43afc3.jpg)

![](images/9302a344ae345c4af24aca2fbdea4e55c9c9ce1e9f2137f05f87915885a0c92d.jpg)

![](images/8d642cad0d94b30d5d40ba19f8dd7a4493024bfc09d925ab4ebbd9a28b6a8336.jpg)  
Fig. 6: Results of the wrench estimation experiment. This figure compares the wrench estimation results from our proposed wrench estimation algorithm (blue) with those obtained using the momentum observer method (red) [7], as well as with the actual measurements recorded by the wrench measurement device (green) across all 6 DoF.

![](images/33e80e0f7c7952e9d407840702844d589a3f717d1abf398b98aace13583142a8.jpg)  
Virtual Impedance Realization in Translation (x Direction) Quadrotor Type: Dragonfly

![](images/7068b0e07bc248af729780fe2bddf098db39f3489496454ee9b8732e03347848.jpg)

![](images/93ac031a579f48bc823df816f7c3988dbcc8359b35331862ffccef23a28755df.jpg)  
Fig. 7: Virtual impedance realization in the $x$ direction of the translational motion. A step force input of $\mathbf { F } _ { H } = \left[ 0 . 5 \quad 0 \quad 0 \right] ^ { \top } \mathrm { N }$ is given into the system at the start of the plots. We choose the parameters of the admittance controller in the $\mathbf { X }$ direction as $M _ { x } = 0 . 2 5 , K _ { x } = 0 . 0$ , and $D _ { x } = 1$ , 2, 5, 10 for comparison.

In the cable force estimation experiment, we hover a quadrotor in midair and run the proposed UKF onboard. The measurement device is connected to the center of mass of the quadrotor and a human operator pulls the measurement device into various directions to evaluate the algorithms. The results are shown in Fig. 5. In the plots, we compare the measured forces to the estimated forces in all 3 DoF and the estimated cable forces track measured ground truth accurately.

During the wrench estimation experiment, we hover the system with the regular payload controller without activating the admittance controller. Subsequently, the human operator

pulls the payload with the force measurement device, and we record both the ground truth wrench and the estimation results. In addition to the ground truth force, the ground truth external torque is obtained by crossing the attached point position vector in $\mathcal { L }$ and the measured ground truth force vector from the measurement device. The payload is pulled so that the external wrench is non-zero in all six DoF, as shown in Fig. 4.

The results are shown in Fig. 6. In the plots, we compare the measured wrenches to the estimated wrenches using our proposed method in Section VI-A2 and the momentum observer method presented in [7] in all 6 DoF. As we can observe

![](images/d1cf404ed4921a2880df04499003599d374f4faaedaffbcc0506e5f86d6061c0.jpg)  
Virtual Impedance Realization in Translation (x Direction) Quadrotor Type: Hummingbird

![](images/7ada52db7ccbed9d3376eb357a1de4d2e3c2013947dbc33b46ed2c846df9f4ad.jpg)

![](images/8220fa486604bf6e99add0acb8490c4da851d65647c76e314095ef2127678631.jpg)  
Fig. 8: Virtual impedance realization in the $x$ direction of the translational motion. A step force input of $\mathbf { F } _ { H } = \left[ 1 . 0 \quad 0 \quad 0 \right] ^ { \top } \mathrm { ~ N ~ }$ is given into the system at the start of the plots. We choose the parameters of the admittance controller in the $\mathbf { X }$ direction as $M _ { x } = 0 . 2 5 , K _ { x } = 0 . 0$ , and $D _ { x } = 1$ , 2, 5, 10 for comparison.

![](images/f0e69b1173ffa1ea66d25fecd8da092cb7d1fe5e857329e9175ba13c0dc7c621.jpg)  
Virtual Impedance Realization in Rotation (Yaw Direction) Quadrotor Type: Dragonfly

![](images/0e9ee6b807b47489d18a765e21ca102017c08fce695767910a2587b7ccf52ba5.jpg)

![](images/39afd83696b1b8f1a1f370a65740e67edaeda342f22279818e9bf630acad9e95.jpg)  
Fig. 9: Virtual impedance realization in the yaw direction of the rotational motion. A step moment input of $\mathbf { M } _ { H } \mathbf { \Psi } = \mathbf { \Phi }$ $\begin{array} { r l } { \left[ 0 \quad 0 \quad 0 . 0 5 \right] ^ { \top } \mathrm { N m } } \end{array}$ is given into the system at the start of the plots. We choose the parameters of the admittance controller in the yaw direction as $M _ { \psi } = 0 . 1$ $M _ { \psi } = 0 . 1 , ~ K _ { \psi } = 0 . 0$ $K _ { \psi } = 0 . 0$ , and $D _ { \psi } = 0 . 0 5$ , 0.25, 1.25, 2.5 for comparison.

in Fig. 6, the estimated wrenches from our method track the measured ground truth quite accurately. However, on the other hand, the momentum observer method tends to smooth the estimates excessively, leading to underestimating the external wrench. The root mean square errors in all six directions are also reported in Table II, confirming a good accuracy.

# B. Admittance Control with Wrench Estimation

After validating the wrench estimation, we jointly test it with the admittance controller.

1) Virtual Impedance Realization: In this section, we present results in simulation to quantitatively analyze the performance of our proposed methods, particularly regarding the rendering of the desired virtual impedance of our proposed

-Payload Pose - - -Desired Pose from Admitance Ctrl ---- Estimate Wrench

![](images/270783daa3e0850004421caa770d6f141b13f359b6a44b26fca96f6789cc902f.jpg)

![](images/6c37a798ba0d44b34f74227c7896d95391a323c9177a2bddf35905e5c991b5fb.jpg)

![](images/f1598439e2b5016feab2219a61a300caa99993da0c2c70539c03d0f85cac0dca.jpg)

![](images/78b9c19ef0d05038fade65731c3d3e50a7e0581727835e544f89f39ec1be2067.jpg)

![](images/c330d66d056370fad70423458e0e1f11ad76f3b0150cf3d3a4e302473de7fc86.jpg)

![](images/6e2f7a4d8c46b9d7c82ac1f852c678b50d78ea1d81d808cd30a08adca0839191.jpg)  
Fig. 10: We test the admittance controller together with wrench estimation in all 6 DoF. The $\mathcal { X } _ { t r a j }$ are where the plots start and the derivative $\dot { \mathcal X } _ { t r a j } ~ \ddot { \mathcal X } _ { t r a j }$ are zero. The actual payload pose, desired payload pose from the admittance controller, and estimated wrench are plotted. On the top: translation tests in x, y, z in I. On the bottom: rotation tests in roll, pitch, yaw in $\mathcal { L }$ .

system. We deploy robot teams that consist of 3 “Dragonfly” quadrotors or 3 “Hummingbird” quadrotors with $1 \textrm { m }$ cable in our open-source simulator [57] to validate the realization of desired impedance values. In the following experiments, we introduce a step wrench input and observe the system’s response.

In the first experiment, we apply a step force input on the payload in the positive $x$ direction and set different impedance values (1, 2, 5, 10) in the admittance controller. The second experiment involves the application of a step moment input on the payload in the positive yaw direction, with different impedance values (0.05, 0.25, 1.25, 2.5) set in the admittance controller. The results are shown in Figs. 7- 9. We evaluate the actual impedance in the system using the ground truth force and moment, divided by the actual velocity of the payload along the corresponding direction. Hence the actual impedance we obtain in Figs. 7- Fig. 9 are FHx $\frac { \mathbf { F } _ { H x } } { \dot { \mathbf { x } } _ { L x } }$ and MHz˙ , respectively. In $\frac { \mathbf { M } _ { H z } } { \dot { \Omega } _ { L z } }$ x˙ Lx Ω Lz the plots, we compare the actual impedance with the desired impedance set in the admittance controller.

As illustrated by the plots, upon application of step force and moment inputs to the system, the payload promptly accelerates in the $x$ and yaw directions, respectively. As the wrench estimation updates, the admittance controller starts to adjust the desired payload state to adapt the human input, shown by the dashed lines in the bottom plots in both Figs. 7 - 9. Through the comparison, we can see that with larger values of $D _ { x } , D _ { \psi }$ , the desired velocity derived from the admittance controller evolves slower and smaller in magnitude. As the experiment proceeds, the desired velocity from the admittance controller ultimately converges to final values, respectively equivalent to $\frac { \mathbf { F } _ { H x } } { D _ { x } }$ Dx and MHz $\frac { \mathbf { M } _ { H z } } { D _ { \psi } }$ Dψ

Moreover, a larger desired impedance value results in noticeable spikes in the actual impedance before the convergence. This can be attributed to the fact that a higher impedance value leads to a smaller corresponding desired velocity, which in turn causes larger velocity errors at the initial stage. This subsequently results in an overshooting response of the actual payload velocity, causing it to cross the zero line and trigger spikes in the actual impedance realization.

Lastly, as the experiments progress and the transient effects resulting from the step input reduce, the payload’s linear and angular velocities converge toward the desired payload velocity determined by the admittance controller. Consequently, the actual virtual impedance also aligns with the value set by the admittance controller. We observe similar results for the other Cartesian and angular axes that are not reported for simplicity.

2) Real-World Experiments: We conduct six tests involving all 6 DoF of the admittance controller in real-world experiments. The human operator manipulates the payload by translating the payload in x, y, and $z$ and rotating the payload in roll, pitch, and yaw, respectively, to show that the load can be fully manipulated. At the end of each experiment, the human operator releases the payload. The square gain matrices in the admittance controller have a blockdiagonal structure as $\mathbf { M } = d i a g ( 0 . 2 5 \mathbf { I } _ { 3 \times 3 } , 0 . 1 \mathbf { I } _ { 3 \times 3 } )$ , ${ \textbf { D } } =$ diag(1.25I3×3, 5.0I3×3), $\mathbf { K } = d i a g ( \mathbf { 0 } _ { 3 \times 3 } , \mathbf { 0 } _ { 3 \times 3 } )$ .

The experimental results are presented in Fig. 10. As shown in the plots, the human operator translates the payload approximately $1 \textrm { m }$ in $x$ and $y$ direction, $0 . 4 \mathrm { ~ m ~ }$ in the $z$ direction. In the rotation part of the experiment, the human operator rotates the payload approximately $3 0 ^ { \circ }$ in the roll and pitch direction and $6 0 ^ { \circ }$ in the yaw direction. The tests show that

![](images/ae9ad4ae53e57e14436272028bad5abf16d412ae40a0c4bf004e19daf544e2a5.jpg)  
Fig. 11: Human-robot collaborative transportation task. In this task, the human operator collaborates with a team of quadrotors to transport a payload from the start position (•) to the final position $( { \star } )$ . The human operator and the quadrotor team translate the payload in the Cartesian space, moving its position along the x, y, and $z$ axes.

the admittance controller, coupled with the wrench estimator, can successfully update the payload’s desired position or orientation according to the human operator’s interactive force as input. As the human operator releases the payload, the wrench estimation outputs $\left[ \mathbf { 0 } _ { 6 \times 1 } \right]$ as wrench estimation. Since K in the admittance controller is $\left[ \mathbf { 0 } _ { 6 \times 6 } \right]$ in this set of experiments, the payload remains at the position or orientation released by the human operator without returning to its original reference position or orientation. It further confirms the effectiveness of the wrench estimation and admittance controller pipeline in assisting object transportation and manipulation.

# C. Human-Aware Human-Robot Collaborative Transportation

In this section, we show that our system enables a human operator to physically collaborate with the robot team to accomplish the following two tasks

1) The robot team and the human operator collaboratively manipulate the payload to a goal location, as demonstrated in Fig. 11.   
2) Human operator corrects the payload trajectory to avoid an obstacle in an existing trajectory, as demonstrated in Fig. 12

The gradient-based and optimization-based methods for human-aware force distribution are tested for each of the two tasks. For the optimization-based method, the drone-to-drone distance limit is set to be $\ge 0 . 7 5 \mathrm { ~ m ~ }$ , and the human-to-drone distance limit is set to b $\mathrm { ~ a ~ } \geq \ 0 . 7 5 \mathrm { ~ m ~ }$ . The gradient-based method does not require a predetermined distance.

In addition, as we show in Fig. 3 and discuss in Section V-B, we feed the human operator’s position $\mathbf { p } _ { H }$ from the Vicon

![](images/39c56e731ed7b9acb63bc869597a66e04a2af8fecddfa9148b18bb115f322532.jpg)  
Fig. 12: Human-assisted obstacle avoidance task. In this task, the human operator moves the payload from the desired trajectory (yellow path) to guide the payload away from an unknown obstacle and then releases the payload, allowing it to rejoin the desired trajectory and reach the final position $( { \star } )$ .

in $\mathcal { T }$ as $\mathbf { p } _ { O }$ to the eqs. (20) and (25) for application to physical human-robot interaction. We would also like to note that by using deep-learning-based human pose estimation techniques [67], the robots can also use onboard camera to estimate $\mathbf { p } _ { H }$ , but this is out of the scope of this paper and we refer to it as future work.

1) Human-robot collaborative transportation: In this experiment, the robot team and the human operator collaborate together to move a payload from the starting location to the final location via direct force interaction. Payload translates in all three axes, as shown in Fig. 11. The square gain matrices are selected block-diagonal as $\textbf { M } =$ $d i a g ( 0 . 2 5 { \bf I } _ { 3 \times 3 } , 0 . 1 { \bf I } _ { 3 \times 3 } )$ , $\mathbf { D } = d i a g ( 5 . 0 \mathbf { I } _ { 3 \times 3 } , 5 . 0 \mathbf { I } _ { 3 \times 3 } )$ , $\mathbf K =$ $l i a g ( \mathbf { 0 } _ { 3 \times 3 } , \mathbf { 0 } _ { 3 \times 3 } )$ .

Note that the spring constant coefficient for the admittance controller is set to zero so that the payload stays at the position/orientation once the human operator releases the payload.

The experimental results are shown in Fig. 13, where we compare the actual payload position with the desired payload position from the admittance controller.

The results demonstrate the proposed methods can confidently update the desired payload position to satisfy the human operator’s intention of moving the payload under both gradient-based and optimization-based methods. Furthermore, the movement introduced by the human-aware force distribution does not affect the performance of the payload wrench estimation or admittance controller.

In Fig. 14, we show the effects of the two methods for human-aware force distribution with a top view of the entire collaboration task. From the plots, we can observe that, as the

![](images/233f434ac694fb2e586f195ad0498b7a8a0801666920cbb756d0b4acde3cef79.jpg)  
Fig. 13: Human-robot collaborative transportation experiment results. Payload Position vs. Desired Position from Admittance Controller. Transnational results when optimization-based human-aware method is used (top row). Transnational results when gradient-based human-aware method is used (bottom row).

![](images/1180b7d5c2d804626d44934023064fba2c81cba8e3426bebcc83e7e1d180915d.jpg)  
Fig. 14: Human-robot collaborative transportation experiment results. We show the top down view of the human operator (star) and the team of drones (circles). On the top: trajectory when optimization-based human-aware method is used. On the bottom: trajectory when gradient-based human-aware method is used.

human operator, denoted by the purple star, approaches the 3 robots with a suspended payload, the human-aware force distribution starts to be effective. The controller expands the 2 robots (blue and green circles) that are close to the human operator to keep the distance.

To quantitatively support our analysis, we conducted multiple iterations of the same experiments and recorded the distances between the robots and the human operator. The distribution of these distance measurements is illustrated in Figs. 15 and 16, with corresponding mean and standard deviation values summarized in Table III.

As shown in Figs. 15 and 16, both the optimization-based and gradient-based methods effectively maintain a consistent distance between the robots and the human operator throughout multiple repeated experiments. This observation is further

validated by the statistical data presented in Table III. Notably, the optimization-based method distinguishes itself from the gradient-based method as it enforces inter-robot distance constraints. This is evident in the left plot of Fig. 16, where all three drones maintain a minimum separation of $0 . 7 5 \mathrm { m }$ , as specified by the constraint.

To provide additional insights, Figs. 17 and 18 depict the distances between each robot and the human operator, as well as the inter-robot distances, throughout the duration of a single sample experiment. Initially, the human operator starts approximately 2 to 3m away from the robot team. As the operator approaches, the distances between the human and robots 1 and 3 (represented by blue and green) decrease. At this point, the human-aware force distribution becomes active, maintaining stable human-robot distances.

![](images/5d812144db6ab70c88bd82173058741da8e6e174e2dbce5cf44d7584b60edf52.jpg)

![](images/3ffead1c65b7a49c76c0ee0765f190aecbfd877912556dfd25c7ad3463a05566.jpg)  
Fig. 15: Box plot with mean lines of the robot to robot distances and robot to head distances during the human-aware collaborative transportation experiments using the gradientbased method. The data are collected from multiple repeated experiments.

![](images/e61f4e3213df4944e9eac5f6d2fc0229cf77c00059fe752aa01daa742b5e7c6c.jpg)

![](images/2dda6d689261d1865712b946857f88617059ff7dd374508775ad6891efcb2fab.jpg)  
Fig. 16: Box plot with mean lines of the robot to robot distances and robot to head distances during the humanaware collaborative transportation experiments using the optimization-based method. The data are collected from multiple repeated experiments.

2) Human-assisted Obstacle Avoidance: In this experiment, the payload follows a straight trajectory from the starting location to the final location, as the robot team is unaware of the obstacle. The human operator corrects the payload trajectory to avoid the obstacle, as shown in Fig. 12. Both gradient-based and optimization-based methods are also applied here. The square gain matrices for the admittance controller have a block-diagonal structure as $\mathbf { M } =$ $d i a g ( 0 . 2 5 { \bf I } _ { 3 \times 3 } , 0 . 1 { \bf I } _ { 3 \times 3 } )$ , $\mathbf { D } = d i a g ( 5 . 0 \mathbf { I } _ { 3 \times 3 } , 5 . 0 \mathbf { I } _ { 3 \times 3 } )$ , $\mathbf K =$ $d i a g ( 1 . 2 \mathbf { I } _ { 3 \times 3 } , \mathbf { 0 } _ { 3 \times 3 } )$ .

Note that the constant spring coefficient for the admittance controller is no longer zero. The payload will now return to the position/orientation commanded by the trajectory when the human operator releases the payload.

As we can see from Fig. 19, the correction takes effects according to the admittance controlled trajectory. Once the human operator stops the correction, the non-zero K constant starts to allow the corrected trajectory to converge with the original trajectory. As expected, such behavior is present in both the gradient-based and optimization-based methods.

# VIII. COMPUTATIONAL COMPLEXITY DISCUSSION

In this section, we discuss the theoretical computational time complexity of the methods proposed in this paper,

![](images/fb8118a585ac49329ce6918f96939daf1f824b3854776f3c3872cb40a91cd949.jpg)

![](images/7da5c44f0cd88f04d1b1931fe1127ba2965256353c027cc69779a6acbbfa8dbf.jpg)  
Fig. 17: Human-robot collaborative transportation experiment results. Drone to drone distance and human to drone distance when gradient-based method is used; the gradient-based method does not require a predetermined distance.

![](images/eda450f346880e0c90faee2a100d9e33a44dfad6cdc4b916800f31dd66031637.jpg)

![](images/a98a79623be9ff0c7af100f01d57f15a68207ac60e02635e933a91df91757ca7.jpg)  
Fig. 18: Human-robot collaborative transportation experiment results. Drone-to-drone distance and human-to-drone distance when optimization-based method is used; minimum drone-todrone distance is set to be $0 . 7 5 \mathrm { ~ m ~ }$ , and the minimum humanto-drone distance is set to be $0 . 7 5 \mathrm { ~ m ~ }$ .

focusing on how each algorithm’s computational complexity scales with the number of robots. Through this discussion, we aim to offer insights into the proposed methods and guide the corresponding system design choices. We summarize the results regarding the computational complexity of our algorithms in Table IV.

# A. Physical Human-Robot Interaction

We begin our discussion with the Physical Human-Robot Interaction module, comprising the robot state estimator, the human wrench estimator, and the payload admittance controller.

TABLE III: Distance Summary: Robot-Robot and Robot-Head Pairs.   

<table><tr><td>Method</td><td>Pair Type</td><td>Mean</td><td>Std</td></tr><tr><td rowspan="6">Gradient-based</td><td>1-2</td><td>0.57978</td><td>0.096378</td></tr><tr><td>1-3</td><td>0.79629</td><td>0.084538</td></tr><tr><td>2-3</td><td>0.54679</td><td>0.076384</td></tr><tr><td>Head-1</td><td>0.87464</td><td>0.097718</td></tr><tr><td>Head-2</td><td>1.0433</td><td>0.041136</td></tr><tr><td>Head-3</td><td>0.79129</td><td>0.071813</td></tr><tr><td rowspan="6">Optimization-based</td><td>1-2</td><td>0.81366</td><td>0.053177</td></tr><tr><td>1-3</td><td>1.2506</td><td>0.10804</td></tr><tr><td>2-3</td><td>0.74762</td><td>0.050086</td></tr><tr><td>Head-1</td><td>0.89176</td><td>0.05772</td></tr><tr><td>Head-2</td><td>0.96053</td><td>0.080423</td></tr><tr><td>Head-3</td><td>0.80493</td><td>0.038652</td></tr></table>

![](images/3bd94f68bd97b880b2a8e5732709dbf39f9ccbd0d4c01a0756feb21f3b2e2082.jpg)  
Fig. 19: Correcting payload trajectory experiment result. Comparison between actual trajectory, desired trajectory, admittance controller output, and estimated external wrench on the payload. Optimization-based safety controller is used (left). Gradient-based safety controller is used (right).

Firstly, each quadrotor runs its robot state estimator, a UKF with a fixed state vector size of 19 and a fixed input vector size of 4. Similarly, the payload admittance controller’s computation, as described in eq. (40), is independent of the number of quadrotors, as it controls only the 6 degrees of freedom (DoFs) of the payload. Consequently, both the UKF and the payload admittance controller exhibit a computational complexity of $\mathcal { O } ( 1 )$ , independent of the number of quadrotors $n$ in the system.

Next, the human wrench estimation requires quadrotors in the team to share individual estimated cable tension forces, which are then aggregated to derive the total external wrench on the payload using eq.(39). The computation, shown in eq.(39), scales linearly with the number of quadrotors due to the linear tension mapping matrix P. Thus, the computation complexity in eq.(39) is bounded by ${ \mathcal { O } } ( n )$ , with the dimension of matrix P, as depicted in eq.(4), scaling accordingly with $n$ . This linear time complexity is manageable with the available

computational resources, as $n$ would need to reach the order of thousands to make this linear-complexity matrix multiplication the system’s bottleneck.

# B. Planning and Control

In the domain of planning and control, the system includes payload trajectory planner, payload trajectory tracking controller, dynamic force distribution, and robot controller. The payload trajectory planner and tracking controller function similarly to the payload admittance controller, meaning their computation also remains independent of the number of quadrotors $n$ . Additionally, each quadrotor independently runs its robot controller as specified in eqs. (29) and (30), thus these components also maintain a computational complexity of $\mathcal { O } ( 1 )$ .

The dynamic force distribution involves two parts: nominal force distribution and human-aware force distribution. It requires linear mapping via matrix multiplication, as shown in eq. (13), with a complexity bound of ${ \mathcal { O } } ( n )$ .

Regarding human-aware force distribution, we propose two methods: an optimization-based method and a gradient-based method. We discuss them separately below:

i) The optimization-based method employs the Sequential Least-Squares Quadratic Programming (SLSQP) solver, requiring $\scriptstyle { \mathcal { O } } ( a ^ { 2 } )$ storage and $\mathcal { O } ( a ^ { 3 } )$ time, where $a = 3 \times$ $( n - 6 )$ represents the problem dimension.   
ii) The gradient-based method computes the cable tension force modifier through null space projection of a scaled gradient vector, optimizing eq. (19). The sum of $\mathcal { L } _ { 2 }$ -norm distances between each quadrotor and the human operator, combined with the closed-form solution for null space projection, leads to a computational complexity of ${ \mathcal { O } } ( n )$ . This complexity is less than that of the optimizationbased method, attributed to the utilization of closed-form solutions for both gradient computation and null space projection.

# IX. CONCLUSION AND FUTURE WORKS

In this paper, we presented a human-aware human-robot collaborative transportation and manipulation approach considering a team of aerial robots with a cable-suspended payload. Our approach combines a novel control method that leverages system redundancy with a collaborative wrench estimator, enabling a human operator to interact in 6 DoF with a rigid structure being transported by a team of aerial robots via cable. Additionally, the system can achieve secondary tasks like keeping a certain distance between the human operator and robots, or inter-robot separation by exploiting the additional system redundancy without affecting the quality or accuracy of the interactive experience. We demonstrated, through real-world experiments, our system’s capabilities. The system can assist the human operator in manipulation tasks, as well as enable the human operator to effectively assist the load navigation, as demonstrated in the experiments.

In future research, we aim to expand our study into humancentric considerations, prioritizing metrics related to comfortness and acceptance of human operators. These elements are

TABLE IV: Computational Complexity Summary   

<table><tr><td></td><td>Scalability</td><td>Time Complexity</td></tr><tr><td colspan="3">Physical Human-Robot Interaction</td></tr><tr><td>Robot State Estimation</td><td>High</td><td>O(1)</td></tr><tr><td>Human Wrench Estimation</td><td>Medium</td><td>O(n)</td></tr><tr><td>Payload Admittance Controller</td><td>High</td><td>O(1)</td></tr><tr><td colspan="3">Planning and Control</td></tr><tr><td>Payload Trajectory Planner</td><td>High</td><td>O(1)</td></tr><tr><td>Payload Trajectory Tracking Controller</td><td>High</td><td>O(1)</td></tr><tr><td>Nominal Force Distribution</td><td>Medium</td><td>O(n)</td></tr><tr><td>Human-Aware Force Distribution: Gradient-Based Method</td><td>High</td><td>O(n)</td></tr><tr><td>Human-Aware Force Distribution: Optimization-Based Method</td><td>Low</td><td>O(n3)</td></tr><tr><td>Robot Controller</td><td>High</td><td>O(1)</td></tr></table>

crucial in the domain of human-robot interaction. Additionally, we plan to develop safety methods to counteract unexpected human actions, such as sudden or forceful human physical inputs to the load that could lead to cable slack or actuator overload. This could ensure further robust operation under varied conditions.

In addition, we want to extend our framework to explicitly address collision avoidance between the cables and the human operator as well. Our current approach relies on the human’s ability to navigate around the cables. However, by modeling the cables as convex polygons and incorporating them into the optimization process, we can develop a more comprehensive collision avoidance strategy that ensures human safety. Further developments also include the design of an onboard sensing mechanism. We plan to employ tension-measurement tools, onboard cameras, IMUs, and ESCs on each vehicle. Our goal is to achieve comprehensive onboard state estimation, therefore eliminating dependence on external motion capture systems. We also intend to investigate the impacts of state estimation and control delays, lags, and noise on system performance. Understanding these factors will enable us to improve our the robustness of our framework, enhancing interaction experience.

Finally, we would like to integrate a more advanced onboard perception module. It can empower the robot team to identify and navigate around complex hazardous spaces. This feature will enable autonomous obstacle avoidance maneuvers while leveraging the system’s redundancy to maintain the intended payload trajectory without compromise. We also envision employing deep learning techniques with robots’ onboard cameras to analyze the human operator’s posture, enhancing our human-aware force distribution strategy.

# REFERENCES

[1] K. Schwab, The fourth industrial revolution. London, England: Portfolio Penguin, 2017.   
[2] S. S. Mansouri, C. Kanellakis, E. Fresk, D. Kominiak, and G. Nikolakopoulos, “Cooperative coverage path planning for visual inspection,” Control Engineering Practice, vol. 74, pp. 118–131, 2018.   
[3] K. Shah, G. Ballard, A. Schmidt, and M. Schwager, “Multidrone aerial surveys of penguin colonies in antarctica,” Science Robotics, vol. 5, no. 47, p. eabc3000, 2020.   
[4] G. Loianno, Y. Mulgaonkar, C. Brunner, D. Ahuja, A. Ramanandan, M. Chari, S. Diaz, and V. Kumar, “Autonomous flight and cooperative control for reconstruction using aerial robots powered by smartphones,” The International Journal of Robotics Research, vol. 37, no. 11, pp. 1341–1358, 2018.   
[5] N. Michael, S. Shen, K. Mohta, Y. Mulgaonkar, V. Kumar, K. Nagatani, Y. Okada, S. Kiribayashi, K. Otake, K. Yoshida, K. Ohno, E. Takeuchi, and S. Tadokoro, “Collaborative mapping of an earthquake-damaged

building via ground and aerial robots,” Journal of Field Robotics, vol. 29, no. 5, pp. 832–841, 2012.   
[6] A. E. Jimenez-Cano, D. Sanalitro, M. Tognon, A. Franchi, and J. Cort ´ es, ´ “Precise Cable-Suspended Pick-and-Place with an Aerial Multi-robot System,” Journal of Intelligent & Robotic Systems, vol. 105, no. 3, p. 68, 2022.   
[7] D. Sanalitro, M. Tognon, A. J. Cano, J. Cortes, and A. Franchi, “Indirect ´ force control of a cable-suspended aerial multi-robot manipulator,” IEEE Robotics and Automation Letters, vol. 7, no. 3, pp. 6726–6733, 2022.   
[8] M. Saska, V. Vonasek, J. Chudoba, J. Thomas, G. Loianno, and V. Ku-´ mar, “Swarm distribution and deployment for cooperative surveillance by micro-aerial vehicles,” Journal of Intelligent & Robotic Systems, vol. 84, no. 1, pp. 469–492, 2016.   
[9] G. Li and G. Loianno, “Design and experimental evaluation of distributed cooperative transportation of cable suspended payloads with micro aerial vehicles,” in Experimental Robotics, B. Siciliano, C. Laschi, and O. Khatib, Eds. Cham: Springer International Publishing, 2021, pp. 28–36.   
[10] B. E. Jackson, T. A. Howell, K. Shah, M. Schwager, and Z. Manchester, “Scalable cooperative transport of cable-suspended loads with UAVs using distributed trajectory optimization,” IEEE Robotics and Automation Letters, vol. 5, no. 2, pp. 3368–3374, 2020.   
[11] G. Li, R. Ge, and G. Loianno, “Cooperative transportation of cable suspended payloads with MAVs using monocular vision and inertial sensing,” IEEE Robotics and Automation Letters, vol. 6, no. 3, pp. 5316– 5323, 2021.   
[12] A. Ollero, M. Tognon, A. Suarez, D. Lee, and A. Franchi, “Past, present, and future of aerial robotic manipulators,” IEEE Transactions on Robotics, vol. 38, no. 1, pp. 626–645, 2022.   
[13] A. Afifi, G. Corsini, Q. Sable, Y. Aboudorra, D. Sidobre, and A. Franchi, “Physical human-aerial robot interaction and collaboration: Exploratory results and lessons learned,” in International Conference on Unmanned Aircraft Systems (ICUAS), 2023, pp. 956–962.   
[14] A. Tagliabue, M. Kamel, R. Siegwart, and J. Nieto, “Robust collaborative object transportation using multiple MAVs,” The International Journal of Robotics Research, vol. 38, no. 9, pp. 1020–1044, 2019.   
[15] G. Loianno and V. Kumar, “Cooperative transportation using small quadrotors using monocular vision and inertial sensing,” IEEE Robotics and Automation Letters, vol. 3, no. 2, pp. 680–687, 2018.   
[16] D. Mellinger, M. Shomin, N. Michael, and V. Kumar, Cooperative Grasping and Transport Using Multiple Quadrotors. Berlin, Heidelberg: Springer Berlin Heidelberg, 2013, pp. 545–558.   
[17] J. Thomas, G. Loianno, J. Polin, K. Sreenath, and V. Kumar, “Toward autonomous avian-inspired grasping for micro aerial vehicles,” Bioinspiration & biomimetics, vol. 9, no. 2, p. 025010, 2014.   
[18] A. Afifi, M. van Holland, and A. Franchi, “Toward physical human-robot interaction control with aerial manipulators: Compliance, redundancy resolution, and input limits,” in IEEE International Conference on Robotics and Automation (ICRA), 2022, pp. 4855–4861.   
[19] G. Corsini, M. Jacquet, H. Das, A. Afifi, D. Sidobre, and A. Franchi, “Nonlinear model predictive control for human-robot handover with application to the aerial case,” in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2022.   
[20] M. Tognon, R. Alami, and B. Siciliano, “Physical human-robot interaction with a tethered aerial vehicle: Application to a force-based human guiding problem,” IEEE Transactions on Robotics, vol. 37, no. 3, pp. 723–734, 2021.   
[21] J. Lee, R. Balachandran, Y. S. Sarkisov, M. De Stefano, A. Coelho, K. Shinde, M. J. Kim, R. Triebel, and K. Kondak, “Visual-inertial telepresence for aerial manipulation,” in IEEE International Conference on Robotics and Automation (ICRA), 2020, pp. 1222–1229.

[22] J. Geng and J. Langelaan, “Cooperative transport of a slung load using load-leading control,” Journal of Guidance, Control, and Dynamics, vol. 43, no. 7, pp. 1313–1331, 2020.   
[23] H. Rastgoftar and E. M. Atkins, “Cooperative aerial payload transport guided by an in situ human supervisor,” IEEE Transactions on Control Systems Technology, vol. 27, no. 4, pp. 1452–1467, 2019.   
[24] M. Romano, A. Ye, J. Pye, and E. Atkins, “Cooperative multilift slung load transportation using haptic admittance control guidance,” Journal of Guidance, Control, and Dynamics, vol. 45, no. 10, pp. 1899–1912, 2022.   
[25] K. Klausen, C. Meissen, T. I. Fossen, M. Arcak, and T. A. Johansen, “Cooperative control for multirotors transporting an unknown suspended load under environmental disturbances,” IEEE Transactions on Control Systems Technology, vol. 28, no. 2, pp. 653–660, 2020.   
[26] M. Bernard, K. Kondak, I. Maza, and A. Ollero, “Autonomous transportation and deployment with aerial robots for search and rescue missions,” Journal of Field Robotics, vol. 28, no. 6, pp. 914–931, 2011.   
[27] V. P. Tran, F. Santoso, M. A. Garratt, and S. G. Anavatti, “Distributed artificial neural networks-based adaptive strictly negative imaginary formation controllers for unmanned aerial vehicles in time-varying environments,” IEEE Transactions on Industrial Informatics, vol. 17, no. 6, pp. 3910–3919, 2021.   
[28] X. Zhang, F. Zhang, P. Huang, J. Gao, H. Yu, C. Pei, and Y. Zhang, “Selftriggered based coordinate control with low communication for tethered multi-uav collaborative transportation,” IEEE Robotics and Automation Letters, vol. 6, no. 2, pp. 1559–1566, 2021.   
[29] Y. Liu, F. Zhang, P. Huang, and X. Zhang, “Analysis, planning and control for cooperative transportation of tethered multi-rotor UAVs,” Aerospace Science and Technology, vol. 113, p. 106673, 2021.   
[30] T. Lee, K. Sreenath, and V. Kumar, “Geometric control of cooperating multiple quadrotor UAVs with a suspended payload,” in 52nd IEEE Conference on Decision and Control (CDC), 2013, pp. 5510–5515.   
[31] A. Tagliabue, M. Kamel, S. Verling, R. Siegwart, and J. Nieto, “Collaborative transportation using mavs via passive force control,” in IEEE International Conference on Robotics and Automation (ICRA), 2017, pp. 5766–5773.   
[32] M. Gassner, T. Cieslewski, and D. Scaramuzza, “Dynamic collaboration without communication: Vision-based cable-suspended load transport with two quadrotors,” in IEEE International Conference on Robotics and Automation (ICRA), 2017, pp. 5196–5202.   
[33] H. Rastgoftar and E. M. Atkins, “Continuum deformation of a multiple quadcopter payload delivery team without inter-agent communication,” in International Conference on Unmanned Aircraft Systems (ICUAS), 2018, pp. 539–548.   
[34] H. Xie, K. Dong, and P. Chirarattananon, “Cooperative transport of a suspended payload via two aerial robots with inertial sensing,” IEEE Access, vol. 10, pp. 81 764–81 776, 2022.   
[35] M. Tognon, C. Gabellieri, L. Pallottino, and A. Franchi, “Aerial comanipulation with cables: The role of internal force for equilibria, stability, and passivity,” IEEE Robotics and Automation Letters, vol. 3, no. 3, pp. 2577–2583, 2018.   
[36] T. Lee, “Geometric control of quadrotor UAVs transporting a cablesuspended rigid body,” IEEE Transactions on Control Systems Technology, vol. 26, no. 1, pp. 255–264, 2018.   
[37] G. Wu and K. Sreenath, “Geometric control of multiple quadrotors transporting a rigid-body load,” in 53rd IEEE Conference on Decision and Control (CDC), 2014, pp. 6141–6148.   
[38] J. Fink, N. Michael, S. Kim, and V. Kumar, “Planning and control for cooperative manipulation and transportation with aerial robots,” The International Journal of Robotics Research, vol. 30, no. 3, pp. 324–334, 2011.   
[39] N. Michael, J. Fink, and V. Kumar, “Cooperative manipulation and transportation with aerial robots,” Autonomous Robots, vol. 30, no. 1, pp. 73–86, 2011.   
[40] R. C. Sundin, P. Roque, and D. V. Dimarogonas, “Decentralized model predictive control for equilibrium-based collaborative uav bar transportation,” in IEEE International Conference on Robotics and Automation (ICRA), 2022, pp. 4915–4921.   
[41] G. Tartaglione, E. D’Amato, M. Ariola, P. S. Rossi, and T. A. Johansen, “Model predictive control for a multi-body slung-load system,” Robotics and Autonomous Systems, vol. 92, pp. 1–11, 2017.   
[42] T. Lee, “Geometric control of multiple quadrotor UAVs transporting a cable-suspended rigid body,” in 53rd IEEE Conference on Decision and Control (CDC), 2014, pp. 6155–6160.   
[43] J. Geng, P. Singla, and J. W. Langelaan, “Load-distribution-based trajectory planning and control for a multilift system,” Journal of Aerospace Information Systems, vol. 19, no. 5, pp. 366–381, 2022.

[44] C. Masone, H. H. Bulthoff, and P. Stegagno, “Cooperative transportation ¨ of a payload using quadrotors: A reconfigurable cable-driven parallel robot,” in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2016, pp. 1623–1630.   
[45] E. Bulka, C. He, J. Wehbeh, and I. Sharf, “Experiments on collaborative transport of cable-suspended payload with quadrotor UAVs,” in International Conference on Unmanned Aircraft Systems (ICUAS), 2022, pp. 1465–1473.   
[46] L. v. der Spaa, M. Gienger, T. Bates, and J. Kober, “Predicting and optimizing ergonomics in physical human-robot cooperation tasks,” in IEEE International Conference on Robotics and Automation (ICRA), 2020, pp. 1799–1805.   
[47] J. Stuckler and S. Behnke, “Following human guidance to cooperatively carry a large object,” in 11th IEEE-RAS International Conference on Humanoid Robots, Bled, Slovenia, 2011, p. 218–223.   
[48] M. Gienger, D. Ruiken, T. Bates, M. Regaieg, M. MeiBner, J. Kober, P. Seiwald, and A.-C. Hildebrandt, “Human-robot cooperative object manipulation with contact changes,” in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2018, pp. 1354–1360.   
[49] W. Sheng, A. Thobbi, and Y. Gu, “An integrated framework for human–robot collaborative manipulation,” IEEE Transactions on Cybernetics, vol. 45, no. 10, p. 2030–2041, 2015.   
[50] F. Augugliaro and R. D’Andrea, “Admittance control for physical human-quadrocopter interaction,” in European Control Conference (ECC), 2013, p. 1805–1810.   
[51] D. Sieber, S. Music, and S. Hirche, “Multi-robot manipulation controlled ´ by a human with haptic feedback,” in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2015, p. 2440–2446.   
[52] G. A. Yashin, D. Trinitatova, R. T. Agishev, R. Ibrahimov, and D. Tsetserukou, “Aerovr: Virtual reality-based teleoperation with tactile feedback for aerial manipulation,” in International Conference on Advanced Robotics (ICAR), 2019, p. 767–772.   
[53] S. O. Sachidanandam, S. Honarvar, and Y. Diaz-Mercado, “Effectiveness of augmented reality for human swarm interactions,” in IEEE International Conference on Robotics and Automation (ICRA), 2022, p. 11258–11264.   
[54] M. L. Elwin, B. Strong, R. A. Freeman, and K. M. Lynch, “Humanmultirobot collaborative mobile manipulation: The omnid mocobots,” IEEE Robotics and Automation Letters, vol. 8, no. 1, p. 376–383, 2023.   
[55] D. Sirintuna, I. Ozdamar, and A. Ajoudani, “Carrying the uncarriable: a deformation-agnostic and human-cooperative framework for unwieldy objects using multiple robots,” in IEEE International Conference on Robotics and Automation (ICRA), 2023, pp. 4915–4921.   
[56] N. E. Carey and J. Werfel, “A force-mediated controller for cooperative object manipulation with independent autonomous robots,” in International Symposium on Distributed Autonomous Robotic Systems, 2022.   
[57] G. Li, X. Liu, and G. Loianno, “Rotortm: A flexible simulator for aerial transportation and manipulation,” IEEE Transactions on Robotics, pp. 1–20, 2023.   
[58] G. Li and G. Loianno, “Nonlinear model predictive control for cooperative transportation and manipulation of cable suspended payloads with multiple quadrotors,” in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2023, pp. 1–7.   
[59] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, Robotics Modelling, Planning and Control. Springer London, 2009.   
[60] D. Bertsekas, Nonlinear Programming. Athena Scientific, 1999.   
[61] D. Kraft, “Algorithm 733: Tomp–fortran modules for optimal control calculations,” ACM Trans. Math. Softw., vol. 20, no. 3, p. 262–281, 1994.   
[62] S. G. Johnson, The NLopt nonlinear-optimization package, 2011. [Online]. Available: http://ab-initio.mit.edu/nlopt   
[63] D. Mellinger and V. Kumar, “Minimum snap trajectory generation and control for quadrotors,” in IEEE International Conference on Robotics and Automation (ICRA), 2011, pp. 2520–2525.   
[64] J. Sola, “Quaternion kinematics for the error-state kalman filter,” arXiv preprint arXiv:1711.02508, 2017.   
[65] S. Thrun, W. Burgard, and D. Fox, Probabilistic Robotics. MIT Press, 2005.   
[66] G. Loianno, C. Brunner, G. McGrath, and V. Kumar, “Estimation, control, and planning for aggressive flight with a small quadrotor with a single camera and imu,” IEEE Robotics and Automation Letters, vol. 2, no. 2, pp. 404–411, 2017.   
[67] S. Ren, K. He, R. Girshick, and J. Sun, “Faster R-CNN: Towards realtime object detection with region proposal networks,” in Advances in Neural Information Processing Systems, C. Cortes, N. Lawrence, D. Lee, M. Sugiyama, and R. Garnett, Eds., vol. 28. Curran Associates, Inc., 2015.

![](images/81556b55cbf181fdb8514c509e71712d3b37c9079135a2e1b90bf66b63df604b.jpg)

Guanrui Li is an Assistant Professor at the Worceter Polytechnic Institute (WPI), USA and director of the Aerial-robot Control and Perception Lab (ACP Lab) at WPI. He earned his Ph.D. in Electrical and Computer Engineering at New York University, USA, with a focus on robotics and aerial systems. He obtained his Bachelor degree in Theoretical and Applied Mechanics from Sun Yat-sen University, where he was recognized as an Honors Undergraduate, and his Master degree in Robotics from the GRASP Lab at the University of Pennsylvania. His research is

centered on the dynamics, planning, and control of robotics systems, with applications in aerial transportation and manipulation, as well as human-robot collaboration. Guanrui has received several notable recognitions, including the NSF CPS Rising Stars in 2023, the Outstanding Deployed System Paper Award finalist at 2022 IEEE ICRA, and the 2022 Dante Youla Award for Graduate Research Excellence at NYU. He has an extensive publication record in top-tier robotics conferences and journals like ICRA, RA-L, and T-RO, and his work has garnered attention in various media, including IEEE Spectrum and the Discovery Channel.

![](images/795224a7ebb23a18d027828bb5c985dc27f71122c95f4ab688583ecc7c278f89.jpg)

Xinyang Liu Xinyang Liu was borned in Beijing, China, in 1999. He received his B.S. degree in mechanical engineering with double minors in robotics and computer science from New York University, New York, NY, in 2022, where he was named a University Honor Scholar and was a member of Tau Beta Pi. He is currently in his final year pursuing an M.S. degree in Aeronautics and Astronautics at Stanford University, Stanford, CA. His research interests include control theory, robotics, humanrobot interactions, and autonomous systems.

![](images/2cb8f4e2ba1c861bfcf459d06ce617443faed64fba25019c2b2d97a3e1540d89.jpg)

Giuseppe Loianno is an assistant professor at the New York University, USA and director of the Agile Robotics and Perception Lab (https://wp.nyu.e du/arpl/) working on autonomous robots. He received a Ph.D. in robotics from University of Naples ”Federico II”, Italy in 2014. Prior joining NYU, he was post-doctoral researcher, research scientist and team leader at the GRASP Lab at the University of Pennsylvania in Philadelphia, USA. Dr. Loianno has published more than 70 conference papers, journal papers, and book chapters. His research interests

include perception, learning, and control for autonomous robots. He received the NSF CAREER Award in 2022 and DARPA Young Faculty Award in 2022. He is recipient of the IROS Toshio Fukuda Young Professional Award in 2022, Conference Editorial Board Best Associate Editor Award at ICRA 2022, Best Reviewer Award at ICRA 2016, and he was selected as Rising Star in AI from KAUST in 2023. He is also currently the co-chair of the IEEE RAS Technical Committee on Aerial Robotics and Unmanned Aerial Vehicles. He was the the general chair of the IEEE International Symposium on Safety, Security and Rescue Robotics (SSRR) in 2021 as well as program chair in 2019, 2020, and 2022. His work has been featured in a large number of renowned international news and magazines.