import numpy as np


class Scaler:
    def __init__(self, A=None):
        self.A = A

    def scale_list(self, ts):
        for t in ts:
            yield self.scale(t)

    def scale(self, t):
        return t


class Linear(Scaler):  # no transformation, for SP-CT
    pass


class AlphaToT(Scaler):  # α > 0 -> 0 < t < α^{-1}
    def __init__(self, A=None):
        super().__init__(A)
        cfm = np.linalg.eigvals(self.A)
        self.rho = np.max(np.abs(cfm))

    def scale(self, alpha):
        return 1 / (1 / alpha + self.rho)


class Rho(Scaler):  # pWalk, Walk
    def __init__(self, A=None):
        super().__init__(A)
        cfm = np.linalg.eigvals(self.A)
        self.rho = np.max(np.abs(cfm))

    def scale(self, t):
        return t / self.rho


class Fraction(Scaler):  # Forest, logForest, Comm, logComm, Heat, logHeat, SCT, SCCT, ...
    def scale(self, t):
        return 0.5 * t / (1.0 - t)


class FractionReversed(Scaler):  # RSP, FE
    def scale(self, beta):
        return (1.0 - beta) / beta
