import json
from decimal import Decimal


class Operation:
    def __init__(self, operation: str, unitCost: Decimal , quantity: int):
        self.operation = operation
        self.unitCost = unitCost
        self.quantity = quantity


class OperationEncoder(json.JSONEncoder):
    
    def default(self, o):
        if isinstance(o, Operation):
            return { 'operation': str(o.operation), 'quantity': str(o.quantity), 'unit-cost': str(o.unitCost)}
        
        return super().default(o)
    

def OperationDecoder(jsonDict) -> Operation:
    return Operation(str(jsonDict["operation"]), Decimal(jsonDict["unit-cost"]), int(jsonDict["quantity"]))