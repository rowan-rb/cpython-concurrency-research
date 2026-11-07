# CPython Execution Model and the GIL

## The `sum(range(0))` anomaly
A common misconception is that the GIL only switches threads during Python bytecode instructions like `FOR_ITER` or `CALL`. However, we empirically observed that `sum(range(0))` (a completely empty loop) is enough to cause a context switch, resulting in ~90% lost updates in our counter.

## Why does this happen?
The `sum()` function is implemented in C. It does not execute Python bytecode. Instead, it performs a C-level loop over the iterator.

To prevent C extensions from monopolizing the interpreter, CPython's C loops periodically check the `eval_breaker` (a global variable in `ceval.c`). When the GIL's time slice expires (`sys.setswitchinterval`), the `eval_breaker` is triggered. 

Even if the iterator is exhausted on the very first check (`range(0)`), `sum()` performs an initial iteration cycle to verify emptiness. During this cycle, the interpreter checks `eval_breaker`, which gives the OS a chance to release the GIL and switch to another thread.

## Python Bytecode vs. C-Extensions
- **Python Bytecode:** Context switches happen at specific instructions (e.g., `JUMP_BACKWARD`, `CALL`) due to the `eval_breaker` check in the evaluation loop.
- **C-Extensions:** The GIL is held for the entire duration of the C function, *unless* the function explicitly releases it or hits a loop that checks `eval_breaker`.

This experiment proves that any C-level iterator loop acts as a yield-point, even if it processes zero items.
