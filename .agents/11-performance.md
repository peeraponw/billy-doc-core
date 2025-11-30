# 11. Performance Guidelines

## 11.1 Measurement Before Optimization

* Performance optimizations MUST be based on measurement (profiling) rather than speculation.
* Tools such as `cProfile`, `py-spy`, or equivalent MUST be used before significant optimization work.

## 11.2 Caching and Resource Use

* Expensive pure functions MAY use `functools.lru_cache`.
* For large datasets, iterators and generators MUST be preferred over loading everything into memory.
