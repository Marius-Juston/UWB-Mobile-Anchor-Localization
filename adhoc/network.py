import numpy as np

from adhoc.node import StationaryNode, MobileNode

class NodeEnum:
    StationaryNode = 0
    MobileNode = 1


class RandomNetwork:
    node_weight = {
        NodeEnum.StationaryNode: .1,
        NodeEnum.MobileNode: .9
    }

    def __init__(self, N=10) -> None:
        super().__init__()

        self.N = N
        self.network = None

        self.create_random_nodes()

    def create_random_nodes(self):
        node_choices = np.random.choice(
            tuple(RandomNetwork.node_weight.keys()),
            self.N,
            p=tuple(RandomNetwork.node_weight.values())
        )



        print(node_choices)


if __name__ == '__main__':
    