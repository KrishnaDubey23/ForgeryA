# Quick Setup Reference

## TL;DR - Get Running in 5 Minutes

### Windows (PowerShell)
```powershell
# 1. Backend setup
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Frontend setup (new terminal)
cd frontend
npm install

# 3. Start backend (terminal 1)
cd backend
.\.venv\Scripts\python main.py
# → http://localhost:8000

# 4. Start frontend (terminal 2)
cd frontend
npm start
# → http://localhost:3000
```

### macOS/Linux
```bash
# 1. Backend setup
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Frontend setup (new terminal)
cd frontend
npm install

# 3. Start backend (terminal 1)
cd backend && source .venv/bin/activate && python main.py
# → http://localhost:8000

# 4. Start frontend (terminal 2)
cd frontend && npm start
# → http://localhost:3000
```

---

## Or Use Auto-Setup Scripts

**Windows:**
```powershell
.\setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

---

## What Gets Installed

| Component | Command | Size |
|-----------|---------|------|
| Python deps | `pip install -r backend/requirements.txt` | ~500MB |
| Frontend deps | `npm install` | ~300MB |
| **Total** | | **~800MB** |

---

## Verify It Works

```bash
# Backend health
curl http://localhost:8000/health

# Get demo token
curl -X POST http://localhost:8000/auth/demo

# View API docs
open http://localhost:8000/docs
```

---

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| Python not found | Install Python 3.9+ from python.org |
| `pip install` fails | Run `python -m pip install --upgrade pip` first |
| Port 8000 in use | Kill: `lsof -i :8000 \| kill -9` (macOS) or use different PORT |
| npm install fails | Run `npm cache clean --force` then retry |
| venv activation fails | Use full path: `.\.venv\Scripts\python` (Windows) |

---

## What's Ready to Use

✅ Demo login (no password)  
✅ Image upload  
✅ Mock ML predictions  
✅ Admin dashboard  
✅ Heatmap visualization  

❌ Dataset (download from Roboflow + extract to `dataset/`)  
❌ Real trained models (optional - use `backend/ml/train.py`)  

---

For detailed setup guide, see **SETUP.md**
