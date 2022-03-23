import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyplot_themes as themes

class Figure:
    def make_fig(df, quiz_num):
        plot_df = df['Post Minus Pre'].apply(pd.to_numeric, errors = 'coerce').dropna().value_counts().reindex(index = np.arange(-4, 4.1)).fillna(0)
        print(plot_df)
        ans = input('Save table? : y/n \n')
        if ans == 'y':
            plot_df.to_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Results\quiz_'+quiz_num+'_plot_table.csv')
        fig = plt.figure(figsize = (10,5))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        ax.set_xticks(plot_df.index.values)
        plt.bar(plot_df.index.values, plot_df.values)
        plt.xlabel('Post Minus Pre')
        plt.ylabel('Number of Students')
        plt.title('Quiz' + quiz_num +'\n')
        plt.show()

while True:
    quiz_num = input('Which quiz would you like to graph? : \n')
    file = f'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz'+quiz_num+'_combined.csv'
    df = pd.read_csv(file)
    Figure.make_fig(df, quiz_num)
    ans = input('Make another graph : (y/n)\n')
    if ans == 'n':
        quit()
    else:
        continue
