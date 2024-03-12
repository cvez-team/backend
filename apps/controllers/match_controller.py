from typing import Dict, List, Tuple, Any, Union
import numpy.typing as npt
from ..providers.vectordb_provider import VectorDatabaseProvider

vector_database = VectorDatabaseProvider(size=768)

def calculate_average_scores(vectors: List[Tuple[str, float]]) -> Dict[str, float]:
    # Tạo một từ điển để lưu trữ trung bình cộng theo ID
    average_scores = {}

    # Lặp qua từng danh sách tuples
    for vector in vectors:
        # Lặp qua từng cặp giá trị trong danh sách
        for id_, score in vector:
            # Nếu ID chưa tồn tại trong từ điển, thêm mới với giá trị là list chứa score
            if id_ not in average_scores:
                average_scores[id_] = [score]
            else:
                # Nếu ID đã tồn tại, thêm score vào list tương ứng
                average_scores[id_].append(score)
    
    # Tạo từ điển mới chứa trung bình cộng của mỗi ID
    average_scores_result = {}
    for id_, scores in average_scores.items():
        # Tính trung bình cộng của các scores
        average_score = sum(scores) / len(scores)
        # Lưu trung bình cộng vào từ điển kết quả
        average_scores_result[id_] = average_score
    
    return average_scores_result

def match_controller(collection_name: str, query_vector: npt.NDArray, limit: int = 10) -> List[Tuple[str, float]]:
    match_result =  vector_database.search(collection_name, query_vector, limit)
    
    # Chuyển đổi match_result thành một list các tuples
    match_tuples = [(item[0], item[1]) for item in match_result]
    
    # Gọi hàm calculate_average_scores với kết quả tìm kiếm và trả về kết quả
    return calculate_average_scores(match_tuples)
