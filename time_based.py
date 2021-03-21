import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

np.random.seed(42)


class Localize:

    def __init__(self) -> None:
        super().__init__()

        self.c1 = 2
        self.c2 = np.pi
        self.c3 = 1
        self.c4 = 2.1
        self.c5 = 1
        self.c6 = 3
        self.c7 = -np.pi
        self.c8 = np.pi
        self.c9 = 7 * np.pi / 3
        self.c10 = 1

        self.a = 0.32
        self.b = 0.17

    def calcualte_derivative(self, t, x0, y0):
        c1 = self.c1
        c2 = self.c2
        c3 = self.c3
        c4 = self.c4
        c5 = self.c5
        c6 = self.c6
        c7 = self.c7
        c8 = self.c8
        c9 = self.c9
        c10 = self.c10

        a = self.a
        b = self.b

        top = 2 * (-a * np.cos(t) * np.sin(c1 * (t - c2)) * c10 + a * np.cos(c1 * (t - c2)) * c1 * (
                c7 - np.sin(t) * c10)) * (a * np.sin(c1 * (t - c2)) * (c7 - np.sin(t) * c10) + x0) + 2 * b * (
                      np.cos(c3 * (t - c4)) * np.cos(c5 * (t - c6)) * c3 * (c8 - np.cos(t) * c9) + np.sin(
                  c3 * (t - c4)) * (np.cos(c5 * (t - c6)) * np.sin(t) * c9 - np.sin(c5 * (t - c6)) * c5 * (
                      c8 - np.cos(t) * c9))) * (
                      b * np.cos(c5 * (t - c6)) * np.sin(c3 * (t - c4)) * (c8 - np.cos(t) * c9) + y0)

        bottom = 2 * np.sqrt((a * np.sin(c1 * (t - c2)) * (c7 - np.sin(t) * c10) + x0) ** 2 + (
                b * np.cos(c5 * (t - c6)) * np.sin(c3 * (t - c4)) * (c8 - np.cos(t) * c9) + y0) ** 2)

        return top / bottom

    def create_mobile_robot_positions(self, initial_pose=(0, 0, 0), resolution=1000):
        t = np.linspace(0, 2 * np.pi, num=resolution)

        x = initial_pose[0] + self.a * (self.c10 * np.sin(t) - self.c7) * np.sin(self.c1 * (t - self.c2))
        y = initial_pose[1] + self.b * (self.c9 * np.cos(t) - self.c8) * np.sin(self.c3 * (t - self.c4)) * np.cos(
            self.c5 * (t - self.c6))
        z = initial_pose[2] + np.zeros(t.shape[0])

        path_coordinate = np.vstack([x, y, z])

        return t, path_coordinate

    def random_stationary_robot(self, random_position_range=((-10, 10), (-10, 10), (-10, 10))):
        x = np.random.uniform(*random_position_range[0])
        y = np.random.uniform(*random_position_range[1])
        z = np.random.uniform(*random_position_range[2])

        return np.array([x, y, z])

    def ranges_calculation(self, path_coordinate, robot_position, mean=0.0, std=0.0):
        diff = robot_position.reshape((-1, 1)) - path_coordinate

        ranges = np.linalg.norm(diff, axis=0)

        return ranges + np.random.normal(mean, std, path_coordinate.shape[1])

    def trilateration(self, t, path_coordinate, ranges, started_pose=(0, 0, 0)):
        def residuals(x):
            diff = x.reshape((-1, 1)) - path_coordinate

            distances = np.linalg.norm(diff, axis=0)
            distance_residual = distances - ranges

            path_derivative = self.calcualte_derivative(t, x[0], x[1])
            path_derivative = path_derivative[1:]

            derivatives = (distances[1:] - distances[:-1]) / (t[1:] - t[:-1])

            derivative_residual = (derivatives - path_derivative)

            print(np.sum(derivative_residual) * 1000)

            # return np.concatenate([distance_residual, derivative_residual])
            # return distance_residual
            return derivative_residual * 1000

        res = least_squares(residuals, started_pose)

        return res.x


if __name__ == '__main__':
    l = Localize()
    times, path_coordinate = l.create_mobile_robot_positions()
    robot_pose = l.random_stationary_robot()

    # fig, position_ax = plt.subplots(1)
    fig, (position_ax, range_ax, derivative_ax) = plt.subplots(3)

    position_ax.set_aspect('equal')

    position_ax.plot(times[0], times[1], c='b')
    # derivatives = (ranges[1:] - ranges[:-1]) / (1 / 100)

    error = np.zeros(3)

    print(robot_pose)

    N = 1

    for i in range(N):
        ranges = l.ranges_calculation(path_coordinate, robot_pose, mean=0, std=0.5)
        estimated_location = l.trilateration(times, path_coordinate, ranges, np.random.uniform(0, 0, 3))
        # print(estimated_location)
        position_ax.scatter(estimated_location[0], estimated_location[1], c='g')

        error += (estimated_location - robot_pose) ** 2

    position_ax.scatter(robot_pose[0], robot_pose[1], c='r')
    error = np.sqrt(error / N)
    print(error)

    # range_ax.plot(ranges)
    derivative_ax.plot(np.linspace(0, 2 * np.pi, num=1000), l.calcualte_derivative(times, -1.3, -9))
    derivative_ax.grid(True)

    plt.show()
