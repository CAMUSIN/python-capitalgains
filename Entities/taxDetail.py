from decimal import Decimal
import json


class TaxDetail:
    def __init__(self, tax: Decimal):
        self.tax = round(tax, 2)

class TaxDetailEncoder(json.JSONEncoder):
    
    def default(self, o):
        if isinstance(o, TaxDetail):
            return { 'tax': str(o.tax) }
        
        return super().default(o)
    
def TaxDetailDecoder(jsonDict) -> TaxDetail:
    return TaxDetail(Decimal(jsonDict["tax"]))