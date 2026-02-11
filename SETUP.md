# ForgeryA - Setup & Installation Guide

After cloning the repository, run these commands to set up the complete project.

## Prerequisites
- Python 3.9+
- Node.js 16+
- pip (Python package manager)
- npm (Node package manager)

---

## 1. Backend Setup

### Create Python Virtual Environment
```bash
cd backend
python -m venv .venv
```

**Activate virtual environment:**
- On Windows (PowerShell):
  ```bash
  .\.venv\Scripts\Activate.ps1
  ```
- On Windows (Command Prompt):
  ```bash
  .\.venv\Scripts\activate.bat
  ```
- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Verify Backend Installation
```bash
python -c "import fastapi; import torch; print('✓ Backend dependencies OK')"
```

---

## 2. Frontend Setup

### Install Node Dependencies
```bash
cd frontend
npm install
```

### Verify Frontend Installation
```bash
npm list react react-dom
```

---

## 3. Environment Configuration

### Backend `.env` Setup
The `.env` file is already included with default values:
```bash
cd backend
cat .env
```

**Required variables (already set):**
- `CONVEX_URL` - Your Convex database URL
- `SECRET_KEY` - JWT secret (change in production!)
- `CORS_ORIGINS` - CORS allowed origins

**To use your own Convex backend:**
1. Create a Convex account at https://www.convex.dev
2. Update `CONVEX_URL` in `backend/.env`
3. Run `npx convex deploy` in the `convex/` directory

---

## 4. Dataset Setup (Optional)

The dataset is excluded from Git. Download from Roboflow:

### Option A: Using Your Own Aadhaar Dataset
1. Visit https://roboflow.com
2. Create/use your forgery detection dataset
3. Download in YOLO format
4. Extract to `dataset/` folder

### Option B: Direct File Structure
```
dataset/
├── data.yaml
├── test/
│   ├── images/
│   └── labels/
├── train/
│   ├── images/
│   └── labels/
└── valid/
    ├── images/
    └── labels/
```

---

## 5. Start the Application

### Terminal 1: Start Backend
```bash
cd backend
.\.venv\Scripts\python main.py
```
Backend runs on `http://localhost:8000`

### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```
Frontend runs on `http://localhost:3000`

### Terminal 3: Convex (Optional - for real database)
```bash
cd convex
npx convex dev
```

---

## 6. Verify Installation

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### Check Available Endpoints
```bash
curl http://localhost:8000/docs
```

### Test Authentication
```bash
curl -X POST http://localhost:8000/auth/demo
```

---

## Complete Setup One-Liner (Windows PowerShell)

```powershell
# Backend
cd backend; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; cd ..

# Frontend
cd frontend; npm install; cd ..

# Ready to start!
echo "Setup complete. Run 'cd backend && .\.venv\Scripts\python main.py' in one terminal"
echo "and 'cd frontend && npm start' in another terminal"
```

---

## Complete Setup One-Liner (macOS/Linux)

```bash
# Backend
cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cd ..

# Frontend
cd frontend && npm install && cd ..

# Ready to start!
echo "Setup complete. Run 'cd backend && python main.py' in one terminal"
echo "and 'cd frontend && npm start' in another terminal"
```

---

## Troubleshooting

### Python Package Installation Fails
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then retry requirements
pip install -r requirements.txt
```

### Frontend Won't Start
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Backend Port Already in Use
```bash
# Kill existing process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Convex Connection Issues
```bash
# Run convex dev in the convex directory
cd convex
npx convex dev

# Or update CONVEX_URL in backend/.env to your deployment URL
```

---

## Features Ready to Test

✅ **Demo Authentication** - No password required  
✅ **Image Upload** - Upload Aadhaar documents  
✅ **Mock ML Inference** - Realistic forgery predictions (no training required)  
✅ **Heatmap Visualization** - See tampered regions  
✅ **Admin Dashboard** - Review predictions  

---

## Next Steps

1. **Train Real Models** (Optional)
   ```bash
   cd backend/ml
   python train.py
   ```

2. **Deploy to Production**
   - Update `SECRET_KEY` in `.env`
   - Deploy backend: `python main.py` on your server
   - Deploy frontend: `npm run build` then serve `build/` folder
   - Configure Convex production deployment

3. **Integrate Real Aadhaar Data**
   - Replace mock inference with trained models from `ml/inference.py`
   - Dataset will use models automatically when available

---

**Questions?** Check individual README files:
- `backend/README.md` - Backend details
- `frontend/README.md` - Frontend details  
- `convex/README.md` - Database details
