from enum import Enum, unique

import numpy as np

from adhoc.node import StationaryNode, MobileNode


@unique
class NodeEnum(Enum):
    StationaryNode = {'id': 0, 'color': (0, 0, 1), 'p': 0}
    MobileNode = {'id': 1, 'color': (0, 1, 0), 'p': 1}


    def __init__(self, N=10) -> None:
        super().__init__()

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



        print(node_choices)


if __name__ == '__main__':
    