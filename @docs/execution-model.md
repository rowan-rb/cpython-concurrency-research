# Modelo de Ejecución de CPython

## Liberación del GIL en `sum()`

### Mecanismo de Liberación del GIL

- **`sum(range(0))`**: La implementación en C de `sum()` verifica el `eval_breaker` del GIL durante su iteración, incluso con 0 elementos, lo que permite la liberación del GIL.

### Rol del `eval_breaker` en `ceval.c`

- El `eval_breaker` en `ceval.c` (CPython 3.14) es responsable de comprobar si se debe ceder el GIL. En el bucle de C de la implementación de `sum()`, se verifica el `eval_breaker` para permitir el cambio de hilo.

### Diferencia entre Bytecode de Python y Funciones C

- **Bytecode de Python**: El bytecode `FOR_ITER` no libera el GIL, ya que el GIL se mantiene mientras se ejecuta el bytecode de Python.
- **Funciones C**: Las funciones C pueden verificar el `eval_breaker` y liberar el GIL, como en el caso de la implementación de `sum()`.