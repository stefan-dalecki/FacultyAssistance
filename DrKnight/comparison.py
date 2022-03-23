import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r'C:\Users\stda9924\Uni\CU\Knight_Rotation/'
file = r'C:\Users\stda9924\Uni\CU\Knight_Rotation\Quiz1_3_4.csv'

class Compare:
    def __init__(self):
        df = pd.read_csv(file)
        quiz1_pope = df['Post Minus Pre - Quiz1'].to_frame().rename(columns = {'Post Minus Pre - Quiz1' : 'Post Minus Pre'})
        quiz1_pope['Quiz'] = 'Quiz 1'
        quiz3_pope = df['Post Minus Pre - Quiz3'].to_frame().rename(columns = {'Post Minus Pre - Quiz3' : 'Post Minus Pre'})
        quiz3_pope['Quiz'] = 'Quiz 3'
        quiz4_pope = df['Post Minus Pre - Quiz4'].to_frame().rename(columns = {'Post Minus Pre - Quiz4' : 'Post Minus Pre'})
        quiz4_pope['Quiz'] = 'Quiz 4'
        quiz4_pope = df['Post Minus Pre - Quiz4'].to_frame().rename(columns = {'Post Minus Pre - Quiz4' : 'Post Minus Pre'})
        quiz4_pope['Quiz'] = 'Quiz '

        plot_df = pd.concat([quiz1_pope, quiz3_pope, quiz4_pope], axis = 0)

        plot_df['Post Minus Pre'] = plot_df['Post Minus Pre'].apply(pd.to_numeric, errors = 'coerce')
        plot_df = plot_df.dropna().reset_index(drop = True)
        print(plot_df)

        quiz1 = plot_df[plot_df['Quiz'] == 'Quiz 1'].value_counts()
        print(quiz1)

    def scatter(df):
        x = df['Quiz']
        y = df['Post Minus Pre']
        plt.scatter(x,y)
        plt.show()

        scatter(plot_df)
