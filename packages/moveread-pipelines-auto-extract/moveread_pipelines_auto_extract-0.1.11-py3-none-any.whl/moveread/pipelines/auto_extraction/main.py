from typing import Protocol, TypeVar, NamedTuple, Generic
import asyncio
from haskellian import funcs as F, Left, Right, either as E
from q.api import ReadQueue, WriteQueue, ReadError
import pure_cv as vc
import robust_extraction2 as re
import scoresheet_models as sm
from dslog import Logger
from .types import Ok, Task, Result

@E.do()
def extract(task: Task, model: re.ExtendedModel): 
  mat = vc.decode(task.img)
  corr_mat, cnts = re.extract(mat, model, autocorrect=not task.already_corrected).unsafe()
  corr = vc.encode(corr_mat, format='.jpg')
  cont = F.pipe(
    vc.draw.contours(corr_mat, cnts, color=(0, 0, 255)), # type: ignore
    vc.descale_h(target_height=768),
    vc.encode(format='.jpg'),
  )
  return Ok(contours=cnts.tolist(), corrected=corr, contoured=cont) # type: ignore

State = TypeVar('State')

class Queues(NamedTuple, Generic[State]):
  Qin: ReadQueue[tuple[Task, State]]
  Qout: WriteQueue[tuple[Result, State]]
    

async def run(
  Qin: ReadQueue[tuple[Task, State]],
  Qout: WriteQueue[tuple[Result, State]],
  *, logger: Logger = Logger.of(print).prefix('[AUTO-EXTRACT]')
):
  """Extract all tasks from `Qin`; push results to `Qerr` or `Qok`, passing along the associated state"""

  models: dict[str, re.ExtendedModel] = {}

  @E.do()
  async def fetch_model(id: str):
    if id not in models:
      logger(f'Fetching model "{id}"', level='DEBUG')
      models[id] = (await sm.fetch_model(id)).unsafe()
    return models[id]

  @E.do[ReadError]()
  async def run_one():
    id, (task, state) = (await Qin.read()).unsafe()
    logger(f'Extracting "{id}"')
    model = (await fetch_model(task.model)).unsafe()
    res = extract(task, model)
    (await Qout.push(id, (res, state))).unsafe()
    logger(f'Extracted "{id}": {"OK" if res.tag == "right" else f"ERR: {res.value}"}')
    (await Qin.pop(id)).unsafe()

  while True:
    e = await run_one()
    if e.tag == 'left':
      logger(e.value, level='ERROR')
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(0) # release the loop