import numpy as np


class AsymetricMotion:

    def __init__(self) -> None:
        super().__init__()

        self.a = 3
        self.b = 1.6
        self.c1 = 1
        self.c2 = 1
        self.c3 = 1
        self.c4 = 2.5
        self.c5 = 3
        self.c6 = 8.2
        self.c7 = 1
        self.c8 = 4.56

    def calculate(self, t):
        self.r = np.vstack([self.a * np.cos(self.c1 * (t - self.c2)) * np.cos(self.c3 * (t - self.c4)),
                            self.b * np.cos(self.c5 * (t - self.c6)) * np.sin(self.c7 * (t - self.c8))])

        self.v = np.vstack(
            [
                -self.a * (np.cos(self.c3 * (t - self.c4)) * np.sin(self.c1 * (t - self.c2)) * self.c1 +
                           np.cos(self.c1 * (t - self.c2)) * np.sin(self.c3 * (t - self.c4)) * self.c3),
                -self.b * np.sin(self.c5 * (t - self.c6)) * np.sin(self.c7 * (t - self.c8)) * self.c5 +
                self.b * np.cos(self.c5 * (t - self.c6)) * np.cos(self.c7 * (t - self.c8)) * self.c7
            ]
        )

        self.ac = np.vstack(
            [
                2 * self.a * np.sin(self.c1 * (t - self.c2)) *
                np.sin(self.c3 * (t - self.c4)) * self.c1 * self.c3 -
                self.a * np.cos(self.c1 * (t - self.c2)) * np.cos(self.c3 * (t - self.c4)) *
                (self.c1 ** 2 + self.c3 ** 2),
                -2 * self.b * np.cos(self.c7 * (t - self.c8)) *
                np.sin(self.c5 * (t - self.c6)) *
                self.c5 * self.c7 -
                self.b * np.cos(self.c5 * (t - self.c6)) *
                np.sin(self.c7 * (t - self.c8)) *
                (self.c5 ** 2 + self.c7 ** 2)
            ]
        )

        self.v_mag = np.linalg.norm(self.v, axis=0)

        self.k = np.cross(self.v, self.ac, axis=0) / (self.v_mag ** 3)

        self.w = self.v_mag * self.k

    def calculate_offset(self, d=0):
        rotation_matrix = np.array([
            [0, 1],
            [-1, 0]
        ])

        rotated_scaled_v = rotation_matrix @ self.v / self.v_mag

        return self.r + d * rotated_scaled_v


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    t = np.linspace(0, np.pi)

    model = AsymetricMotion()

    model.calculate(t)

    plt.plot(model.r[0], model.r[1])

    r = model.calculate_offset(-0.13)

    plt.plot(r[0], r[1])
    plt.show()

    plt.plot(t, model.v_mag)
    plt.plot(t, model.w)
    plt.show()
