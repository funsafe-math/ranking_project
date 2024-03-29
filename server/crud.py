from sqlalchemy.orm import Session, Query
from typing import List

import numpy as np

import schemas
from models import *
# import main

# Tworzymy ranking
def create_ranking(db: Session, ranking: schemas.Ranking):
    new_ranking = Rankings(
        ranking_id=ranking.ranking_id,
        description=ranking.description,
        expiring=ranking.expiring
    )
    db.add(new_ranking)
    db.commit()
    db.refresh(new_ranking)
    return new_ranking


# Dodawanie alternatywy do rankingu
def create_alternative(db: Session, alternative: schemas.Alternative, ranking_id: int):
    new_alternative = Alternatives(
        alternative_id=alternative.alternative_id,
        ranking_id=ranking_id,
        description=alternative.description,
        name=alternative.name
    )
    db.add(new_alternative)
    db.commit()
    db.refresh(new_alternative)
    return new_alternative


# Dodawanie kryterium do rankingu
def create_criteria(db: Session, criteria: schemas.Criterion, ranking_id):
    new_criteria = Criteria(
        criteria_id=criteria.criteria_id,
        ranking_id=ranking_id,
        name=criteria.name,
        description=criteria.description)
    db.add(new_criteria)
    db.commit()
    db.refresh(new_criteria)
    return new_criteria


# Dodawanie skali do rankingu
def create_scale(db: Session, scale: schemas.Scale, ranking_id: int):
    new_scale = Scale(
        scale_id=scale.scale_id,
        ranking_id=ranking_id,
        description=scale.description,
        value=scale.value)
    db.add(new_scale)
    db.commit()
    db.refresh(new_scale)
    return new_scale


# Dodawanie zmiennych do rankingu
def create_variables(db: Session, variables: schemas.Variables, ranking_id: int):
    new_variables = Variables(
        ranking_id=ranking_id,
        variable_id=ranking_id,
        ranking_method=variables.ranking_method,
        aggregation_method=variables.aggregation_method,
        completness_required=variables.completness_required
    )
    db.add(new_variables)
    db.commit()
    db.refresh(new_variables)
    return new_variables

# Zbieranie zmiennych dla rankingu
def get_variables(db: Session, ranking_id: int) -> Variables | None:
    return db.query(Variables).filter(Variables.ranking_id == ranking_id).first()


# Tworzymy eksperta
def create_expert(db: Session, expert: schemas.Expert, ranking_id: int):
    new_expert = Experts(
        ranking_id=ranking_id,
        expert_id=expert.expert_id,
        name=expert.name,
        email=expert.email,
        admin=expert.admin,
    )
    db.add(new_expert)
    db.commit()
    db.refresh(new_expert)
    return new_expert


# Dodawanie danych
def create_data(db: Session, data_id: int, ranking_id: int, expert_id: int,
                criteria_id: int, alternative1_id: int, alternative2_id: int,
                result: int):
    result_bool = (result == alternative1_id)
    new_data = Data(data_id=data_id,
                    ranking_id=ranking_id,
                    expert_id=expert_id,
                    criteria_id=criteria_id,
                    alternative1_id=alternative1_id,
                    alternative2_id=alternative2_id,
                    result=result_bool)  # TODO: investigate if `result` is bool or int?
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


def create_weight(db: Session, ranking_id: int, data: schemas.Weights) -> Weights:
    new_weight = Weights(
        weights_id = data.weights_id,
        ranking_id = data.ranking_id,
        expert_id = data.expert_id,
        criteria_id = data.criteria_id,
        scale_id = data.scale_id,
    )
    db.add(new_weight)
    db.commit()
    db.refresh(new_weight)
    return new_weight


# Admin pyta o wszystkie rankingi
def get_rankings(db: Session):
    return db.query(Rankings)

def get_experts(db: Session, ranking_id: int) -> List[Experts]:
    return db.query(Experts).filter(Experts.ranking_id == ranking_id).all()


# Ekspert pyta o rankingi
def get_expert_ranking(db: Session, expert_id: int) -> List[Rankings]:
    expert = db.query(Experts).filter(Experts.expert_id == expert_id).first()
    if expert is None:
        return []
    result = db.query(Rankings).filter(Rankings.ranking_id == expert.ranking_id).all()
    return result


# Usunięcie alternatywy dla rankingu
def delete_alternative(db: Session, ranking_id: int, alternative_id: int) -> bool:
    try:
        alternative = (
            db.query(Alternatives)
            .filter(Alternatives.ranking_id == ranking_id, Alternatives.alternative_id == alternative_id)
            .first()
        )
        if alternative:
            db.delete(alternative)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting alternative: {e}")
        return False

def delete_expert(db: Session, ranking_id: int, expert_id: int) -> bool:
    try:
        expert = (
            db.query(Experts)
            .filter(Experts.ranking_id == ranking_id, Experts.expert_id == expert_id)
            .first()
        )
        if expert:
            db.delete(expert)
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting alternative: {e}")
        return False


