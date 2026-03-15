def parse_security(security_info):
    for entity in security_info:
        entity["type"] = entity["type"].lower()

    return security_info
