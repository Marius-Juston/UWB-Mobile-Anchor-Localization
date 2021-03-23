import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares


class Localize:

    def create_mobile_robot_positions(self, initial_pose=(0, 0, 0), resolution=1000):
        t = np.linspace(0, 2 * np.pi, num=resolution)

        c1 = 2
        c2 = np.pi
        c3 = 1
        c4 = 2.1
        c5 = 1
        c6 = 3
        c7 = -np.pi
        c8 = np.pi
        c9 = 7 * np.pi / 3
        c10 = 1

        a = 0.32
        b = 0.17

        x = initial_pose[0] + a * (c10 * np.sin(t) - c7) * np.sin(c1 * (t - c2))
        y = initial_pose[1] + b * (c9 * np.cos(t) - c8) * np.sin(c3 * (t - c4)) * np.cos(c5 * (t - c6))
        z = initial_pose[2] + np.zeros(resolution)

        path_coordinate = np.vstack([x, y, z])

        return path_coordinate

    def random_stationary_robot(self, random_position_range=((-10, 10), (-10, 10), (-10, 10))):
        x = np.random.uniform(*random_position_range[0])
        y = np.random.uniform(*random_position_range[1])
        z = np.random.uniform(*random_position_range[2])

        return np.array([x, y, z])

    def ranges_calculation(self, path_coordinate, robot_position, mean=0.0, std=0.0):
        diff = robot_position.reshape((-1, 1)) - path_coordinate

        ranges = np.linalg.norm(diff, axis=0)

        return ranges + np.random.normal(mean, std, path_coordinate.shape[1])

    def trilateration(self, positions, ranges, started_pose=(0, 0, 0)):
        def residuals(x):
            angle = x[-1]

            c = np.cos(angle)
            s = np.sin(angle)

            position = np.matmul((
                (c, -s, 0),
                (s, c, 0),
                (0, 0, 1)
            ), positions)

            diff = x[:-1].reshape((-1, 1)) - position

            return np.linalg.norm(diff, axis=0) - ranges

        res = least_squares(residuals, started_pose, jac='3-point', tr_solver='lsmr')

        return res.x[:-1]


if __name__ == '__main__':
    l = Localize()
    path_coordinate = l.create_mobile_robot_positions()
    robot_pose = l.random_stationary_robot()

    fig, position_ax = plt.subplots(1)
    # fig, position_ax,range_ax,derivative_ax = plt.subplots(1)

    position_ax.set_aspect('equal')

    position_ax.plot(path_coordinate[0], path_coordinate[1], c='b')
    # derivatives = (ranges[1:] - ranges[:-1]) / (1 / 100)

    error = np.zeros(3)

    print(robot_pose)

    N = 1000

    for i in range(N):
        ranges = l.ranges_calculation(path_coordinate, robot_pose, mean=0, std=0.5)
        estimated_location = l.trilateration(path_coordinate, ranges, np.random.uniform(0, 0, 4))
        # print(estimated_location)
        position_ax.scatter(estimated_location[0], estimated_location[1], c='g')

        error += (estimated_location - robot_pose) ** 2

    position_ax.scatter(robot_pose[0], robot_pose[1], c='r')
    error = np.sqrt(error / N)
    print(error)

    # range_ax.plot(ranges)
    # derivative_ax.plot(derivatives)

    plt.show()
