import cv2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import numpy as np


def select_image():
    file_path = filedialog.askopenfilename()
    return file_path


def encode_message():
    image_path = select_image()
    if not image_path:
        return
    img = cv2.imread(image_path)

    msg = simpledialog.askstring("Input", "Enter secret message:")
    password = simpledialog.askstring("Input", "Enter a passcode:", show='*')

    d = {chr(i): i for i in range(255)}

    m, n, z = 0, 0, 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n += 1
        m += 1
        z = (z + 1) % 3

    cv2.imwrite("encryptedImage.jpg", img)
    messagebox.showinfo("Success", "Message encoded successfully!")
    os.system("start encryptedImage.jpg")


def decode_message():
    image_path = select_image()
    if not image_path:
        return
    img = cv2.imread(image_path)

    pas = simpledialog.askstring("Input", "Enter passcode for Decryption", show='*')
    password = simpledialog.askstring("Input", "Re-enter original passcode", show='*')

    if password != pas:
        messagebox.showerror("Error", "Incorrect passcode!")
        return

    c = {i: chr(i) for i in range(255)}
    message = ""
    n, m, z = 0, 0, 0

    for i in range(img.shape[0]):
        try:
            message += c[img[n, m, z]]
            n += 1
            m += 1
            z = (z + 1) % 3
        except KeyError:
            break

    messagebox.showinfo("Decrypted Message", message)


root = tk.Tk()
root.title("Image Steganography")

tk.Button(root, text="Encode Message", command=encode_message).pack(pady=10)
tk.Button(root, text="Decode Message", command=decode_message).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
