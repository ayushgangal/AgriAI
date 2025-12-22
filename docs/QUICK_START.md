# AgriAI: The Digital Greenhouse 🌾🚀

AgriAI is a premium, multi-modal agricultural advisor designed to empower farmers with AI-driven insights. From bioluminescent UI design to real-time bio-matching algorithms, AgriAI bridges the gap between high-tech data science and sustainable farming.

---

## 🛠 Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.11+**
- **Node.js 18+** (Required for React 18 & Spline)
- **WSL2** (Crucial if developing on Windows)
- **Git**

---

## 📥 Installation & Setup

### 1. Clone the Project
```bash
git clone <repository-url>
cd AgriAI_Hackathon

### 2. Backend (FastAPI)
```bash
cd backend

# Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Linux/WSL
# .\venv\Scripts\activate # Windows alternative

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env1 .env
# Important: Open .env and add your OPENAI_API_KEY

# Database Setup
pip install alembic
alembic upgrade head

# Launch Server
uvicorn main:app --reload --port 8000

## Backend live at: http://localhost:8000 | Docs: http://localhost:8000/docs

### 3. Frontend (React+GSAP)
```bash
cd frontend

# Force clean to prevent dependency ghosts
rm -rf node_modules package-lock.json

# Install with legacy peer handling (Required for React 18 compatibility)
npm install --legacy-peer-deps

# Launch Frontend
npm start

## Web App live at: http://localhost:3000

### Troubleshooting
WSL "Invalid Token" Error
If you see invisible character errors in your JS files, run this scrub command to fix Windows/Linux line-ending mismatches:

```bash
find src -name "*.js" -exec sed -i 's/\r//' {} +
"AJV Module Not Found"
If Webpack crashes on start, force-link the validator:

```bash
npm install ajv --save-dev
Black Screen / Invalid Hook Call
Ensure you only have one React instance running:

```bash
npm ls react
# If versions are mismatched, run:
npm dedupe