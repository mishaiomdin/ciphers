import Alphabets
import CipherSolver

TEXT_FILE = 'texts/RussianText.txt'
ALPHABET = Alphabets.ALPHABET_RU


with open(TEXT_FILE) as file:
    GIVEN_TEXT = file.read()

cipher = CipherSolver.CipherSolver(
    GIVEN_TEXT=GIVEN_TEXT,
    TITLE='Разгадываем шифр',
    ALPHABET=ALPHABET,
    USED_FONT='Courier')
cipher.main()