import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def perform_canny_edge_detection(image_path, threshold1, threshold2):
    original_image = cv2.imread(image_path)
    imgGray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, threshold1, threshold2)
    return imgCanny, original_image

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp *.jpeg")])
    if file_path:
        input_image_path.set(file_path)

def process_image(event):
    image_path = input_image_path.get()
    if image_path:
        threshold1_val = int(threshold1_slider.get())
        threshold2_val = int(threshold2_slider.get())

        edges, original_image = perform_canny_edge_detection(image_path, threshold1_val, threshold2_val)
        
        # Find contours in the Canny edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw green contours on the original image
        img_with_contours = original_image.copy()
        cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)

        # Display the image with contours in a separate window
        cv2.imshow("Canny Edges with Contours", img_with_contours)
        cv2.waitKey(1)

root = tk.Tk()
root.title("Canny Edge Detection with Contours")

input_image_path = tk.StringVar()
threshold1_val = tk.IntVar()
threshold2_val = tk.IntVar()

open_button = tk.Button(root, text="Open Image", command=open_file)
open_button.pack()

input_image_label = tk.Label(root, text="Image Path:")
input_image_label.pack()
input_image_entry = tk.Entry(root, textvariable=input_image_path, state="readonly")
input_image_entry.pack()

threshold1_label = tk.Label(root, text="Threshold 1:")
threshold1_label.pack()
threshold1_slider = tk.Scale(root, from_=0, to=500, variable=threshold1_val, orient="horizontal")
threshold1_slider.bind("<Motion>", process_image)
threshold1_slider.pack()

threshold2_label = tk.Label(root, text="Threshold 2:")
threshold2_label.pack()
threshold2_slider = tk.Scale(root, from_=0, to=500, variable=threshold2_val, orient="horizontal")
threshold2_slider.bind("<Motion>", process_image)
threshold2_slider.pack()

root.mainloop()
