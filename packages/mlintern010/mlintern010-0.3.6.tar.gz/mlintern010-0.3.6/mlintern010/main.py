from termcolor import colored
from collections import Counter
import os

def print_hyperlink(url, text):
        escape_code = f'\033]8;;{url}\033\\{text}\033]8;;\033\\'
        print(escape_code)

class About: 
    def intern():
        text = colored("This package made by:\nR KIRAN KUMAR REDDY\n22CSEAIML010\nGIETU (GUNPUR)", 'red', attrs=['reverse', 'blink'])
        print(text)
    def docs():
        print('Vist this utl for installation tutorial')
        text = colored('https://colab.research.google.com/drive/1YPyOOzG9DifXAM-nPhrEn_PprBFE8K-9?usp=sharing', 'yellow', attrs=['reverse', 'blink'])
        print(text)

    
class EDA:
    def mean(dset):
        a = list(dset.columns)
        text = colored("Mean of all cols.", 'green', attrs=['reverse', 'blink'])
        print(text)
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                print(a[i],":",dset[a[i]].mean())


    def median(dset):
        a = list(dset.columns)
        text = colored("Median of all cols.", 'green', attrs=['reverse', 'blink'])
        print(text)
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                l = list(dset[a[i]])
                if (dset[a[i]].shape[0])%2 == 0:
                    l1 = int(len(l)/2)
                    mid = (l[l1]+l[(l1+1)])/2
                else:
                    l1 = int(len(l)/2)
                    mid = l[l1]
                print(a[i],":",mid )


    def mode(dset):
        a = list(dset.columns)
        text = colored("Mode of all cols.", 'green', attrs=['reverse', 'blink'])
        print(text)
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                l = list(dset[a[i]])
                data_counter = Counter(l)
                max_frequency = max(data_counter.values())
                modes = [key for key, frequency in data_counter.items() if frequency == max_frequency]
                print(a[i],":",modes[0])
        
        
