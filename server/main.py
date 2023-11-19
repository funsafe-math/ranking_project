from typing import Annotated, List, Literal, Union

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field
import time
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ranking API",
    description="API for binary ranking app",
    version="0.0.1",
    # root_path="/api",
    servers=[ 
        { "url": "http://127.0.0.1:8000/api/v1" },
        {"url": "http://127.0.0.1:8000", "description": "Local test server"},
    ],
)
app.openapi_version = "3.0.2"
origins = [
    "http://localhost:5000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Ranking(BaseModel):
    desc: str = 'Superheroes ranking'
    id: int = 99999999
    expiring: int = 1699899952 # Unix timestamp

class Alternative(BaseModel):
    id: int = 0
    name: str = 'Batman'
    description: str = 'Batman comicbook character'


class ABChoice(BaseModel):
    choiceType: Literal['ABChoice']
    choiceA: Alternative = Alternative()
    choiceB: Alternative = Alternative()

class CriterionChoice(BaseModel):
    choiceType: Literal['CriterionChoice']
    name: str = 'strength'
    description: str = 'lorem ipsum'
    options: list[str] = ['important', 'not important']

class Result(BaseModel):
    rankingId: int = -1
    alternative_id: int = -1
    place: int = -1

Choice = Annotated[Union[ABChoice, CriterionChoice], Field(discriminator="choiceType")]

class ABInput(BaseModel):
    alternativeA_id: int = -1
    alternativeB_id: int = -1
    winner_id: int = -1

class CriterionInput(BaseModel):
    name: str = 'strength'
    chosen_option: str = 'not important'

class Variables(BaseModel):
    ranking_method: str = 'EVM'
    aggregation_method: str = 'AIP'
    completness_required: bool = True

class ResultRawCriterion(BaseModel):
    id: int = 1
    parent_criterion: str = 'none'
    name: str = 'lore ipsum'
    description: str = 'lore lore ipsum'

class ResultRawExpert(BaseModel):
    id: int = 1
    name: str = 'Joe Doe'
    address: str = 'example@example.com'

class Scale(BaseModel):
    value: float = 0.5
    description: str = 'moderate important'

class ResultRawModel(BaseModel):
    alternatives: List[Alternative] = []
    criteria: List[ResultRawCriterion] = []
    experts: List[ResultRawExpert] = []
    ranking_method: str = 'EVM'
    aggregation_method: str = 'AIP'
    completeness_required: bool = True
    scale: List[Scale] = []

class ResultRawMatrix(BaseModel):
    criterion: int = 3
    pcm: List[List[float]] = []

class ResultRawDataSet(BaseModel):
    matrices: List[ResultRawMatrix] = []

class ResultRawData(BaseModel):
    expertId: int = 1
    data_set: List[ResultRawDataSet] = []

class ResultRawWeight(BaseModel):
    criterion: int = 3
    w: List[float] = []

    
class ResultRawDecisionScenario(BaseModel):
    model: ResultRawModel = ResultRawModel()
    data: List[ResultRawData] = []
    weights: List[ResultRawWeight] = []

class ResultRaw(BaseModel):
    decision_scenario: ResultRawDecisionScenario = ResultRawDecisionScenario()

@app.get('/rankings')
def read_rankings() -> List[Ranking]:
    rankings = [
        Ranking(desc="Superheroes ranking"),
        Ranking(desc="Superheroes ranking v2"),
        Ranking(desc="Profesor ranking"),
        Ranking(desc="Car ranking"),
    ]
    # ranking = Ranking()
    # time.sleep(2)
    return rankings

counter = 0
@app.get('/rank/{rankingId}')
def read_rank(rankingId: int) -> Choice:
    global counter
    counter+=1
    if counter & 1 == 1:
        return CriterionChoice(choiceType='CriterionChoice')
    else:
        choiceA = Alternative(name="Opcja A", description="option A", id=69)
        choiceB = Alternative(name="Opcja B", description="option B", id=420)
        return ABChoice(choiceA=choiceA, choiceB=choiceB, choiceType="ABChoice")

@app.post('/rankAB/{rankingId}')
def write_rank_AB(rankingId: int, data: ABInput):
    print(data)
    return

@app.post('/rankCriterion/{rankingId}')
def write_rank_criterion(rankingId: int, data: CriterionInput):
    print(data)
    return

@app.get('/results')
def read_results() -> List[Result]:
    return []

@app.get('/variables/{rankingId}')
def read_variables(rankingId: int) -> Variables:
    return Variables()

@app.put('/variables/{rankingId}')
def write_variables(rankingId: int, data: Variables):
    return

@app.get('/raw_results/{rankingId}')
def get_raw_results(rankingId: int) -> ResultRaw:
    return ResultRaw()

# @app.get("/")
# def read_root():
#     return "Hello World"


