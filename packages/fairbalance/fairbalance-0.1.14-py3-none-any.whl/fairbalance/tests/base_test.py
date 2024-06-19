import pandas as pd


class BaseSetUp:
    def setUp(self, multi=False):
        data = {
            'feature1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'feature2': [5, 6, 7, 1, 3, 1, 12, 7, 3, 9, 24, 1, 6, 2, 9, 20, 6, 18, 19, 2],
            'protected_attribute': ['A', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'B'],
            'protected_attribute_2': ['C', 'C', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'C', 'D'],
        }
        # A 1: 7 and 0: 3
        # B 1: 6 and 0: 4
        target = [1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0]
        # target = [A, A, A, B, A, B, B, B, B, B, A, B, A, B, A, A, A, B, A, B]
        self.dataset = pd.DataFrame(data)
        self.target = pd.DataFrame(target, columns=["target"])
        if multi:
            self.protected_attributes = [
                "protected_attribute", "protected_attribute_2"]
            self.privileged_groups = {
                "protected_attribute": "A", "protected_attribute_2": "C"}
        else:
            self.protected_attributes = ["protected_attribute"]
            self.privileged_groups = {"protected_attribute": "A"}
        self.cont_columns = ["feature2"]
        self.cat_columns = ["feature1",
                            "protected_attribute", "protected_attribute_2"]
