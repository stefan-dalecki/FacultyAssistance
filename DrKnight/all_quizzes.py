import pandas as pd
import numpy as np
import os
import itertools



class Quiz:
    def __init__(self, path, quiz_num):
        fileprefix = f'{path}\\Quiz_{quiz_num}'
        self.path = path
        self.num = quiz_num
        self.refl_path = f'{fileprefix}_reflections.csv'
        self.refl_df = pd.read_csv(self.refl_path)
        self.grade_path = f'{fileprefix}_grades.csv'
        self.grade_df = pd.read_csv(self.grade_path)
        self.key_df = pd.read_csv(r'C:\Users\sjdal\Coding\DrKnight\CSV_Files\Analysis_Files\letter_number.csv')

    def reflections(self):
        self.refl_prompts = self.refl_df.columns[-4:]

    def grades(self):
        self.grade_info = {'Grade_Name': self.grade_df.columns[0],
                           'Grade_ID': self.grade_df.columns[1],
                           'Grade_Refl': self.grade_df.columns[7],
                           'Grade_Grade': self.grade_df.columns[3]}
        if self.grade_df['letter'].empty == True and \
            self.grade_df['numerical grade'].empty == True:
            for i, row in self.grade_df.iterrows():
                self.grade_df.at[i, 'letter'], self.grade_df.at[i, 'numerical grade'] = Task.grade_conv(self.grade_df['percent'].values)
        self.grade_df = pd.concat([self.grade_df, Task.post_pre(self.grade_df)])

    def export_csv(self):
        Task.overwrite(self.grade_path, self.grade_df)
        Task.overwrite(self.refl_path, self.refl_df)

    def export_final(self, df, type='csv'):
        subdir = r'Updated_Quizzes'
        name = f'Quiz_{quiz_num}_combined.{type}'
        outpath = os.path.join(self.path, subdir, name)
        if os.path.isfile(outpath) == True:
            ans = input('File already exists.\nOverwrite current file? : y/n\n')
            if ans == 'y':
                os.remove(outpath)
                df.to_csv(outpath, index = False)
            else:
                quit()
        else:
            df.to_csv(outpath, index = False)

class Task:
    def grade_conv(grade, grade_letter='absent'):
        key_df = pd.read_csv(r'C:\Users\sjdal\Coding\DrKnight\CSV_Files\Analysis_Files\letter_number.csv')
        if grade_letter == 'absent':
            grade_percent = grade / 0.5
            if grade_percent >= 90:
                grade_letter = 'A'
            elif 80 <= grade_percent <90:
                grade_letter = 'B'
            elif 70 <= grade_percent <80:
                grade_letter = 'C'
            elif 60 <= grade_percent <70:
                grade_letter = 'D'
            else:
                grade_letter = 'F'
            grade_number = key_df[key_df['Letter'] == grade_letter] \
                                  ['Number'].values[0]
            return grade_letter, grade_number
        elif grade_letter == 'present':
            try:
                grade_number = key_df[key_df['Letter'] == grade] \
                                      ['Number'].values[0]
                return grade_number
            except Exception:
                return np.nan

    def post_pre(df):
        assert df['expected grade'].empty == False, 'No expected grade'
        assert df['numerical grade'].empty == False, 'No numerical grade'
        postpre = [row['numerical grade']-Task.grade_conv(row['expected grade'], grade_letter='present') for i, row in df.iterrows()]
        return pd.DataFrame(data=postpre, columns=['post minus pre'])


    def combine(quizo):
        left_df = quizo.grade_df.iloc[:,:-1]
        right_df = quizo.refl_df
        out_df = left_df.merge(right_df, on = ['last name', 'first name', 'ID'], how = 'left')
        return out_df.fillna('no response')

    def overwrite(path, df, w=True):
        if os.path.isfile(path) == True:
            if w:
                os.remove(path)
                df.to_csv(path, index = False)
                print('File overwritten')
            else:
                print('File exists, original file will not be overwritten')
        else:
            df.to_csv(path, index = False)

path = r'C:\Users\sjdal\Coding\DrKnight\CSV_Files\Raw_CSV_Files'
quiz1 = Quiz(path, 1)
quiz1.grades()
# quiz1.export_csv()
com_df = Task.combine(quiz1)
