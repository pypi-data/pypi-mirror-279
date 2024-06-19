# TTL Cache

A function-level memory cache that supports Time To Live (TTL).

- **Per-function argument caching**: Caching is possible based on the data passed to function arguments. The cache key is composed of the function name, argument names, and the values of the arguments.
- **Automatic expiration**: Cached data expires and is automatically deleted after the specified TTL (in seconds).
- **LRU policy**: When the cache exceeds its maximum size (`max_size`), the Least Recently Used (LRU) policy is applied to delete items.
- **Easy application**: Simply add the `@TtlCache(ttl=seconds)` decorator to the function you want to cache.

## Parameters:

- **ttl**: TTL for the cached data (in seconds).
- **max_size**: Maximum number of cache entries.
- **applying_params**: List of parameter names to use as the cache key. If `None`, all parameters are used. If `[]`, only the function name is used.

## Member Functions:

- **force_expire(key)**: Forces expiration of the cache entry for the specified key.
- **is_exist(key)**: Checks if a specific key exists in the cache.
- **get_item(key)**: Returns the cache item for the specified key.
  - *Note*: The key can include partial elements of the cache key.

## Usage:

1. Add the `@TtlCache(ttl=seconds)` decorator to the function you want to cache.
2. Cache keys are generated in the format `"{class_name.}method_name(param1=value1, param2=value2, ...)"`.
3. To call the member functions of `TtlCache`, create an instance of `TtlCache` and use that instance as the decorator.

### Example:
```python
some_cache = TtlCache(ttl=5)

@some_cache
def some_function(x):
    return x * 2

@TtlCache(ttl=5, max_size=10, applying_params=['key'])
def another_function(key, value):
    return f'{key} = {value}'

# Usage
result = some_function(1)
some_cache.force_expire('some_function(x=1)')
```
