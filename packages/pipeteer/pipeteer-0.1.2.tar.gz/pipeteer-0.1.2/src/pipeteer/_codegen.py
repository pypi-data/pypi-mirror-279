# BEGIN
from typing import Unpack, TypedDict
from q.api import WriteQueue, ReadQueue, Queue
from pipeteer import MakeQueue, make_queues as _make_queues, PipelineQueues
# UNCOMMENT from MODULE import MOD_IMPORTS
INPUTS = str; OUTPUTS = str; INPUT_TYPE = str; OUTPUT_TYPE = str; STATEFUL_INPUT = str # DELETE
class SUBFLOW_CLASS: # DELETE
  Queues = int # DELETE
class STATEFUL_PIPELINE: # DELETE
  Queues = int # DELETE

# LOOP PIPELINE_CLASS INPUTS OUTPUTS
class PIPELINE_CLASS:
  In = INPUTS
  Out = OUTPUTS
  QueueIn = ReadQueue[INPUTS]
  QueueOut = WriteQueue[OUTPUTS]
  Queues = PipelineQueues[INPUTS, OUTPUTS]

# END

# LOOP STATEFUL_CLASS STATEFUL_INPUT STATEFUL_PIPELINE
class STATEFUL_CLASS:
  class Queues(TypedDict):
    Qin: Queue[STATEFUL_INPUT]
    internal: 'STATEFUL_PIPELINE.Queues'

# END

class WORKFLOW:
  class InternalQueues(TypedDict):
    # LOOP SUBFLOW_ID SUBFLOW_CLASS
    SUBFLOW_ID: SUBFLOW_CLASS.Queues
    # END
    # LOOP PIPELINE_ID PIPELINE_CLASS
    PIPELINE_ID: PIPELINE_CLASS.Queues  
    # END
    # LOOP STATEFUL_ID STATEFUL_CLASS
    STATEFUL_ID: STATEFUL_CLASS.Queues
    # END

  class Queues(TypedDict):
    Qin: Queue[INPUT_TYPE]
    internal: 'WORKFLOW.InternalQueues'

  @staticmethod
  def make_queues(make_queue: MakeQueue, output_queue: WriteQueue[OUTPUT_TYPE]) -> Queues:
    VARIABLE = ... # type: ignore # DELETE
    return _make_queues(VARIABLE, make_queue, output_queue) # type: ignore
  
  @staticmethod
  def artifacts(**queues: Unpack['WORKFLOW.InternalQueues']):
    ...
    
# END
from typing import Sequence
from haskellian import Thunk
from templang import parse
from pipeteer import Workflow, Stateful

source = Thunk(lambda: open(__file__).read())

def union_type(types: Sequence[type]):
  return  ' | '.join(t.__name__ for t in types)

def codegen(workflow: Workflow, *, variable: str, module: str, classname: str) -> str:

  translations = {
    'MODULE': module,
    'WORKFLOW': classname,
    'VARIABLE': variable,
    'INPUT_TYPE': workflow.input_type.__name__,
    'OUTPUT_TYPE': union_type(workflow.output_types),
    'SUBFLOW_CLASS': [],
    'SUBFLOW_ID': [],
    'STATEFUL_CLASS': [],
    'STATEFUL_PIPELINE': [],
    'STATEFUL_ID': [],
    'STATEFUL_INPUT': [],
    'PIPELINE_CLASS': [],
    'PIPELINE_ID': [],
    'INPUTS': [],
    'OUTPUTS': [],
  }

  imports = [variable, workflow.input_type.__name__] + [t.__name__ for t in workflow.output_types]

  for id, pipe in workflow.pipelines.items():
    match pipe:
      case Workflow():
        translations['SUBFLOW_CLASS'].append(id.title())
        translations['SUBFLOW_ID'].append(id)
        imports.append(id.title())
      case Stateful():
        translations['STATEFUL_CLASS'].append(id.title() + 'Stateful')
        translations['STATEFUL_ID'].append(id)
        translations['STATEFUL_INPUT'].append(pipe.input_type.__name__)
        translations['STATEFUL_PIPELINE'].append(id.title())
        imports.extend([pipe.input_type.__name__, id.title()])
      case _:
        translations['INPUTS'].append(pipe.input_type.__name__)
        translations['OUTPUTS'].append(union_type(pipe.output_types))
        translations['PIPELINE_CLASS'].append(id.title() + 'Pipeline')
        translations['PIPELINE_ID'].append(id)
        imports.append(pipe.input_type.__name__)
        imports.extend([t.__name__ for t in pipe.output_types])

  translations['MOD_IMPORTS'] = ', '.join(set(imports))

  return parse(source(), translations)
  