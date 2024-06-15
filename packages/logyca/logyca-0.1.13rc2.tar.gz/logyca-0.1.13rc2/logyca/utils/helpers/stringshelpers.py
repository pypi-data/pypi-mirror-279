from urllib import parse

def buildUrl(url1:str,url2:str)->str:
    '''Description    
    Build a from url correctly
    :param url1: http(s)://initial/string
    :param url2: following url path
    :return str: url
    '''
    return parse.urljoin(url1, url2)

def convert_string_to_boolean(truth_value: str) -> bool:
    # TODO - Deprecated 2024/05/24
    print("Soon this function will be retired: convert_string_to_boolean(), please change it to the following: parse_bool()")
    lowercased_value = str(truth_value).lower()

    if lowercased_value in ("yes", "true", "1", "on"):
        return True
    elif lowercased_value in ("no", "false", "0", "off"):
        return False
    else:
        raise ValueError(f"Invalid boolean string value: {truth_value}"
        )
