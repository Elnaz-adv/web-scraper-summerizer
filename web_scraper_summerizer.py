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

class WebScraperGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper")

        self.LANGUAGE = "english"
        self.SENTENCES_COUNT = 2
        self.stemmer = Stemmer(self.LANGUAGE)
        self.summarizer = Summarizer(self.stemmer)
        self.summarizer.stop_words = get_stop_words(self.LANGUAGE)

        self.url_input = tk.Entry(self.root)
        self.url_input.pack(fill=tk.X, padx=10, pady=10)

        self.scrape_button = tk.Button(self.root, text="Scrape", command=self.scrape_website)
        self.scrape_button.pack(padx=10, pady=10)

        self.title_label = tk.Label(self.root, font=("Arial", 16, "bold"), fg="blue")
        self.title_label.pack(fill=tk.X, padx=10, pady=10, expand=True)

        self.summary_label = tk.Label(self.root, font=("Arial", 12))
        self.summary_label.pack(fill=tk.X, padx=10, pady=10, expand=True)

    def scrape_website(self):
        # get the URL from the user input
        url = self.url_input.get()

        # make a GET request to the URL and parse the HTML content with Beautiful Soup
        response = requests.get(url)
        parser = HtmlParser.from_url(url, Tokenizer(self.LANGUAGE))
        soup = BeautifulSoup(response.content, 'html.parser')

        # extract the important information from the page (for example, the title and summary)
        title = soup.title.string
        summary = self.summarizer(parser.document, self.SENTENCES_COUNT)

        # display the results in the GUI
        self.title_label.config(text=title)
        self.summary_label.config(text=summary)

        # adjust the GUI size automatically
        self.root.update()
        self.root.geometry("")

    def run(self):
        # start the GUI
        self.root.mainloop()

# create the GUI
root = tk.Tk()
scraper_gui = WebScraperGUI(root)
scraper_gui.run()
