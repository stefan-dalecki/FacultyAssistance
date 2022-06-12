"""Generate binned heatmaps"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

quiz_num = "5"

file = (
    r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Results\Quiz"
    f"{quiz_num}_binning.csv"
)

quiz_df = pd.read_csv(file)

if "no pre-grade for calculation" in quiz_df["Post Minus Pre"]:
    df_postpre = quiz_df[
        ~quiz_df["Post Minus Pre"].str.contains("no pre-grade for calcuation")
    ]
else:
    df_postpre = quiz_df
df_postpre = df_postpre.apply(pd.to_numeric, errors="coerce")


grade = quiz_df.columns[0]
grade_name = "Grade"
postpre = quiz_df.columns[1]
postpre_name = "Prediction Accuracy"
aware = quiz_df.columns[2]


def heatmap(df: pd.DataFrame, col1: str, col2: str) -> None:
    """Generate a heatmap comparing two columns of data

    Args:
        df (pd.DataFrame): quiz data
        col1 (str): first column
        col2 (str): second column
    """
    assert col1 and col2 in df.columns
    quiz_heatmap = df[[col1, col2]].dropna().reset_index(drop=True)
    bar_label = "# of Students " + "(n = " + str(quiz_heatmap.shape[0]) + ")"
    value_counts = (
        quiz_heatmap.groupby([col1, col2])
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )
    df_array_style = pd.DataFrame(
        index=range(df[col2].min(), df[col2].max() + 1),
        columns=range(df[col1].min(), df[col1].max() + 1),
    )

    for count in range(value_counts.shape[0]):
        row = value_counts.iloc[count, :]
        val = row["count"]
        df_array_style.at[row[col2], row[col1]] = val

    heat_df = df_array_style.fillna(value=0).iloc[::-1, :]

    x_labels = list(range(df[col1].min(), df[col1].max() + 1))
    y_labels = reversed(list(range(df[col2].min(), df[col2].max() + 1)))

    heat_array = heat_df.to_numpy()

    fig, ax = plt.subplots()
    # either CMRmap_r, gist_earth_r
    im = ax.imshow(heat_array, cmap=cm.bone_r, vmin=0, vmax=100)

    ax.set_xticks(np.arange(len(df_array_style.columns)))
    ax.set_yticks(np.arange(len(df_array_style.index)))
    ax.set_xticklabels(x_labels)
    if col2 == grade:
        ax.set_yticklabels(["A", "B", "C", "D", "F"])
    else:
        ax.set_yticklabels(y_labels)

    cbar = fig.colorbar(im, ax=ax, ticks=[0, 100])
    cbar.ax.set_yticklabels([0, 100])  # vertically oriented colorbar
    cbar.ax.set_ylabel(bar_label, rotation=-90, va="bottom")

    ax.set_xticks(np.arange(heat_array.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(heat_array.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)
    if col2 == grade:
        ax.set_title(col1 + " vs " + "Quiz " + quiz_num + " Grade")
        plt.ylabel("Grade (avg = " + str(df[col2].mean())[:4] + ")\n")
    elif col2 == postpre:
        ax.set_title(col1 + " vs " + postpre_name)
        plt.ylabel("Prediction Accuracy (avg = " + str(df[col2].mean())[:4] + ")\n")
    else:
        ax.set_title(col1 + " vs " + col2)
        plt.ylabel(col2 + "(avg = " + str(df[col2].mean())[:4] + ")\n")
    plt.xlabel("\n" + col1 + " (avg = " + str(df[col1].mean())[:4] + ")\n")

    if col2 == grade:
        for i in range(df[col2].min(), df[col2].max() + 1):
            for j in range(df[col1].min(), df[col1].max() + 1):
                textcolors = ("black", "white")
                threshold = im.norm(heat_array.max()) / 1.5
                ax.text(
                    j,
                    i,
                    heat_array[i, j],
                    ha="center",
                    va="center",
                    color=textcolors[int(im.norm(heat_array[i, j]) > threshold)],
                )

    fig.tight_layout()
    plt.show(block=True)


heatmap(quiz_df, aware, grade)
