import pytest

# 定义前置处理器
@pytest.fixture
def dynamic_user_symbol(request):
    # 获取当前测试用例的方法名
    test_method_name = request.node.name
    # 执行前置处理器逻辑
    user, symbol = {}, {}  # 这里假设是前置处理器的返回值
    if hasattr(request, 'param'):
        print(f"{test_method_name} 所需要要的用户 和 交易对为 {request.param}")

        if 'symbol' in request.param:
            print(f"锁定交易对 {test_method_name}+{request.param['symbol']}")
        if 'user' in request.param:
            print(f"锁定用户 {test_method_name}+{request.param['user']}")
        user, symbol = {"user":1}, {"symbol":2}  # 这里假设是前置处理器的返回值

    yield user, symbol
    # 执行后置处理器逻辑
    print(f"\n释放用户 及 symbol {user},{symbol}\n")
    # 这里可以添加后置处理器的逻辑

# 测试类
class TestMyClass:
    user_symbol={
        'init1':{'user':{'kyclevel':0},'symbol':{'symbol_type':'etf'},},
        'init2':{'user':{'kyclevel':3},'symbol':{'symbol_type':'margin'},},
    }
    datas2={
        'ag-s1':{'sss':{'a':1}},
        'ag-s2':{'fff':{'a':2}},
    }

    # 测试方法 A
    @pytest.mark.parametrize('datas2',datas2.values(),ids=datas2.keys())
    @pytest.mark.parametrize('dynamic_user_symbol',user_symbol.values(),ids=user_symbol.keys(),indirect=True)
    def test_method_A(self, dynamic_user_symbol,datas2):
        result1, result2 = dynamic_user_symbol

        assert result1 == {"user":1}
        assert result2 == {"symbol":2}
        # 在这里执行测试逻辑，并使用 result1 和 result2

    # 测试方法 B
    def test_method_B(self, dynamic_user_symbol):
        result1, result2 = dynamic_user_symbol
        assert result1 == 1
        assert result2 == {}
        # 在这里执行测试逻辑，并使用 result1 和 result2

    # 测试方法 C
    def test_method_C(self, dynamic_user_symbol):
        result1, result2 = dynamic_user_symbol
        assert result1 == {}
        assert result2 == {}
        # 在这里执行测试逻辑，并使用 result1 和 result2
