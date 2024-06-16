from typing import Mapping, Protocol, TypedDict, Generic, Sequence, TypeVar, TypeAlias, Callable, NamedTuple
from functools import cache
from haskellian import Left, Either, either as E
from q.api import Queue, ReadQueue, WriteQueue, QueueError, ops
from .specs import Pipeline, Workflow, Stateful

A = TypeVar('A')
B = TypeVar('B')
S1 = TypeVar('S1')
S2 = TypeVar('S2')

class PipelineQueues(TypedDict, Generic[A, B]):
  Qin: Queue[A]
  Qout: WriteQueue[B]

class NestedQueues(TypedDict, Generic[A, B]):
  Qin: WriteQueue[A]
  internal: Mapping[str, 'WorkflowQueues']

WorkflowQueues: TypeAlias = PipelineQueues[A, B] | NestedQueues[A, B]

class prejoin(WriteQueue[A], Generic[A]):
  def __init__(self, queues: Sequence[tuple[WriteQueue[A], Sequence[type[A]]]]):
    self.queues = queues
  
  async def push(self, key: str, value: A) -> Either[QueueError, None]:
    for q, types in self.queues:
      for t in types:
        if isinstance(value, t):
          return await q.push(key, value)
    return Left(QueueError(f'Invalid type {type(value).__name__} for {value}'))

class state_merged(WriteQueue[B], Generic[B]):
  def __init__(
    self, post: Callable[[S1, B], S2],
    Qin: ReadQueue[S1], Qout: WriteQueue[S2]
  ):
    self.post = post
    self.Qin = Qin
    self.Qout = Qout

  @E.do[QueueError]()
  async def push(self, key: str, value: B): # type: ignore (python, bruh)
    state = (await self.Qin.read(key)).unsafe()
    next = self.post(state, value)
    (await self.Qout.push(key, next)).unsafe()
    (await self.Qin.pop(key)).unsafe()

class MakeQueue(Protocol):
  def __call__(self, id: Sequence[str], type: type[A], /) -> Queue[A]:
    ...

def make_queues(
  workflow: Workflow[A, B],
  make_queue: MakeQueue,
  output_queue: WriteQueue[B]
) -> WorkflowQueues[A, B]:
  
  def _input_queue(task: Pipeline[A, B], prefix: tuple[str, ...]) -> tuple[Queue[A], Sequence[type[A]]]:
    match task:
      case Workflow():
        return _input_queue(task.pipelines[task.input_task], prefix + (task.input_task,))
      case Pipeline():
        return make_queue(prefix, task.input_type), [task.input_type]
  
  @cache
  def _make_queues(task: Pipeline[A, B], prefix: tuple[str, ...], output_queue: WriteQueue[B]) -> WorkflowQueues[A, B]:
    match task:
      case Workflow():
        def input_of(id: str) -> tuple[WriteQueue, Sequence[type]]:
          if id == 'output':
            return output_queue, task.output_types
          else:
            return _make_queues(task.pipelines[id], prefix + (id,), output_queue)['Qin'], [task.pipelines[id].input_type]

        queues = {
          id: _make_queues(
            pipe, prefix + (id,),
            prejoin([
              input_of(id)
              for id in task.next_tasks(pipe.output_types)
            ])
          )
          for id, pipe in task.pipelines.items()
        }
        return NestedQueues(
          Qin=queues[task.input_task]['Qin'],
          internal=queues
        )
      case Stateful():
        Qstate = make_queue(prefix, task.input_type)
        Qout = state_merged(task.post, Qstate, output_queue)
        queues = dict(_make_queues(task.pipeline, prefix + ('internal',), Qout))
        Qin: Queue = queues['Qin'] # type: ignore
        return NestedQueues(
          Qin=ops.tee(Qstate, Qin.premap(task.pre)),
          internal=queues # type: ignore
        )
      case Pipeline():
        return PipelineQueues(
          Qin=_input_queue(task, prefix)[0],
          Qout=output_queue
        )

  return _make_queues(workflow, (), output_queue)
