import os
import base64
import requests

import warnings
warnings.filterwarnings('ignore')

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

script_path = os.path.dirname(os.path.realpath(__file__))

def get_image_file(file_entry):
    global image_file
    image_file = filedialog.askopenfilename(parent = master, initialdir = "/", title = "Select Image File", filetypes = (("Image File", "*.jpg"), ("Image File", "*.jpeg"), ("Image File", "*.png"),))
    file_entry.delete(0, 'end')
    file_entry.insert(0, image_file)

def run_and_close(event = None):
    close()

def close(event = None):
    master.withdraw()
    master.destroy()

image_file = None

master = tk.Tk()
master.config(bg = "#002855")
master.title("")

master.resizable(False, False)

window_height = 560
window_width = 980

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

from PIL import Image, ImageTk
logo_image = ImageTk.PhotoImage(Image.open(script_path + "\\actNable_Logo.png"))

label = tk.Label(master, text = "", image = logo_image)
label.place(x = 5, y = 5)

entry_data1 = tk.Entry(master, text = "", width = 90)
entry_data1.place(x = 220, y = 250)

tk.Label(master, text = "Select Image File", font = ('Arial', 10, 'bold'), bg = "#ABFF4F").place(x = 80, y = 250)
tk.Button(master, text = "Browse...", font = ('Arial', 10, 'bold'), bg = "#ABFF4F", activebackground = "#ABFF4F", width = 10, command = lambda:get_image_file(entry_data1)).place(x = 780, y = 250)

tk.Button(master, text = "Analyze Image", font = ('Arial', 10, 'bold'), bg = "#ABFF4F", activebackground = "#ABFF4F", command = run_and_close, width = 20).place(x = 420, y = 300)

master.bind('<Return>', run_and_close)
master.bind('<Escape>', close)

master.mainloop()

cwd = os.path.dirname(os.path.realpath(image_file))
os.chdir(cwd)

# Function to encode the image
def encode_image(image_file):
  with open(image_file, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image(image_file)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {OPENAI_API_KEY}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers = headers, json = payload)

img_description = response.json()['choices'][0]['message']['content']

text_file = open("Imgage_Description.txt", "w")
text_file.write("IMGAGE DESCRIPTION:\n")
text_file.write(img_description)
text_file.close()

master = tk.Tk()
master.config(bg = "#002855")
master.title("")

master.resizable(False, False)

window_height = 700
window_width = 1400

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

from PIL import Image, ImageTk
logo_image = ImageTk.PhotoImage(Image.open(script_path + "\\actNable_Output.png"))

label = tk.Label(master, text = "", image = logo_image)
label.place(x = 5, y = 5)

lbl = tk.Label(master, text = "IMAGE ANALYSIS RESULTS ", bg = '#002855', font = ('Arial', 25, 'bold'), fg = '#ABFF4F')
lbl.place(x = 15, y = 15)

lbl = tk.Label(master, text = "")
lbl.grid(row = 0, column = 0, sticky = 'w')

lbl = tk.Label(master, text = "")
lbl.grid(row = 1, column = 1, sticky = 'w')

lbl = tk.Label(master, text = "")
lbl.grid(row = 2, column = 1, sticky = 'w')

image_section = ttk.LabelFrame(master, text = "Image Description: ")
image_section.grid(row = 3, column = 2, padx = 10, pady = 10, sticky = "nsew")

image_description = ttk.Label(image_section, text = img_description, wraplength = 600)
image_description.grid(row = 3, column = 2, padx = 10, pady = 10)

master.mainloop()
