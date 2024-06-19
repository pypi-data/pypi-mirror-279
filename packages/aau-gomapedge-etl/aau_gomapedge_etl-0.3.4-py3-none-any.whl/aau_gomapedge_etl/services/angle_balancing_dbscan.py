import math
from typing import Sequence

import numpy as np
from numpy import ndarray
from sklearn.cluster import DBSCAN


# Not threadsafe
class AngleBalancingDBSCAN:
    def __init__(
        self,
        max_distance: float = 10,
        max_angle: float = 0.34907,
        min_samples: int = 5,
        degrees: bool = False,
    ) -> None:
        if max_distance <= 0:
            raise ValueError("max_distance must be a float >0.0")
        if max_angle <= 0:
            raise ValueError("max_angle must be a float >0.0")
        self.max_distance = max_distance
        self.degrees = degrees
        self.max_angle = math.radians(max_angle) if self.degrees else max_angle
        self.min_samples = min_samples

        self.__dbscan = DBSCAN(eps=self.max_distance, min_samples=self.min_samples)

    def _compute_scale_factor(self) -> float:
        if self.max_angle == 0:
            return 1
        # Using The Law of Cosines c^2=a^2+b^2-2ab*cos(C)
        # However we are on the unit circle therefore
        # c^2=1^2+1^2-2*1*1*cos(C)
        # => c^2=2-2*cos(C)
        # => c=sqrt(2-2*cos(C))
        return self.max_distance / np.sqrt(2 - 2 * np.cos(self.max_angle))

    @staticmethod
    def _expand(x: float, y: float, angle: float) -> ndarray:
        return np.array([x, y, math.cos(angle), math.sin(angle)])

    def _balance(self, x, y, cos, sin) -> ndarray:
        scale_factor = self._compute_scale_factor()
        return np.array([x, y, cos * scale_factor, sin * scale_factor])

    def fit_predict(self, X: Sequence[tuple[float, float, float]], y=None) -> ndarray:
        """Clusters an array of [x, y, angle] data points

        Args:
            X (ndarray): [[x, y, angle], [x, y, angle], ...],
            where x and y should be in a metric based coordinate system and
            angle should be in radians or degrees dependent on the degrees instance variable
            y (_type_, optional): _description_. Defaults to None.

        Returns:
            ndarray: An array of cluster IDs where -1 indicate outliers.
            Indices with the same ID belongs to the same cluster.
        """
        copy = np.copy(X)

        if self.degrees:
            copy[:, 2] = np.radians(copy[:, 2])

        scale_factor = self._compute_scale_factor()
        copy[:, 2] = np.cos(copy[:, 2]) * scale_factor
        new_col = np.sin(copy[:, 2]) * scale_factor
        copy = np.column_stack((copy, new_col))

        self.__dbscan.fit(copy)
        return self.__dbscan.labels_
