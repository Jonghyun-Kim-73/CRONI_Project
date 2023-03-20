from PyQt5.QtCore import *
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
def convexhull(points):
    """_summary_

    Args:
        points (list): [QPoint, QPoint, ...]

    Returns:
        _type_: convexhull points: [QPoint, QPoint, ...]
    """
    hull_points = []
    
    # 최소 X 값을 탐색
    start_point:QPointF = points[0]
    min_x = start_point.x()
    for p in points[1:]:
        if p.x() < min_x:
            min_x = p.x()
            start_point = p
    
    point = start_point
    hull_points.append(start_point)
    
    far_point = None
    while far_point is not start_point:
        # get the first point (initial max) to use to compare with others
        p1 = None
        for p in points:
            if p is point:
                continue
            else:
                p1 = p
                break

        far_point = p1

        for p2 in points:
            # ensure we aren't comparing to self or pivot point
            if p2 is point or p2 is p1:
                continue
            else:
                direction = (((p2.x() - point.x()) * (far_point.y() - point.y())) - 
                             ((far_point.x() - point.x()) * (p2.y() - point.y())))
                if direction > 0:
                    far_point = p2

        hull_points.append(far_point)
        point = far_point
    
    return hull_points