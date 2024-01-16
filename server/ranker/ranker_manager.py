import crud, models, schemas
# from database import SessionLocal, engine
from sqlalchemy.orm import Session

class RankerManager:
    def __init__(self):
        pass

    def start_ranking_algorithm(self, db: Session, ranking_id: int):
        criterias = crud.get_criteria_by_ranking_id(db, ranking_id) 


