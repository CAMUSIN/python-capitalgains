from decimal import Decimal
import typing
from abc import ABC, abstractmethod
from Services.Rules import Rules
from Entities.operation import Operation
from Entities.taxDetail import TaxDetail


class Processor(ABC):

    @abstractmethod
    def taxes_processor(self, transactions):
        pass


class TaxProcessor(Processor):

    def __init__(self, rules_manager: Rules):
        self.rulesManager = rules_manager

    def taxes_processor(self, transactions: list[Operation]) -> typing.List[TaxDetail]:
        taxes = []
        if transactions:
            loss: Decimal = 0
            current_stock_quantity: int = 0
            weighted_avg_price: Decimal = 0
            for operation in transactions:
                if operation.operation == "buy":
                    weighted_avg_price = self.rulesManager.calculated_weighted_avg(current_stock_quantity, weighted_avg_price, operation.quantity, operation.unitCost)
                    current_stock_quantity += operation.quantity
                    taxes.append(TaxDetail(self.rulesManager.calculate_taxes(0)))
                elif operation.operation == "sell":
                    if self.rulesManager.apply_for_taxes(operation):
                        if self.rulesManager.is_with_losses(operation, weighted_avg_price):
                            loss += self.rulesManager.calculate_losses(weighted_avg_price, operation.quantity, operation.unitCost)
                            overall_profit = self.rulesManager.calculate_profits_with_losses(operation, weighted_avg_price, loss)
                            taxes.append(TaxDetail(self.rulesManager.calculate_taxes(overall_profit)))
                        else:
                            overall_profit: Decimal = self.rulesManager.calculate_profits(operation, weighted_avg_price)
                            if loss > 0:
                                if loss >= overall_profit:
                                    loss -= overall_profit
                                    overall_profit = 0
                                else:
                                    overall_profit = overall_profit - loss
                                    loss -= loss
                            taxes.append(TaxDetail(self.rulesManager.calculate_taxes(overall_profit)))
                    else:
                        if self.rulesManager.is_with_losses(operation, weighted_avg_price):
                            loss += self.rulesManager.calculate_losses(weighted_avg_price, operation.quantity, operation.unitCost)
                        taxes.append(TaxDetail(self.rulesManager.calculate_taxes(0)))
                    current_stock_quantity -= operation.quantity
        return taxes

