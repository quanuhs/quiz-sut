def get_code_regex():
    return r'(?P<code>[A-Za-z0-9]{5})/$'


def get_uuid_regex():
    return r'(?P<secret_id>[A-Za-z0-9]{6})/$'