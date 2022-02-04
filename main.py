from View.Menu import Menu
from contextlib import nullcontext
from Data.bdd_score import BDDSCORE
import os

print("Hello world.")

menu = Menu()


try:
    bddScore = BDDSCORE()
except ValueError:
    bddScore = False


os.system("pause")
