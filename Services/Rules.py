import json
from decimal import Decimal
from abc import ABC, abstractmethod
from Entities.operation import Operation

with open("config.json", "r") as f:
    config = json.load(f)
    f.close()


class Rules(ABC):
    @abstractmethod
    def calculated_weighted_avg(self, current_stock_quantity: int, weighted_avg_price: Decimal, new_stock_quantity: int, new_price: Decimal) -> Decimal:
        pass

    @abstractmethod
    def calculate_losses(self, weighted_avg_price: Decimal, sell_stock_quantity: int, sell_price: Decimal) -> Decimal:
        pass

    @abstractmethod
    def calculate_taxes(self, overall_profit: Decimal) -> Decimal:
        pass

    @abstractmethod
    def apply_for_taxes(self, operation: Operation) -> bool:
        pass

    @abstractmethod
    def is_with_losses(self, operation: Operation, weighted_avg_price: Decimal) -> bool:
        pass

    @abstractmethod
    def calculate_profits(self, operation: Operation, weighted_avg_price: Decimal) -> Decimal:
        pass

    @abstractmethod
    def calculate_profits_with_losses(self, operation: Operation, weighted_avg_price: Decimal, losses: Decimal) -> Decimal:
        pass


class TaxRules(Rules):

    def calculated_weighted_avg(self, current_stock_quantity: int, weighted_avg_price: Decimal, new_stock_quantity: int, new_price: Decimal) -> Decimal:
        if current_stock_quantity == 0:
            return new_price
        return ((current_stock_quantity * weighted_avg_price) + (new_stock_quantity * new_price)) / (
                current_stock_quantity + new_stock_quantity)

    def calculate_losses(self, weighted_avg_price: Decimal, sell_stock_quantity: int, sell_price: Decimal) -> Decimal:
        return (sell_stock_quantity * weighted_avg_price) - (sell_stock_quantity * sell_price)

    def calculate_taxes(self, overall_profit: Decimal) -> Decimal:
        tax_percentage = Decimal(config["Rules"]["TaxPercentage"])
        return round((overall_profit * tax_percentage), 2)

    def apply_for_taxes(self, operation) -> bool:
        tax_operation_amount = int(config["Rules"]["OperationAmount"])
        if (operation.quantity * operation.unitCost) > tax_operation_amount:
            return True
        return False

    def is_with_losses(self, operation, weighted_avg_price: Decimal) -> bool:
        if (operation.unitCost < weighted_avg_price):
            return True
        return False

    def calculate_profits(self, operation, weighted_avg_price: Decimal) -> Decimal:
        return (operation.quantity * operation.unitCost) - (operation.quantity * weighted_avg_price)

    def calculate_profits_with_losses(self, operation, weighted_avg_price: Decimal, losses: Decimal) -> Decimal:
        transaction_amount = (operation.quantity * operation.unitCost)
        if losses >= transaction_amount:
            return 0
        else:
            transaction_amount = ((operation.quantity * weighted_avg_price) - transaction_amount) - losses
        return transaction_amount