def delete_ranking(db: Session, ranking_id: int) -> bool:
    try:
        ranking = (
            db.query(Rankings)
            .filter(Rankings.ranking_id == ranking_id)
            .first()
        )
        if ranking:
            db.delete(ranking)
            db.commit()
            return True
            # TODO: remove linked data
        else:
            return False
    except Exception as e:
        print(f"Error deleting ranking: {e}")
        return False

# Pytanie o listę alternatyw dla rankingu
def get_alternatives_by_ranking_id(db: Session, ranking_id: int) -> List[Alternatives]:
    alternatives = db.query(Alternatives).filter(Alternatives.ranking_id == ranking_id).all()
    return alternatives


# Pytanie o listę kryteriów dla rankingu
def get_criteria_by_ranking_id(db: Session, ranking_id: int) -> List[Criteria]:
    criteria = db.query(Criteria).filter(Criteria.ranking_id == ranking_id).all()
    return criteria


# Usunięcie kryterium dla rankingu
def delete_criteria_by_ranking_id(db: Session, ranking_id: int) -> bool:
    try:
        criteria_list = db.query(Criteria).filter(Criteria.ranking_id == ranking_id).all()

        for criteria in criteria_list:
            db.delete(criteria)

        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting criteria: {e}")
        return False


# Ekspert pyta o skalę do ocen kryteriów dla rankingu

def get_scale_values_by_ranking_id(db: Session, ranking_id: int) -> List[schemas.Scale]:
    scales = db.query(Scale).filter(Scale.ranking_id == ranking_id).all()
    ret = []
    for s in scales:
        print(s.scale_id)
        ret.append(schemas.Scale(value=s.value, description=s.description, scale_id=s.scale_id, ranking_id = s.ranking_id))
    return ret

def delete_scale(db: Session, ranking_id: int, scale_id: int) -> bool:
    try:
        scale_list = db.query(Scale).filter(Scale.ranking_id == ranking_id, Scale.scale_id == scale_id).all()
        print(f"Deleting {len(scale_list)} scales")

        for scale in scale_list:
            db.delete(scale)

        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting scale: {e}")
        return False



# Edycja rankingu przez admina (nadpisanie)
def update_ranking_info(db: Session, ranking_id: int, new_description: str, new_expiring: int) -> bool:
    try:
        ranking = db.query(Rankings).filter(Rankings.ranking_id == ranking_id).first()

        if ranking:
            ranking.description = new_description
            ranking.expiring = new_expiring
            db.commit()
            db.refresh(ranking)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error updating ranking info: {e}")
        return False



# Pytanie o wyniki dla rankingu
def get_results_by_alternative_id(db: Session, alternative_id: int):
    results = db.query(Results).filter(Results.alternative_id == alternative_id).all()
    return results


# Pytanie o dane dla rankingu
def get_data_by_ranking_id(db: Session, ranking_id: int):
    data = db.query(Data).filter(Data.ranking_id == ranking_id).all()
    return data


# Pytanie o wagi dla rankingu
def get_weights_by_ranking_id(db: Session, ranking_id: int):
    weights = db.query(Weights).filter(Weights.ranking_id == ranking_id).all()
    return weights

def get_all_alternatives_by_ranking_id(db: Session, ranking_id: int) -> List[Alternatives]:
    alternatives = db.query(Alternatives).filter(Alternatives.ranking_id == ranking_id).all()
    return alternatives


# # Dodawanie wag
def add_weights_from_matrix(db: Session, matrix_data: schemas.ResultRawMatrix, ranking_id: int, expert_id: int,
                            scale_id: int):
    new_weights = Weights(
        ranking_id=ranking_id,
        expert_id=expert_id,
        weights_id=ranking_id,
        criteria_id=matrix_data.criterion,
        scale_id=scale_id,
        weights=matrix_data.pcm
    )
    db.add(new_weights)
    db.commit()
    return new_weights


