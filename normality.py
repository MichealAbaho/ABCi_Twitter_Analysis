import pandas as plib
import statistics as stat
import scipy.stats as stats
from tweet_processing import working_directory

def normality(file):
    
    working_directory()
    mostly_advise = []
    moderately_advise = []
    not_advise = []
    purely_advise = []
    
    pf = plib.read_csv(file, encoding="latin1")
    
    for i,j in zip(list(pf['Class']), list(pf['Term-frequency-weight'])):
        if (i == 'purely_advise'):
            purely_advise.append(j)
        elif (i == 'mostly_advise'):
            mostly_advise.append(j)
        elif (i == 'moderately_advise'):
            moderately_advise.append(j)
        elif (i == 'not_advise'):
            not_advise.append(j)
    
    '''testing the assumption of normality within the term-frequencies for each of the classes using shapiro wilk test, if the shapiro value
    is less tha 0.05, the term-frequencies for that particular class are not normaly distributed otherwise, they exhibt a normal distribution'''
    print (stats.shapiro(purely_advise), '\n', stats.shapiro(mostly_advise), '\n',
           stats.shapiro(moderately_advise), '\n', stats.shapiro(not_advise))
    
    #btaining descriptive stats of mode, median, mean and standard deviation of each of the classes
    print (len(purely_advise), stat.mean(purely_advise), '\n', stat.median(purely_advise), '\n',
           stat.mode(purely_advise),'\n', stat.pstdev(purely_advise))
    print (len(mostly_advise), stat.mean(mostly_advise), '\n', stat.median(mostly_advise), '\n',
           stat.mode(mostly_advise),'\n', stat.pstdev(mostly_advise))
    print (len(moderately_advise), stat.mean(moderately_advise), '\n', stat.median(moderately_advise), '\n',
           stat.mode(moderately_advise),'\n', stat.pstdev(moderately_advise))
    print (len(not_advise), stat.mean(not_advise), '\n', stat.median(not_advise), '\n',
           stat.mode(not_advise), '\n',stat.pstdev(not_advise))
       
    
normality('diabetes\\diabetes-training-set.csv')
