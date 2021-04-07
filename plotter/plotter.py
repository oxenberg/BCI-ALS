import pandas as pd
import seaborn as sns

from inputModule import read_params


class Plotter:
    def __init__(self,debug = False):
        self.params = read_params()
        self.debug = debug
        self.data = pd.DataFrame(columns=["game_index", "pred_label", "real_label"])
    def plot_acc(self):...

    def plot_label_dis(self):
        action_dict = self.params["ACTIONS"]
        self.data["x_round_label"] = self.data[["game_index","real_label"]].apply(lambda row:
                                                                                  f"{row['game_index']},{action_dict[str(row['real_label'])]}")

        g = sns.catplot(
            data=self.data, kind="count",
            x="x_round_label", hue="pred_label",
            ci="sd", palette="dark", alpha=.6, height=6
        )
        g.legend.set_title("label distribution per game")
    def collect_data(self, game_index, predicted_labels, label):
        """
        collect data to dataframe
        :param game_index:  int, game index
        :param predicted_labels: list, predicted labels in game
        :param label: int, real label for game
        """
        # game index get always next round index
        game_index -=1

        raw_index = self.data.shape[0]
        labels = [label] * len(predicted_labels)
        for predicted_label, label in zip(predicted_labels, labels):
            self.data.loc[raw_index] = [game_index, predicted_label, label]
            raw_index += 1

    def plot(self):
        if self.debug:
            self.plot_acc()
            self.plot_label_dis()

    def save_data(self):
        self.data.to_csv("games_data.csv")