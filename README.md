#  FinSight AI — Financial Intelligence Assistant

A full-stack, production-ready fintech application that analyzes user transactions, detects anomalies, and provides intelligent financial insights using adaptive scoring and user feedback.

---

##  Live Application

-  Frontend (Vercel): https://finsight-ai-swart.vercel.app  
-  Backend API (Render): https://finsight-api-muwe.onrender.com  
-  API Docs: https://finsight-api-muwe.onrender.com/docs  

---

##  Project Overview

FinSight AI simulates a real-world personal finance intelligence system used in fintech applications.

It evaluates financial behavior using:

- Transaction data (income, spending patterns)  
- Rule-based anomaly detection  
- User feedback-driven score adjustments  

The system not only detects unusual activity but also explains *why* it was flagged.

---

##  Key Features

###  Authentication System
- User signup & login  
- User-specific data isolation  

###  Smart Data Ingestion
- Upload bank statements (CSV)  
- Automatic preprocessing & cleaning  
- Intelligent transaction categorization  

###  Anomaly Detection Engine
- Assigns anomaly scores to transactions  
- Detects unusual financial behavior  
- Uses rule-based + behavioral logic  

###  Smart Alerts System
- Flags suspicious transactions  
- Provides explanation for each alert  
- Risk levels:
  - Low  
  - Medium  
  - High  

###  Feedback Learning System
- Users mark transactions as:
  - Normal  
  - Suspicious  
- System dynamically adjusts scores  
- Simulates adaptive financial intelligence  

###  Financial Insights Dashboard
- Income vs Spending analysis  
- Savings rate calculation  
- Financial health score  
- Interactive charts and summaries  

---

##  Tech Stack

### Frontend
- React.js  
- Tailwind CSS  
- Recharts  

### Backend
- FastAPI  
- SQLAlchemy  
- PostgreSQL  

### Data Processing
- Pandas  

### Deployment
- Vercel (Frontend)  
- Render (Backend)  
- GitHub (Version Control)  

---

##  Project Structure

finsight-ai/  
│  
├── frontend/  
│   ├── components/  
│   ├── pages/  
│   └── api/  
│  
├── backend/  
│   ├── main.py  
│   ├── routes.py  
│   ├── models.py  
│   ├── database.py  
│   └── services/  
│  
├── data/  
│   ├── raw/  
│   ├── processed/  
│   └── final/  
│  
├── requirements.txt  
├── package.json  
└── README.md  

---

##  System Architecture

User → React Frontend → FastAPI Backend → Database → Scoring Engine → Response → Dashboard  

---

##  How It Works

1. User logs in  
2. Uploads transaction data (CSV)  
3. Backend:
   - Cleans and categorizes data  
   - Builds financial profile  
   - Runs anomaly detection  
4. Dashboard displays:
   - Alerts  
   - Scores  
   - Insights  
5. User provides feedback  
6. System updates scoring dynamically  

---

## Screenshots


01-login.png
<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/bfb14f29-1448-4f2c-88b4-953de19dc24a" />




02-login-filled.png
<img width="1919" height="885" alt="image" src="https://github.com/user-attachments/assets/2ba2245e-e778-458d-985c-d4422a5f657e" />



03-upload-empty.png
<img width="1919" height="883" alt="image" src="https://github.com/user-attachments/assets/062feda5-02e4-4280-b3d2-536a1de4b0dd" />




04-upload-file-selected.png
<img width="1919" height="875" alt="image" src="https://github.com/user-attachments/assets/8221fd4e-2d72-49f0-afa7-63e5055e10b4" />




05-dashboard-overview.png
<img width="1898" height="761" alt="image" src="https://github.com/user-attachments/assets/c1f692fb-fb93-4c71-9c9b-7d68ab9bf3ea" />




06-spending-insights.png
<img width="1888" height="606" alt="image" src="https://github.com/user-attachments/assets/5ed58215-f467-41d9-969d-bee8deacedc7" />





07-smart-alerts.png
<img width="1898" height="904" alt="image" src="https://github.com/user-attachments/assets/a2620bb6-a13f-4485-8b63-ad1719fc48b2" />




08-anomaly-explanations.png
<img width="1889" height="901" alt="image" src="https://github.com/user-attachments/assets/1549ded6-093c-4541-87b3-080788f675ab" />





09-transactions-table.png
<img width="1893" height="895" alt="image" src="https://github.com/user-attachments/assets/08949603-55ba-4212-87e9-7ff284678996" />











##  API Endpoints

| Endpoint | Method | Description |
|--------|--------|------------|
| /signup | POST | Create new user |
| /login | POST | Authenticate user |
| /upload | POST | Upload CSV data |
| /build-profile | POST | Generate user profile |
| /analyze | POST | Run analysis engine |
| /feedback | POST | Submit feedback |
| /data | GET | Fetch user transactions |

---

##  Example Workflow

Upload CSV → Analyze → View Alerts → Give Feedback → Updated Scores  

---

##  Current Limitations

- Rule-based anomaly detection (not ML yet)  
- No JWT authentication (basic auth system)  

---

##  Future Enhancements

- Machine learning-based anomaly detection  
- Persistent feedback visualization  
- Real-time transaction integration  
- Budget tracking & forecasting  
- Mobile app version  
- Advanced personalization  

---

##  Key Learning Outcomes

- Full-stack development (React + FastAPI)  
- API integration & deployment  
- Database design & user isolation  
- Data processing with Pandas  
- Feedback-driven system design  
- Debugging real-world deployment issues (CORS, state sync)  

---

##  Author

**Preeti Gorial**  
GitHub: https://github.com/Preeti080204  

---

##  Final Note

This project demonstrates an end-to-end financial intelligence system including:

- Data ingestion  
- Processing & analysis  
- Feedback-driven adaptation  
- Full deployment pipeline  

Built with focus on real-world fintech applications.
