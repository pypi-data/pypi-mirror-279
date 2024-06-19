import numpy as np
from dataclasses import dataclass, field
from typing import Union, Tuple


class SheetPileWall:
    name: str = "BZ17"
    b: float = 500.0
    H: float = 300.0
    e: float = 10.0
    a: float = 9.5
    I_x: float = field(init=False)
    W_x: float = field(init=False)

    def __post_init__(self) -> None:

        areas = self._areas(self.e, self.a)
        xs = self._xs(self.H, self.e)

        x_center = areas.dot(xs) / areas.sum()

        self.I_x = areas.dot((xs-x_center)**2)
        self.I_x /= (self.b / 1_000)

        self.W_x = self.I_x / (self.H * 1e-1 / 2)
        self.W_x *= 1670 / 1177.4  # BZ properties: W_x = 1670, Calculation with C=0: W_x = 1177

    def _areas(self, e: Union[float, np.ndarray[("n_C_grid"), float]],
               a: Union[float, np.ndarray[("n_C_grid"), float]])\
            -> Union[float, np.ndarray[("n_C_grid"), float]]:
        area_1 = 0.42 * self.b * e
        area_2 = 0.54 * self.b * a
        area_3 = 0.42 * self.b * e
        areas = np.array([area_1, area_2, area_3]) * 1e-2
        return areas

    def _xs(self, H: Union[float, np.ndarray[("n_C_grid"), float]],
            e: Union[float, np.ndarray[("n_C_grid"), float]])\
            ->Union[float, np.ndarray[("n_C_grid"), float]]:
        x_1 = H - e / 2
        x_2 = H / 2
        x_3 = e / 2
        xs = np.array([x_1, x_2, x_3]) * 1e-1
        return xs

    def reduce_thickness(self, C: Union[float, np.ndarray[("n_C_grid"), float]])\
            -> Tuple[Union[float, np.ndarray[("n_C_grid"), float]], Union[float, np.ndarray[("n_C_grid"), float]]]:

        H = self.H - C
        e = self.e - C
        a = self.a - C

        areas = self._areas(e, a)
        xs = self._xs(H, e)

        x_center = np.multiply(areas, xs).sum(axis=0) / areas.sum(axis=0)

        I_x = np.multiply(areas, (xs-x_center[np.newaxis, :])**2).sum(axis=0)
        I_x /= (self.b / 1_000)

        W_x = I_x / (H * 1e-1 / 2)
        W_x *= 1670 / 1177.4

        return I_x, W_x


if __name__ == "__main__":

    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    wall = SheetPileWall()

    C_grid = np.linspace(0, min(wall.a, wall.e), 100)
    I_x, W_x = wall.reduce_thickness(C_grid)

    I_reduction_model_intercept = I_x[0]
    I_reduction_model_slope = (I_x[-1] - I_x[0]) / (C_grid[-1] - C_grid[0])
    I_x_model = I_reduction_model_intercept + I_reduction_model_slope * C_grid

    W_reduction_model_intercept = W_x[0]
    W_reduction_model_slope = (W_x[-1] - W_x[0]) / (C_grid[-1] - C_grid[0])
    W_x_model = W_reduction_model_intercept + W_reduction_model_slope * C_grid

    fig = plt.figure()
    plt.plot(C_grid, I_x, c='b', label='Calculation')
    plt.plot(C_grid, I_x_model, c='r', label='Model')
    plt.xlabel('Corrosion [mm]', fontsize=14)
    plt.ylabel('Section modulus per m [${cm}^{3}$/m]', fontsize=14)
    plt.legend(title="Section modulus by:", fontsize=12)

    fig = plt.figure()
    plt.plot(C_grid, W_x, c='b', label='Calculation')
    plt.plot(C_grid, W_x_model, c='r', label='Model')
    plt.xlabel('Corrosion [mm]', fontsize=14)
    plt.ylabel('Section modulus per m [${cm}^{3}$/m]', fontsize=14)
    plt.legend(title="Section modulus by:", fontsize=12)
