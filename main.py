from contextlib import nullcontext
from Data.bdd_score import BDDSCORE
import os

print("Hello world.")



try:
    bddScore = BDDSCORE()
except ValueError:
    bddScore = False

os.system("pause")