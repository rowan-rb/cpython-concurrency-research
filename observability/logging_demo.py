"""Actionable observability — structured logging.
Each op reports ts, thread_id, op, updates_attempted, updates_committed, delta.
If delta != 0, the failure is counted in real time (no manual inspection needed).
"""
from __future__ import annotations
import logging, sys, threading, time
sys.setswitchinterval(1e-6)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(thread)s %(levelname)s op=%(op)s attempted=%(attempted)s committed=%(committed)s delta=%(delta)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger("observability")

counter = 0
updates_attempted = 0
updates_committed = 0

def update(delta):
    global counter, updates_attempted, updates_committed
    updates_attempted += 1
    old = counter
    counter += delta
    updates_committed += 1
    delta_reported = counter - old - delta
    # Si delta != 0, el bug está reportado en tiempo real.
    log.debug(
        "op=update attempted=%d committed=%d delta=%d",
        updates_attempted, updates_committed, delta_reported,
        extra={"op": "update", "attempted": updates_attempted, "committed": updates_committed, "delta": delta_reported}
    )
    return delta_reported
