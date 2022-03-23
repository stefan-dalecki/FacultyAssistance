import pandas as pd
import numpy as np

#Let's be frank, a lot of this is lazy, copy and paste coding
#but it works
df = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Results\Quiz_1345.csv')
df = df.apply(pd.to_numeric, errors = 'coerce')

c_df = pd.DataFrame(columns = ['Quiz 1 - 3 Grade Change',
    'Quiz 1 - 3 Confidence Change',
    'Quiz 3 - 4 Grade Change',
    'Quiz 3 - 4 Confidence Change',
    'Quiz 4 - 5 Grade Change',
    'Quiz 4 - 5 Confidence Change'])


for count in range(df.shape[0]):
    row = df.iloc[count]
    q1_g = row['Quiz 1 numerical letter grade - Quiz1']
    q3_g = row['Quiz 3 numerical letter grade - Quiz3']
    q4_g = row['Quiz 4 numerical letter grade - Quiz4']
    q5_g = row['Quiz 5 numerical letter grade - Quiz5']

    c1_g = row['Post Minus Pre - Quiz1']
    c3_g = row['Post Minus Pre - Quiz3']
    c4_g = row['Post Minus Pre - Quiz4']
    c5_g = row['Post Minus Pre - Quiz5']

    q13c = q3_g - q1_g
    q34c = q4_g - q3_g
    q45c = q5_g - q4_g

    c13c = abs(c3_g) - abs(c1_g)
    c34c = abs(c4_g) - abs(c3_g)
    c45c = abs(c5_g) - abs(c4_g)

    c_df = c_df.append({'Quiz 1 - 3 Grade Change' : q13c,
        'Quiz 1 - 3 Confidence Change' : c13c,
        'Quiz 3 - 4 Grade Change' : q34c,
        'Quiz 3 - 4 Confidence Change' : c34c,
        'Quiz 4 - 5 Grade Change' : q45c,
        'Quiz 4 - 5 Confidence Change' : c45c}
        ,ignore_index = True)

print(c_df.head(20))
c_df.to_csv(r'heatmap_raw.csv', index = False)
