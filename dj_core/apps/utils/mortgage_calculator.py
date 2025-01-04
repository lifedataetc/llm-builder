import numpy as np
import pandas as pd
from apps.backoffice.models import *


class Calculator:
    def __init__(self, **kwargs):
        """ Mortgage Calculator

        Please provide inputs as a dictionary with the inputs as keys shown below
        Inputs:
            Required:
                down_payment: down payment + closing costs as a float, e.g. 100000
                income: total household income as a float, e.g. 154000

            Optional:
                max_payment: maximum monthly payment buyer wants as a float
                sale_price: value of the property, if known, as a float
                mortgage_years: number of years for the mortgage term as an integer, e.g. 30
                interest_rate: mortgage interest percentage rate as a float, e.g. 2.5
                tax_rate: property tax rate percentage as a float, e.g. 1.25
                home_insurance: yearly home insurance as a float, e.g. 1000
                factor: the ratio of monthly income to use as a max_payment, e.g. 0.31 for
                    using 31% of monthly income as maximum monthly payment
        """

        # input, number field
        self.interest = None
        self.payment_components = None
        self.x = None
        self.total_payment = None
        self.tax_amount = None
        self.loan_amount = None
        self.down_payment = kwargs.get('down_payment', False)
        if not self.down_payment:
            raise ValueError('Downpayment and closing cost value must be provided')

        # input, number field
        self.income = kwargs.get('income', False)
        if not self.income:
            raise ValueError('Household income must be provided')

        # slider, from (min - 200k loan monthly payment, high - of monthly)
        self.max_payment = kwargs.get('max_payment', False)

        self.sale_price = kwargs.get('sale_price', False)
        if not self.sale_price:
            self.closing_cost = False
        else:
            # need to take 2% of the loan amount as closing cost and rest to be used as downpayment
            appx_loan_amount = self.sale_price - self.down_payment
            self.closing_cost = 0.02 * appx_loan_amount
            self.down_payment -= self.closing_cost

        self.mortgage_years = kwargs.get('mortgage_years', 30)
        self.interest_rate = kwargs.get('interest_rate', 2.8)
        self.tax_rate = float(kwargs.get('tax_rate', 1.25)) / 100
        self.home_insurance = kwargs.get('home_insurance', 1000)
        self.factor = kwargs.get('factor', 0.50)

        # total loan term
        self.loan_term = int(12 * self.mortgage_years)

        self.r = 1 + self.interest_rate / (12 * 100)

        # home insurance per month
        self.home_ins = self.home_insurance / 12

    def get_max_sale_price(self):
        """This function computes and store maximum sale price as self.max_payment when no value is given."""
        if not self.max_payment:
            self.max_payment = self.factor * self.income / 12 - self.home_ins
        else:
            self.max_payment -= self.home_ins

        self.r = 1 + self.interest_rate / (12 * 100)

        # of no sale price is given, we will first approximate a loan, use that to obtain a closing cost and re-calculate the loan
        if not self.sale_price:
            loan_amount = (self.max_payment - self.down_payment * (self.tax_rate / 12)) / (
                        (self.r ** self.loan_term) * (1 - self.r) / (1 - self.r ** self.loan_term) + self.tax_rate / 12)
            self.closing_cost = round(0.0199 * loan_amount, 2)
            self.down_payment = round(self.down_payment - self.closing_cost, 2)

            # recompute with the new down payment
            self.loan_amount = round((self.max_payment - self.down_payment * (self.tax_rate / 12)) / (
                        (self.r ** self.loan_term) * (1 - self.r) / (
                            1 - self.r ** self.loan_term) + self.tax_rate / 12), 2)
            self.sale_price = round(self.loan_amount + self.down_payment, 2)
        else:
            self.loan_amount = round(self.sale_price - self.down_payment, 2)

    def calculate_mortgage(self):
        """This function will calculate the mortage parameters including the full payment schedule"""

        # tax per month
        self.tax_amount = round((self.sale_price * self.tax_rate) / 12, 2)

        # monthly payment
        self.x = self.loan_amount * (self.r ** self.loan_term) * (1 - self.r) / (1 - self.r ** self.loan_term)
        self.total_payment = np.round(np.round(self.x, 2) + np.round(self.tax_amount, 2) + np.round(self.home_ins, 2),
                                      2)
        self.payment_components = {'p&i': np.round(self.x, 2), 'taxes': np.round(self.tax_amount, 2),
                                   'ins': np.round(self.home_ins, 2)}

        monthly_interest = []
        monthly_balance = []

        LA = self.loan_amount
        for i in range(1, self.loan_term + 1):
            self.interest = LA * (self.r - 1)
            LA = LA - (self.x - self.interest)
            monthly_interest = np.append(monthly_interest, self.interest)
            monthly_balance = np.append(monthly_balance, LA)

        df = pd.DataFrame(list(zip(monthly_balance, monthly_interest)), columns=['monthly_balance', 'monthly_interest'])
        df = df.apply(lambda x: np.round(x, 2))

        df['monthly_payment'] = np.round(self.x, 2)
        df['tax'] = np.round(self.tax_amount, 2)
        df['ins'] = np.round(self.home_ins, 2)
        df['total_payment'] = np.round(self.x, 2) + np.round(self.tax_amount, 2) + np.round(self.home_ins, 2)
        df['month'] = list(range(1, self.loan_term + 1))

        df = df[['month', 'total_payment', 'monthly_payment', 'tax', 'ins', 'monthly_balance', 'monthly_interest']]
        self.data = df
