from typing import Iterable, Sequence
from pipeteer import WorkflowQueues
from q.api import ReadQueue

def flatten_queues(queues: WorkflowQueues, prefix: tuple[str, ...] = ()) -> Iterable[tuple[Sequence[str], ReadQueue]]:
  # if 'Qin' in queues and isinstance(queues['Qin'], ReadQueue):
  #   yield prefix + ('Qin',), queues['Qin']
  for id, q in queues.items():
    if isinstance(q, dict):
      yield from flatten_queues(q, prefix + (id,)) # type: ignore
    elif isinstance(q, ReadQueue):
      yield prefix + (id,), q