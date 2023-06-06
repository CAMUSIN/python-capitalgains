from abc import ABC, abstractmethod


class Sender(ABC):

    @abstractmethod
    def send(self, taxes: str):
        pass


class TaxSender(Sender):

    def send(self, taxes: str):
        print(taxes)
