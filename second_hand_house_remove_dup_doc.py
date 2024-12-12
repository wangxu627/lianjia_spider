from itertools import chain
from pymongo import MongoClient

def post_mongodb_handler():
    uri = 'mongodb://router.wxioi.fun:27018/'
    username = 'admin'
    password = 'Wx**8962789620'
    client = MongoClient(uri, username=username, password=password)

    db = client.get_database("second_hand_house")
    col = db.get_collection("blocks")

    pipeline = [
        {
            "$project": {
                "day": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at"
                    }
                },
                "lj_action_housedel_id": 1,
                "_id": 1,
                "other_fields": "$$ROOT",
            }
        },
        {
            "$group": {
                "_id": {
                    "day": "$day",
                    "lj_action_housedel_id": "$lj_action_housedel_id"
                },
                "docs_id": {
                    "$push": "$_id"
                }
            }
        },
        {
            "$match": {
                "docs_id.1": {
                    "$exists": True
                }
            }
        },
        {
            "$project": {
                "first_doc": {
                    "$arrayElemAt": [
                        "$docs_id",
                        0
                    ]
                },
                "remaining_docs": {
                    "$slice": [
                        "$docs_id",
                        1,
                        {
                            "$size": "$docs_id"
                        }
                    ]
                }
            }
        },
        {
        "$unset": "first_doc"
        }
    ]
    results = col.aggregate(pipeline)
    flattened_values = list(chain.from_iterable(record["remaining_docs"] for record in results))
    print(flattened_values)
    result = col.delete_many({
        "_id": { "$in": flattened_values }
    })
    print(f"Deleted {result.deleted_count} documents.")


if __name__ == '__main__':
    post_mongodb_handler()