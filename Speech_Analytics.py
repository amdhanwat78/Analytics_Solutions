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
from tkinter import filedialog
from tkinter import *

script_path = os.path.dirname(os.path.realpath(__file__))

def get_audio_file(file_entry):
    global audio_file
    audio_file = filedialog.askopenfilename(parent = master, initialdir = "/", title = "Select Audio File", filetypes = (("Audio Files", "*.mp3"), ("Audio Files", "*.wav"),))
    file_entry.delete(0, 'end')
    file_entry.insert(0, audio_file)

def run_and_close(event = None):
    close()

def close(event = None):
    master.withdraw()
    master.destroy()

audio_file = None

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
entry_data1.place(x = 200, y = 250)

tk.Label(master, text = "Select Audio File", font = ('Arial', 10, 'bold'), bg = "#ABFF4F").place(x = 70, y = 250)
tk.Button(master, text = "Browse...", font = ('Arial', 10, 'bold'), bg = "#ABFF4F", activebackground = "#ABFF4F", width = 10, command = lambda:get_audio_file(entry_data1)).place(x = 750, y = 250)

analysis_list = ["Speech Translation", "Speech Summary", "Word Cloud", "Sentiment Analysis"]

analysis = []

def chkbox_checked():
    for ix, item in enumerate(cb):
        analysis[ix] = cb_v[ix].get()

lbl = tk.Label(master, text = "Audio Analysis Required", font = ('Arial', 10, 'bold'), bg = "#ABFF4F")
lbl.place(x = 70, y = 300)

cb = []
cb_v = []

rowNum = 330
col = 70

for ix, text in enumerate(analysis_list):
    cb_v.append(tk.StringVar())
    off_value = 0
    cb.append(tk.Checkbutton(master, text = text.rstrip(), font = ('Arial', 10, 'bold'), onvalue = text, offvalue = off_value,
                             variable = cb_v[ix], bg = "#ABFF4F", activebackground = "#ABFF4F",
                             command = chkbox_checked))
    cb[ix].place(x = col, y = rowNum)
    analysis.append(off_value)
    cb[-1].deselect()
    col = col + 200

    if (col > 700):
        col = 150
        rowNum = rowNum + 35

tk.Button(master, text = "Analyze Audio", font = ('Arial', 10, 'bold'), command = run_and_close, width = 20, bg = "#ABFF4F", activebackground = "#ABFF4F").place(x = 320, y = 450)

master.bind('<Return>', run_and_close)
master.bind('<Escape>', close)

master.mainloop()

cwd = os.path.dirname(os.path.realpath(audio_file))
os.chdir(cwd)

client = OpenAI()

# FUNCTION TO CONVERT AUDIO TO TEXT USING SPEECH RECOGNITION LIBRARY
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file, response_format = "text")
        return transcript

##### AUDIO TO TEXT CONVERSION
audio_text = transcribe_audio(audio_file)
org_text = audio_text
src_lang = detect(org_text)

text_file = open("Audio_Description.txt", "w")
text_file.write("SPEECH TO TEXT:\n")
text_file.write(org_text)

##### TRANSLATE TEXT TO ENGLISH
if "Speech Translation" in analysis:
    if (src_lang != 'en'):
        # Prompt for Text Translation
        prompt = f"Translate the following text to English: {org_text}"

        audio_text = client.completions.create(
            model = "gpt-3.5-turbo-instruct",
            prompt = prompt,
            max_tokens = 2 * len(org_text)
            )

        # Extract the Translation
        audio_text = audio_text.choices[0].text

        text_file.write("\n\nSPEECH TRANSLATION:\n")
        text_file.write(audio_text)

##### SUMMARY OF TEXT FROM SPEECH
if "Speech Summary" in analysis:
    # Prompt for Text Summarization
    prompt = f"Summarize the following text: {audio_text}"

    speech_summary = client.completions.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens = len(org_text)
        )

    # Extract the Summary
    speech_summary = speech_summary.choices[0].text

    text_file.write("\n\nSPEECH SUMMARY:\n")
    text_file.write(speech_summary)

text_file.close()

##### SENTIMENT ANALYSIS
if "Sentiment Analysis" in analysis:
    # Initialize the sentiment analysis pipeline
    sentiment_analyzer = pipeline("sentiment-analysis")

    # Perform sentiment analysis
    results = sentiment_analyzer(audio_text)

    # Determine overall sentiment
    average_score = sum(result['score'] for result in results) / len(results)

    if (average_score <= 0.4): overall_sentiment = "Negative"
    if (average_score > 0.4 and average_score < 0.6): overall_sentiment = "Neutral"
    if (average_score >= 0.6): overall_sentiment = "Positive"

##### WORD CLOUD
if "Word Cloud" in analysis:
    # Tokenization and stop word removal
    tokens = word_tokenize(audio_text)
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

lbl = tk.Label(master, text = "AUDIO ANALYSIS RESULTS: ", bg = '#002855', font = ('Arial', 25, 'bold'), fg = '#ABFF4F')
lbl.place(x = 15, y = 15)

lbl = tk.Label(master, text = "")
lbl.grid(row = 0, column = 0, sticky = 'w')

lbl = tk.Label(master, text = "")
lbl.grid(row = 1, column = 0, sticky = 'w')

##### AUDIO TO TEXT
transcript_section = ttk.LabelFrame(master, text = "Audio Speech Transcription: ")
transcript_section.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "nsew")

speech_2_text = ttk.Label(transcript_section, text = org_text, wraplength = 500)
speech_2_text.grid(row = 2, column = 0, padx = 10, pady = 10)

##### TRANSLATION OF TEXT IN ENGLISH
if "Speech Translation" in analysis:
    if (src_lang != 'en'):
        translation_section = ttk.LabelFrame(master, text = "Speech Translation: ")
        translation_section.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "nsew")

        speech_trans = ttk.Label(translation_section, text = audio_text, wraplength = 500)
        speech_trans.grid(row = 3, column = 0, padx = 10, pady = 10)

##### SUMMARY OF TEXT FROM SPEECH
if "Speech Summary" in analysis:
    summary_section = ttk.LabelFrame(master, text = "Speech Summary: ")
    summary_section.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "nsew")

    summary_text = ttk.Label(summary_section, text = speech_summary, wraplength = 300)
    summary_text.grid(row = 2, column = 1, padx = 10, pady = 10)

##### SENTIMENT ANALYSIS
if "Sentiment Analysis" in analysis:
    sentiment_section = ttk.LabelFrame(master, text = "Sentiment Analysis: ")
    sentiment_section.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = "nsew")

    sentiment_text = ttk.Label(sentiment_section, text = "Sentiment Score: "  + str(round(average_score, 2)) + ", Overall Sentiment: " + overall_sentiment)
    sentiment_text.grid(row = 3, column = 1, padx = 10, pady = 10)

##### WORD CLOUD
if "Word Cloud" in analysis:
    from PIL import Image, ImageTk

    wordcloud_image = ImageTk.PhotoImage(Image.open(script_path + "\\WordCloud.png"))

    label = tk.Label(master, text = "Word Cloud: ", image = wordcloud_image)
    label.grid(row = 2, column = 2, columnspan = 3)

master.mainloop()
