import unittest
from unittest.mock import MagicMock, patch
from typing import List, Literal, Callable
from dataclasses import dataclass
from typing import Literal

import cv2
import numpy as np

from upic.vision.tagdetector import TagDetector


sleep = MagicMock()

class TestTagDetector(unittest.TestCase):
    def setUp(self):
        self.detector = TagDetector()

    def tearDown(self):
        self.detector.release_camera()

    def test_init(self):
        self.assertIsNone(self.detector._camera)
        self.assertEqual(self.detector._tag_id, TagDetector.Config.default_tag_id)

    def test_reopen_cam(self):
        self.detector.open_camera(0)
        self.detector.release_camera()
        self.detector.open_camera(0)
        self.assertIsNotNone(self.detector._camera)

    def test_open_camera(self):
        self.detector.open_camera(0)
        self.assertIsNotNone(self.detector._camera)
        self.assertIsInstance(self.detector.camera_device, cv2.VideoCapture)

    def test_release_camera(self):
        self.detector.open_camera(0)
        self.detector.release_camera()
        self.assertIsNone(self.detector._camera)

    def test_apriltag_detect_start_stop(self):
        with self.assertRaises(ValueError):
            self.detector.apriltag_detect_start()
        self.detector.open_camera().apriltag_detect_start()
        self.assertTrue(self.detector._continue_detection)
        self.detector.apriltag_detect_end()
        self.assertFalse(self.detector._continue_detection)

    def test_halt_resume_detection(self):
        with self.assertRaises(ValueError):
            self.detector.apriltag_detect_start()
        self.detector.open_camera().apriltag_detect_start()
        self.detector.halt_detection()
        self.assertTrue(self.detector._halt_detection)
        self.detector.resume_detection()
        self.assertFalse(self.detector._halt_detection)

    def test_set_cam_resolution(self):
        self.detector.open_camera(0)
        self.detector.set_cam_resolution(640, 480)

    def test_tag_id_accessor(self):
        self.assertEqual(self.detector.tag_id, TagDetector.Config.default_tag_id)

if __name__ == '__main__':
    unittest.main()
