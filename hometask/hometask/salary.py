class Salary:
    def __init__(self, text: str):
        no_price = False
        if len(text) == 0 or text == 'з/п не указана':
            no_price = True
            self.price_from = 'Нет данных'
            self.price_to = 'Нет данных'
            self.currency = 'руб.'
        elif text.startswith('от'):
            self.price_from = ''.join(filter(str.isdigit, text))
            self.price_to = '-'
        elif text.startswith('до'):
            self.price_from = 'Нет данных'
            self.price_to = ''.join(filter(str.isdigit, text))
        elif '–' in text:
            from_to = text.split('–')
            self.price_from = ''.join(filter(str.isdigit, from_to[0]))
            self.price_to = ''.join(filter(str.isdigit, from_to[1]))
        else:
            price = ''.join(filter(str.isdigit, text))
            self.price_from = price
            self.price_to = price
        if not no_price:
            chunks = text.split(' ')
            self.currency = chunks[-1]

    def __str__(self):
        return f"от {self.price_from} до {self.price_to} {self.currency}"