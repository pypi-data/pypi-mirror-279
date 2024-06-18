class ZeroToZeroPowerError(ArithmeticError):
    def __init__(self):
        super().__init__("0 cannot be raised to the power of 0")