import time
import pyautogui
import matplotlib.pyplot as plt 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
from unidecode import unidecode

class Whats():
    '''Whats App Automation'''
    def __init__(self):
        self.words = ""
        self.driver = None

    def login(self):
        '''Opens WhatsApp Web and waits for login'''
        self.driver = webdriver.Firefox()
        self.driver.get("https://web.whatsapp.com/")
        time.sleep(15)

    def chat(self, name):
        '''Opens the chosen chat'''
        chats = self.driver.find_elements_by_class_name("_3ko75")
        for chat in chats:
            if chat.text == name:
                chat.click()

    def load_messages(self):
        '''Load the older messages of the chat'''
        width, height = pyautogui.size()
        pyautogui.moveTo((width/6)*5, height/2)
        pyautogui.click()

        start_time = time.time()
        while time.time() - start_time < 1000:
            pyautogui.scroll(5)
            time.sleep(0.1)

    def save_messages(self):
        '''Save messages in a .txt file'''
        messages = self.driver.find_elements_by_class_name("eRacY")
        msg_file_name = str(datetime.now()) + ".txt"
        
        with open("file_list.txt\n", "a") as file:
            file.write(msg_file_name)
            file.close()

        with open(msg_file_name, "w") as file:        
            for message in messages:
                file.write(message.text.lower()+"\n")

        return msg_file_name

    def clean_messages(self, file_name):
        '''Read the file, remove some words and return a cleaned string'''
        ponctuations = ('.', ',', '?', '!', ':', '#', '@')
        
        with open(file_name) as file:
            text = file.read()
            file.close()

        text = unidecode(text)
        
        for ponctuation in ponctuations:            
            text = text.replace(ponctuation, "")

        text = text.lower()
        text = text.split()

        for word in text:
            try:
                if word[:4] == "http":
                    text.remove(word)
            except:
                pass

        with open("words_to_remove.txt") as file:
            for word in file:
                word = word.rstrip("\n")
                text = list(filter((word).__ne__, text))

        text = " ".join(word for word in text)
        return text       

    def make_word_cloud(self, words):
        '''Return a word cloud made with the given sting'''
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(words)
        return wordcloud

    def plot_word_cloud(self, wordcloud):
        '''Plot the given word cloud'''
        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0)  
        plt.show()        

        
if __name__ == "__main__":
    w = Whats()
    w.login()
    w.chat("Alao em danger BN")
    w.load_messages()
    file_name = w.save_messages()
    msgs = w.clean_messages(file_name)
    wd = w.make_word_cloud(msgs)
    w.plot_word_cloud(wd)
