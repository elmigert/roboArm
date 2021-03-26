#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the RobotHandler class, which handles the communication with the uArm Swift pro.
"""

import time




from libraries.uArm_Python_SDK.uarm.wrapper import SwiftAPI
from src.geometry_helper import GeometryHelper
from src.robot_error import ErrorCode, RobotError
from src.user_challenge import UserChallenge


class RobotHandler:
    def __init__(self):
        """
        Connect on initialization.
        """
        # connect to uArm
        self.__swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        self.__swift.waiting_ready(timeout=5)
        # set general mode: 0
        self.__swift.set_mode(0)

        # TODO (ALR): Measure Servo offset again once uArm is installed.
        # set measured wrist servo scaling offset
        # It's 90+-78
        self.__lower_servo_limit = 12.0
        self.__higher_servo_limit = 168.0
        self.__angle_range_servo_limit = self.__higher_servo_limit-self.__lower_servo_limit
        self.__pick_up_height_correction = -9

        # set sleep time to wait for servo to finish
        self.__sleep_time = 1.0

        # initialize geometry helper
        self.__geometry_helper = GeometryHelper()

        # initialize empty position values
        self.__x_uarm = 0
        self.__y_uarm = 0
        self.__z_uarm = 0
        self.__wrist_angle = 0
        # set values and move to predefined position (3, 8)
        self.reset()

    def disconnect(self):
        """
        Disconnect robot.
        """
        self.__swift.flush_cmd()
        time.sleep(3)
        self.__swift.disconnect()

    def reset(self):
        """
        Reset robot, go back to start position.
        """
        # reset arm to home
        self.__swift.reset(wait=True, speed=10000)
        # get pose values in uarm frame
        pose = self.__swift.get_position()
        # check if successful
        if isinstance(pose, list):
            self.__x_uarm = pose[0]
            self.__y_uarm = pose[1]
            self.__z_uarm = pose[2]
        else:
            message = "Die Roboter Position konnte nicht gelesen werden, überprüfe die Verbindung."
            raise RobotError(ErrorCode.E0001, message)
        
        self.pump_off()
        # set servo value in degrees
        wrist_angle = 90.0
        self.__swift.set_servo_angle(servo_id=3, angle=wrist_angle)
        self.__wrist_angle = wrist_angle


        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

        # move to fix starting position
        self.position_new([3, 8])
        self.height_new([2])
        self.__swift.flush_cmd()

    def position_new(self, position_user):
        """
        Move robot arm to new position x, y in user frame.
        :param position_user: position in user frame [x_user, y_user]
        :type position_user: list[int]
        """
        [x_user, y_user] = position_user
        self.x_user = x_user
        self.y_user = y_user
        # transform frames of positions
        uarm_dict = self.__geometry_helper.transform_position_user_to_uarm(x_user, y_user, self.__z_uarm)
        x_uarm_new = uarm_dict['x']
        y_uarm_new = uarm_dict['y']

        # calculate new wrist angle that keeps object in the same orientation
        wrist_angle_new = self.__geometry_helper.calculate_equal_wrist_rotation_new(self.__x_uarm, x_uarm_new,
                                                                                self.__y_uarm, y_uarm_new,
                                                                                self.__wrist_angle)
        #z_uarm_new = self.__geometry_helper.transform_height_user_to_uarm(self.__z_uarm, x_uarm_new, y_uarm_new)
        self.__swift.set_position(x=x_uarm_new, y=y_uarm_new)
        self.__swift.set_wrist(angle=wrist_angle_new, wait=True)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

        # set new values
        self.__x_uarm = x_uarm_new
        self.__y_uarm = y_uarm_new
        # set wrist angle to new, not to corrected because the correction is only for the motor
        self.__wrist_angle = wrist_angle_new

    def height_new(self, z_user_list):
        """x_uarm_new
        Move robot arm to z position in user frame.
        :param z_user_list: new height in user frame [z_user]
        :type z_user_list: list[int]
        """
        z_user = z_user_list[0]
        # calculate new height in uarm frame
        z_uarm_new = self.__geometry_helper.transform_height_user_to_uarm(z_user, self.__x_uarm, self.__y_uarm)

        # move arm
        self.__swift.set_position(z=z_uarm_new)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

        # set values
        self.__z_uarm = z_uarm_new

    def pump_on(self):
        """
        Turn on the pump.
        """
        #Correct angle to allow a wide range of corrections
        angle =  self.__geometry_helper.adjust_wrist_rotation_before_pumpe_an(self.x_user,self.y_user)
        self.__wrist_angle = angle
        self.__swift.set_servo_angle(servo_id=3,angle = self.__wrist_angle)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)
        
       

        # move arm slightly down (those, the arm will not touch blocks and only grips them if the pump is on)
        z_uarm_corrected = self.__z_uarm +self.__pick_up_height_correction
        self.__swift.set_position(z=z_uarm_corrected)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)
        
        # TUrns pump on
        self.__swift.set_pump(on=True)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)
        
        # move arm slightly up again to reach previous position
        z_uarm_corrected = self.__z_uarm -self.__pick_up_height_correction
        self.__swift.set_position(z=z_uarm_corrected)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)

    def pump_off(self):
        """
        Turn off the pump.
        """
        self.__swift.set_pump(on=False)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)
   
    def drehen(self, rotation):
        rotation = rotation[0]
        current_angle = self.__wrist_angle
        angle = self.__geometry_helper.gripper_angle_rotation(current_angle,rotation)
        self.__wrist_angle = angle
        self.__swift.set_servo_angle(servo_id=3,angle = self.__wrist_angle)
        self.__swift.flush_cmd()
        time.sleep(self.__sleep_time)
 
        

    
    def test_c(self,*args):
        # Function only for testing

        if len(args) == 1:
            rotation = (args[0])[0]
        else:
            rotation = 90
        print("Checking servo limits")
        
        # Servo Test
        if len(args) == 1:
            if (args[0])[0] == 0:
                for rot in range (22,120,10):
                    print("angle {}".format(rot))
                    self.__wrist_angle = self.__wrist_servo_correction(rot)
                    self.__swift.set_servo_angle(servo_id=3,angle = self.__wrist_angle)
                    self.__swift.flush_cmd()
                    time.sleep(self.__sleep_time*2)
            elif (args[0])[0] == 1:
            
                for x in range( 5,7,1):
                    for y in range(3,12,1):
                        self.position_new([x,y])
                    
                    
           
        
        
        

    def __wrist_servo_correction(self, wrist_angle):
        """
        Correct wrist servo offset / scaling.
        :param wrist_angle: geometrically calculated wrist angle
        :type wrist_angle: float
        :return: corrected / scaled wrist angle according to servo offset
        :rtype: float
        """
        # linearly scaling angle to real wrist limits
        if wrist_angle <= 90.0:
            wrist_angle_corrected = (wrist_angle - self.__lower_servo_limit) * 90.0 / (90.0 - self.__lower_servo_limit)
        else:
            wrist_angle_corrected = 90.0 + 90.0 * (wrist_angle - 90) / (self.__higher_servo_limit - 90.0)

        return wrist_angle_corrected
    def __wrist_angle_limits(self,wrist_angle):
        # If wrist angle is inside the limit, return the percentage of the low and upper limit. Otherwise, return false
        
        angle_limit_ratio = (wrist_angle - self.__lower_servo_limit)/(self.__angle_range_servo_limit)
        
        if angle_limit_ratio >=0 and angle_limit_ratio <= 1:
            return angle_limit_ratio
        else:
            return False
        
    
    def __wrist_servo_correction_new(self, wrist_angle):
        """
        Correct wrist servo offset / scaling.
        :param wrist_angle: geometrically calculated wrist angle
        :type wrist_angle: float
        :return: corrected / scaled wrist angle according to servo offset
        :rtype: float
        """
        # linearly scaling angle to real wrist limits
        if wrist_angle < self.__lower_servo_limit:
            pass
        if wrist_angle > self.__higher_servo_limit:
            pass
        return wrist_angle
