from PIL import Image
import cv2


def screenshot():
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval:
        cv2.imwrite("../screen.png", frame)
    cam.release()
    return retval


def load_screenshot():
    im = Image.open('../screen.png')
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i+1) * width] for i in range(height)]
    return pixels


def check_shiny():
    def dist(p1, p2):
        return sum([ (p1[i]-p2[i])**2 for i in range(3) ])**0.5

    screenshot()
    img = load_screenshot()

    # for r in range(len(img)):
    #     for c in range(len(img[0])):
    #         if img[r][c] == (216, 219, 213):
    #             print(r, c)

    return img[183][1883] == (101, 103, 100), dist(img[31][1883], (218, 221, 218)) <= 20

if __name__ =="__main__":
    print(check_shiny())
