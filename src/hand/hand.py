# External imports

from cv2 import sqrt
import mediapipe
import numpy as np
import math


# Public mediapipe types

Landmark = mediapipe.solutions.hands.HandLandmark


# Protected mediapipe types

_NormalizedLandmarkList = mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList


# Public types

class Hand:
    # Private Constants
    __FINGER_TIPS = {
        Landmark.INDEX_FINGER_TIP,
        Landmark.MIDDLE_FINGER_TIP,
        Landmark.RING_FINGER_TIP,
        Landmark.PINKY_TIP,
    }



    # Lifecycle methods

    def __init__(
        self,
        landmarks: _NormalizedLandmarkList
    ) -> None:
        self.raw_landmarks = landmarks
        self.__landmarks = landmarks.landmark


    # Public methods

    def is_finger_up(
        self,
        finger_tip: Landmark,
    ) -> bool:
        if not finger_tip in self.__FINGER_TIPS:
            return False

        # Iterate over finger landmarks, and determine if they are above
        #   the previous landmark
        for landmark in range(finger_tip - 2, finger_tip):
            curr_y = self.__landmarks[landmark].y
            prev_y = self.__landmarks[landmark - 1].y

            if curr_y >= prev_y:
                return False

        return True


    def is_only_finger_up(
        self,
        finger_tip: Landmark,
    ) -> bool:
        if not finger_tip in self.__FINGER_TIPS:
            return False

        # Check finger is actually up
        if not self.is_finger_up(finger_tip):
            return False

        # Check that other finger tips aren't up
        for other_finger_tip in self.__FINGER_TIPS - {finger_tip}:
            if self.is_finger_up(other_finger_tip):
                return False

        return True


    def is_only_fingers_up(
        self,
        *finger_tips: tuple[Landmark],
    ) -> bool:
        finger_tips: set[Landmark] = {*finger_tips}

        if not finger_tips < self.__FINGER_TIPS:
            return False

        # Check fingers are actually up
        for finger_tip in finger_tips:
            if not self.is_finger_up(finger_tip):
                return False

        # Check that other finger tips aren't up
        for other_finger_tip in self.__FINGER_TIPS - finger_tips:
            if self.is_finger_up(other_finger_tip):
                return False

        return True


    def deepest_landmark(
        self,
        a: Landmark,
        b: Landmark,
    ) -> Landmark:
        la = self.__landmarks[a]
        lb = self.__landmarks[b]

        return a if la.z >= lb.z else b



    def distance_between_landmarks(
        self,
        a: Landmark,
        b: Landmark
    ) -> float:
        la = self.__landmarks[a]
        lb = self.__landmarks[b]

        # Calculate delta between points
        dx = (la.x - lb.x)
        dy = (la.y - lb.y)

        # Calculate distance
        return math.sqrt(dx ** 2 + dy ** 2)


    def leftmost_landmark(
        self,
        a: Landmark,
        b: Landmark,
    ) -> Landmark:
        la = self.__landmarks[a]
        lb = self.__landmarks[b]

        return a if la.x <= lb.x else b


    def landmark_position_xy(
        self,
        landmark: Landmark,
    ) -> tuple[float]:
        position = self.__landmarks[landmark]
        return (position.x, position.y)
