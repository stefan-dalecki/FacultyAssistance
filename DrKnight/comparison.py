"""Compare post and pre scores"""
import pandas as pd
import matplotlib.pyplot as plt

path = r"C:\Users\stda9924\Uni\CU\Knight_Rotation/"
file = r"C:\Users\stda9924\Uni\CU\Knight_Rotation\Quiz1_3_4.csv"


class Compare:
    """Comparing scores"""

    def __init__(self, quiz_file: str) -> None:
        self.df = pd.read_csv(quiz_file)
        self.quiz1_pope = None
        self.quiz3_pope = None
        self.quiz4_pope = None
        self.plot_df = None

    def quizzes(self) -> None:
        """Establish quizzes"""
        self.quiz1_pope = (
            self.df["Post Minus Pre - Quiz1"]
            .to_frame()
            .rename(columns={"Post Minus Pre - Quiz1": "Post Minus Pre"})
        )
        self.quiz1_pope["Quiz"] = "Quiz 1"
        self.quiz3_pope = (
            self.df["Post Minus Pre - Quiz3"]
            .to_frame()
            .rename(columns={"Post Minus Pre - Quiz3": "Post Minus Pre"})
        )
        self.quiz3_pope["Quiz"] = "Quiz 3"
        self.quiz4_pope = (
            self.df["Post Minus Pre - Quiz4"]
            .to_frame()
            .rename(columns={"Post Minus Pre - Quiz4": "Post Minus Pre"})
        )
        self.quiz4_pope["Quiz"] = "Quiz 4"
        self.quiz4_pope = (
            self.df["Post Minus Pre - Quiz4"]
            .to_frame()
            .rename(columns={"Post Minus Pre - Quiz4": "Post Minus Pre"})
        )
        return self

    def format_plot(self):
        """Format data for plotting"""
        self.plot_df = pd.concat(
            [self.quiz1_pope, self.quiz3_pope, self.quiz4_pope], axis=0
        )

        self.plot_df["Post Minus Pre"] = self.plot_df["Post Minus Pre"].apply(
            pd.to_numeric, errors="coerce"
        )
        self.plot_df = self.plot_df.dropna().reset_index(drop=True)
        print(self.plot_df.head())

        quiz1 = self.plot_df[self.plot_df["Quiz"] == "Quiz 1"].value_counts()
        print(quiz1)
        return self

    @staticmethod
    def scatter(df: pd.DataFrame) -> None:
        """Make scatter plot of data

        Args:
            df (pd.DataFrame): quiz data
        """
        x = df["Quiz"]
        y = df["Post Minus Pre"]
        plt.scatter(x, y)
        plt.show()


q = Compare(file)
q.quizzes().format_plot()
Compare.scatter(q.plot_df)
