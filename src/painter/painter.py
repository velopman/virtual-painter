# External imports

import cv2
import numpy


# Internal imports

from hand import Hand, HandResolver
from .modes import Mode, Paint, Erase, ColorSelect


# Public types

class Painter:
    # Lifecycle methods

    def __init__(
        self,
        camera: int = 0,
    ) -> None:
        self.__color: tuple[int] = (176, 123, 136)
        self.__current_mode: Mode = None

        self.__canvas: numpy.ndarray = numpy.zeros((720, 1280, 3), numpy.uint8)
        self.__capture: cv2.VideoCapture = cv2.VideoCapture(camera)
        self.__resolver: HandResolver = HandResolver(min_detection_confidence=0.85)


    # Public methods

    def run(
        self,
    ) -> None:
        while True:
            _, image = self.__capture.read()
            hands = self.__resolver.find_hands(image)

            self.__process(hands)

            image_gray = cv2.cvtColor(self.__canvas, cv2.COLOR_RGB2GRAY)
            _, image_inverse = cv2.threshold(
                image_gray,
                50,
                255,
                cv2.THRESH_BINARY_INV,
            )
            image_inverse = cv2.cvtColor(
                image_inverse,
                cv2.COLOR_GRAY2BGR,
            )
            image = cv2.bitwise_and(image, image_inverse)
            image = cv2.bitwise_or(image, self.__canvas)

            flipped = cv2.flip(image, 1)
            cv2.imshow("Image", flipped)
            cv2.waitKey(1)


    # Private methods

    def __process(
        self,
        hands: list[Hand],
    ) -> None:
        if len(hands) == 0:
            return

        mode = Mode.from_hand(hands[0])

        if type(mode) is Paint:
            start = mode.position
            if self.__current_mode:
                start = self.__current_mode.position

            start = self.__scale(start)
            end = self.__scale(mode.position)

            cv2.line(
                self.__canvas,
                start,
                end,
                (0, 255, 0),
                15,
            )
        elif type(mode) is Erase:
            start = mode.position
            if self.__current_mode:
                start = self.__current_mode.position

            start = self.__scale(start)
            end = self.__scale(mode.position)

            cv2.line(
                self.__canvas,
                start,
                end,
                (0, 0, 0),
                30,
            )

        self.__current_mode = mode


    # Private methods

    def __scale(
        self,
        position: tuple[float],
    ) -> tuple[int]:
        return (
            int(position[0] * 1280),
            int(position[1] * 720),
        )
