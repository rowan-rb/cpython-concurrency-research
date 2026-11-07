# Analysis — bytecode

## Counter — `self.value += 1`

Captured with `dis` at runtime (CPython 3.14):

```
  38 LOAD_FAST_BORROW         0 (self)
  39 COPY                     1
  40 LOAD_ATTR                0 (value)
  41 LOAD_SMALL_INT           1
  42 BINARY_OP               13 (+=)
  43 SWAP                     2
  44 STORE_ATTR               0 (value)
```

Sequence: LOAD_ATTR (read) → BINARY_OP (compute) → STORE_ATTR (write).
Interleaving between 42 (BINARY_OP) and 44 (STORE_ATTR) = `lost update`.

The GIL makes each instruction atomic, not the full sequence.

## Cache — `if key not in d:`

Captured with `dis` at runtime:

```
  LOAD_FAST                0 (d)
  LOAD_FAST                1 (key)
  CONTAINS_OP              0
  POP_JUMP_IF_FALSE        ...
```

TOCTOU (Time-Of-Check-Time-Of-Use): the check (`CONTAINS_OP`) and the act (`d[key] = ...`)
are separate instructions. Between them, another thread can insert.

`cache` thread-local does NOT solve: each thread would have its own copy;
the bug would be missing shared cache, not elimination of thundering herd.
