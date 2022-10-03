# External imports

import cv2
import mediapipe
import numpy as np


# Internal imports

from .hand import Hand


# Protected mediapipe types

_Hands = mediapipe.solutions.hands.Hands


# Public Types

class Resolver:
    # Lifecycle methods

    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self.__hand_resolver = _Hands(
            static_image_mode,
            max_num_hands,
            model_complexity,
            min_detection_confidence,
            min_tracking_confidence,
        )


    # Public methods

    def find_hands(
        self,
        image: np.ndarray,
    ) -> list[Hand]:
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.__hand_resolver.process(image)

        return [
            Hand(landmarks)
            for landmarks in (results.multi_hand_landmarks or [])
        ]
