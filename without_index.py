from flask import Blueprint, request, jsonify
import time
from elastic_connection import es
from dummy_data_generator import generate_dummy_data

without_index_bp = Blueprint('without_index', __name__)

INDEX = "skycars"


# POST /without-index/write
@without_index_bp.route('/write', methods=['POST'])
def write_data():
    data = request.get_json()
    seed: int = data.get('seed', 0)

    if not es.indices.exists(index=INDEX):
        es.indices.create(index=INDEX)

    before_count = es.count(index=INDEX)["count"]
    start_time = time.time()

    for _ in range(seed):
        es.index(index=INDEX, body=generate_dummy_data())

    after_count = es.count(index=INDEX)["count"]
    elapsed_time = time.time() - start_time

    return jsonify({
        "before": before_count,
        "after": after_count,
        "elapsed_time_sec": elapsed_time,
        "avg_time_per_record_sec": elapsed_time / seed
    })


# GET /without-index/count
@without_index_bp.route('/count', methods=['GET'])
def count_data():
    count = 0
    if es.indices.exists(index=INDEX):
        count = es.count(index=INDEX)["count"]

    return jsonify({
        'count': count
    })

# GET /without-index/read


@without_index_bp.route('/read', methods=['GET'])
def read_data():
    skycar = request.args.get('skycar')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = {"bool": {"must": []}}

    if skycar:
        query["bool"]["must"].append({"term": {"skycar": int(skycar)}})
    if start_date and end_date:
        query["bool"]["must"].append({
            "range": {
                "created": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })

    if not es.indices.exists(index=INDEX):
        es.indices.create(index=INDEX)

    start_time = time.time()
    result = es.search(index=INDEX, body={"query": query, "size": 20})
    elapsed_time = time.time() - start_time

    count = es.count(index=INDEX)["count"]

    return jsonify({
        "result": [hit["_source"] for hit in result["hits"]["hits"]],
        "limit": 20,
        "elapsed_time_sec": elapsed_time,
        "total_in_db": count
    })


# DELETE /without-index/reset
@without_index_bp.route('/reset', methods=['DELETE'])
def reset():
    # Delete the existing index
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)

    return jsonify({
        "status": "reset successfully"
    })
