"""Alternate linear regression"""
import warnings
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class Fit:
    """Fit data to linear regression"""

    @staticmethod
    def regression(df: pd.DataFrame, col_1: str, col_2: str) -> None:
        """Actual regression pipeline

        Args:
            df (pd.DataFrame): quiz data
            col_1 (str): first column
            col_2 (str): second column
        """
        assert col_1 and col_2 in df
        col_1_data = df[col_1]
        col_2_data = df[col_2]
        data = {col_1_data.name: col_1_data, col_2_data.name: col_2_data}
        reg_df = pd.concat(data, axis=1)
        x = np.array(reg_df.iloc[:, 0].values.tolist()).reshape(-1, 1)
        y = np.array(reg_df.iloc[:, 1].values.tolist()).reshape(-1, 1)
        regr = LinearRegression().fit(x, y)
        print(
            col_1_data.name,
            "vs",
            col_2_data.name,
            "\n y =",
            regr.coef_[0][0],
            "x +",
            regr.intercept_[0],
        )
        r2 = regr.score(x, y)
        print("R-Squared : ", r2)
        if r2 < 0.5:
            print("---roughly no correlation---\n")
        else:
            print()


warnings.simplefilter(action="ignore", category=FutureWarning)

quiz_num = "5"

file = "filename"

quiz_df = pd.read_csv(file)

aware = "Awareness"
grade = f"Quiz {quiz_num} numerical letter grade"
postpre = "Post Minus Pre"

Fit.regression(quiz_df, aware, grade)
Fit.regression(quiz_df, aware, postpre)
