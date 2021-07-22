class UI:

    def __init__(self):
        self.options = {1: "15hz", 0: "20hz"}
        print("------- Game start -------")

    def input(self, classification):
        classification_text = self.options[classification]
        self.show(classification_text)

    def show(self, classification_text):
        print(classification_text)
