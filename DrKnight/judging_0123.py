import pandas as pd
import numpy as np

quiz_num = '5'

filename = r'C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz' + quiz_num+'_combined.csv'

df = pd.read_csv(filename).fillna('none')

Student_Codes = pd.DataFrame(columns = ['Quiz ' + quiz_num + ' numerical letter grade', 'Post Minus Pre', 'Awareness'],
)
for row in df.itertuples():
    awareness = 0
    for val in row.Code_1, row.Code_2, row.Code_3:
        if 'K' in val or 'R' in val:
            awareness = awareness + 1
    print('Name :', row.Name,'\n',
    'Codes :',row.Code_1,row.Code_2,row.Code_3,'\n',
    'Awareness :', awareness,'\n')

    new_series = pd.Series(data = {
        'Quiz ' + quiz_num + ' numerical letter grade' : row._8,
        'Post Minus Pre' : row._9,
        'Awareness' : awareness})

    Student_Codes = Student_Codes.append(new_series, ignore_index = True)

Student_Codes.to_csv('Quiz'+quiz_num+'_binning.csv', index = False)

def heatmap(df, col1, col2):
    quiz_heatmap = df[[col1, col2]].dropna().reset_index(drop = True)
    bar_label = '# of Students ' + '(n = ' + str(quiz_heatmap.shape[0]) + ')'
    value_counts = quiz_heatmap.groupby([grade_c, acc_c]).size().reset_index().rename(columns={0:'count'})
    df_array_style = pd.DataFrame(index = range(0, 5), columns = range(0, 4))
    print(df_array_style)

    for count in range(value_counts.shape[0]):
        row = value_counts.iloc[count, :]
        val = row['count']
        df_array_style.at[row[acc_c], row[grade_c]] = val
    heat_df = df_array_style.fillna(value = 0).iloc[::-1,:]
    x_labels = ['0','1','2','3']
    y_labels = ['0','1','2','3','4']
    heat_array = heat_df.to_numpy()

    fig, ax = plt.subplots()
    #either CMRmap_r, gist_earth_r
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

    ax.set_title('Quiz ' + q1 + ' - ' + q2 + ' Change in Accuracy vs. Grade')
    plt.xlabel('\nΔ Grade')
    plt.ylabel('Δ Prediction Accuracy\n')

    # for i in range(9):
    #     for j in range(9):
    #         text = ax.text(j, i, heat_array[i, j],
    #                        ha="center", va="center", color= '0.5')

    fig.tight_layout()
    plt.show(block = True)
