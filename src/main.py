# External imports

# import cv2


# Internal imports

# from hand import HandLandmark, HandResolver
from painter import Painter

# Debug

# import mediapipe

# mp_drawing = mediapipe.solutions.drawing_utils
# mp_drawing_styles = mediapipe.solutions.drawing_styles
# mp_hands = mediapipe.solutions.hands


# Entrypoint

def main() -> None:
    painter = Painter(0)
    painter.run()
    # capture = cv2.VideoCapture(0)
    # hand_resolver = HandResolver(min_detection_confidence=0.85)

    # while True:
    #     _, image = capture.read()
    #     height, width, _ = image.shape

    #     hands = hand_resolver.find_hands(image)

    #     for hand in hands:
    #         deepest = hand.deepest_landmark(
    #             HandLandmark.PINKY_MCP,
    #             HandLandmark.PINKY_DIP,
    #         )

    #         leftmost = hand.leftmost_landmark(
    #             HandLandmark.INDEX_FINGER_MCP,
    #             HandLandmark.PINKY_MCP,
    #         )

    #         #           | Pinky MCP | Pinky DIP
    #         #           -----------------------
    #         # Index MPC |   left    |   right
    #         # Pinky MPC |   right   |   left

    #         a = deepest == HandLandmark.PINKY_MCP
    #         b = leftmost == HandLandmark.PINKY_MCP

    #         # right if a == b else left

    #         mp_drawing.draw_landmarks(
    #             image,
    #             hand.raw_landmarks,
    #             mp_hands.HAND_CONNECTIONS,
    #             mp_drawing_styles.get_default_hand_landmarks_style(),
    #             mp_drawing_styles.get_default_hand_connections_style(),
    #         )

    #     flipped = cv2.flip(image, 1)
    #     cv2.imshow("Image", flipped)
    #     cv2.waitKey(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
