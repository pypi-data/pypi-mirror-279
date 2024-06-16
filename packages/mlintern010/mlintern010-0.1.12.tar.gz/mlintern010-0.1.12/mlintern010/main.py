from termcolor import colored
class about: 
    def intern():
        text = colored("This package made by:\nR KIRAN KUMAR REDDY\n22CSEAIML010\nGIETU (GUNPUR)", 'red', attrs=['reverse', 'blink'])
        print(text)

class EDA:
    def mean(dset):
        a = list(dset.columns)
        print("Mean of all cols.")
        for i in range(len(a)):
            if dset[a[i]].dtype == 'int64' or dset[a[i]].dtype == 'float64' or dset[a[i]].dtype == 'int32' or dset[a[i]].dtype == 'float32':
                print(a[i],":",dset[a[i]].mean())
        
