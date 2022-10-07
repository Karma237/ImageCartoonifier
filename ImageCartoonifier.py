'''

 Name : Karma Yasser Ismail Mahmoud
 Project : Cartoonify the Image
 Machine Learning Intern associated by Intern'spedia

'''

# Importing Libraries

# For GUI
from tkinter import *
import tkinter as tk
import tkinter.font as font           # To use Font on the window
from tkinter import filedialog as fd  # To Select Image from device by button
from PIL import ImageTk, Image

# for Plotting
import sys
import matplotlib.pyplot as plt

# For Image processing / Computer Vision From opencv Package
import cv2
import os

# -------------------------------------------------------------------------------------------------

# GUI

MainWindow = tk.Tk()
MainWindow.title("Image Cartoonifier")

Canvas = tk.Canvas(MainWindow, width=600, height=623)
Canvas.grid(columnspan=3)

# Logo

logo = Image.open("logo.jpg")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

# button
txt = tk.StringVar()
btnFont = font.Font(family='Comic Sans MS', weight='bold', slant='italic')
btn = Button(MainWindow, textvariable=txt, font=btnFont,command=lambda :Cartoonify(), bg="#104E8B", fg="white", width=50, height=2,activeforeground='#104E8B')
txt.set("Select an Image from your device to be Cartoonified")
btn.grid(column=1, row=30)

# -----------------------------------------------------------------------------------------------------

def ReadImage(ImgPath):
    ChosenOriginally = cv2.imread(ImgPath)  # To Store The image as number
    ChosenOriginally = cv2.cvtColor(ChosenOriginally, cv2.COLOR_BGR2RGB ) # Convert From BGR To RGB to be saved as a correct Image
    # print(ChosenOriginally) to show the Image number matrix

    # Check if the selected file is an image type aka JPEG , PNG
    if ChosenOriginally is None:
        print("The Choosen File is not an Image.\n Please, Choose appropriate file")
        sys.exit()

    Resized1 = cv2.resize(ChosenOriginally, (960, 540))  # To Resize Image

    # plt.imshow(ResizedImage, cmap='gray')   # To plot Image after Resizing
    return Resized1, ChosenOriginally

def GrayScale(original):
    # Convert Image to Grey Scale
    GrayScaled = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  # Convert to grey
    Resized2 = cv2.resize(GrayScaled, (960, 540))
    # plt.imshow(ReSized2, cmap='gray')
    return Resized2, GrayScaled

def SmoothImage(gray):
    # applying median blur to smoothen an image
    SmoothedImage = cv2.medianBlur(gray, 5)
    Resized3 = cv2.resize(SmoothedImage, (960, 540))
    # plt.imshow(ReSized3, cmap='gray')
    return Resized3, SmoothedImage

def RetrieveEdges(smoothed):
    # retrieving the edges for cartoon effect by using thresholding technique
    Edged = cv2.adaptiveThreshold(smoothed, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(Edged, (960, 540))
    # plt.imshow(ReSized4, cmap='gray')
    return ReSized4, Edged

def RemoveNoise(original):
    # by bilateral filter  and keeping the edge sharp as required
    Colored = cv2.bilateralFilter(original, 9, 300, 300)
    ReSized5 = cv2.resize(Colored, (960, 540))
    # plt.imshow(ReSized5, cmap='gray')
    return ReSized5, Colored

def CartoonImage(colored, getEdge):
    CartoonImage = cv2.bitwise_and(colored, colored,mask=getEdge)  # masking edged image with our "BEAUTIFY" image
    ReSized6 = cv2.resize(CartoonImage, (960, 540))
    # plt.imshow(ReSized6, cmap='gray')
    return ReSized6, CartoonImage

def save(ReSized6, ImagePath):
    # saving an image using imwrite()
    newName = "Cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName + extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName + " at " + path
    tk.messagebox.showinfo(title=None, message=I)

def Cartoonify():
    ImgPath = fd.askopenfilename()
    Resized1, original = ReadImage(ImgPath)
    Resized2,grayScaleImage = GrayScale(original)
    Resized3, smoothGrayScale = SmoothImage(grayScaleImage)
    Resized4, getEdge = RetrieveEdges(smoothGrayScale)
    ReSized5, colorImage = RemoveNoise(original)
    ReSized6,cartoonImage = CartoonImage(colorImage, getEdge)

    # Plotting the whole transition
    images = [Resized1, Resized2, Resized3, Resized4, ReSized5, ReSized6]
    Names = ['Original', 'GrayScaled', 'Smoothed', 'Retrieve Edges', 'Colored and Noise Reduction', 'Cartoonified Photo']

    Figures, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.3, wspace=0.1))  # rows = 3 , cols = 2

    for i, img in enumerate(axes.flat):
        img.set_title(Names[i])
        img.imshow(images[i], cmap='gray')


    Savebtn = font.Font(family='Comic Sans MS', weight='bold', slant='italic')
    Savebtn = Button(MainWindow, text="Click here to save your Cartoon Image!", font=btnFont,
                     command=lambda: save(ReSized6, ImgPath), bg="Black", fg="white",
                     width=50, height=1, activeforeground='#104E8B')
    Savebtn.grid(column=1, row=100)

    plt.show()


# Continue Looping all runtime
MainWindow.mainloop()