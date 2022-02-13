"""This NYT Spelling Bee Bot can solve the puzzle and submit all valid words."""

from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from customdriver import start_webdriver


class NYTSpellingBeeBot:
    """This NYT Spelling Bee Bot can solve the puzzle and submit all valid words."""
    _driver: WebDriver
    _all_words: list
    _valid_words: list
    _required_letter: str
    _other_valid_letters: list
    _invalid_letters: list

    def __init__(self) -> None:
        """Initialize the webdriver and variables"""
        self._driver = start_webdriver()
        self._required_letter = ""
        self._other_valid_letters = []
        self._all_words = []
        self._valid_words = []
        self._invalid_letters = []

    def play_game(self) -> None:
        """Starts the game and solves it"""
        try:
            self.open_url()
            self.click_play()
            self.get_letters()
            self.get_invalid_letters()
            self.get_all_words()
            self.get_valid_words()
            self.submit_words()
        finally:
            print("Browser closed")
            self._driver.close()

    def open_url(self) -> None:
        """Opens the url"""
        URL = "https://www.nytimes.com/puzzles/spelling-bee"
        self._driver.get(URL)
        sleep(3)

    def click_play(self) -> None:
        """Clicks the play button and waits for the puzzle to load"""
        self._driver.find_element(By.CLASS_NAME, "pz-moment__button").click()
        sleep(2)

    def get_letters(self) -> None:
        """Gets the 7 available letters from the puzzle, the first letter is the required letter"""
        letters = self._driver.find_elements(By.CLASS_NAME, "cell-letter")

        for INDEX, LETTER in enumerate(letters):
            if INDEX == 0:
                self._required_letter = LETTER.text.lower()
            else:
                self._other_valid_letters.append(LETTER.text.lower())

    def get_all_words(self) -> None:
        """Reads all words from the words text file"""
        with open("words.txt", "r", encoding="utf-8") as file:
            self._all_words = file.read().splitlines()

    def get_valid_words(self) -> None:
        """Gets all valid words from the words text file by using the is_valid_word function"""
        for WORD in self._all_words:
            if self.is_valid_word(WORD):
                self._valid_words.append(WORD)

    def is_valid_word(self, word: str) -> bool:
        """Checks if a word is valid according to the NYT Spelling Bee rules.

        Case 1:
            The word must contain the required letter or else it returns False.
        Case 2:
            Checks if the word contains any invalid letters if so it returns False.

        If word passes both cases it returns True by default.
        """
        if word.find(self._required_letter) == -1:
            return False

        for LETTER in word:
            if self._invalid_letters.count(LETTER) > 0:
                return False

        return True

    def get_invalid_letters(self) -> None:
        """
        Step 1:
            Gets invalid letters from the puzzle.
        Step 2:
            Starts with full alphabet & removes the required letter
        Step 3:
            Removes the other 6 possible letters. Doing so gives us the list of invalid letters."""
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        alphabet.remove(self._required_letter)
        for letter in self._other_valid_letters:
            alphabet.remove(letter)

        self._invalid_letters = alphabet

    def submit_words(self) -> None:
        """Submits all valid words into the game via the selenium keyboard (ActionChains).
        Each word from the _valid_words list is submitted & then backspaces the amount of letters.
        This is done because the game does not give and error if you submit a word that is not
        valid via the DOM"""
        ACTIONS = ActionChains(self._driver)

        for WORD in self._valid_words:
            ACTIONS.send_keys(WORD).send_keys(Keys.ENTER).perform()
            for _ in range(len(WORD)):
                ACTIONS.send_keys(Keys.BACKSPACE).perform()


if __name__ == "__main__":
    NYTSpellingBeeBot().play_game()
