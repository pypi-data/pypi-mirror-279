from termcolor import colored
from collections import Counter
import matplotlib.pyplot as plt
import os



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

    def Correlation(X,Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        numerator = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(len(X)))
        denominator_X = sum((X[i] - mean_X) ** 2 for i in range(len(X)))
        denominator_Y = sum((Y[i] - mean_Y) ** 2 for i in range(len(Y)))
        correlation = numerator / (denominator_X ** 0.5 * denominator_Y ** 0.5)
        if correlation >= 1:
            text = colored(('Positive correlation :',correlation),'green', attrs=['reverse', 'blink'])
        elif correlation > 0 and correlation < 1:
            text = colored(('No correlation :',correlation),'yellow', attrs=['reverse', 'blink'])
        else:
            text = colored(('Negative correlation :',correlation),'red', attrs=['reverse', 'blink'])
        print(text)


        

class Scaler:
    def Normalization(dset):
        a = list(dset.columns)
        text = colored("Normalization ...", 'yellow', attrs=['reverse', 'blink'])
        print(text)
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                l = list(dset[a[i]])
                min_val = min(l)
                max_val = max(l)
                normalized_data = [(x - min_val) / (max_val - min_val) for x in l]     
                dset[a[i]] = normalized_data
        return dset
    
    def Standardization(dset):
        a = list(dset.columns)
        text = colored("Standardization ...", 'yellow', attrs=['reverse', 'blink'])
        print(text)
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                data = list(dset[a[i]])
                mean_val = sum(data) / len(data)
                std_dev = (sum([(x - mean_val) ** 2 for x in data]) / len(data)) ** 0.5
                standardized_data = [(x - mean_val) / std_dev for x in data]
                dset[a[i]] = standardized_data
        return dset
    
    def Decimal(dset):
        a = list(dset.columns)
        text = colored("Decimal Scaler ...", 'yellow', attrs=['reverse', 'blink'])
        print(text)
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                data = list(dset[a[i]])
                max_val = max(abs(x) for x in data)
                j = len(str(int(max_val)))
                decimal_scaled_data = [x / (10 ** j) for x in data]
                dset[a[i]] = decimal_scaled_data
        return dset



class Plot:
    def Box(data):
        plt.boxplot(data, 
                    notch=True,    
                    patch_artist=True, 
                    boxprops=dict(facecolor='green'), 
                    whiskerprops=dict(color='blue'),     
                    capprops=dict(color='blue'),    
                    flierprops=dict(marker='.', color='red', alpha=0.5), 
                    medianprops=dict(color='red'))
        plt.show()