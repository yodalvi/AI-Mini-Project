# QuickBite ETA 🛵

A food-delivery **ETA predictor** built with scikit-learn + FastAPI, fully dockerized.
Part of the *Dockerize Everything: ML → LLM → Agents* masterclass.

> **Predicts:** how many minutes until a food order arrives, based on distance,
> restaurant prep time, rider availability, and whether it's raining.

---

## 📁 What's in this folder

| File | Purpose |
|---|---|
| `train.py` | Generates synthetic delivery data and trains a RandomForest → saves `eta_model.pkl` |
| `app.py` | FastAPI service that loads the model and exposes `/predict` |
| `requirements.txt` | Pinned Python dependencies (the "shopping list") |
| `Dockerfile` | The recipe — how to build the container image |
| `.dockerignore` | Files that should NOT go into the image |
| `README.md` | This file |

1. **Docker Desktop** installed and running.
2.  Verify it works: docker --version
3.  ## 🚀 Step-by-step: run this project

### Step 1 — Extract the folder
### Step 2 — Open it in VS Code
### Step 3 — Make sure Docker Desktop is running
Check for the whale 🐳 icon in your menu bar. If it's animating, wait until it's steady.
### Step 4 — Build the image
Open the VS Code integrated terminal with `` Ctrl + ` `` and run:
```bash
docker build -t quickbite-eta:v1 .
```
The first build takes **2–3 minutes** (it pulls the Python base image and installs
scikit-learn). Watch the output — you'll see `Model saved: eta_model.pkl ✅` scroll by,
because the model is trained **inside** the image at build time.

Confirm the image exists:
```bash
docker images
```
### Step 5 — Run the container
```bash
docker run -d -p 8000:8000 --name eta-service quickbite-eta:v1
Check it's alive:
```bash
docker ps
```
### Step 6 — Test the API
**Option A — curl:**
### Batch Prediction

```bash
curl -X POST "http://localhost:8000/batch_predict" \
-H "Content-Type: application/json" \
-d '[
  {
    "distance_km": 4.5,
    "prep_time_min": 15,
    "rider_available": 1,
    "is_raining": 1
  },
  {
    "distance_km": 2,
    "prep_time_min": 10,
    "rider_available": 1,
    "is_raining": 0
  },
  {
    "distance_km": 8,
    "prep_time_min": 20,
    "rider_available": 0,
    "is_raining": 1
  }
]'
```

**Option B — Swagger UI (best for live demos):**
Open **http://localhost:8000/docs** in your browser, expand `POST /batch_predict`

### Step 7 — Explore the running container (optional, great demo moment)
```bash
docker logs -f eta-service          # watch live logs (Ctrl+C to exit)
docker exec -it eta-service bash    # step INSIDE the container
  ls                                # you'll see app.py, eta_model.pkl, etc.
  cat app.py
  exit
```
### Step 8 — Clean up
```bash
docker stop eta-service
docker rm eta-service
docker rmi quickbite-eta:v1         # optional: also delete the image
```
