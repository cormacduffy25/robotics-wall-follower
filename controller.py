from controller import Robot

def run_robot(robot):
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    # Setting Max Speed
    max_speed = 6.28

    # Enabling Motors
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)

    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)

    # Enabling Proximity Sensors 
    p_sensors = []
    for ind in range(8):
        sensor_name = "ps" + str(ind)
        p_sensors.append(robot.getDevice(sensor_name))
        p_sensors[ind].enable(timestep)

    # Perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        # Print sensor values
        for ind in range(8):
            print("ind: {}, val: {}".format(ind, p_sensors[ind].getValue()))

        # Define conditions based on sensor values
        left_wall = p_sensors[5].getValue() > 80.0
        too_close = p_sensors[6].getValue() > 80.0
        wall_front = p_sensors[7].getValue() > 80.0 and p_sensors[0].getValue() > 80.0
        right_wall = p_sensors[2].getValue() > 80.0
       # no_wall = all(p_sensors[i].getValue() < 71.0 for i in range(8))
        # Set initial motor speeds
        left_speed = max_speed
        right_speed = max_speed
      
        # Adjust speeds based on sensor inputs    
        if wall_front:
            print("Front Wall Detected Turning Right")
            left_speed = max_speed
            right_speed = -max_speed
        else: 
            if left_wall:
                print("Left Wall Detected Drive Forward")
                left_speed = max_speed 
                right_speed = max_speed 
            else:
                if right_wall:
                    print("Right Wall Detected")
                    left_speed = max_speed
                    right_speed = -max_speed           
                else: 
                    print("Turn Left")
                    left_speed = max_speed/2.5
                    right_speed = max_speed
     
        if too_close:
            print("Too Close Left Wall")
            left_speed = max_speed
            right_speed = -max_speed
      #  if no_wall:
       #     print("No Wall")
        #    left_speed = max_speed*0.7
         #   right_speed = max_speed*0.75  

        # Apply calculated speeds to motors
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

# Main execution block
if __name__ == "__main__":
    wall_bot = Robot()
    run_robot(wall_bot)