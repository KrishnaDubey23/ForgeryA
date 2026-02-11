## Backend – Aadhaar Forgery Detection

This FastAPI backend provides JWT-secured endpoints for uploading Aadhaar images, running an AI-powered forgery pipeline (ELA, ROI detection, QR validation, DenseNet121 + MobileNetV2 ensemble with Grad-CAM), and persisting metadata and predictions to **Convex DB** over its HTTP API.

### Setup

1. **Create and activate a virtualenv** (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment in `.env` (already created):

- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CONVEX_DEPLOYMENT_URL`, `CONVEX_API_KEY`
- `STORAGE_DIR` (default `storage/uploads`)
- `MODEL_CHECKPOINT_DIR` (default `ml/checkpoints`)
- `TRAIN_DATA_DIR` (for retraining; default `data`)

4. Run the API:

```bash
uvicorn main:app --reload
```

### Key Endpoints

- `POST /auth/register` – register user (Convex-backed) and receive JWT.
- `POST /auth/login` – login and receive JWT.
- `GET /auth/me` – current user info.
- `POST /uploads/` – upload Aadhaar image (JWT required).
- `POST /predictions/` – run full forgery analysis for an upload (JWT required).
- `GET /admin/metrics` – model metrics from Convex (admin only).
- `POST /admin/retrain` – trigger local retraining job + Convex audit event (admin only).

### Dataset & Training

Expected dataset structure for training:

```text
data/
  train/
    authentic/
    forged/
  val/
    authentic/
    forged/
```

Run training:

```bash
python -m ml.train --data_dir data --checkpoint_dir ml/checkpoints --epochs 5
```

