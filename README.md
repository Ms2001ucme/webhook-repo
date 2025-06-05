
# Webhook Receiver – GitHub Event Listener

This repository handles incoming GitHub webhook events from the [`action-repo`](https://github.com/your-username/action-repo) and stores minimal data in MongoDB. It also provides a clean frontend to display recent GitHub activity (Push, Pull Request, Merge).

---

## 📌 Features

- Receives webhooks from GitHub for:
  - Push
  - Pull Request (opened)
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
```

Create a `.env` file (optional) or set Mongo URI in `__init__.py`:

```python
app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookDB"
```

### Run Flask App

```bash
python run.py
```

Visit: `http://localhost:5000/`

---

## 🔗 Setting Up GitHub Webhook

1. Go to your `action-repo` on GitHub
2. Settings → Webhooks → Add webhook
3. Payload URL: `http://your-ip:5000/webhook/receiver`
4. Content type: `application/json`
5. Events to send:
   - Just the push event
   - Pull requests
6. Save

---

## 📂 Project Structure

```
webhook-repo/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   └── webhook/
│       └── routes.py
├── templates/
│   └── index.html
├── run.py
├── requirements.txt
└── README.md
```

---

## ✅ Testing

- Push to `action-repo` or create a PR to trigger webhooks
- Check MongoDB: `db.events.find().pretty()`
- Watch the frontend update in real-time every 15s


---

## 🤝 Contributing

PRs and suggestions are welcome! Open an issue or fork this repo.

---

## 📝 License

This project is licensed for assessment and learning purposes.
