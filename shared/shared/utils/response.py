"""
レスポンスレベルに関するユーティリティ関数。

レスポンスレベルとは、サーバーサイドで生成される出力に優先度をつけるためのラベルです。

- "main": レスポンスの第一の目的となる出力（例：最終的な回答）
- "sub": 処理の補足的・中間的な出力（例：デバッグ情報、部分的な説明など）
"""

def check_response_level(level: str) -> bool:
    """
    指定されたレベルが有効なレスポンスレベルかどうかを判定します。

    Args:
        level (str): チェック対象のレスポンスレベル。

    Returns:
        bool: 登録されているレベルであれば True、それ以外は False。
    """
    level_list = ["main", "sub"]
    return level in level_list


def set_response_level(data: dict, level: str) -> dict:
    """
    レスポンスデータにレスポンスレベルを設定します。

    Args:
        data (dict): レスポンスデータの辞書。
        level (str): 設定するレスポンスレベル

    Returns:
        dict: "level" キーを追加または上書きした辞書。
    
    Raises:
        ValueError: 無効なレスポンスレベルが指定された場合。
    """
    if not check_response_level(level):
        raise ValueError(f"無効なレスポンスレベルです: {level}")
    data["level"] = level
    return data
