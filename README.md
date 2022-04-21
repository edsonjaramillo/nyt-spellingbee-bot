# NYT Spelling Bee Solver

This program uses the selenium web driver to solve the daily NYT Spelling Bee.

![NYT Spelling Bee Banner](https://media.graphassets.com/AGom4yWSLuuY8E2HrO3E)

## Links

**NYT Spelling Bee:** [Link](https://www.nytimes.com/puzzles/spelling-bee)

**Youtube Demo:** [Link](https://youtube.com)

## Technologies used

- [Python 3.10](https://www.python.org/)
- [Selenium Library](https://www.selenium.dev/)

## Game Rules

- Words must contain at least 4 letters.
- Words must include the center letter.
- Our word list does not include words that are obscure, hyphenated, or proper nouns.
- No cussing either, sorry.
- Letters can be used more than once.
- 4-letter words are worth 1 point each.
- Longer words earn 1 point per letter.
- Each puzzle includes at least one “pangram” which uses every letter. These are worth 7 extra points!

## Word List

I grabbed the word list from [this Github repo](https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt).

## Data Cleanup

- First I cleaned up the data by removing all the words that are not 4 letters long.
- Then I removed all the words that contain more than 7 individual letters.

The original word list contained `370,105 words` and the cleaned up list contains about `181,519 words`.

## Process

![NYT Spelling Bee Banner](https://media.graphassets.com/t8AcaXOeSPGv2kFmsgeL)

1. Get all the letters from the puzzle
2. Loop through the word list and check if the word contains the letters and the required letter
3. Add the words to the list if it is valid
4. Enter all the words into the puzzle via the ActionKeys into the game.
5. **WIN!**
