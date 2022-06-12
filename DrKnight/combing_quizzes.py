"""Combine multiple quizzes for analysis over time"""
import functools
import pandas as pd


class BigQuiz:
    """All quizzes combined"""

    def __init__(self) -> None:
        self.quiz1 = pd.read_csv(
            r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz1_combined.csv"
        )
        self.quiz3 = pd.read_csv(
            r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz3_combined.csv"
        )
        self.quiz4 = pd.read_csv(
            r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz4_combined.csv"
        )
        self.quiz5 = pd.read_csv(
            r"C:\Users\stda9924\Uni\CU\Knight_Rotation\CSV_Files\Updated_Quizzes\Quiz5_combined.csv"
        )

        self.data_frames = [self.quiz1, self.quiz3, self.quiz4, self.quiz5]

    @staticmethod
    def suffix(df: pd.DataFrame, num: int) -> pd.DataFrame:
        """Establish column to merge dataframes

        Args:
            df (pd.DataFrame): quiz data
            num (int): quiz number

        Returns:
            pd.DataFrame: columns for merge
        """
        return df.columns.map(
            lambda x: x + " - Quiz" + str(num) if x != "Name" and x != "S_ID" else x
        )


big = BigQuiz()
BigQuiz.suffix(big.quiz1, 1)
BigQuiz.suffix(big.quiz3, 3)
BigQuiz.suffix(big.quiz4, 4)
BigQuiz.suffix(big.quiz5, 5)

df_merged = functools.reduce(
    lambda left, right: pd.merge_ordered(left, right, on=["Name", "S_ID"], how="outer"),
    big.data_frames,
).fillna("void")

df_merged.to_csv("perhaps.csv", index=False)
