"""Predict COVID status based on survey results"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers


class Data:
    """Read in survey data"""

    def __init__(self, survey, key):
        self.survey = pd.read_excel(survey).dropna().reset_index(drop=True)
        self.key = pd.read_excel(key)
        self.data = None
        self.labels = None
        self.raw_train_data = None
        self.raw_train_labels = None
        self.raw_test_data = None
        self.raw_test_labels = None

    def identify(self):
        """Identify labels and questions in survey"""
        self.data = self.survey.iloc[:, 1:]
        self.labels = self.survey.iloc[:, 0]
        assert len(self.data) == len(self.labels)
        return self

    def separate_data(self):
        """Separate data categories"""
        split = int(len(self.data) / 2)
        self.raw_train_data = self.data.iloc[:split, :].reset_index(drop=True)
        self.raw_train_labels = self.labels[:split].values
        self.raw_test_data = self.data.iloc[split:, :].reset_index(drop=True)
        self.raw_test_labels = self.labels[split:].values
        return self


class Pipeline:
    """The machine learning pipeline"""

    def __init__(self, raw_file):
        self.raw = raw_file
        self.train_data = self.vectorize(self.raw.raw_train_data)
        self.train_labels = np.asarray(self.raw.raw_train_labels).astype("float32")
        self.test_data = self.vectorize(self.raw.raw_test_data)
        self.test_labels = np.asarray(self.raw.raw_test_labels).astype("float32")
        self.model = None
        self.history = None

    def vectorize(self, raw_data):
        """Transform survey responses into vectors"""
        tensor = np.zeros((len(raw_data), len(self.raw.key)))
        cols = list(raw_data.columns)
        for response in raw_data.itertuples():
            for col in cols:
                one_response = int(getattr(response, col))
                response_index = Pipeline.binarize(self.raw.key, col, one_response)
                participant_index = response.Index
                tensor[participant_index, response_index] = 1
        return tensor

    @staticmethod
    def binarize(df, question_id: str, response_id: str):
        """Convert answers to binary response

        Args:
            df (pd.DataFrame): question and response dataframe
            question_id (str): short question identifier
            response_id (str): short response identifier

        Returns:
            index: location of vector '1' value
        """
        row = df[df["Question_ID"] == question_id]
        index = row[row["Response_ID"] == response_id].index[0]
        return index

    def set_layers(self):
        """Establish model layers"""
        self.model = keras.Sequential(
            [
                layers.Dense(16, activation="relu"),
                layers.Dense(16, activation="relu"),
                layers.Dense(1, activation="sigmoid"),
            ]
        )
        print("layers set")
        return self

    def compile_model(self):
        """Compile model"""
        assert self.model, "No modile to compile"
        self.model.compile(
            optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"]
        )
        print("compiled")
        return self

    def fit_data(self):
        """Fit data to model"""
        test_split = int(len(self.test_data) / 2)

        x_val = self.train_data[:test_split]
        partial_x_train = self.train_data[test_split:]

        y_val = self.train_labels[:test_split]
        partial_y_train = self.train_labels[test_split:]

        self.history = self.model.fit(
            partial_x_train,
            partial_y_train,
            epochs=20,
            batch_size=512,
            validation_data=(x_val, y_val),
        )


survey_path = r"C:\Users\sjdal\Coding\MachineLearning\shuffled_data.xlsx"
key_path = r"C:\Users\sjdal\Coding\MachineLearning\decoding.xlsx"
file = Data(survey_path, key_path).identify().separate_data()

flow = Pipeline(file)

flow.set_layers()
flow.compile_model()
test_frac = int(len(flow.test_data) / 2)
model_x_val = flow.train_data[:test_frac]
model_partial_x_train = flow.train_data[test_frac:, :]
model_y_val = flow.train_labels[:test_frac]
model_partial_y_train = flow.train_labels[test_frac:]

history = flow.model.fit(
    model_partial_x_train,
    model_partial_y_train,
    epochs=20,
    batch_size=256,
    validation_data=(model_x_val, model_y_val),
)
results = flow.model.evaluate(flow.test_data, flow.test_labels)
history_dict = history.history
loss_values = history_dict["loss"]
val_loss_values = history_dict["val_loss"]
acc = history_dict["accuracy"]
val_acc = history_dict["val_accuracy"]
epochs = range(1, len(loss_values) + 1)
plt.plot(epochs, loss_values, "bo", label="Training loss")
plt.plot(epochs, val_loss_values, "b", label="Validation loss")
plt.plot(epochs, acc, "ro", label="Training acc")
plt.plot(epochs, val_acc, "r", label="Validation acc")
plt.title("Model Performance")
plt.xlabel("Epochs")
plt.ylabel("Loss/Accuracy")
plt.legend(loc=1, bbox_to_anchor=(1.35, 1))
plt.show()

print(f"Test Loss : {results[0]}, Test Accuracy : {results[1]}")
print(history.history)
