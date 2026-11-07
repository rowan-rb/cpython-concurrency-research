# Analysis — cache TOCTOU

Real bytecode (`dis.dis(buggy_access)` from `demo_cache.py`):
```
  54 LOAD_FAST_BORROW 0 (key)
  55 LOAD_GLOBAL 4 (d)
  56 CONTAINS_OP 1 (not in)
  57 POP_JUMP_IF_FALSE ...
  ... COMPUTE call ...
  61 STORE_SUBSCR          # d[key] = val
```
Not `STORE_ATTR` (the dict uses `STORE_SUBSCR`). TOCTOU between `CONTAINS_OP` and `STORE_SUBSCR`.

Bug: `if key not in d: d[key] = compute()` is not atomic.
Consequences: double-compute (thundering herd) and stale-read (if value were mutable).
Lock mitigation restores linearizability, but thundering herd is MITIGATED, not ELIMINATED by design.
