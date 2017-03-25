import datetime
from sqlalchemy.sql import sqltypes


class AdminValidationError(Exception):
    pass


def validate_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        raise AdminValidationError('Wrong value for integer type: {}!'.format(value))


def validate_boolean(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise AdminValidationError(
            'Wrong value for boolean type: {}!'.format(value)
        )


def validate_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        raise AdminValidationError('Wrong value for float type: {}!'.format(value))


def validate_string(value, col_len):
    if not isinstance(value, str):
        raise AdminValidationError('Not string value for string column: {}'.format(value))

    if len(value) < col_len:
        return str(value)
    else:
        raise AdminValidationError(
            'Too long value {} for type sqltype.String with len {}!'.format(value, col_len)
        )


def validate_datetime(value):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    except (ValueError, TypeError):
        raise AdminValidationError('Wrong value for datetime type: {} '
                                   '(must be rfc-3339 compatible)!'.format(value))


def validate_date(value):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        raise AdminValidationError('Wrong value for date type: {} '
                                   '(must be rfc-3339 compatible)!'.format(value))


def validate_time(value):
    if not isinstance(value, str):
        raise AdminValidationError('Not string value for string column: {}'.format(value))

    try:
        return datetime.datetime.strptime(value, '%H:%M:%S').time()
    except (ValueError, TypeError):
        raise AdminValidationError('Wrong value for datetime type: {} '
                                   '(must be rfc-3339 compatible)!'.format(value))


def validate_field(value, column_field):
    column_type = column_field.type
    if isinstance(column_type, sqltypes.Text):
        return str(value)
    if isinstance(column_type, sqltypes.String):
        return validate_string(value, column_type.length)

    elif isinstance(column_type, sqltypes.Boolean):
        return validate_boolean(value)
    elif isinstance(column_type, sqltypes.Integer):
        return validate_int(value)
    elif isinstance(column_type, sqltypes.Float):
        return validate_float(value)
    elif isinstance(column_type, sqltypes.DateTime):
        return validate_datetime(value)
    elif isinstance(column_type, sqltypes.Date):
        return validate_date(value)
    elif isinstance(column_type, sqltypes.Time):
        return validate_time(value)
    else:
        raise AdminValidationError('Unsupported type of column: {}'.format(column_type))
