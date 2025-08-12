"""
Exceptions for project.
"""

from enum import StrEnum

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError

from utils.exceptions.dto_exceptions_reader import (
    get_fields_containing_errors_from_dto_error,
)


class AppErrorCodes(StrEnum):
    ALREADY_EXISTS = "already_exists"
    DOES_NOT_EXIST = "does_not_exists"
    BAD_REQUEST = "bad_request"
    SERVICE_UNAVAILABLE = "service_unavailable"
    WEIGHT_SENSOR_REQUEST_ERROR = "weight_sensor_request_error"
    GENERAL_SENSOR_REQUEST_ERROR = "general_sensor_request_error"
    WEIGHT_SENSOR_REQUEST_INVALID_READING = "weight_sensor_request_invalid_reading"


class ObjectAlreadyExists(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Объект с такими полями уже существует"
    default_code = AppErrorCodes.ALREADY_EXISTS


class ObjectDoesNotExists(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Объект с такими полями не существует"
    default_code = AppErrorCodes.DOES_NOT_EXIST


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Неверный запрос"
    default_code = AppErrorCodes.BAD_REQUEST


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Не удалось получить ответ от сервиса"
    default_code = AppErrorCodes.SERVICE_UNAVAILABLE


class DTOValidationError(ValidationError):
    """
    Add to error detail description of error if error_data is None.
    """

    def __init__(self, detail=None, code=None, error_data=None):
        super().__init__(detail, code)
        if error_data is not None:
            self.error_data = get_fields_containing_errors_from_dto_error(error_data)
            self.detail = f"Обнаружены ошибки - некорректны значения полей: {self.error_data}."

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Обнаружены ошибки - некорректны значения полей."
    default_code = AppErrorCodes.BAD_REQUEST
