from pydantic import BaseModel, Field
from typing import Annotated, List, Literal, Union

class Ranking(BaseModel):
    ranking_id: int
    description: str
    expiring: int  # Unix timestamp
    class Config:
        from_attributes = True


class Alternative(BaseModel):
    alternative_id: int = 0
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

class Criterion(BaseModel):
    criteria_id : int = 1
    parent_criterion: str = 'none'
    name: str = 'lore ipsum'
    description: str = 'lore lore ipsum'
    class Config:
        from_attributes = True

class Expert(BaseModel):
    id: int = 1
    name: str = 'Joe Doe'
    address: str = 'example@example.com'

class Scale(BaseModel):
    value: float = 0.5
    description: str = 'moderate important'

class ResultRawModel(BaseModel):
    alternatives: List[Alternative] = []
    criteria: List[Criterion] = []
    experts: List[Expert] = []
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