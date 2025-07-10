import datetime
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class FuncInfo:
    """ 一つの実行可能オブジェクトに関するデータ. """
    id: Any
    func: Callable
    description : str

class ExecFuncSelector:
    """
    関数を登録し, 標準入力で指定された関数を実行するクラス.
  
    func_list : list of tuple
        登録する関数情報のリスト。各要素は以下の形式のタプル：
        (func_id: int or str, func: Callable, description: str)
            - func_id: 関数を識別するid
            - func: 関数
            - description: 関数の説明または関数名
    """
    def __init__(self, func_list):
        self.func_map = {funcid: FuncInfo(funcid, func, desc) for funcid, func, desc in func_list}

        # 関数を指定するIDのタイプ. intかstr.
        self.func_id_type = self._get_func_id_type()
    
    def run(self, func_id=None):
        """ 関数を実行. 引数で関数を指定しない場合, 標準入力で関数を選択する. """
        if not func_id:
            func_id = self._set_func_id() 
        
        if not (func := self._get_funcinfo(func_id)):
            print("Error: Illegal id specified")
            return False

        print(f"\n==={func.description}===")
        datetime_start = datetime.datetime.now()
        print(f"Start {datetime_start.strftime("%Y/%m/%d %H:%M:%S")}\n")

        try:
            result = func.func()
        except Exception as e:
            print(f"Exception detected: {e}")
            result = False

        if not result:
            print(f"{func.description} FAILED!")
        else:
            print(f"{func.description} SUCCESS!")

        datetime_finish = datetime.datetime.now()
        print(f"\nFinish {datetime_finish.strftime("%Y/%m/%d %H:%M:%S")}")
        datetime_delta = datetime_finish - datetime_start
        print(f"Total time(sec): {datetime_delta.total_seconds()}")
        
        return result

    def _get_func_id_type(self):
        if not self.func_map:
            return int
        for key in self.func_map:
            if isinstance(key, str):
                return str
        return int
    
    def _get_funcinfo(self, func_id):
        """ 実行関数を取得 """
        if self.func_id_type is int:
            try:
                func_id = int(func_id)
            except Exception as e:
                print(f"Exception detected: {e}")
                return None

        if self.func_id_type is str:
            if not func_id:
                return None
        
        return self.func_map.get(func_id)

    def _set_func_id(self):
        """ メッセージを表示して, 実行タイプの入力を受けて返す """
        for key, func in self.func_map.items():
            print(f"{key} : {func.description}")
        print("Please specify a function:")
        return input()