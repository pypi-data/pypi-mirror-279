class ErrorHolder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ErrorHolder, cls).__new__(cls)
            cls._instance.__initialize()
        return cls._instance

    def __initialize(self) -> None:
        self.errors = []

    def add_error(self, e: Exception) -> None:
        self.errors.extend(e)

    def get_errors(self) -> list:
        return self.errors
