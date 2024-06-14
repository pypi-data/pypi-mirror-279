def parse_bool(bool_value: str|int|bool|None) -> bool | None:
    true_values = {"true", "1"}
    false_values = {"false", "0"}

    if isinstance(bool_value,bool):
        return bool_value
    
    if isinstance(bool_value,int):
        if bool_value == 1:
            bool_value = "1"
        elif bool_value== 0:
            bool_value = "0"
        else:
            return None

    if isinstance(bool_value,str):
        bool_value = str(bool_value).lower()
        if bool_value in true_values:
            return True
        elif bool_value in false_values:
            return False
        else:
            return None

    return None