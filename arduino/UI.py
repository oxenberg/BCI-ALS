class UI:

    def __init__(self):
        # self.options = {1: "15hz", 0: "20hz"}
        self.hz_txt = "hz"
        print("------- Game start -------")

    def input(self, classification):
        # classification_text = self.options[classification]
        self.show(classification)

    def show(self, classification_text):
        print(f"the freq is: {classification_text}{self.hz_txt}")
