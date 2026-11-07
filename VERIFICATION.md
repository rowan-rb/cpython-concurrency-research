## Entorno
> python -V
Python 3.14.7 (tags/v3.14.7:823f032, Aug  5 2026, 10:51:32) [MSC v.1944 64 bit (AMD64)]
> python -c "import sys; print('GIL:', sys._is_gil_enabled())"
GIL: True

## Demo counter (con gap, 3 runs — debe fallar 3/3)
> python demo_counter.py
counter.value=59237 expected=600000
Traceback (most recent call last):
  File "C:\Users\VZ\Proyecto_1.0\demo_counter.py", line 73, in <module>
    assert counter_obj.value == EXPECTED, f"LOST UPDATE: {counter_obj.value} vs {EXPECTED}"
AssertionError: LOST UPDATE: 59237 vs 600000

> python demo_counter.py
counter.value=58425 expected=600000
Traceback (most recent call last):
  File "C:\Users\VZ\Proyecto_1.0\demo_counter.py", line 73, in <module>
    assert counter_obj.value == EXPECTED, f"LOST UPDATE: {counter_obj.value} vs {EXPECTED}"
AssertionError: LOST UPDATE: 58425 vs 600000

> python demo_counter.py
counter.value=59572 expected=600000
Traceback (most recent call last):
  File "C:\Users\VZ\Proyecto_1.0\demo_counter.py", line 73, in <module>
    assert counter_obj.value == EXPECTED, f"LOST UPDATE: {counter_obj.value} vs {EXPECTED}"
AssertionError: LOST UPDATE: 59572 vs 600000

## Demo counter --no-gap (5 runs — debe dar 600000)
> python demo_counter.py --no-gap
no-gap: counter.value=600000 expected=600000

> python demo_counter.py --no-gap
no-gap: counter.value=600000 expected=600000

> python demo_counter.py --no-gap
no-gap: counter.value=600000 expected=600000

> python demo_counter.py --no-gap
no-gap: counter.value=600000 expected=600000

> python demo_counter.py --no-gap
no-gap: counter.value=600000 expected=600000

## Demo cache (3 runs — debe fallar 3/3)
> python demo_cache.py
compute_count=12 d={'shared_key': 'value_for_shared_key_count_...'}
Traceback (most recent call last):
  File "C:\Users\VZ\Proyecto_1.0\demo_cache.py", line 77, in main
    assert compute_count == 1, f"BUG: double-compute / thundering herd detected compute_count={compute_count} (expected 1, got >1)"
AssertionError: BUG: double-compute / thundering herd detected compute_count=12 (expected 1, got >1)

> python demo_cache.py
compute_count=12 d=...
AssertionError: BUG: double-compute / thundering herd detected compute_count=12 (expected 1, got >1)

> python demo_cache.py
compute_count=12 d=...
AssertionError: BUG: double-compute / thundering herd detected compute_count=12 (expected 1, got >1)

## Bytecode counter
> python -c "import dis, demo_counter; dis.dis(demo_counter.Counter.inc)"
  44 LOAD_FAST_BORROW         0 (self)
  45 COPY                     1
  46 LOAD_ATTR                0 (value)
  47 LOAD_SMALL_INT           1
  48 BINARY_OP               13 (+=)
  49 SWAP                     2
  50 STORE_ATTR               0 (value)

## Bytecode cache
> python -c "import dis, demo_cache; dis.dis(demo_cache.buggy_access)"
  54 LOAD_FAST_BORROW         0 (key)
  55 LOAD_GLOBAL              4 (d)
  56 CONTAINS_OP              1 (not in)
  57 POP_JUMP_IF_FALSE       ...
  58 LOAD_FAST_BORROW         1 (val)
  59 LOAD_GLOBAL              4 (d)
  60 LOAD_FAST_BORROW         0 (key)
  61 STORE_SUBSCR

## Tests
> python -m unittest discover -s tests -v
Ran 4 tests in 12.572s
OK

## Scripts README
> .\run.ps1 demo
counter.value=... LOST UPDATE ...
BUG: ... compute_count=12 ...
> .\run.ps1 test
Ran 4 tests ... OK
