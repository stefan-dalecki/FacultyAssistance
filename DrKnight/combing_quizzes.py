import pandas as pd
import numpy as np
import functools as functools

class BigQuiz:
    def __init__():
        quiz1 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz1_combined.csv')
        quiz3 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz3_combined.csv')
        quiz4 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz4_combined.csv')
        quiz5 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz5_combined.csv')

        data_frames = [quiz1, quiz3, quiz4, quiz5]

    def suffix(df, num):
         df.columns = df.columns.map(lambda x : x + ' - Quiz' +str(num) if x != 'Name' and x != 'S_ID' else x)

suffix(quiz1, 1)
suffix(quiz3, 3)
suffix(quiz4, 4)
suffix(quiz5, 5)

df_merged = functools.reduce(lambda left,right: pd.merge_ordered(left, right, on = ['Name', 'S_ID'], how = 'outer'), data_frames).fillna('void')

df_merged.to_csv('perhaps.csv', index = False)
