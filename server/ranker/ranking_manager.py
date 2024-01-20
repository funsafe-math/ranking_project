from asyncio import Future

import crud, models, schemas
# from database import SessionLocal, engine
from sqlalchemy.orm import Session

import numpy as np
from .ranking_makers import *


class RankerManager:
    def __init__(self):
        pass

    def start_ranking_algorithm(self, db: Session, ranking_id: int) -> Future[str]:
        criterias = crud.get_criteria_by_ranking_id(db, ranking_id)
        alternatives = crud.get_alternatives_by_ranking_id(db, ranking_id)
        scales = crud.get_scale_values_by_ranking_id(db, ranking_id)
        data = crud.get_data_by_ranking_id(db, ranking_id)
        weights = crud.get_weights_by_ranking_id(db, ranking_id)

        experts = list(set([d.expert_id for d in data]))

        alternative_id_to_matrix_place_map = {alternatives[i].alternative_id: i for i in range(len(alternatives))}
        matrix_place_to_alternative_id_map = {i: alternatives[i].alternative_id for i in range(len(alternatives))}

        matrices_count = 0
        all_matrices = []
        for e in experts:
            weights_for_expert = [w for w in weights if w.expert_id == e]
            for c in criterias:
                weight = 0
                for w in weights_for_expert:
                    if w.criteria_id == c.criteria_id:
                        scale_id = w.scale_id
                        for s in scales:
                            if s.scale_id == scale_id:
                                weight = s.value
                                break
                        break

                matrix = [[0 for i in range(len(alternatives))] for j in range(len(alternatives))]
                for d in data:
                    if d.expert_id == e and d.criteria_id == c.criteria_id:
                        if d.result == True:
                            matrix[alternative_id_to_matrix_place_map[d.alternative1_id]] \
                                [alternative_id_to_matrix_place_map[d.alternative2_id]] = weight
                            matrix[alternative_id_to_matrix_place_map[d.alternative2_id]] \
                                [alternative_id_to_matrix_place_map[d.alternative1_id]] = 1 / weight
                            matrices_count += 1
                        else:
                            matrix[alternative_id_to_matrix_place_map[d.alternative1_id]] \
                                [alternative_id_to_matrix_place_map[d.alternative2_id]] = 1 / weight
                            matrix[alternative_id_to_matrix_place_map[d.alternative2_id]] \
                                [alternative_id_to_matrix_place_map[d.alternative1_id]] = weight
                            matrices_count += 1
                all_matrices.append(matrix)

        np_matrices = np.array(all_matrices)

        var = crud.get_variables(db, ranking_id)
        ranker = EVM()
        group_method_arg = 'AIJ'
        if var is not None:
            if var.ranking_method == 'EVM':
                ranker = EVM()
            elif var.ranking_method == 'GMM':
                ranker = GMM()
            if var.aggregation_method == 'AIJ':
                group_method_arg = 'AIJ'
            elif var.aggregation_method == 'AIP':
                group_method_arg = 'AIP'

        result = ranker(np_matrices, group_method=group_method_arg)
        result = result.tolist()

        alternatives_with_rank = [(matrix_place_to_alternative_id_map[i], result[i]) for i in range(len(alternatives))]
        print(alternatives_with_rank)

        alternatives_with_rank.sort(key=lambda x: x[1], reverse=True)

        for i in range(len(alternatives_with_rank)):
            crud.update_alternative_rank(db, ranking_id, alternatives_with_rank[i][0], i + 1)

        return "Ranking finished"
