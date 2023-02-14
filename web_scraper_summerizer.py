from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
import nltk

nltk.download('punkt')

# set the summarizer language and create a summarizer object
LANGUAGE = "english"
SENTENCES_COUNT = 2
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)



def scrape_website():
    # get the URL from the user input
    url = url_input.get()

    # make a GET request to the URL and parse the HTML content with Beautiful Soup
    response = requests.get(url)
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract the important information from the page (for example, the title and summary)
    title = soup.title.string
    summary = summarizer(parser.document, SENTENCES_COUNT)

    # display the results in the GUI
    title_label.config(text=title)
    summary_label.config(text=summary)

    # adjust the GUI size automatically
    root.update()
    root.geometry("")

# create the GUI
root = tk.Tk()
root.title("Web Scraper")

# create the URL input box and scrape button
url_input = tk.Entry(root)
url_input.pack(fill=tk.X, padx=10, pady=10)
scrape_button = tk.Button(root, text="Scrape", command=scrape_website)
scrape_button.pack(padx=10, pady=10)

# create the labels for the scraped information
title_label = tk.Label(root, font=("Arial", 16, "bold"), fg="blue")
title_label.pack(fill=tk.X, padx=10, pady=10, expand=True)
summary_label = tk.Label(root, font=("Arial", 12))
summary_label.pack(fill=tk.X, padx=10, pady=10, expand=True)

# start the GUI
root.mainloop()
