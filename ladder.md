# Correctness ladder and failure modes

## thread → process
- What breaks: `threading.Lock` does not cross processes.
- What is needed: `multiprocessing.Lock`.
- Why the previous fix doesn't work: separate memory.

## process → node
- What breaks: node fails, local lock doesn't protect remote data.
- What is needed: transactional DB or Raft consensus.
- Why it doesn't work: `multiprocessing.Lock` is local to the machine.

## node → distributed
- What breaks: network, partitions, message duplication.
- What is needed: Raft / CRDT / consensus.
- Why it doesn't work: no shared-memory solution scales to network.

## Concrete failure modes
- Lock doesn't cross processes.
- Lock doesn't protect if process dies mid-section; persistence / transaction missing.
- `itertools.count` loses its guarantee under PEP 703.
- Correct cache under lock, but double-compute is mitigated, not eliminated.
