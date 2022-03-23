import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

file = r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Results\q135_progression.csv'

df = pd.read_csv(file)

df = df[['Post Minus Pre Progress', 'Awareness Progress', 'Average Grade']]

def scatter(df,col1,col2):
    sns.set(style = 'whitegrid')
    sns.stripplot(x = col1, y = col2, data = df, jitter = 0.2)
    plt.show()

# scatter(df, 'Awareness Progress', 'Average Grade')
def grade_averages(df, column):
    dec = df[df[column] == 'decreasing'].mean()
    inc = df[df[column] == 'increasing'].mean()
    sta = df[df[column] == 'stagnant'].mean()
    un = df[df[column] == 'unpredictable'].mean()
    return inc, dec, sta, un


# scatter(df, 'Awareness Progress', 'Average Grade')

def manyframes(df, col):
    for val in df[col].unique():
        unique_df = df[df[col] == val]
        yield unique_df
frames = list(manyframes(df, 'Awareness Progress'))

def whiskers(list, col):
    col1 = list[0][col]
    col2 = list[1][col]
    col3 = list[2][col]
    col4 = list[3][col]

    data = [col3, col4, col2, col1]
    print(data)

    fig, ax = plt.subplots()
    ax.boxplot(data, patch_artist = False, meanline = True, showmeans = True)

    plt.xticks([1,2,3,4],['Increasing\nn = '+str(col3.shape[0]), 'Decreasing\nn = '+str(col4.shape[0]), 'Always Unaware\nn ='+str(col2.shape[0]), 'Unpredictable\nn ='+str(col1.shape[0])])
    plt.xlabel('\nAwareness Over Time')
    plt.ylabel('Average Grade\n')
    plt.title('Progress in Quizzes 1, 3, 5 : Awareness vs. Grade')
    fig.tight_layout()
    plt.show()

whiskers(frames, 'Average Grade')
"""Notes"""
'The box part represents +- 1 quartile of the data, dashed line is average, solid line is median, wiskers are maximum and minimum values'

# aware = grade_averages(df, 'Awareness Progress')
# print('Awareness Over Time and Average Grade',
# '\nIncreasing :', aware[0].values[0],
# '\nDecreasing :', aware[1].values[0],
# '\nStagnant :', aware[2].values[0],
# '\nUnpredictable :', aware[3].values[0])
#
# print('\n')
#
# postpre = grade_averages(df, 'Post Minus Pre Progress')
# print('Post Minus Pre Over Time and Average Grade',
# '\nIncreasing :', postpre[0].values[0],
# '\nDecreasing :', postpre[1].values[0],
# '\nStagnant :', postpre[2].values[0],
# '\nUnpredictable :', postpre[3].values[0])
