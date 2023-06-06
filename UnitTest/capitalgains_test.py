from decimal import Decimal
import unittest 
from unittest.mock import patch
from Entities.operation import Operation
from Services.Processor import TaxProcessor
from Services.Rules import TaxRules

class Processor_TestCase(unittest.TestCase):

    def taxes_processor_number_of_transactions_OK(self):
        #arrange
        transactions = []
        transactions.append(operation = Operation("buy", 20, 1000))
        transactions.append(operation = Operation("sell", 21, 1000))
        rules = TaxRules()
        processor = TaxProcessor(rules)
        #act
        result = processor.taxes_processor(transactions)
        #assert
        self.assertCountEqual(transactions, result)



class Rules_TestCase(unittest.TestCase):

    def calculate_weighted_avg_should(self):
        #arrange
        csq: int = 20
        wap: Decimal = 10
        nsq: int = 10
        np: Decimal = 10
        rules = TaxRules()
        #act
        result = rules.calculated_weighted_avg(csq,wap,nsq,np)
        #assert
        self.assertTrue(result == 10)

    def calculate_losses_should(self):
        #arrange
        ssq:int = 10
        wap:Decimal = 10
        sp = 9
        rules = TaxRules()
        #act
        result = rules.calculate_losses(wap,ssq,sp)
        #assert
        self.assertTrue(result == 10)

    def calculate_taxes_should(self):
        #arrange
        op: Decimal = 100
        rules = TaxRules()
        #act
        result = rules.calculate_taxes(op)
        #assert
        self.assertTrue(result == 20)

    def apply_for_taxes_should(self):
        #arrange
        operation = Operation("sell", 21, 1000)
        rules = TaxRules()
        #act
        result = rules.apply_for_taxes(operation)
        #assert
        self.assertTrue(result)

    def is_with_losses_should(self):
        #arrange
        wap:Decimal = 21
        operation = Operation("sell", 20, 1000)
        rules = TaxRules()
        #act
        result = rules.is_with_losses(operation, wap)
        #assert
        self.assertTrue(result)


