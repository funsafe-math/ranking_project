from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import time
import random
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Annotated
import crud, models, schemas
from database import SessionLocal, engine

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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


# User
@app.post('/token')
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    expert = crud.find_expert(db, form.username)
    if expert is None:
        raise HTTPException(status_code=400, detail="Unknown user")
    return {"acces_token": form.username, "token_type": "bearer"}

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    print("token: ", token, type(token))
    expert = crud.find_expert(db, token)
    print("expert: ", expert)
    if not expert:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return expert

@app.get('/me', response_model=schemas.Expert)
def return_current_user(expert: Annotated[schemas.Expert, Depends(get_current_user)], db: Session = Depends(get_db)):
    # expert = crud.find_expert(db, token) # Token is the same as username
    return expert

@app.post('/create_expert/{rankingId}')
def create_expert(rankingId: int, data: schemas.Expert, db: Session = Depends(get_db)):
    ## TODO: get all experts and check for conflicts
    experts = crud.get_experts(db, rankingId)
    if any([r.email == data.email for r in experts]):
        raise HTTPException(status_code=409, detail="Expert with this email already exists")

    while True:
        new_id = random.randint(0, 1<<32)
        if not any([r.expert_id == new_id for r in experts]):
            break
    data.expert_id = new_id
    return crud.create_expert(db, data, rankingId)

@app.get('/experts/{rankingId}', response_model=List[schemas.Expert])
def all_experts_by_ranking(rankingId: int, db: Session = Depends(get_db)):
    return crud.get_experts(db, rankingId)

@app.put('/experts/{ranking_id}/{expert_id}')
def update_expert(ranking_id: int, expert_id:int, db: Session = Depends(get_db)):
    # TODO
    return

@app.delete('/experts/{ranking_id}/{expert_id}')
def delete_expert(ranking_id: int, expert_id:int, db: Session = Depends(get_db)):
    return crud.delete_expert(db, ranking_id, expert_id)

# Ranking
@app.post('/create_ranking', status_code=status.HTTP_201_CREATED)
def create_ranking(data: schemas.Ranking, expert: Annotated[schemas.Expert, Depends(get_current_user)], db: Session = Depends(get_db)):
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

@app.get('/all_rankings', response_model=List[schemas.Ranking])
def read_all_rankings(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    print('token: ', token)
    rankings = crud.get_rankings(db)
    if not rankings:
        return JSONResponse(
            content=[],
            status_code=404
        )
    print([r.ranking_id for r in rankings])
    return rankings

@app.get('/rankings/{expert_id}', response_model=List[schemas.Ranking])
def read_rankings_available_for_expert(expert_id: int, db: Session = Depends(get_db)):
    rankings = crud.get_expert_ranking(db, expert_id)
    if not rankings:
        return JSONResponse(
            content=[],
            status_code=404
        )
    print([r.ranking_id for r in rankings])
    return rankings

@app.put('/ranking/{rankingId}')
def update_ranking(rankingId: int, data: schemas.Ranking, db: Session = Depends(get_db)):
    if crud.update_ranking_info(db, rankingId, data.description, data.expiring):
        return
    raise HTTPException(status_code=409, detail="Could not update ranking")


@app.delete('/ranking/{rankingId}')
def delete_ranking(rankingId: int, expert: Annotated[schemas.Expert, Depends(get_current_user)], db: Session = Depends(get_db)):
    print("Deleting ", rankingId, " by: ", expert.email)
    return crud.delete_ranking(db, rankingId)

# Variables
@app.post('/create_variables/{rankingId}')
def create_variables(rankingId: int, data: schemas.Variables, db: Session = Depends(get_db)):
    return crud.create_variables(db, data, rankingId)

@app.get('/variables/{rankingId}', response_model=schemas.Variables)
def get_variables(rankingId: int, db: Session = Depends(get_db)):
    variables = crud.get_variables(db, rankingId)
    if variables is None:
        raise HTTPException(status_code=404, detail="No variables for ranking")
    return variables

@app.put('/variables/{ranking_id}')
def update_variables(rankingId: int, data: schemas.Variables, db: Session = Depends(get_db)):
    #TODO
    return

@app.delete('/variables/{ranking_id}')
def delete_variables(rankingId: int, db: Session = Depends(get_db)):
    #TODO
    return

# Alternatives
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

@app.get('/all_alternatives/{rankingId}', response_model=List[schemas.Alternative])
def get_all_alternatives(rankingId: int, expert: Annotated[schemas.Expert, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.get_all_alternatives_by_ranking_id(db, rankingId)

@app.delete('/alternative/{rankingId}/{alternativeId}')
def delete_alternative(rankingId: int, alternativeId: int, db: Session = Depends(get_db)):
    if crud.delete_alternative(db, rankingId, alternativeId):
        return
    raise HTTPException(status_code=409, detail="Could not delete alternative")

# Criteria
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

@app.get('/criteria/{ranking_id}', response_model=List[schemas.Criterion])
def get_criteria_for_ranking(ranking_id: int, db: Session = Depends(get_db)):
    return crud.get_criteria_by_ranking_id(db, ranking_id)

@app.delete('/criteria/{ranking_id}/{criteria_id}')
def delete_criterion(ranking_id: int, db: Session = Depends(get_db)):
    #TODO
    return


# Scale
@app.post('/create_scale/{rankingId}')
def create_scale(rankingId: int, data: schemas.Scale, db: Session = Depends(get_db)):
    scales_in_ranking = crud.get_scale_values_by_ranking_id(db, rankingId)
    if any([a.value == data.value for a in scales_in_ranking]):
        raise HTTPException(status_code=409, detail="scale with this value already exists")
    if any([a.description == data.description for a in scales_in_ranking]):
        raise HTTPException(status_code=409, detail="scale with this description already exists")

    while True:
        new_id = random.randint(0, 1<<32)
        if not any([s.scale_id == new_id for s in scales_in_ranking]):
            print("Using id: ", new_id)
            break
    data.scale_id = new_id

    return crud.create_scale(db, data, rankingId)

@app.get('/get_scale/{ranking_id}', response_model=List[schemas.Scale])
def get_scale_for_ranking(ranking_id: int, db: Session = Depends(get_db)):
    return crud.get_scale_values_by_ranking_id(db, ranking_id)

@app.delete('/scale/{ranking_id}/{scale_id}')
def delete_scale(ranking_id: int, scale_id: int, db: Session = Depends(get_db)):
    return crud.delete_scale(db, ranking_id, scale_id)


# Get data from user

@app.post('/rankAB/{rankingId}')
def write_rank_AB(rankingId: int, data: schemas.ABInput, db: Session = Depends(get_db)):
    all_data = crud.get_data_by_ranking_id(db, rankingId)
    while True:
        new_id = random.randint(0, 1<<32)
        if not any([d.data_id == new_id for d in all_data]):
            break
    crud.create_data(db,
      data_id=new_id,
      ranking_id=rankingId,
      expert_id=data.expert_id,
      criteria_id=data.criteria_id,
      alternative1_id=data.alternativeA_id,
      alternative2_id=data.alternativeB_id,
      result=data.winner_id
    )
    return

@app.post('/weight/{rankingId}')
def add_weight(rankingId: int, data: schemas.Weights, db: Session = Depends(get_db)):
    all_weights = crud.get_weights_by_ranking_id(db, rankingId)
    while True:
        new_id = random.randint(0, 1<<32)
        if not any([w.weights_id == new_id for w in all_weights]):
            break
    data.weights_id = new_id
    return crud.create_weight(db, rankingId, data)
    




    
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
