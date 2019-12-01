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
        pose_1 = geometry_helper.transform_position_user_to_uarm(7, 7)
        pose_2 = geometry_helper.transform_position_user_to_uarm(0, 0)
        pose_3 = geometry_helper.transform_position_user_to_uarm(0, 15)

        self.assertEqual(pose_1['x'], 300.0)
        self.assertEqual(pose_1['y'], -20.0)
        self.assertEqual(pose_2['x'], 20.0)
        self.assertEqual(pose_2['y'], -300.0)
        self.assertEqual(pose_3['x'], 20.0)
        self.assertEqual(pose_3['y'], 300.0)

        with self.assertRaises(RobotError) as raised:
            geometry_helper.transform_position_user_to_uarm(10, 10)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0000)
