# Webhook Receiver – GitHub Event Listener

This repository handles incoming GitHub webhook events from the [`action-repo`]and stores minimal data in MongoDB. It also provides a clean frontend to display recent GitHub activity (Push, Pull Request).

---

## 📌 Features

- Receives webhooks from GitHub for:
  - Push
  - Pull Request (opened)
  - Merge (closed + merged)
- Stores event data in MongoDB
- Frontend UI auto-refreshes every 15 seconds to show latest actions

---

## 🛠️ Tech Stack

- Python + Flask
- MongoDB (via `flask-pymongo`)
- HTML + JavaScript (vanilla)
- GitHub Webhooks

---

## 🧾 MongoDB Schema

Each event is stored with the following schema:

| Field         | Type            | Description                                     |
|---------------|------------------|-------------------------------------------------|
| `_id`         | ObjectID         | MongoDB auto-generated ID                       |
| `request_id`  | string           | Git commit hash or PR ID                        |
| `author`      | string           | GitHub username of the contributor              |
| `action`      | string           | One of: `PUSH`, `PULL_REQUEST`, `MERGE`         |
| `from_branch` | string or null   | Source branch (for PRs and merges)              |
| `to_branch`   | string           | Target branch                                   |
| `timestamp`   | string (datetime)| Time of the event in UTC                        |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB running locally (or MongoDB Atlas)
- GitHub account

### Installation

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

### Setting Up GitHub Webhook
1.Go to your action-repo on GitHub

2.Settings → Webhooks → Add webhook

3.Payload URL: http://your-ip:5000/webhook/receiver

4.Content type: application/json

4.Events to send:

5.Just the push event

6.Pull requests

7.Save
