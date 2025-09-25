from PIL import Image
import cv2
import datetime, shutil


def screenshot():
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval:
        path = "../screen.png"
        cv2.imwrite(path, frame)
    cam.release()
    return retval

def save_screenshot_file():
    shutil.copy("../screen.png", "../Pictures/")
    new_path = f"../Pictures/{str(datetime.datetime.now().strftime("%y%m%d%H%S"))}.png"
    shutil.move(f"../Pictures/screen.png", new_path)
    return new_path

def load_screenshot():
    im = Image.open('../screen.png')
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i+1) * width] for i in range(height)]
    return pixels

def save_screenshot():
    screenshot()
    path = save_screenshot_file()
    return path

def check_shiny():
    def dist(p1, p2):
        return sum([ (p1[i]-p2[i])**2 for i in range(3) ])**0.5

    screenshot()
    img = load_screenshot()
    
    shiny = img[183][1883] == (101, 103, 100)
    present = dist(img[31][1883], (218, 221, 218)) <= 20

    return shiny, present

if __name__ =="__main__":
    print(save_screenshot_file())
