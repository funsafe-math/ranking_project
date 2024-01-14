from fastapi import Depends, FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
import time
import random
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine
import ranker.ranking_manager as ranking_manager

app = FastAPI(
    title="Ranking API",
    description="API for binary ranking app",
    version="0.0.1",
    # root_path="/api",
    servers=[
        # {"url": "http://127.0.0.1:8000/api/v1"},
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create_ranking')
def create_ranking(data: schemas.Ranking, db: Session = Depends(get_db)):
    rankings = crud.get_rankings(db)
    if any([r.description == data.description for r in rankings]):
        raise HTTPException(status_code=409, detail="Ranking with this description already exists")

    while True:
        new_id = random.randint(0, 1<<32)
        if not any([r.ranking_id == new_id for r in rankings]):
            break
    data.ranking_id = new_id
    crud.create_ranking(db, data)
    return

@app.post('/create_alternative/{rankingId}')
def create_alternative(rankingId: int, data: schemas.Alternative, db: Session = Depends(get_db)):
    alternatives_in_ranking = crud.get_alternatives_by_ranking_id(db, rankingId)
    if any([a.name == data.name for a in alternatives_in_ranking]):
        raise HTTPException(status_code=409, detail="Alternative with this name already exists")
    if any([a.description == data.description for a in alternatives_in_ranking]):
        raise HTTPException(status_code=409, detail="Alternative with this description already exists")

    while True:
        new_id = random.randint(0, 1<<32)
        if not any([r.alternative_id == new_id for r in alternatives_in_ranking]):
            break
    data.alternative_id = new_id
    return crud.create_alternative(db, data, rankingId)

@app.post('/create_criteria/{rankingId}')
def create_criteria(rankingId: int, data: schemas.Criterion, db: Session = Depends(get_db)):
    criterias_in_ranking = crud.get_criteria_by_ranking_id(db, rankingId)
    if any([a.name == data.name for a in criterias_in_ranking]):
        raise HTTPException(status_code=409, detail="criteria with this name already exists")
    if any([a.description == data.description for a in criterias_in_ranking]):
        raise HTTPException(status_code=409, detail="criteria with this description already exists")

    while True:
        new_id = random.randint(0, 1<<32)
        if not any([r.criteria_id == new_id for r in criterias_in_ranking]):
            break
    data.criteria_id = new_id
    return crud.create_criteria(db, data, rankingId)


@app.post('/create_scale/{rankingId}')
def create_scale(rankingId: int, data: schemas.Scale, db: Session = Depends(get_db)):
    scales_in_ranking = crud.get_scale_values_by_ranking_id(db, rankingId)
    if any([a.value == data.value for a in scales_in_ranking]):
        raise HTTPException(status_code=409, detail="scale with this value already exists")
    if any([a.description == data.description for a in scales_in_ranking]):
        raise HTTPException(status_code=409, detail="scale with this description already exists")

    return crud.create_scale(db, data, rankingId)


@app.post('/update_ranking_info/{rankingId}')
def update_ranking(rankingId: int, data: schemas.Ranking, db: Session = Depends(get_db)):
    if crud.update_ranking_info(db, rankingId, data.description, data.expiring):
        return
    raise HTTPException(status_code=409, detail="Could not update ranking")

@app.post('/create_variables/{rankingId}')
def create_variables(rankingId: int, data: schemas.Variables, db: Session = Depends(get_db)):
    return crud.create_variables(db, data, rankingId)

@app.post('/create_expert/{rankingId}')
def create_expert(rankingId: int, data: schemas.Expert, db: Session = Depends(get_db)):
    ## TODO: get all experts and check for conflicts
    return crud.create_expert(db, data, rankingId)

@app.get('/rankings', response_model=List[schemas.Ranking])
def read_rankings(db: Session = Depends(get_db)):
    rankings = crud.get_rankings(db)
    if not rankings:
        return JSONResponse(
            content=[],
            status_code=404
        )
    print([r.ranking_id for r in rankings])
    return rankings

class QuestionGenerator:
    #TODO: implement
    counter = 0
    def __init__(self):
        self.counter = 0

    def get_question(self, ranking_id: int, expert_id: int) -> schemas.Choice:
        self.counter += 1
        if self.counter & 1 == 1:
            return schemas.CriterionChoice(choiceType='CriterionChoice')
        else:
            choiceA = schemas.Alternative(name="Opcja A", description="option A", alternative_id=69)
            choiceB = schemas.Alternative(name="Opcja B", description="option B", alternative_id=420)
            return schemas.ABChoice(choiceA=choiceA, choiceB=choiceB, choiceType="ABChoice")

generator = QuestionGenerator()

@app.get('/rank/{rankingId}')
def read_a_question(rankingId: int) -> schemas.Choice:
    global generator
    return generator.get_question(ranking_id=rankingId, expert_id=0)



@app.post('/rankAB/{rankingId}')
def write_rank_AB(rankingId: int, data: schemas.ABInput):
    print(data)
    return

# @app.post('/rankCriterion/{rankingId}')
# def write_rank_criterion(rankingId: int, data: CriterionInput):
#     print(data)
#     return

# @app.get('/results')
# def read_results() -> List[Result]:
#     return []

# @app.get('/variables/{rankingId}')
# def read_variables(rankingId: int) -> Variables:
#     return Variables()

# @app.get('/raw_results/{rankingId}')
# def get_raw_results(rankingId: int) -> ResultRaw:
#     return ResultRaw()
