import json
import warnings

from .encoders import PriceCypherJsonEncoder


class HttpException(Exception):
    def __init__(self, **kwargs):
        super().__init__()

        self.message = kwargs.get('message', 'An unknown error has occurred')
        self.status_code = kwargs.get('status_code', 500)
        self.code = kwargs.get('error_code', "Internal Server Error")
        self.extra = kwargs.get('extra')

    def __str__(self):
        return f'{self.status_code} {self.code}: {self.message}'

    def format_response(self) -> dict:
        return {
            'statusCode': self.status_code,
            'headers': {
                'Content-Type': 'text/plain',
                'x-amzn-ErrorType': self.code,
            },
            'isBase64Encoded': False,
            'body': f'{self.code}: {str(self)}',
            'extra': json.dumps(self.extra, cls=PriceCypherJsonEncoder)
        }


class MissingInputException(HttpException):
    """Exception raised when one of the necessary inputs is missing.

    Attributes:
        scopes -- scope missing from user input
        business_cell -- boolean value, if True, business cell scope is missing
        message -- explanation of the error
    """

    def __init__(self, **kwargs):
        scopes: list[str] = kwargs.get('scopes', [])
        msg = f"Missing input variable(s): [{', '.join(kwargs.get('scopes'))}]"
        super().__init__(status_code=400, error_code='Bad Request', message=msg, extra={'scopes': scopes}, **kwargs)


class IncorrectVolumeException(HttpException):
    """Exception raised when user input has incorrect volume.

    Attributes:
        val -- incorrect volume value
        message -- explanation of the error
    """

    def __init__(self, **kwargs):
        val = kwargs.get('val')
        msg = f"Incorrect volume entered ({val}). Please enter a positive value."
        super().__init__(status_code=400, error_code='Bad Request', message=msg, extra={'volume': val}, **kwargs)


class DataNotFoundException(HttpException):
    """Exception raised when one of the necessary input by the user is missing from the dataset.

    Attributes:
        key -- column/scope with missing data
        value -- data value that is missing
        message -- explanation of the error
    """

    def __init__(self, **kwargs):
        key = kwargs.get('key', "Unknown")
        value = kwargs.get('value', "Unknown")
        msg = f"Data point not found in dataset for column '{key}' (with value '{value}')"
        extra = {'key': key, 'value': value}
        super().__init__(status_code=404, error_code='Not Found', message=msg, extra=extra, **kwargs)


class MissingRepresentationException(HttpException):
    """Exception raised when the script expects a representation,
    but it is not found due to excel configuration.

    Attributes:
        val -- column that should be indicated as a representation
        message -- explanation of the error
    """

    def __init__(self, **kwargs):
        val = kwargs.get('val')
        msg = "Unable to find representation. Please update scopes file."
        super().__init__(status_code=409, error_code='Conflict', message=msg, extra={'column': val}, **kwargs)


class RateLimitException(HttpException):
    def __init__(self, status_code=429, error_code='Too Many Requests', message=None, **kwargs):
        self.reset_at = kwargs.get('reset_at')
        msg = message if not None else f"Rate limit reached. Reset at: '{self.reset_at or 'Unknown'}'."
        extra = {'reset_at': self.reset_at}
        super().__init__(status_code=status_code, error_code=error_code, message=msg, extra=extra, **kwargs)


class PriceCypherError(HttpException):
    def __init__(self, status_code, error_code, message):
        warnings.warn('Use of the class `PriceCypherError` is deprecated. Please use `HttpException` instead.')
        super().__init__(message=message, status_code=status_code, error_code=error_code)


class RateLimitError(PriceCypherError):
    def __init__(self, error_code=429, message=None, reset_at=None):
        warnings.warn('Use of the class `RateLimitError` is deprecated. Please use `RateLimitException` instead.')
        self.reset_at = reset_at
        super().__init__(status_code=error_code, error_code='Too Many Requests', message=message)
