from sklearn import linear_model
from src.blockchain.block import Block
import copy
from src.model.model import Model

# https://scikit-learn.org/0.15/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor.partial_fit
# https://scikit-learn.org/0.15/modules/scaling_strategies.html

class SgdModel(Model):
    def __init__(self):
        self.current_model = linear_model.SGDRegressor()
        self.current_model.coef_ = None
        self.current_model.intercept_ = None

    def get_score(self, datapoints):
        data = []
        targets = []
        for datapoint in datapoints:
            data.append(datapoint.get_data())
            targets.append(datapoint.get_target())
        return self.current_model.score(data, targets)

    def train(self, datapoints):
        data = []
        targets = []
        for datapoint in datapoints:
            data.append(datapoint.get_data())
            targets.append(datapoint.get_target())
        self.current_model.partial_fit(data, targets)

    def __eq__(self, other_model):            
        if other_model is None:
            return False

        curr_coef = self.current_model.coef_
        other_ceof = other_model.get_coef()

        if (curr_coef is None) and (other_ceof is None):
            pass
        elif (((curr_coef is None) and (other_ceof is not None)) or ((curr_coef is not None) and (other_ceof is None))):
            return False
        else:            
            if curr_coef.__class__.__name__ != other_ceof.__class__.__name__:
                return False

            if len(curr_coef) != len(other_ceof):
                return False

            for i in range(len(curr_coef)):
                if curr_coef[i] != other_ceof[i]:
                    return False

        curr_intercept = self.current_model.intercept_
        other_intercept = other_model.get_intercept()

        if (curr_intercept is None) and (other_intercept is None):
            pass
        elif (((curr_intercept is None) and (other_intercept is not None)) or ((curr_intercept is not None) and (other_intercept is None))):
            return False
        else:    
            if curr_intercept.__class__.__name__ != other_intercept.__class__.__name__:
                return False

            if isinstance(curr_intercept, float):
                if curr_intercept != other_intercept:
                    return False
            else:
                if len(curr_intercept) != len(other_intercept):
                    return False

                for i in range(len(curr_intercept)):
                    if curr_intercept[i] != other_intercept[i]:
                        return False

        return True

    def set_from_block(self, block):
        model = block.get_model()
        self.current_model.coef_ = copy.deepcopy(model.get_coef())
        self.current_model.intercept_ = copy.deepcopy(model.get_intercept())

    def set_from_model(self, ref_model):
        self.current_model.coef_ = copy.deepcopy(ref_model.get_coef())
        self.current_model.intercept_ = copy.deepcopy(ref_model.get_intercept())

    def get_coef(self):
        return self.current_model.coef_

    def get_intercept(self):
        return self.current_model.intercept_

    def __str__(self):
        return "COEF: " + str(self.current_model.coef_) + ", INTERCEPT: " + str(self.current_model.intercept_)

    def set_coef(self, new_coef):
        self.current_model.coef_ = new_coef

    def set_intercept(self, new_intercept):
        self.current_model.intercept_ = new_intercept

    def aggregate_models(self, model_list):
        new_coef = 0
        new_intercept = 0
        for model in model_list:
            new_coef += model.get_coef()
            new_intercept += model.get_intercept()
        new_coef /= len(model_list)
        new_intercept /= len(model_list)

        aggregated_model = SgdModel()
        aggregated_model.set_coef(new_coef)
        aggregated_model.set_intercept(new_intercept)

        return aggregated_model
    
    def predict(self, datapoint):
        return self.current_model.predict([datapoint.get_data()])