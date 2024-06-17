

class StateHistory: # temporal distribution of a solution
    pass


class State: # spatial distribution of a solution

    def __init__(self, model, data):
        self.model = model

    def interpolate(self, x, elem=None):
        pass

class ScalarState: pass

class VectorState: pass

class VersorState: pass


