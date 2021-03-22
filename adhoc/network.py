from enum import Enum, unique

import numpy as np

from adhoc.node import StationaryNode, MobileNode


@unique
class NodeEnum(Enum):
    StationaryNode = {'id': 0, 'color': (0, 0, 1), 'p': 0}
    MobileNode = {'id': 1, 'color': (0, 1, 0), 'p': 1}


class RandomNetwork:
    def __init__(self, N=10, start_range=((-10, 10), (-10, 10))) -> None:
        super().__init__()

        self.start_range = start_range
        self.N = N
        self.network = None

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


if __name__ == '__main__':
    node_network = RandomNetwork()
