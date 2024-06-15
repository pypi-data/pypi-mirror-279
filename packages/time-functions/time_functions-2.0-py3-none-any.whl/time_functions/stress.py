# @michaelrex2012
# 6/14/2024
# Adds the stress() function

from alive_progress import alive_bar


def stress(rep: int, showBar: bool):
    runs = 0

    if showBar == 0:
        while runs < rep:
            numVar = 2793755435.67623748687525982657856285346786761525487532718478653867816784658637 / 8495.397482374897457475894735
            runs = runs + 1
            percent = runs / rep
    elif showBar == 1:
        with alive_bar(rep, bar="smooth") as bar:
            for i in range(rep):
                numVar = 2793755435.67623748687525982657856285346786761525487532718478653867816784658637 / 8495.397482374897457475894735
                numVar = str(numVar)
                numVar = float(numVar)
                bar()
