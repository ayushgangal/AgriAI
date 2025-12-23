# AgriAI - AI-Powered Agricultural Advisor

## Overview
AgriAI is a comprehensive AI-powered agricultural advisor designed to help farmers and agricultural stakeholders make informed decisions. The system addresses real-world challenges including low digital access, multilingual support, and the need for reliable, explainable AI solutions.

## Key Features

### 🌱 Multi-Modal Query Support
- Natural language processing for local, colloquial queries
- Voice input/output for low-literacy users
- Image analysis for crop disease identification
- Multi-language support (Hindi, English, and regional languages)

### 📊 Comprehensive Data Integration
- Weather data and forecasting
- Soil health information
- Crop cycle recommendations
- Market price analysis
- Government policy updates
- Financial credit information

### 🎯 Core Capabilities
- **Irrigation Timing**: Optimal irrigation scheduling based on weather and soil conditions
- **Crop Selection**: Weather-adaptive seed variety recommendations
- **Yield Protection**: Early warning systems for adverse weather conditions
- **Market Intelligence**: Price trends and optimal selling timing
- **Financial Guidance**: Credit availability and government subsidy information

### 🔧 Technical Architecture
- **Frontend**: React-based responsive web application
- **Backend**: FastAPI with async processing
- **AI/ML**: Multi-modal LLM integration with grounding mechanisms
- **Data Sources**: Public datasets with proper attribution
- **Offline Capability**: Core features available without internet

## Project Structure
```
AgriAI_Hackathon/
├── frontend/                 # React web application
├── backend/                  # FastAPI backend
├── ml_models/               # AI/ML models and data processing
├── data/                    # Public datasets and processed data
├── docs/                    # Documentation
└── deployment/              # Deployment configurations
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd AgriAI_Hackathon

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
pip install "bcrypt==4.0.1"
uvicorn main:app --reload

# Frontend setup
cd ../frontend
npm install
npm install lucide-react
npm install react-markdown
npm start
```

## Data Sources
This project uses publicly available datasets with proper attribution:
- Indian Meteorological Department (IMD) weather data
- Ministry of Agriculture crop statistics
- NABARD financial data
- State agricultural department datasets

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.