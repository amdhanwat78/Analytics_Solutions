import os
from openai import OpenAI

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from transformers import pipeline
from langdetect import detect

import warnings
warnings.filterwarnings('ignore')

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Text, Button

script_path = os.path.dirname(os.path.realpath(__file__))

def get_text():
    user_input = text_widget.get("1.0", "end-1c")
    save_to_variable(user_input)

def save_to_variable(text):
    global OE_text
    OE_text = text
    run_and_close()

def run_and_close(event = None):
    close()

def close(event = None):
    master.withdraw()
    master.destroy()

text_file = None

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

text_widget = Text(master, wrap = "word", height = 11, width = 85)
text_widget.place(x = 30, y = 230)
text_widget.insert(tk.END, "Enter Your Text Here...")

OE_text = ""

analysis_list = ["Text Translation", "Text Summary", "Word Cloud", "Sentiment Analysis"]

analysis = []

def chkbox_checked():
    for ix, item in enumerate(cb):
        analysis[ix] = cb_v[ix].get()

lbl = tk.Label(master, text = "Text Analysis Required", font = ('Arial', 10, 'bold'), bg = "#ABFF4F")
lbl.place(x = 750, y = 230)

cb = []
cb_v = []

rowNum = 270
col = 750

for ix, text in enumerate(analysis_list):
    cb_v.append(tk.StringVar())
    off_value = 0
    cb.append(tk.Checkbutton(master, text = text.rstrip(), font = ('Arial', 10, 'bold'), onvalue = text, offvalue = off_value,
                             variable = cb_v[ix], bg = "#ABFF4F", activebackground = "#ABFF4F", 
                             command = chkbox_checked))
    cb[ix].place(x = col, y = rowNum)
    analysis.append(off_value)
    cb[-1].deselect()
    col = col + 150

    if (col > 800):
        col = 750
        rowNum = rowNum + 35

get_input_button = Button(master, text = "Analyze Text", command = get_text, font = ('Arial', 10, 'bold'), width = 20, bg = "#ABFF4F", activebackground = "#ABFF4F")
get_input_button.place(x = 300, y = 500)

master.bind('<Return>', run_and_close)
master.bind('<Escape>', close)

master.mainloop()

OE_text = OE_text.rstrip()

client = OpenAI()

##### ORIGINAL TEXT
org_text = OE_text
src_lang = detect(org_text)

text_file = open("Text_Description.txt", "w")
text_file.write("YOUR TEXT:\n")
text_file.write(org_text)

##### TRANSLATE TEXT TO ENGLISH
if "Text Translation" in analysis:
    if (src_lang != 'en'):
        # Prompt for Text Translation
        prompt = f"Translate the following text to English: {org_text}"

        OE_text = client.completions.create(
            model = "gpt-3.5-turbo-instruct",
            prompt = prompt,
            max_tokens = 2 * len(org_text)
            )

        # Extract the Translation
        OE_text = OE_text.choices[0].text

        text_file.write("\n\nTEXT TRANSLATION:\n")
        text_file.write(OE_text)

##### SUMMARY OF TEXT
if "Text Summary" in analysis:
    # Prompt for Text Summarization
    prompt = f"Summarize the following text: {OE_text}"

    text_summary = client.completions.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens = 3000
        )

    # Extract the Summary
    text_summary = text_summary.choices[0].text

    text_file.write("\n\nTEXT SUMMARY:")
    text_file.write(text_summary)

text_file.close()

##### SENTIMENT ANALYSIS
if "Sentiment Analysis" in analysis:
    # Initialize the sentiment analysis pipeline
    sentiment_analyzer = pipeline("sentiment-analysis")

    # Perform sentiment analysis
    results = sentiment_analyzer(OE_text)

    # Determine overall sentiment
    average_score = sum(result['score'] for result in results) / len(results)

    if (average_score <= 0.4): overall_sentiment = "Negative"
    if (average_score > 0.4 and average_score < 0.6): overall_sentiment = "Neutral"
    if (average_score >= 0.6): overall_sentiment = "Positive"

##### WORD CLOUD
if "Word Cloud" in analysis:
    # Tokenization and stop word removal
    tokens = word_tokenize(OE_text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    wordcloud = WordCloud(width = 400, height = 400, background_color = 'white').generate(' '.join(tokens))
    plt.figure(figsize = (10, 5))
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis("off")
    wordcloud.to_file(script_path + "\\WordCloud.png")

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

lbl = tk.Label(master, text = "TEXT ANALYSIS RESULTS: ", bg = '#002855', font = ('Arial', 25, 'bold'), fg = '#ABFF4F')
lbl.grid(row = 0, column = 0, sticky = 'e')

##### ORIGINAL TEXT
transcript_section = ttk.LabelFrame(master, text = "Text: ")
transcript_section.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")

file_text = ttk.Label(transcript_section, text = org_text, wraplength = 500)
file_text.grid(row = 1, column = 0, padx = 10, pady = 10)

##### TRANSLATION OF TEXT IN ENGLISH
if "Text Translation" in analysis:
    if (src_lang != 'en'):
        translation_section = ttk.LabelFrame(master, text = "Text Translation: ")
        translation_section.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "nsew")

        text_trans = ttk.Label(translation_section, text = OE_text, wraplength = 500)
        text_trans.grid(row = 2, column = 0, padx = 10, pady = 10)

##### SUMMARY OF TEXT
if "Text Summary" in analysis:
    summary_section = ttk.LabelFrame(master, text = "Text Summary: ")
    summary_section.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "nsew")

    summary_text = ttk.Label(summary_section, text = text_summary, wraplength = 300)
    summary_text.grid(row = 1, column = 1, padx = 10, pady = 10)

##### SENTIMENT ANALYSIS
if "Sentiment Analysis" in analysis:
    sentiment_section = ttk.LabelFrame(master, text = "Sentiment Analysis: ")
    sentiment_section.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "nsew")

    sentiment_text = ttk.Label(sentiment_section, text = "Sentiment Score: "  + str(round(average_score, 2)) + ", Overall Sentiment: " + overall_sentiment)
    sentiment_text.grid(row = 2, column = 1, padx = 10, pady = 10)

##### WORD CLOUD
if "Word Cloud" in analysis:
    from PIL import Image, ImageTk

    wordcloud_image = ImageTk.PhotoImage(Image.open(script_path + "\\WordCloud.png"))

    label = tk.Label(master, text = "Word Cloud: ", image = wordcloud_image)
    label.grid(row = 1, column = 2, columnspan = 3)

master.mainloop()
