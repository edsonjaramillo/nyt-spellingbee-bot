from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from SeleniumDriver import init_webdriver


class NYTSpellingBeeBot:
    driver: WebDriver = init_webdriver()
    required_letter: str
    other_letters: list = []
    all_words: list = []
    valid_words: list = []
    invalid_letters: list = []

    def __init__(self):
        try:
            self.open_website()
            self.click_play()
            self.get_letters()
            self.get_invalid_letters()
            self.get_all_words()
            self.get_valid_words()
            self.submit_words()
        except Exception as e:
            print("Exception below:\n", e)
        finally:
            print("Browser closed")
            self.driver.close()

    def open_website(self):
        url = "https://www.nytimes.com/puzzles/spelling-bee"
        self.driver.get(url)
        sleep(3)

    def click_play(self):
        self.driver.find_element(By.CLASS_NAME, "pz-moment__button").click()
        sleep(1)

    # gets letters from the puzzle
    def get_letters(self):
        letters = self.driver.find_elements(By.CLASS_NAME, "cell-letter")

        # loop through all letters and the first one is always the required letter
        for index, letter in enumerate(letters):
            if index == 0:
                self.required_letter = letter.text.lower()
            else:
                self.other_letters.append(letter.text.lower())

    # read all words from the words text file
    def get_all_words(self):
        with open("words.txt") as file:
            self.all_words = file.read().splitlines()

    # get all valid words with isValidWord function
    def get_valid_words(self):
        for word in self.all_words:
            if self.isValidWord(word):
                self.valid_words.append(word)

    def isValidWord(self, word: str):
        # if word does not have required letter return false
        if word.find(self.required_letter) == -1:
            return False

        # if word has invalid letters (not from the 7 possible letters) return false
        for letter in word:
            if self.invalid_letters.count(letter) > 0:
                return False

        # if none of the above return true
        return True

    # used to as list to check if a letter is invalid
    def get_invalid_letters(self):
        # start with full alphabet
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        # remove required letter
        alphabet.remove(self.required_letter)
        # remove other letters
        for letter in self.other_letters:
            alphabet.remove(letter)

        self.invalid_letters = alphabet

    # submit all valid words
    def submit_words(self):
        # initialize action chains object
        actions = ActionChains(self.driver)

        for word in self.valid_words:
            # type the word and press enter
            actions.send_keys(word).send_keys(Keys.ENTER).perform()

            # backspace the length of the word
            # ex if word is "hello" backspace 5 times
            # used in case word is not valid according to NYT
            for _ in range(len(word)):
                actions.send_keys(Keys.BACKSPACE).perform()


if __name__ == "__main__":
    NYTSpellingBeeBot()