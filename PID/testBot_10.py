from pid_controller_3.pid import PID, twiddle
from pidSim_10 import *
from pprint import pprint
from random import randint

def run_robot(left_p, left_i, left_d, right_p, right_i, right_d):
    leftPid = PID(p=left_p, i=left_i, d=left_d)
    rightPid = PID(p=right_p, i=right_i, d=right_d)
    
    # We want to drive the robot towards the 0 angle.
    leftPid.target = 0
    rightPid.target = 0
    
    target = Target(CANVAS_SIZE['width'] - 50, CANVAS_SIZE['height']/4)
    target = Target(CANVAS_SIZE['width'] * 5.5, -4 * CANVAS_SIZE['height'])
    
    robot = Robot(25, CANVAS_SIZE['height'], target)
    
    N = 1000
    
    for step in range(N):
        #Y = robot.y - 0 # error
        #cte_sum += Y#should be here?
        #alpha = -tau_p * Y - tau_d * (Y - Y_last) - tau_i * cte_sum
        
        robot.updateError()
        
        leftAlpha = leftPid(feedback=robot.error, curr_tm=step)
        rightAlpha = rightPid(feedback=robot.error, curr_tm=step)
        
        #print(step, robot.error, leftAlpha, rightAlpha)
        
        robot.setLeftVelocity(leftAlpha)
        robot.setRightVelocity(rightAlpha)
        
        #print("dist:",robot.distanceToTarget(), robot.error)
        
        if robot.distanceToTarget() < .001:
            print("BREAK")
            break
        
        robot.move()

    return {'left' : leftPid.error, 'right' : rightPid.error}

if __name__ == "__main__":
    initial_guess = (0.4, 0.03, 1.5)
    start_guess = initial_guess + initial_guess
    err0 = run_robot(*start_guess)
        
    print("=====================================")
    
    best_params = twiddle(
        evaluator=run_robot,
        params=3,
        tol=0.0001,
        initial_guess=initial_guess)
    err1 = run_robot(left_p=best_params['left'][0], 
                                 left_i=best_params['left'][1], 
                                 left_d=best_params['left'][2], 
                                 right_p=best_params['right'][0], 
                                 right_i=best_params['right'][1], 
                                 right_d=best_params['right'][2])
    
    print("---------------------------")
    print("err0", err0)
    print("initial_guess", initial_guess)
    print()
    print("err1", err1)
    print("best_params") 
    pprint(best_params)