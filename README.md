## Aadhaar Document & Image Forgery Detection – Full Stack

This project is a full-stack, AI-powered Aadhaar forgery detection lab:

- **Backend**: FastAPI + PyTorch + OpenCV, JWT auth, Convex DB over HTTP.
- **ML**: DenseNet121 + MobileNetV2 ensemble, ELA, ROI detection, QR validation, Grad-CAM, severity scoring and training scripts.
- **Database**: **Convex DB only** – TypeScript backend with queries/mutations.
- **Frontend**: Create React App, Tailwind CSS, Framer Motion, Convex React client.

### 1. Backend (FastAPI)

Location: `backend/`

Install and run:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Configure `.env` (already scaffolded):

- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CONVEX_DEPLOYMENT_URL`, `CONVEX_API_KEY`
- `STORAGE_DIR`, `MODEL_CHECKPOINT_DIR`, `TRAIN_DATA_DIR`

### 2. Convex Backend

Location: `convex/`

Files:

- `schema.ts` – tables: `users`, `uploads`, `predictions`, `models`, `retrainTriggers`.
- `users.ts` – `createUser`, `getUserByEmail`.
- `uploads.ts` – `createUpload`, `getUploadById`, `getUploadsByUser`.
- `predictions.ts` – `createPrediction`, `getPredictionsByUpload`, `getHistoryByUser`.
- `models.ts` – `createModelMetric`, `getModelMetrics`, `triggerRetrain`.

Initialize Convex:

```bash
npx convex dev
```

Point `CONVEX_DEPLOYMENT_URL` and `CONVEX_API_KEY` in `backend/.env` and `REACT_APP_CONVEX_URL` in `frontend/.env` to the Convex deployment.

### 3. Frontend (React + Tailwind + Framer Motion + Convex)

Location: `frontend/`

Install and run:

```bash
cd frontend
npm install
npm start
```

Key structure:

- `src/styles/theme.css` – noir cyber-forensics theme and CSS variables.
- `src/services/api.js` – FastAPI REST client with JWT.
- `src/hooks/useAuth.js` – auth state, login/register/logout.
- `src/pages/` – `LandingPage`, `AuthPage`, `DashboardPage`, `AdminPage`.
- `src/components/` – `SeverityMeter`, `HistoryTimeline` (live Convex history).
- `src/index.js` – wraps `App` with `ConvexProvider`.

Set environment variables (optional) in `frontend/.env`:

- `REACT_APP_API_BASE_URL=http://localhost:8000`
- `REACT_APP_CONVEX_URL=https://YOUR-DEPLOYMENT.convex.cloud`

### 4. ML Training & Checkpoints

Dataset layout (using the root-level `dataset/` folder you added):

```text
dataset/
  train/
    authentic/
    forged/
  val/
    authentic/
    forged/
```

The backend `.env` already points `TRAIN_DATA_DIR=../dataset` so the admin
retrain endpoint will use this folder by default.

To train models manually:

```bash
cd backend
python -m ml.train --data_dir ../dataset --checkpoint_dir ml/checkpoints --epochs 5
```

This writes:

- `ml/checkpoints/densenet121_aadhaar.pt`
- `ml/checkpoints/mobilenetv2_aadhaar.pt`

Convex `models` table can be populated from training runs via `createModelMetric`, and the admin UI reads metrics via `getModelMetrics`.

