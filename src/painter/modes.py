# External imoprts

from typing import ForwardRef


# Internal imports

from hand import Hand, HandLandmark


# Public types

class Mode:
    # Lifecycle methods

    def __init__(
        self,
        position: tuple[float],
    ) -> None:
        self.position: tuple[float] = position


    # Static methods
    @staticmethod
    def from_hand(
        hand: Hand,
    ) -> ForwardRef('Mode'):
        # Thumb is outside index / pink MCP gap = no mode
        leftmost = hand.leftmost_landmark(
            HandLandmark.THUMB_TIP,
            HandLandmark.INDEX_FINGER_MCP,
        )
        if leftmost == HandLandmark.INDEX_FINGER_MCP:
            return None

        index_position: tuple[float] = hand.landmark_position_xy(
            HandLandmark.INDEX_FINGER_TIP,
        )

        # Index finger is up, and thumb is between the index / pinky MCP
        #   Closer to index = paint mode
        #   Closer to pinky = erase mode
        if hand.is_only_finger_up(HandLandmark.INDEX_FINGER_TIP):
            return Paint(index_position)

            # distance_index = hand.distance_between_landmarks(
            #     HandLandmark.THUMB_TIP,
            #     HandLandmark.INDEX_FINGER_MCP,
            # )
            # distance_pinky = hand.distance_between_landmarks(
            #     HandLandmark.THUMB_TIP,
            #     HandLandmark.PINKY_MCP,
            # )

            # if distance_index <= distance_pinky:
            #     return Paint(index_position)
            # else:
            #     return Erase(index_position)

        # Index and middle fingers are up = color select mode
        index_and_pinky_up = hand.is_only_fingers_up(
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.MIDDLE_FINGER_TIP,
        )
        if index_and_pinky_up:
            return Erase(index_position)

        # Index and pink fingers are up = color select mode
        index_and_pinky_up = hand.is_only_fingers_up(
            HandLandmark.INDEX_FINGER_TIP,
            HandLandmark.PINKY_TIP,
        )
        if index_and_pinky_up:
            return ColorSelect(index_position)




class Paint(Mode):
    pass


class Erase(Mode):
    pass


class ColorSelect(Mode):
    pass
