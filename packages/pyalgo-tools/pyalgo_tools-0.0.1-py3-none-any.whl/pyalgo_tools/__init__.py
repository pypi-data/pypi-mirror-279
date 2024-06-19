import math
import urllib

import numpy as np


def dhondt(total: int, votes: np.ndarray | list[int]) -> np.ndarray:
    """ドント方式で議席数を計算

    :param total: 総議席数
    :param votes: 得票数の1次元配列
    :return: 議席数の1次元配列
    """
    votes_ = np.asarray(votes)
    seats = np.zeros_like(votes_, dtype=int)
    for _ in range(total):
        i = (votes_ / (seats + 1)).argmax()
        seats[i] += 1
    return seats


def circle_overlap_area(x1: float, y1, r1: float, x2: float, y2: float, r2: float) -> float:
    """2つの円の重なる面積

    :param x1: 円1のX座標
    :param y1: 円1のY座標
    :param r1: 円1の半径
    :param x2: 円2のX座標
    :param y2: 円2のY座標
    :param r2: 円2の半径
    :return: 面積
    """
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if d >= r1 + r2:
        return 0.0
    elif d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    p1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    p2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    p3 = math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)) / 2
    return p1 + p2 - p3


def read_spreadsheets(id: str):
    """GoogleスプレッドシートからCSVの読込

    :param id: URLのID（誰でも読取り可であること）
    :return: DataFrame
    """
    import pandas as pd

    url = f"https://docs.google.com/spreadsheets/d/{id}/export?format=csv"
    with urllib.request.urlopen(url) as fp:
        df = pd.read_csv(fp)
    return df
