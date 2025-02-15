import Alphabets
import CipherSolver

TEXT_FILE = 'texts/GeorgianText1.txt'
ALPHABET = Alphabets.ALPHABET_GR_RANDOM


with open(TEXT_FILE) as file:
    GIVEN_TEXT = file.read()

cipher = CipherSolver.CipherSolver(
    GIVEN_TEXT=GIVEN_TEXT,
    TITLE='Грузинский текст №1',
    ALPHABET=ALPHABET,
    USED_FONT='Courier')
cipher.main()