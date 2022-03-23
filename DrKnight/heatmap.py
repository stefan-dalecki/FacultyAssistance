import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.linear_model import LinearRegression


file = r'C:\Users\stda9924\Uni\CU\Not_PhD\MCDB\Knight_Rotation\CSV_Files\Results\heatmap_raw.csv'

df = pd.read_csv(file)

def heatmap(df, q1, q2):
    q1 = str(q1)
    q2 = str(q2)
    grade_c = f'Quiz {q1} - {q2} Grade Change'
    acc_c = f'Quiz {q1} - {q2} Accuracy Change'
    quiz_heatmap = df[[grade_c, acc_c]].dropna().reset_index(drop = True)
    bar_label = f'# of Students (n = {str(quiz_heatmap.shape[0])})''
    value_counts = quiz_heatmap.groupby([grade_c, acc_c]).size().reset_index().rename(columns={0:'count'})
    df_array_style = pd.DataFrame(index = range(-4, 5), columns = range(-4, 5))
    pos_pos, pos_neg, neg_pos, neg_neg, null_neg, null_pos, pos_null, neg_null = 0,0,0,0,0,0,0,0
    for row in value_counts.itertuples(index = True):
        if row._1 >0 and row._2 > 0:
            pos_pos = pos_pos + row.count
        if row._1 > 0 and row._2 < 0:
            pos_neg = pos_neg + row.count
        if row._1 < 0 and row._2 > 0:
            neg_pos = neg_pos + row.count
        if row._1 < 0 and row._2 < 0:
            neg_neg = neg_neg + row.count
        if row._1 > 0 and row._2 == 0:
            pos_null = pos_null + row.count
        if row._1 < 0 and row._2 == 0:
            neg_null = neg_null + row.count
        if row._1 == 0 and row._2 > 0:
            null_pos = null_pos + row.count
        if row._1 == 0 and row._2 < 0:
            null_neg = null_neg + row.count

    print('\n+Grade and +Accuracy :', pos_pos,
    '\n+Grade and -Accuracy :', pos_neg,
    '\n-Grade and +Accuracy :', neg_pos,
    '\n-Grade and -Accuracy :', neg_neg,
    '\n+Grade and =Accuracy :', pos_null,
    '\n-Grade and =Accuracy :', neg_null,
    '\n=Grade and +Accuracy :', null_pos,
    '\n=Grade and -Accuracy :', null_neg)

    for count in range(value_counts.shape[0]):
        row = value_counts.iloc[count, :]
        val = row['count']
        df_array_style.at[row[acc_c], row[grade_c]] = val
    heat_df = df_array_style.fillna(value = 0).iloc[::-1,:]
    x_labels = ['-', '','','', '0','','','','+']
    y_labels = ['+', '','','', '0','','','','-']
    heat_array = heat_df.to_numpy()

    fig, ax = plt.subplots()
    im = ax.imshow(heat_array, cmap=cm.CMRmap_r, vmin = 0, vmax = 100)

    ax.set_xticks(np.arange(len(df_array_style.columns)))
    ax.set_yticks(np.arange(len(df_array_style.index)))
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    cbar = fig.colorbar(im, ax = ax, ticks=[0, 100])
    cbar.ax.set_yticklabels([0, 100])  # vertically oriented colorbar
    cbar.ax.set_ylabel(bar_label, rotation=-90, va="bottom")

    ax.set_xticks(np.arange(heat_array.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(heat_array.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    ax.annotate('', xy = (0,4), xytext = (8,4), arrowprops = dict(arrowstyle = '-'))
    ax.annotate('', xy = (4,0), xytext = (4,8), arrowprops = dict(arrowstyle = '-'))

    ax.set_title(f'Quiz {q1} - {q2} Change in Accuracy vs. Grade')
    plt.xlabel('\nΔ Grade')
    plt.ylabel('Δ Prediction Accuracy\n')

    # for i in range(9):
    #     for j in range(9):
    #         text = ax.text(j, i, heat_array[i, j],
    #                        ha="center", va="center", color= '0.5')

    fig.tight_layout()
    plt.show(block = True)

def regression(df, q1, q2):
    q1 = str(q1)
    q2 = str(q2)
    grade_c = 'Quiz ' + q1 + ' - ' + q2 + ' Grade Change'
    acc_c = 'Quiz ' + q1 + ' - ' + q2 + ' Accuracy Change'
    coo_df = df[[grade_c, acc_c]].dropna()
    x = np.array(coo_df.iloc[:,0].values.tolist()).reshape(-1, 1)
    y = np.array(coo_df.iloc[:,1].values.tolist()).reshape(-1, 1)
    regr = LinearRegression().fit(x,y)
    regr.coef_
    regr.intercept_
    print('Quiz', q1,'-', q2, 'Equation : ', 'y =', regr.coef_[0][0], 'x +', regr.intercept_[0])
    r2 = regr.score(x,y)
    print('R-Squared : ', r2)
    if r2 < 0.9:
        print('roughly no correlation ')

heatmap(df, 1, 3)
heatmap(df, 3, 4)
heatmap(df, 4, 5)

# while True:
#     q1 = input('First Quiz to compare : \n')
#     q2 = input('Second Quiz to compare : \n')
#     ans = input('Heatmap or Regression? : h/r\n')
#     if ans == 'h':
#         heatmap(df, q1, q2)
#     elif ans == 'r':
#         regression(df, q1, q2)
#     else:
#         print('invalid selection, please try again')
#         continue
#     ans = input('Search through another group of quizzes? : y/n\n')
#     if ans == 'y':
#         continue
#     else:
#         ans = input('Are you sure you want to quit? y/n')
#         if ans == 'y':
#             quit()
