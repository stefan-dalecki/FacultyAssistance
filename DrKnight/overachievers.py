import pandas as pd
import numpy as np
import functools

q1 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\Quiz1_binning.csv')
q3 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\Quiz3_binning.csv')
q5 = pd.read_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\Quiz5_binning.csv')
data_frames = [q1, q3, q5]

df = functools.reduce(lambda left,right: pd.merge_ordered(left, right, on = ['S_ID'], how = 'outer'), data_frames).fillna(np.nan).dropna().reset_index(drop = True).apply(pd.to_numeric, errors = 'coerce')

s_p = pd.Series(dtype = str)
s_a = pd.Series(dtype = str)

def changes(list):
    for index, val in enumerate(list):
        if val > 0:
            list[index] = 1
        elif val < 0:
            list[index] = -1
        else:
            list[index] = 0
    if list[0] > 0:
        if list[1] > 0 or list[1] == 0:
            progress = 'increasing'
        else:
            progress = 'unpredictable'
    elif list[0] < 0:
        if list[1] < 0 or list[1] == 0:
            progress = 'decreasing'
        else:
            progress = 'unpredictable'
    else:
        if list[1] > 0:
            progress = 'increasing'
        elif list[1] < 0:
            progress = 'decreasing'
        else:
            if list.mean() > 0:
                progress = 'Stagnant - Aware'
            else:
                progress = 'Stagnant - Unaware'
    return progress


for row in df.itertuples():
    postpres = [row._3, row._6, row._9]
    awares = [row.Awareness_x, row.Awareness_y, row.Awareness]
    sd = np.std(postpres)
    postpre_trend = np.diff(postpres)
    postpre_c = changes(postpre_trend)
    aware_trend = np.diff(awares)
    aware_c = changes(aware_trend)

    s_p = s_p.append(pd.Series([postpre_c]))
    s_a = s_a.append(pd.Series([aware_c]))

s_p = s_p.reset_index(drop = True)
s_a = s_a.reset_index(drop = True)

df['Post Minus Pre Progress'] = df.index.map(s_p)
df['Awarness Progress'] = df.index.map(s_a)

print(df)

df.to_csv(r'C:\Users\stda9924\Uni\CU\Knight_Rotation\q135_progression.csv')
