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
            self._open_url()
            self._click_play()
            self._get_letters()
            self._get__invalid_letters()
            self._get_all_words()
            self._get__valid_words()
            self._submit_words()
        finally:
            print("Browser closed")
            self._driver.close()

    def _open_url(self) -> None:
        """Opens the url"""
        URL = "https://www.nytimes.com/puzzles/spelling-bee"
        self._driver.get(URL)
        sleep(3)

    def _click_play(self) -> None:
        """Clicks the play button and waits for the puzzle to load"""
        self._driver.find_element(By.CLASS_NAME, "pz-moment__button").click()
        sleep(2)

    def _get_letters(self) -> None:
        """Gets the 7 available letters from the puzzle, the first letter is the required letter"""
        letters = self._driver.find_elements(By.CLASS_NAME, "cell-letter")

        for INDEX, LETTER in enumerate(letters):
            if INDEX == 0:
                self._required_letter = LETTER.text.lower()
            else:
                self._other_valid_letters.append(LETTER.text.lower())

    def _get_all_words(self) -> None:
        """Reads all words from the words text file"""
        with open("words.txt", "r", encoding="utf-8") as file:
            self._all_words = file.read().splitlines()

    def _get__valid_words(self) -> None:
        """Gets all valid words from the words text file by using the __is_valid_word function"""
        for WORD in self._all_words:
            if self._is_valid_word(WORD):
                self._valid_words.append(WORD)

    def _is_valid_word(self, word: str) -> bool:
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

    def _get__invalid_letters(self) -> None:
        """
        Step 1:
            Starts with full alphabet
        Step 2:
            Removes the required letter
        Step 3:
            Removes the other 6 possible letters. Doing so gives us the list of invalid letters."""
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        alphabet.remove(self._required_letter)
        for letter in self._other_valid_letters:
            alphabet.remove(letter)

        self._invalid_letters = alphabet

    def _submit_words(self) -> None:
        """Submits all valid words into the game via the selenium keyboard (ActionChains).
        Each word from the __valid_words list is submitted & then backspaces the amount of letters.
        This is done because the game does not give and error if you submit a word that is not
        valid via the DOM"""
        ACTIONS = ActionChains(self._driver)

        for WORD in self._valid_words:
            ACTIONS.send_keys(WORD).send_keys(Keys.ENTER).perform()
            for _ in range(len(WORD)):
                ACTIONS.send_keys(Keys.BACKSPACE).perform()


if __name__ == "__main__":
    NYTSpellingBeeBot().play_game()
