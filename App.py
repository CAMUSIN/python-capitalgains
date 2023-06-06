import json
from Entities.operation import OperationDecoder
from Entities.taxDetail import TaxDetailEncoder
from Services.Processor import Processor
from Services.Sender import Sender


class App():
    def __init__(self, processor: Processor, sender: Sender):
        self.processor = processor
        self.sender = sender

    def Run(self, args):
        try:
            transactions = json.loads(args, object_hook= OperationDecoder)
            taxes = self.processor.taxes_processor(transactions)
            self.sender.send(json.dumps(taxes, cls= TaxDetailEncoder))
        except:
            print("Unexpected parameter")

