import numpy as np

class MaxPlusRegression:
    """
    Max-Plus regression.

    Parameters
    ----------
    gle : bool, default=False
        Whether to fit along GLE.
        (If False, fit alnog MMAE.)
    
    Attributes
    ----------
    coef_ : array
        Estimated coefficients for the Max-Plus regression problem.

    Examples
    --------
    >>> reg = MaxPlusRegression().fit(x, y)
    """
    def __init__(self, gle=False) -> None:
        self.gle = gle

    def fit(self, x, y):
        """
        Fit Max-Plus model.

        Parameters
        ----------
        x : array
            Training data.

        y : array
            Target values.

        Returns
        -------
        self : object
            Fitted Estimator.
        """
        try:
            x = np.asarray(x)
            y = np.asarray(y)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        if x.shape[0] != y.shape[0]:
            print("Error: x and y must have the same number of samples.")
            return None
        
        # GLE
        a_hat = np.min(y-x)
        b_hat = np.min(y)
        self.coef_ = [a_hat, b_hat]

        if self.gle:
            return self

        # MMAE
        y_hat = self.predict(x)

        try:
            self.mu_ = np.max(y-y_hat)/2
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
        self.mu_ = np.max(y-y_hat)/2
        a_tilde = a_hat + self.mu_
        b_tilde = b_hat + self.mu_
        self.coef_ = [a_tilde, b_tilde]

        return self

    def predict(self, x):
        """
        Predict using the Max-Plus model.

        Parameters
        ----------
        x : array
            Samples.

        Returns
        -------
        y_pred: array
            Returns predicted values.
        """
        try:
            x = np.asarray(x)
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
        a = self.coef_[0]
        b = self.coef_[-1]
        arr_b = np.ones(len(x))*b
        y_pred = np.stack([x+a, arr_b]).max(axis=0)

        return y_pred

    def rms_score(self, x, y):
        """
        Calculate RMSE.

        Parameters
        ----------
        x : array
            Training data.

        y : array
            Target values.

        Returns
        -------
        C: float
            RMSE.
        """
        try:
            x = np.asarray(x)
            y = np.asarray(y)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        if x.shape[0] != y.shape[0]:
            print("Error: x and y must have the same number of samples.")
            return None
        
        y_true = y
        y_pred = self.predict(x)

        return np.sqrt(np.mean((y_true - y_pred)**2))

    def uniform_score(self, x, y):
        """
        Calculate uniform score.

        Parameters
        ----------
        x : array
            Training data.

        y : array
            Target values.

        Returns
        -------
        C: float
            Uniform score.
        """
        try:
            x = np.asarray(x)
            y = np.asarray(y)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        if x.shape[0] != y.shape[0]:
            print("Error: x and y must have the same number of samples.")
            return None
        
        y_true = y
        y_pred = self.predict(x)

        if y_pred is None:
            return None

        return np.max(np.abs(y_true - y_pred))


class MinPlusRegression:
    """
    Min-Plus regression.

    Parameters
    ----------
    gue : bool, default=False
        Whether to fit along GUE.
        (If False, fit alnog MMAE.)

    Attributes
    ----------
    coef_ : array
        Estimated coefficients for the Min-Plus regression problem.

    Examples
    --------
    >>> reg = MinPlusRegression().fit(x, y)
    """

    def __init__(self, gue=False) -> None:
        self.gue = gue

    def fit(self, x, y):
        """
        Fit Min-Plus model.

        Parameters
        ----------
        x : array
            Training data.

        y : array
            Target values.

        Returns
        -------
        self : object
            Fitted Estimator.
        """
        try:
            x = np.asarray(x)
            y = np.asarray(y)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        if x.shape[0] != y.shape[0]:
            print("Error: x and y must have the same number of samples.")
            return None

        # GUE
        a_hat = np.max(y-x)
        b_hat = np.max(y)
        self.coef_ = [a_hat, b_hat]

        if self.gue:
            return self

        # MMAE
        y_hat = self.predict(x)
        try:
            self.mu_ = np.min(y-y_hat)/2
        except ValueError as e:
            print(f"Error: {e}")
            return None
        a_tilde = a_hat + self.mu_
        b_tilde = b_hat + self.mu_
        self.coef_ = [a_tilde, b_tilde]

        return self

    def predict(self, x):
        """
        Predict using the Min-Plus model.

        Parameters
        ----------
        x : array
            Samples.

        Returns
        -------
        y_pred: array
            Returns predicted values.
        """
        try:
            x = np.asarray(x)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        a = self.coef_[0]
        b = self.coef_[-1]
        arr_b = np.ones(len(x))*b
        y_pred = np.stack([x+a, arr_b]).min(axis=0)

        return y_pred

    def rms_score(self, x, y):
        """
        Calculate RMSE.

        Parameters
        ----------
        x : array
            Training data.

        y : array
            Target values.

        Returns
        -------
        C: float
            RMSE.
        """
        try:
            x = np.asarray(x)
            y = np.asarray(y)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        if x.shape[0] != y.shape[0]:
            print("Error: x and y must have the same number of samples.")
            return None

        y_true = y
        y_pred = self.predict(x)

        if y_pred is None:
            return None

        return np.sqrt(np.mean((y_true - y_pred)**2))

    def uniform_score(self, x, y):
        """
        Calculate uniform score.

        Parameters
        ----------
        x : array
            Training data.

        y : array
            Target values.

        Returns
        -------
        C: float
            Uniform score.
        """
        try:
            x = np.asarray(x)
            y = np.asarray(y)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        if x.shape[0] != y.shape[0]:
            print("Error: x and y must have the same number of samples.")
            return None

        y_true = y
        y_pred = self.predict(x)

        if y_pred is None:
            return None

        return np.max(np.abs(y_true - y_pred))
