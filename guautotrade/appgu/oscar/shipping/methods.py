from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D

class Standard(methods.Base):
    code = 'standard'
    name = 'Standard shipping'
    is_tax_known = True
    excl_tax = D('5.00')
    incl_tax = D('5.00')

    def calculate(self, basket):
        print('Calculating the shipping costs for Standard...')
        return self

class Express(methods.Base):
    code = 'express'
    name = 'Express shipping'
    is_tax_known = True
    excl_tax = D('10.00')
    incl_tax = D('10.00')

    def calculate(self, basket):
        print('Calculating the shipping costs for Express...')
        return self