def convert_procedure(type_:bool, ab_name_:str) -> str:
    """_summary_

    Args:
        type_ (bool): _description_
        ab_name_ (str): _description_

    Returns:
        str: 절차서명 : ex. 'Ab21_01: 가압기 압력 채널 고장 (고)'
    """
    
    if type_ == 1:
        abnormal_procedure = ''
    else:
        if ab_name_ == 'Ab21_01: 가압기 압력 채널 고장 (고)':
            abnormal_procedure = 'Ab21_01: 가압기 압력 채널 고장 (고)'
        
    return abnormal_procedure