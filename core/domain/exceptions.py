# Ошибки бизнес логики

class InsufficientFundsError(Exception):
    "Исключение: не достаточно средств"
    pass


class OrderNotFoundError(Exception):
    "Исключение: заказ не найден"
    pass