from flask import Blueprint, request, jsonify
import time
from elastic_connection import es
from dummy_data_generator import generate_dummy_data


with_index_bp = Blueprint('with_index', __name__)

INDEX = "indexed-skycars"


@with_index_bp.route('/write', methods=['POST'])  # POST /with-index/write
def write_data():
    if not es.indices.exists(index=INDEX):
        reset()

    data = request.get_json()
    seed: int = data.get('seed', 0)

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


# GET /with-index/read
@with_index_bp.route('/read', methods=['GET'])
def read_data():
    skycar = request.args.get('skycar')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 20, type=int)

    query = {"query": {"bool": {"must": []}}}

    if skycar:
        query["query"]["bool"]["must"].append({"term": {"skycar": int(skycar)}})
    if start_date and end_date:
        query["query"]["bool"]["must"].append({
            "range": {
                "created": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })

    # If limit is -1, do not set a size limit
    if limit != -1:
        query["size"] = limit

    start_time = time.time()

    result = []
    if es.indices.exists(index=INDEX):
        result = es.search(index=INDEX, body=query)

    elapsed_time = time.time() - start_time

    count = es.count(index=INDEX)["count"]
    
    matched = [hit["_source"] for hit in result["hits"]["hits"]]
    return jsonify({
        "result": matched,
        "page_size": len(matched),
        "limit": limit,
        "elapsed_time_sec": elapsed_time,
        "total_in_db": count
    })


# GET /with-index/count
@with_index_bp.route('/count', methods=['GET'])
def count_data():
    count = 0
    if es.indices.exists(index=INDEX):
        count = es.count(index=INDEX)["count"]

    return jsonify({
        'count': count
    })


# DELETE /with-index/reset
@with_index_bp.route('/reset', methods=['DELETE'])
def reset():
    # Delete the existing index
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)

    # Create a new index with mappings
    mappings = {
        "mappings": {
            "properties": {
                "skycarId": {"type": "integer"},
                "message": {"type": "text"},
                "created": {"type": "date"}
            }
        }
    }
    es.indices.create(index=INDEX, body=mappings)

    return jsonify({
        "status": "reset successfully"
    })