#  Dodawanie wyniku algorytmu do bazy danych
def create_results(db: Session, ranking_id: int, alternative_id: int, place: int):
    new_result = Results(
        ranking_id=ranking_id,
        alternative_id=alternative_id,
        place=place
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

def find_expert(db: Session, email: str) -> Experts | None:
    return db.query(Experts).filter(Experts.email == email).first()

def update_alternative_rank(db: Session, ranking_id: int, alternative_id: int, place: int) -> bool:
    try:
        result = db.query(Results).filter(Results.ranking_id == ranking_id, Results.alternative_id == alternative_id).first()

        if result:
            result.place = place
            db.commit()
            db.refresh(result)
            return True
        else:
            new_result = Results(ranking_id=ranking_id, alternative_id=alternative_id, place=place)
            db.add(new_result)
            db.commit()
            db.refresh(new_result)
    except Exception as e:
        print(f"Error updating ranking info: {e}")
        return False

def get_alternative_rank(db: Session, ranking_id: int) -> List[Results]:
    return db.query(Results).filter(Results.ranking_id == ranking_id).all()

def get_ranking_method(db: Session, ranking_id: int):
    return db.query(Variables).filter(Variables.ranking_id == ranking_id).first().ranking_method

def get_aggregation_method(db: Session, ranking_id: int):
    return db.query(Variables).filter(Variables.ranking_id == ranking_id).first().aggregation_method

def get_scales_by_ranking_id(db: Session, ranking_id: int):
    return db.query(Scale).filter(Scale.ranking_id == ranking_id).all()

def get_matrix_by_ranking_id_expert_id_criteria_id(db: Session, ranking_id: int, expert_id: int, criteria_id: int, alternative_map):
    num_of_alternatives = db.query(Alternatives).filter(Alternatives.ranking_id == ranking_id).count()
    data = db.query(Data).filter(Data.ranking_id == ranking_id, Data.expert_id == expert_id, Data.criteria_id == criteria_id).all()
    weight = db.query(Weights).filter(Weights.ranking_id == ranking_id, Weights.expert_id == expert_id, Weights.criteria_id == criteria_id).first()
    scale = db.query(Scale).filter(Scale.ranking_id == ranking_id, Scale.scale_id == weight.scale_id).first().value if weight else 2
    matrix = np.zeros((num_of_alternatives, num_of_alternatives))
    for d in data:
        if d.result == 0:
            matrix[alternative_map[d.alternative1_id]][alternative_map[d.alternative2_id]] = scale
            matrix[alternative_map[d.alternative2_id]][alternative_map[d.alternative1_id]] = 1/scale
        elif d.result == 1:
            matrix[alternative_map[d.alternative2_id]][alternative_map[d.alternative1_id]] += scale
            matrix[alternative_map[d.alternative1_id]][alternative_map[d.alternative2_id]] += 1/scale
    for i in range(num_of_alternatives):
        for j in range(num_of_alternatives):
            if i == j:
                matrix[i][j] = 1
    return matrix


def get_weights_by_ranking_id_criteria_id(db, ranking_id, criteria_id, expert_map):
    weights = db.query(Weights).filter(Weights.ranking_id == ranking_id, Weights.criteria_id == criteria_id).all()
    ret_val = [0 for _ in range(len(expert_map))]
    print(expert_map)
    print(ret_val)
    for w in weights:
        if w.expert_id in expert_map.keys():
            ret_val[expert_map[w.expert_id]] = db.query(Scale).filter(Scale.ranking_id == ranking_id, Scale.scale_id == w.scale_id).first().value
    return ret_val


def export_data(db: Session, ranking_id: int):
    alternative_map = {
        a.alternative_id: i for i, a in enumerate(get_all_alternatives_by_ranking_id(db, ranking_id))
    }
    expert_map = {
        e.expert_id: i for i, e in enumerate(get_experts(db, ranking_id))
    }
    return_value = {
        "decision_scenario": {

            "model" : {
                "alternatives": [ {
                    "id": alternative_map[a.alternative_id],
                    "name": a.name,
                    "description": a.description,
                } for a in get_alternatives_by_ranking_id(db, ranking_id)],
                "criteria": [{
                    "id": c.criteria_id,
                    "name": c.name,
                    "description": c.description,
                } for c in get_criteria_by_ranking_id(db, ranking_id)],
                "experts": [{
                    "id": expert_map[e.expert_id],
                    "name": e.name,
                    "address": e.email,
                } for e in get_experts(db, ranking_id)],
                "ranking_method": get_ranking_method(db, ranking_id),
                "aggregation_method": get_aggregation_method(db, ranking_id),
                "completness_required": db.query(Variables).filter(Variables.ranking_id == ranking_id).first().completness_required,
                "scale": [{
                    "value": s.value,
                    "description": s.description,
                } for s in get_scales_by_ranking_id(db, ranking_id)],
            },

            "data": [{
                "expertId": expert_map[e.expert_id],
                "data_set":{
                    "matrices": [{
                        "criterion": c.criteria_id,
                        "pcm": get_matrix_by_ranking_id_expert_id_criteria_id(db, ranking_id, e.expert_id, c.criteria_id, alternative_map).tolist(),
                    } for c in get_criteria_by_ranking_id(db, ranking_id) ],
                }
            } for e in get_experts(db, ranking_id)],

            "weights": [{
                "criterion": c.criteria_id,
                "w": get_weights_by_ranking_id_criteria_id(db, ranking_id, c.criteria_id, expert_map),
            } for c in get_criteria_by_ranking_id(db, ranking_id)]
        }
    }
    return return_value



# teścik
# create_ranking(session,schemas.r)
# create_alternative(session,schemas.a,50)
# create_criteria(session,schemas.c,50)
# create_scale(session,schemas.s, 10)
# create_variables(session,schemas.v,10)
# create_expert(session, schemas.e,5)
# create_data(session, data_id = 4, ranking_id = 4, expert_id = 7,
#                criteria_id = 5, alternative1_id = 1, alternative2_id = 2, result = 1)
# get_rankings(session)
# get_expert_ranking(session,1)
# get_alternatives_by_ranking_id(session, 50)
# get_criteria_by_ranking_id(session,50)
# get_scales_by_ranking_id(10)
