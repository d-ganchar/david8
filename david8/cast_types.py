text = 'TEXT'
integer = 'INTEGER'
smallint = 'SMALLINT'
bigint = 'BIGINT'
date_ = 'DATE'
time_ = 'TIME'
timestamp_ = 'TIMESTAMP'
boolean = 'BOOLEAN'


def varchar(char_length: int) -> str:
    return f'VARCHAR({char_length})'


def char(char_length: int) -> str:
    return f'CHAR({char_length})'
