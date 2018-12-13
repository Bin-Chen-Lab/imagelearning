from PIL import Image
import glob, os, sys


def main(filename):
    sizes = [(1024,1024), (29,29), (40,40), (50,50), (57,57), (60,60), (72,72), (76,76), (83.5,83.5)]

    for i in sizes:
        try:
            im = Image.open(filename)
        except IOError as e:
            print("Sorry that file does not exist, stopping the program")
            sys.exit(1)
        im.thumbnail(i)
        #AVCam_Icon_29x29@3x.png
        im.save( "Keith_Icon_" + str(i[0]) + "x" + str(i[1])+"@1x.jpg")
    print("Standard sizes created!")


if __name__ == '__main__':
    filename = input("What is the image file you want standardized: ")

    main(filename)
