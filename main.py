"""This NYT Spelling Bee Bot can solve the puzzle and submit all valid words."""

from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from customdriver import start_webdriver


class NYTSpellingBeeBot:
    """This NYT Spelling Bee Bot can solve the puzzle and submit all valid words."""
    __driver: WebDriver
    __all_words: list
    __valid_words: list
    __required_letter: str
    __other_valid_letters: list
    __invalid_letters: list

    def __init__(self) -> None:
        """Initialize the webdriver and variables"""
        self.__driver = start_webdriver()
        self.__required_letter = ""
        self.__other_valid_letters = []
        self.__all_words = []
        self.__valid_words = []
        self.__invalid_letters = []

    def play_game(self) -> None:
        """Starts the game and solves it"""
        try:
            self.__open_url()
            self.__click_play()
            self.__get_letters()
            self.__get__invalid_letters()
            self.__get_all_words()
            self.__get__valid_words()
            self.__submit_words()
        finally:
            print("Browser closed")
            self.__driver.close()

    def __open_url(self) -> None:
        """Opens the url"""
        URL = "https://www.nytimes.com/puzzles/spelling-bee"
        self.__driver.get(URL)
        sleep(3)

    def __click_play(self) -> None:
        """Clicks the play button and waits for the puzzle to load"""
        self.__driver.find_element(By.CLASS_NAME, "pz-moment__button").click()
        sleep(2)

    def __get_letters(self) -> None:
        """Gets the 7 available letters from the puzzle, the first letter is the required letter"""
        letters = self.__driver.find_elements(By.CLASS_NAME, "cell-letter")

        for INDEX, LETTER in enumerate(letters):
            if INDEX == 0:
                self.__required_letter = LETTER.text.lower()
            else:
                self.__other_valid_letters.append(LETTER.text.lower())

    def __get_all_words(self) -> None:
        """Reads all words from the words text file"""
        with open("words.txt", "r", encoding="utf-8") as file:
            self.__all_words = file.read().splitlines()

    def __get__valid_words(self) -> None:
        """Gets all valid words from the words text file by using the __is_valid_word function"""
        for WORD in self.__all_words:
            if self.__is_valid_word(WORD):
                self.__valid_words.append(WORD)

    def __is_valid_word(self, word: str) -> bool:
        """Checks if a word is valid according to the NYT Spelling Bee rules.

        Case 1:
            The word must contain the required letter or else it returns False.
        Case 2:
            Checks if the word contains any invalid letters if so it returns False.

        If word passes both cases it returns True by default.
        """
        if word.find(self.__required_letter) == -1:
            return False

        for LETTER in word:
            if self.__invalid_letters.count(LETTER) > 0:
                return False

        return True

    def __get__invalid_letters(self) -> None:
        """
        Step 1:
            Starts with full alphabet
        Step 2:
            Removes the required letter
        Step 3:
            Removes the other 6 possible letters. Doing so gives us the list of invalid letters."""
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        alphabet.remove(self.__required_letter)
        for letter in self.__other_valid_letters:
            alphabet.remove(letter)

        self.__invalid_letters = alphabet

    def __submit_words(self) -> None:
        """Submits all valid words into the game via the selenium keyboard (ActionChains).
        Each word from the __valid_words list is submitted & then backspaces the amount of letters.
        This is done because the game does not give and error if you submit a word that is not
        valid via the DOM"""
        ACTIONS = ActionChains(self.__driver)

        for WORD in self.__valid_words:
            ACTIONS.send_keys(WORD).send_keys(Keys.ENTER).perform()
            for _ in range(len(WORD)):
                ACTIONS.send_keys(Keys.BACKSPACE).perform()


if __name__ == "__main__":
    NYTSpellingBeeBot().play_game()
