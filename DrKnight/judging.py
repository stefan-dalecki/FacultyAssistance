"""Judge quizzes"""
import pandas as pd

quiz_num = "5"

filename = (
    r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz"
    + quiz_num
    + "_combined.csv"
)

df = pd.read_csv(filename).fillna("none")

Student_Codes = pd.DataFrame(
    columns=[
        f"Quiz {quiz_num} numerical letter grade",
        "Post Minus Pre",
        "Blame",
        "Responsibility",
        "Knowledge",
        "Performance",
        "Mood",
        "Awareness",
    ],
)

print(Student_Codes)
for row in df.itertuples():
    print(row.Index)
    blam_count, resp_count, know_count, perf_count, mood_count = 0, 0, 0, 0, 0
    for val in row.Code_1, row.Code_2, row.Code_3:
        if "B" in val:
            blam_count = blam_count + 1
        if "R" in val:
            resp_count = resp_count + 1
        if "K" in val:
            know_count = know_count + 1
        if "P" in val:
            perf_count = perf_count + 1
        if "M" in val:
            mood_count = mood_count + 1
    print(
        "Name :",
        row.Name,
        "\n",
        "Codes :",
        row.Code_1,
        row.Code_2,
        row.Code_3,
        "\n",
        "Blame :",
        blam_count,
        "\n",
        "Responsibility :",
        resp_count,
        "\n",
        "Knowledge :",
        know_count,
        "\n",
        "Performance :",
        perf_count,
        "\n",
        "Mood :",
        mood_count,
        "\n",
    )

    new_series = pd.Series(
        data={
            "Quiz " + quiz_num + " numerical letter grade": row._8,
            "Post Minus Pre": row._9,
            "Blame": blam_count,
            "Responsibility": resp_count,
            "Knowledge": know_count,
            "Performance": perf_count,
            "Mood": mood_count,
            "Awareness": resp_count + know_count,
        }
    )

    Student_Codes = Student_Codes.append(new_series, ignore_index=True)
save_path = r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Results/"
Student_Codes.to_csv(
    save_path + "Quiz" + quiz_num + "_CodeQuantification.csv", index=False
)
