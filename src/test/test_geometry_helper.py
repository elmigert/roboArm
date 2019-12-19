#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the GeometryHelper class test.
"""

import unittest

from src.robot_error import RobotError, ErrorCode
from src.geometry_helper import GeometryHelper


class TestGeometryHelper(unittest.TestCase):
    """
    GeometryHelper test.
    """
    def test_transform_position_user_to_uarm(self):
        """
        Test transform_position_user_to_uarm function.
        """
        geometry_helper = GeometryHelper()
        pose_1 = geometry_helper.transform_position_user_to_uarm(7, 7, 2)
        pose_2 = geometry_helper.transform_position_user_to_uarm(0, 0, 1)
        pose_3 = geometry_helper.transform_position_user_to_uarm(0, 15, 2)

        self.assertEqual(pose_1['x'], 300.0)
        self.assertEqual(pose_1['y'], -20.0)
        self.assertEqual(pose_2['x'], 20.0)
        self.assertEqual(pose_2['y'], -300.0)
        self.assertEqual(pose_3['x'], 20.0)
        self.assertEqual(pose_3['y'], 300.0)

        with self.assertRaises(RobotError) as raised:
            geometry_helper.transform_position_user_to_uarm(10, 10, 1)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0000)

    def test_calculate_equal_wrist_rotation(self):
        """
        Test the calculate_equal_wrist_rotation function.
        """
        geometry_helper = GeometryHelper()
        wrist_angle_1 = geometry_helper.calculate_equal_wrist_rotation(100, 100, 100, 0, 45)
        test_wrist_angle_1 = 0
        self.assertEqual(wrist_angle_1, test_wrist_angle_1)

        wrist_angle_2 = geometry_helper.calculate_equal_wrist_rotation(100, 100, 100, 100, 45)
        test_wrist_angle_2 = 45
        self.assertEqual(wrist_angle_2, test_wrist_angle_2)

        with self.assertRaises(RobotError) as raised:
            wrist_angle_3 = geometry_helper.calculate_equal_wrist_rotation(100, 100, 100, -100, -135)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0003)

    def test_transform_height_user_to_uarm(self):
        """
        Test the transform_height_user_to_uarm function.
        """
        geometry_helper = GeometryHelper()
        z_uarm_1 = geometry_helper.transform_height_user_to_uarm(1, 100, 100)
        test_z_uarm_1 = 40.0
        self.assertEqual(z_uarm_1, test_z_uarm_1)

        z_uarm_2 = geometry_helper.transform_height_user_to_uarm(2, 200, 200)
        test_z_uarm_2 = 80.0
        self.assertEqual(z_uarm_2, test_z_uarm_2)

        with self.assertRaises(RobotError) as raised:
            geometry_helper.transform_height_user_to_uarm(10, 100, 100)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0004)
