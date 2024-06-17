import orjson


class BybitAPIException(Exception):
    def __init__(self, response, status_code, text):
        self.code = 0
        try:
            json_res = orjson.loads(text)
        except ValueError:
            self.message = "Invalid JSON error message from Bybit: {}".format(response.text)
        else:
            self.code = json_res["code"]
            self.message = json_res["msg"]
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, "request", None)

    def __str__(self):  # pragma: no cover
        return "APIError(code=%s): %s" % (self.code, self.message)


class BybitRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "BybitRequestException: %s" % self.message


class BybitOrderException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "BybitOrderException(code=%s): %s" % (self.code, self.message)


class BybitOrderMinAmountException(BybitOrderException):
    def __init__(self, value):
        message = "Amount must be a multiple of %s" % value
        super().__init__(-1013, message)


class BybitOrderMinPriceException(BybitOrderException):
    def __init__(self, value):
        message = "Price must be at least %s" % value
        super().__init__(-1013, message)


class BybitOrderMinTotalException(BybitOrderException):
    def __init__(self, value):
        message = "Total must be at least %s" % value
        super().__init__(-1013, message)


class BybitOrderUnknownSymbolException(BybitOrderException):
    def __init__(self, value):
        message = "Unknown symbol %s" % value
        super().__init__(-1013, message)


class BybitOrderInactiveSymbolException(BybitOrderException):
    def __init__(self, value):
        message = "Attempting to trade an inactive symbol %s" % value
        super().__init__(-1013, message)


class BybitWebsocketUnableToConnect(Exception):
    pass


class BybitWebsocketOpError(Exception):
    def __init__(self, message):
        self.message = message


class NotImplementedException(Exception):
    def __init__(self, value):
        message = f"Not implemented: {value}"
        super().__init__(message)
