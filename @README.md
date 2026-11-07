# Proyecto de Ingeniería e Investigación

## Descripción

Este proyecto demuestra el mecanismo REAL por el cual `sum(range(0))` permite un cambio de hilo en CPython.

## Hallazgos

- **`--gap-size 0`**: El cambio de hilo no ocurre por un `FOR_ITER` de Python, sino porque la implementación en C de `sum()` verifica el `eval_breaker` del GIL durante su iteración, incluso con 0 elementos.
- **Comportamiento medido en CPython 3.14.7 / Windows 11**.