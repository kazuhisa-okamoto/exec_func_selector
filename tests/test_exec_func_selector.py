import pytest
from unittest.mock import patch
from exec_func_selector import ExecFuncSelector

def test_exec_func_selector():
    """ ExecFuncSelectorのテスト """
    
    def success_func():
        print("Success function executed")
        return True
    
    def failure_func():
        print("Failure function executed")
        return False
    
    def exception_func():
        raise ValueError("Test exception")
    
    func_list = [
        (1, success_func, "成功する関数"),
        (2, failure_func, "失敗する関数"),
        (3, exception_func, "例外を発生させる関数")
    ]
    selector = ExecFuncSelector(func_list)
    
    with patch('builtins.input', return_value='1'):
        result = selector.run()
        assert result
    
    with patch('builtins.input', return_value='3'):
        result = selector.run()
        assert not result