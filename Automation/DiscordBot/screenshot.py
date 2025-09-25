import cv2


def screenshot():
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval:
        cv2.imwrite("screen.png", frame)
    cam.release()
    return retval


if __name__ == "__main__":
    screenshot()