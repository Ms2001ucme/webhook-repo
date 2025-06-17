from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime,timedelta
from flask import current_app as app
# This module defines the webhook routes for handling GitHub events.

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
# This module defines the webhook routes for handling GitHub events.    
@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    Receives GitHub webhook events (push, pull request, merge),
    extracts relevant data, and stores it in MongoDB.

    Expected Header:
        X-GitHub-Event: Type of GitHub event (push, pull_request)

    Returns:
        JSON response with status message and HTTP status code
    """
    try:
        data = request.json
        event = request.headers.get('X-GitHub-Event')
        timestamp = datetime.now() 
        author = data.get('pusher', {}).get('name') or data.get('sender', {}).get('login')

        app.logger.info(f"Received event: {event} by {author}")
        
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
            app.logger.info(f"Processed PUSH event: {doc}")

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
                app.logger.info(f"Processed PR OPENED event: {doc}")

            elif data.get("action") == "closed" and pr.get("merged"):
                doc.update({
                    "request_id": str(pr_id),
                    "action": "MERGE",
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                })
                app.logger.info(f"Processed MERGE event: {doc}")
            else:
                app.logger.info("Ignored non-merged PR close event.")
                return jsonify({"message": "Ignored PR event"}), 200
        else:
            app.logger.warning(f"Unhandled GitHub event type: {event}")
            return jsonify({"message": "Unhandled event type"}), 200

        mongo.db.events.insert_one(doc)
        return jsonify({"message": "Event stored"}), 200

    except Exception as e:
        app.logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@webhook.route('/events', methods=["GET"])
def get_events():
    """
    Fetches and returns all GitHub webhook events
    received in the last 15 seconds from MongoDB.

    Returns:
        JSON list of event objects sorted by timestamp (most recent first)
    """
    try:
        fifteen_seconds_ago = datetime.now() - timedelta(seconds=15)
        cursor = mongo.db.events.find({"timestamp":{"$gte": fifteen_seconds_ago}}, {"_id": 0}).sort("timestamp", -1)
        
        events = []
        for event in cursor:
            if isinstance(event.get("timestamp"), datetime):
                event["timestamp"] = event["timestamp"].isoformat()
            events.append(event)

        return jsonify(events)

    except Exception as e:
        app.logger.error(f"Error retrieving events: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500



