"""
Utils for reading DTO exceptions.
"""

from pydantic import ValidationError


def get_fields_containing_errors_from_dto_error(errors_data: ValidationError) -> str:
    """
    Return a string containing the fields where errors were detected.
    """
    errors = []
    for error in errors_data.errors():
        errors.append(f"{error['loc'][0]}")
    return ", ".join(errors)
