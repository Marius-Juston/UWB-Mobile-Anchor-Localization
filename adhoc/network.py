import numpy as np

from adhoc.node import StationaryNode, MobileNode


class RandomNetwork:
    node_weight = {
        StationaryNode: 0,
        MobileNode: 1
    }

    def __init__(self, N=10) -> None:
        super().__init__()

        self.N = N
        self.network = None

        self.create_random_nodes()

    def create_random_nodes(self):
        node_choices = np.random.choice(RandomNetwork.node_weight.keys(), self.N, p=RandomNetwork.node_weight.values())

        print(node_choices)


if __name__ == '__main__':
    