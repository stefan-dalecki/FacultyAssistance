import pandas as pd
import numpy as np


class Data:
    def __init__(self, survey, key):
        self.survey = pd.read_excel(survey).dropna()
        self.key = pd.read_excel(key)
        self.data = None
        self.labels = None
        self.raw_train_data = None
        self.raw_train_labels = None
        self.raw_test_data = None
        self.raw_test_labels = None

    def identify(self):
        self.data = self.survey.iloc[:, 1:]
        self.labels = self.survey.iloc[:, 0]
        return self

    def separate_data(self):
        split = int(len(self.data) / 2)
        self.raw_train_data = self.data.iloc[:split, :]
        self.raw_train_labels = self.labels[:split]
        self.raw_test_data = self.data.iloc[split:, :]
        self.raw_test_labels = self.labels[split:]
        return self


class Pipeline:
    def __init__(self, raw_file):
        self.raw = raw_file
        self.train_data = self.vectorize(self.raw.raw_train_data)
        self.train_labels = np.asarray(self.raw.raw_train_labels).astype("float32")
        self.test_data = self.vectorize(self.raw.raw_test_data)
        self.test_labels = np.asarray(self.raw.raw_test_labels).astype("float32")

    def vectorize(self, data):
        tensor = np.zeros((len(self.raw.key), len(data)))
        cols = list(data.columns)
        for response in data.itertuples():
            for col in cols:
                one_response = int(getattr(response, col))
                response_index = Pipeline.binarize(self.raw.key, col, one_response)
                participant_index = response.Index
                tensor[response_index, participant_index] = 1
        return tensor

    @staticmethod
    def binarize(df, question_id, response_id):
        row = df[df["Question_ID"] == question_id]
        index = row[row["Response_ID"] == response_id].index[0]
        return index


print("starting")
survey_path = r"C:\Users\sjdal\Coding\MachineLearning\shuffled_data.xlsx"
key_path = r"C:\Users\sjdal\Coding\MachineLearning\decoding.xlsx"
file = Data(survey_path, key_path).identify().separate_data()
flow = Pipeline(file)
print("completed")
