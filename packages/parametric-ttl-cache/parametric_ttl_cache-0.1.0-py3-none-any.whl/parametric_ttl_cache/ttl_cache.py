from collections import OrderedDict

from expiringdict import ExpiringDict

from parametric_ttl_cache.utility import Utility


class TtlCache:
    """
    TTL Cache
        TTL(Time To Live)이 지원되는 함수 단위 메모리 캐시
        함수 인자에 전달되는 데이터 별로 캐싱이 가능하며, 캐싱 키는 함수 이름과 인자의 이름, 인자로 전달된 값으로 구성됨
        캐시에 저장된 데이터는 ttl(초단위) 이 지나면 자동으로 expire되어 삭제됨
        캐시에 저장된 데이터는 max_size를 넘어가면 LRU(Least Recently Used) 정책에 따라 삭제됨
        캐시를 적용하려는 함수에 @TtlCache(ttl=초단위) 데코레이터를 추가하면 됨

    Parameter:
        ttl: 캐시 데이터의 TTL(초단위)
        max_size: 캐시 데이터의 최대 저장 개수
        applying_params: 캐시 키로 사용할 파라미터 이름 리스트. None이면 모든 파라미터를 사용, []이면 함수 이름만 사용

    Member Function:
        force_expire(key): 특정 키에 대한 캐시를 강제로 만료시킴
        is_exist(key): 특정 키가 캐시에 존재하는지 확인
        get_item(key): 특정 키에 대한 캐시 아이템을 반환
        * key는 캐시 키의 일부만 포함 가능

    Usage:
        * 캐시를 적용하려는 함수에 @TtlCache(ttl=초단위) 데코레이터를 추가하면 됨
        * 캐시 키는 "{class_name.}method_name(param1=value1, param2=value2, ...)" 형태로 생성됨
        * TtlCache의 member function을 호출하기 위해서는 TtlCache의 인스턴스를 생성하고 해당 인스턴스를 데코레이터로 사용해야 한다.
        예)
            some_cache = TtlCache(ttl=5)

            @some_cache
            def some_function(x):
                return x*2
            ...

            result = some_function(1)
            some_cache.force_expire('some_function(x=1)')
    """

    def __init__(self, ttl: int, max_size: int = 256, applying_params=None):
        self.__ttl = ttl
        self.__max_size = max_size
        self.__applying_params = applying_params
        self.__cache = ExpiringDict(max_len=max_size, max_age_seconds=ttl, items=None)

    def __call__(self, function):
        def make_key(_function, *args, **kwargs):
            params = Utility.map_arg_to_value(_function, *args, **kwargs)

            if self.__applying_params is not None:
                params = OrderedDict((k, v) for k, v in params.items() if k in self.__applying_params)

            return f'{_function.__qualname__}({Utility.dict_to_string(params)})'

        def wrapped_function(*args, **kwargs):
            key = make_key(function, *args, **kwargs)
            if key in self.__cache:
                return self.__cache[key]
            else:  # cache에 키가 없거나 expire된 경우
                result = function(*args, **kwargs)
                self.__cache[key] = result
                return result

        return wrapped_function

    # 특정 키에 대한 캐시 강제 만료
    def force_expire(self, key):
        item = self.get_item(key)
        if item is not None:
            del self.__cache[item]

    # 특정 키가 캐시에 존재하는지 확인
    def is_exist(self, key):
        return self.get_item(key) is not None

    def get_item(self, key):
        for item in self.__cache:
            if key in item:
                return item
        return None
