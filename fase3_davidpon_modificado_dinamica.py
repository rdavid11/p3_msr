import pybullet as p
import pybullet_data
import time
import math
import csv

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.setRealTimeSimulation(1)

planeID = p.loadURDF("plane.urdf")

euler_angles = [0, 0, math.pi/2]
startOrientation = p.getQuaternionFromEuler(euler_angles)
start_position = [0, 0, 1]
robotID = p.loadURDF("husky/husky.urdf", start_position, startOrientation)

euler_angles = [0, 0, math.pi/2]
startOrientation = p.getQuaternionFromEuler(euler_angles)
start_position = [0, 10, 1]
rampID = p.loadURDF("rampa.urdf", start_position, startOrientation)

euler_angles = [0, 0, math.pi/2]
startOrientation = p.getQuaternionFromEuler(euler_angles)
start_position = [0, 30, 1]
barrierID = p.loadURDF("barrera.urdf", start_position, startOrientation)

euler_angles = [0, 0, math.pi/2]
startOrientation = p.getQuaternionFromEuler(euler_angles)
start_position = [0, 25, 1]
goalID = p.loadURDF("plataforma.urdf", start_position, startOrientation, useFixedBase=True)

numJoints = p.getNumJoints(robotID)
print("n joints: ", numJoints)

for j in range(numJoints):
    print("%d - %s" % (p.getJointInfo(robotID, j)[0], p.getJointInfo(robotID, j)[1]))

# numJoints = p.getNumLinks(barrierID)
# print("n joints: ", numJoints)
# for j in range(numJoints):
#     # print("%d - %s" % (p.getJointInfo(barrierID, j)[0], p.getJointInfo(barrierID, j)[1]))
#     link_name = p.getJointInfo(barrierID, j)[12].decode("utf-8")
#     print(f"Link {j}: {link_name}")

num_joints = p.getNumJoints(barrierID)

for i in range(num_joints):
    joint_info = p.getJointInfo(barrierID, i)
    link_name = joint_info[12].decode("utf-8")
    print(f"Link {i}: {link_name}")


wheels = [2, 3, 4, 5]
final_data = []
final_data.append(["TIME", "POS_Y", "VEL_Y", "V_WHEEL", "F_WHEEL"])
last_dist = 0
t0 = time.time()
Vw = 11
maxForce = 25

lf = 0.93
sf = 0.005
rf = 0.003

for wheel in wheels:
	p.changeDynamics(robotID, wheel,
	                 lateralFriction=lf, 
	                 spinningFriction=sf, 
	                 rollingFriction=rf)
     

p.changeDynamics(goalID, -1,
	                 lateralFriction=0.25, 
	                 spinningFriction=0.25, 
	                 rollingFriction=0.2)

p.changeDynamics(barrierID, 0, localInertiaDiagonal=[1.2625, 11.2625, 12.5])

input("pres enter to start")


pos, ori = p.getBasePositionAndOrientation(barrierID)
sstart_pos = pos[0] 

for i in range (10000):

    # wheels = [2, 3, 4, 5]
    p.setJointMotorControlArray(robotID, wheels,
                                p.VELOCITY_CONTROL,
                                targetVelocities=[Vw, Vw, Vw, Vw],
                                forces=[maxForce, maxForce, maxForce, maxForce])
    
    pos, ori = p.getBasePositionAndOrientation(robotID)
    # print(pos)
    if (pos[1] - last_dist >= 0.01):
        data = []
        data.append(time.time())
        data.append(pos[1])
        data.append(p.getBaseVelocity(robotID)[0][1])
        data.append(Vw)
        data.append(maxForce)

        final_data.append(data)
        
        last_dist = pos[1]
        

    state = p.getJointState(barrierID, 0)
    b_pos = state[0]
    
    print(f"pos: {b_pos}")
    actual_pos = pos[0]
    print(f"moved: {actual_pos - sstart_pos}")
    if (b_pos >= 1):
        break

    # p.stepSimulation()
    time.sleep(1./240.)

with open("archivo.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

p.disconnect()