import pybullet as p
import pybullet_data
import time
import math
import csv

class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0):
        # Coeficientes PID
        self.kp = kp  # Proporcional
        self.ki = ki  # Integral
        self.kd = kd  # Derivativo
        self.setpoint = setpoint  # Valor objetivo o deseado

        # Variables de control
        self.prev_error = 0
        self.integral = 0
        self.prev_time = time.time()

    def update(self, feedback_value):
        # Calcular el error actual
        error = self.setpoint - feedback_value

        # Obtener el tiempo actual y dt
        current_time = time.time()
        dt = current_time - self.prev_time

        # Calcular las tres partes del PID: P, I, y D
        proportional = self.kp * error
        # return proportional

        self.integral += error * dt  # Acumular el error para la parte integral
        integral = self.ki * self.integral

        derivative = self.kd * (error - self.prev_error) / dt

        # Salida del PID
        output = proportional + integral + derivative

        # Guardar los valores del ciclo anterior
        self.prev_error = error
        self.prev_time = current_time

        return output

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

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
start_position = [0, 25, 0]
goalID = p.loadURDF("plataforma.urdf", start_position, startOrientation, useFixedBase=True)

numJoints = p.getNumJoints(robotID)
print("n joints: ", numJoints)

for j in range(numJoints):
    print("%d - %s" % (p.getJointInfo(robotID, j)[0], p.getJointInfo(robotID, j)[1]))

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


linearPID = PIDController(kp=20, ki=3, kd=0, setpoint=2)
v = 11
f = 25
for i in range (10000):
    Vy = p.getBaseVelocity(robotID)[0][1]
    pos, ori = p.getBasePositionAndOrientation(robotID)
    p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=4, cameraPitch=-30,
                                cameraTargetPosition=pos)

    print("f: ", f)
    print("v: ", v)
    print("y: ", Vy)
    
    if (ori[0] > 0.07):
        print("rampa")
        linearPID.setpoint = 3.5
        f = 35
        v = linearPID.update(Vy)
        p.setJointMotorControlArray(robotID, [2,3],
		                            p.VELOCITY_CONTROL,
		                            targetVelocities=[11, 11],
		                            forces=[25, 25])
        p.setJointMotorControlArray(robotID, [4,5],
		                            p.VELOCITY_CONTROL,
		                            targetVelocities=[v, v],
		                            forces=[f, f])

    elif (ori[0] < -0.07):
        print("rampa")
        # f = 25
        linearPID.setpoint = 1
        v = linearPID.update(Vy)
        v = clamp(v, -20, 10)
        p.setJointMotorControlArray(robotID, [2,3],
		                            p.VELOCITY_CONTROL,
		                            targetVelocities=[v, v],
		                            forces=[f, f])
        p.setJointMotorControlArray(robotID, [4, 5],
		                            p.VELOCITY_CONTROL,
		                            targetVelocities=[11, 11],
		                            forces=[25,25])
        
    else:
        print("plano")
        f = 25
        v = 11
        p.setJointMotorControlArray(robotID, wheels,
		                            p.VELOCITY_CONTROL,
		                            targetVelocities=[11]*4,
		                            forces=[25]*4)
        

    if (pos[1] - last_dist >= 0.01):
        data = []
        data.append(time.time())
        data.append(pos[1])
        data.append(Vy)
        data.append(Vw)
        data.append(maxForce)

        final_data.append(data)
        
        last_dist = pos[1]


    state = p.getJointState(barrierID, 0)
    b_pos = state[0]
    
    print(f"pos: {b_pos}")
    # actual_pos = pos[0]
    # print(f"moved: {actual_pos - sstart_pos}")
    if (b_pos >= 1):
        break
    # if (pos[1] > 21):
    #     break

    time.sleep(1./240.)

with open("archivo.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

p.disconnect()