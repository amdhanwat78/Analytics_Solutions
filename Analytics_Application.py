import os

import warnings
warnings.filterwarnings('ignore')

import tkinter as tk
from tkinter import *

script_path = os.path.dirname(os.path.realpath(__file__))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def speech_button():
    global speech_button_text
    speech_button_text = speech_analytics.cget("text")
    run_and_close()

def text_button():
    global text_button_text
    text_button_text = text_analytics.cget("text")
    run_and_close()

def image_button():
    global image_button_text
    image_button_text = image_analytics.cget("text")
    run_and_close()

def video_button():
    global video_button_text
    video_button_text = video_analytics.cget("text")
    run_and_close()

def run_and_close(event = None):
    close()

def close(event = None):
    master.withdraw()
    master.destroy()

speech_button_text = ""
text_button_text = ""
image_button_text = ""
video_button_text = ""

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

lbl = tk.Label(master, text = "", bg = '#002855', font = ('Arial', 25, 'bold'), fg = '#ABFF4F')
lbl.place(x = 25, y = 70)

from PIL import Image, ImageTk
logo_image = ImageTk.PhotoImage(Image.open(script_path + "\\actNable_Logo.png"))

label = tk.Label(master, text = "", image = logo_image)
label.place(x = 5, y = 5)

speech_analytics = tk.Button(master, text = "SPEECH / VOICE -\nTRANSLATE, TRANSCRIBE \n& ANALYZE", width = 25, height = 4, activebackground = "#ABFF4F", bg = "#ABFF4F", command = speech_button, font = ('Arial', 13, 'bold'))
speech_analytics.place(x = 200, y = 250)

text_analytics = tk.Button(master, text = "TEXT\nANALYTICS", width = 25, height = 4, activebackground = "#ABFF4F", bg = "#ABFF4F", command = text_button, font = ('Arial', 13, 'bold'))
text_analytics.place(x = 550, y = 250)

image_analytics = tk.Button(master, text = "IMAGE\nANALYTICS", width = 25, height = 4, activebackground = "#ABFF4F", bg = "#ABFF4F", command = image_button, font = ('Arial', 13, 'bold'))
image_analytics.place(x = 200, y = 400)

video_analytics = tk.Button(master, text = "VIDEO\nANALYTICS", width = 25, height = 4, activebackground = "#ABFF4F", bg = "#ABFF4F", command = video_button, font = ('Arial', 13, 'bold'))
video_analytics.place(x = 550, y = 400)

master.bind('<Return>', run_and_close)
master.bind('<Escape>', close)

master.mainloop()

if (text_button_text == "TEXT\nANALYTICS"):
    exec(open(script_path + "\\Text_Analytics.py").read())

if (speech_button_text == "SPEECH / VOICE -\nTRANSLATE, TRANSCRIBE \n& ANALYZE"):
    exec(open(script_path + "\\Speech_Analytics.py").read())

if (image_button_text == "IMAGE\nANALYTICS"):
    exec(open(script_path + "\\Image_Analytics.py").read())
