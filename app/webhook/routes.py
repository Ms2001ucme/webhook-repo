from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
# This module defines the webhook routes for handling GitHub events.    
@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    event = request.headers.get('X-GitHub-Event')
    timestamp = datetime.utcnow().isoformat()
    author = data.get('pusher', {}).get('name') or data.get('sender', {}).get('login')
    
    doc = {
        "author": author,
        "timestamp": timestamp
    }

    if event == "push":
        doc.update({
            "request_id": data.get('after'),  # commit SHA
            "action": "PUSH",
            "from_branch": None,  # Not applicable
            "to_branch": data.get('ref', '').split('/')[-1],
        })

    elif event == "pull_request":
        pr = data.get("pull_request", {})
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")
        pr_id = pr.get("id")

        if data.get("action") == "opened":
            doc.update({
                "request_id": str(pr_id),
                "action": "PULL_REQUEST",
                "from_branch": from_branch,
                "to_branch": to_branch,
            })

        elif data.get("action") == "closed" and pr.get("merged"):
            doc.update({
                "request_id": str(pr_id),
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch,
            })
        else:
            return jsonify({"message": "Ignored PR event"}), 200

    else:
        return jsonify({"message": "Unhandled event type"}), 200

    mongo.db.events.insert_one(doc)
    return jsonify({"message": "Event stored"}), 200


@webhook.route('/events', methods=["GET"])
def get_events():
    cursor = mongo.db.events.find({}, {"_id": 0}).sort("timestamp", -1)
    return jsonify(list(cursor))

