from enum import Enum, unique

import matplotlib.pyplot as plt
import numpy as np

from adhoc.node import StationaryNode, MobileNode


@unique
class NodeEnum(Enum):
    StationaryNode = {'id': 0, 'color': (0, 0, 1), 'p': .5}
    MobileNode = {'id': 1, 'color': (0, 1, 0), 'p': .5}


class RandomNetwork:
    def __init__(self, N=10, start_range=((-10, 10), (-10, 10)), dt=0.1) -> None:
        super().__init__()

        self.dt = dt
        self.start_range = start_range
        self.N = N
        self.network = None
        self.current_time = 0

        self.create_random_nodes()

    def create_random_nodes(self):
        options = []
        p = []

        for e in NodeEnum:
            options.append(e)
            p.append(e.value['p'])

        node_choices = np.random.choice(
            options,
            self.N,
            p=p
        )

        node_pose = np.vstack([
            np.random.uniform(self.start_range[0][0], self.start_range[0][1], self.N),
            np.random.uniform(self.start_range[1][0], self.start_range[1][1], self.N)
        ])

        anchor_id = 0

        tag_id = 0

        self.network = []

        for index, node in enumerate(node_choices):
            actual_pose = node_pose[:, index]

            if node is NodeEnum.StationaryNode:
                self.network.append(StationaryNode(anchor_id, actual_pose))
                anchor_id += 1
            elif node is NodeEnum.MobileNode:
                self.network.append(MobileNode(anchor_id, tag_id, tag_id + 1, actual_pose))

                anchor_id += 1
                tag_id += 2

            print(node, len(self.network), actual_pose)

    def draw_network(self):
        ax = plt.gca()
        ax.cla()

        for node in self.network:
            node_type = NodeEnum.__members__[type(node).__name__]

            color = node_type.value['color']

            if node_type is NodeEnum.StationaryNode:
                pose = node.x

                ax.scatter(pose[0], pose[1], color=color)
            elif node_type is NodeEnum.MobileNode:
                pose = node.actual_pose

                outline_color = 'r'
                if node.is_localized:
                    outline_color = 'b'

                ax.scatter(pose[0], pose[1], s=75, color=outline_color)
                ax.scatter(pose[0], pose[1], color=color)

    def step(self):
        for node in self.network:
            if NodeEnum.__members__[type(node).__name__] == NodeEnum.MobileNode:
                node.neighbor = [other_node for other_node in self.network if node != other_node]

        for node in self.network:
            node.update()

        self.current_time += self.dt

        self.draw_network()
        plt.show()


if __name__ == '__main__':
    node_network = RandomNetwork()

    plt.ion()
    plt.show(block=False)

    for i in range(100):
        node_network.step()
        plt.pause(0.0001)

    plt.show()
