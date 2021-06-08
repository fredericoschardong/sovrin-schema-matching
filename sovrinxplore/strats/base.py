from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self, ledger: str):
        super(Base, self).__init__()
        self.ledger = ledger

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass
