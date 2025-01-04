from apps.utils.mortgage_calculator import Calculator

class PreQualApp:
    """Lightspeed Pre-qualification Application"""

    def __init__(self, answers, **kwargs):
        self.answers = answers
        self.process_buyer_answers()

    def process_buyer_answers(self):
        downpayment_percent = self.answers.get('down_payment', False)
        household_income = self.answers.get('income', False)
        sale_price = self.answers.get('sale_price', False)

        self.inputs = {'down_payment': float(downpayment_percent),
                       'income': float(household_income)}

        if not sale_price:
            pass
        else:
            self.inputs['sale_price'] = float(sale_price)

        self.calculator = Calculator(**self.inputs)
        self.calculator.get_max_sale_price()
        self.calculator.calculate_mortgage()

    def recalculate_w_params(self, **kwargs):
        """This fuction is for recalculating the mortgage quote with new parameters
            Expected inputs:
                down_payment, max_payment, and income. sale_price will change to False for this.

            Format:
                These should be passed as a dictionary matching the requirements for
                Calculator class above."""
        self.inputs = kwargs
        kwargs['sale_price'] = False
        if 'down_payment' not in kwargs.keys():
            raise ValueError('Downpayment value must be provided')

        if 'max_payment' not in kwargs.keys():
            raise ValueError('Maximum monthly payment must be provided for recalculation')

        if 'income' not in kwargs.keys():
            raise ValueError('Household income must be provided for recalculation')

        self.calculator = Calculator(**self.inputs)
        self.calculator.get_max_sale_price()
        self.calculator.calculate_mortgage()