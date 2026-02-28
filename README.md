# Bank Risk Early Warning Engine

**Real-Time News + Time-Series ML Risk Intelligence for US Regional Banks**

## Overview

This project is a real-time bank risk early-warning system designed to detect emerging liquidity stress, drawdown risk, and systemic pressure signals using:

* Automated financial news ingestion
* Sentiment analysis
* Market-aligned time-series feature engineering
* Bank-specific ML models trained on large-scale historical data
* Structured risk reasoning via a small language model

Unlike traditional models that rely purely on historical price signals, this engine integrates **live news flow with market data** to generate forward-looking risk assessments suitable for real-time decision-making.

This system was built over two months of focused development and model training.

---

## Banks Covered

The engine currently monitors five US regional banks:

* AMAL
* AMTB
* ALRS
* ABCB
* ACNB

Each bank has its own trained time-series model suite.

Total trained time-series models: **15**
(3 models per bank × 5 banks)

---

## System Architecture

### 1. Automated News Ingestion (`main.py`)

`main.py` runs as a scheduled workflow and performs the following:

* Executes daily at **10:00 AM**
* Retrieves financial news for the five monitored banks
* Uses the **Vantage API (free tier)** for news retrieval
* Stores processed news into **Firebase**

This ensures a continuously updated news pipeline aligned with market activity.

This is not a static dataset pipeline — it is an active ingestion workflow.

---

### 2. Risk Engine Backend (`evaluator.py`)

`evaluator.py` is the main backend service (hosted via Render).

When a user selects a bank, the system executes the following pipeline:

#### Step 1 — Input

User provides:

* `bank_name`

#### Step 2 — News Retrieval

* Fetches relevant stored news from Firebase
* Aligns news with publication timestamps

#### Step 3 — Market Data Retrieval

* Retrieves historical stock prices using Yahoo Finance
* Aligns stock price data with news dates

#### Step 4 — Sentiment Computation

* Computes sentiment scores for retrieved news
* Generates structured sentiment features

#### Step 5 — Feature Engineering

* Merges sentiment signals with stock data
* Computes time-series features required for prediction

  * Volatility
  * Drawdowns
  * Volume anomalies
  * Trend dynamics
  * Price gaps
  * Liquidity-aligned indicators

#### Step 6 — Model Inference

Each bank folder contains:

* Liquidity prediction model
* Stress prediction model
* Drawdown prediction model

All models are:

* Trained on 200,000+ rows of historical bank stock data
* Derived from the FNSpid dataset
* Source dataset: `sabareesh888/fnspid` on Hugging Face

Models are stored as binary `.pkl` files.

#### Step 7 — Risk Scoring

Model outputs are combined into a structured risk score.

#### Step 8 — Structured Risk Explanation

The final risk result is passed through:

`meta-llama/Llama-3.2-3B-Instruct`

This small language model is used strictly for:

* Structured explanation
* Financial reasoning articulation
* Clear decision-ready output formatting

It does not perform prediction.
It interprets model outputs and produces human-readable analysis.

---

## Repository Structure

```
.
├── .github/workflows/        # Scheduled ingestion workflow
├── AMAL_corporation/
├── AMTB_corporation/
├── ALRS_corporation/
├── ABCB_corporation/
├── ACNB_corporation/
│   ├── liquidity_model.pkl
│   ├── stress_model.pkl
│   └── drawdown_model.pkl
├── main.py                   # Automated news ingestion
├── evaluator.py              # Core risk engine backend
├── requirements.txt
└── Procfile                  # Uvicorn deployment config
```

---

## Key Design Philosophy

This is not a price prediction engine.

This is a **risk state detection system** built to answer:

* Is liquidity stress emerging?
* Is downside acceleration increasing?
* Is systemic risk building?
* Does current news amplify or reduce structural risk?

The system integrates:

* News signals (current information)
* Market microstructure
* Bank-specific historical risk patterns
* Model-based inference
* Structured reasoning

---

## Deployment

Backend:

* Hosted via Render
* Served using Uvicorn

News ingestion:

* GitHub Actions scheduled workflow
* Runs daily at 10:00 AM

Database:

* Firebase (news storage layer)

---

## Data Source

Time-series model training data:

* FNSpid Dataset
* Hugging Face Dataset: `sabareesh888/fnspid`

Models trained using:

* Statsmodels
* Scikit-learn

---

## Why This Is Different

Traditional financial ML systems:

* Rely only on historical data
* Ignore live information flow
* Produce static probability outputs

This engine:

* Continuously ingests real news
* Aligns sentiment with market reaction
* Uses bank-specific models
* Produces interpretable risk reasoning
* Designed for real-time operational decisions

It bridges quantitative modeling and qualitative information flow.

---

## Future Improvements

* Intraday ingestion frequency
* Liquidity gap modeling using balance sheet proxies
* Cross-bank contagion detection
* Macro overlay integration
* Volatility regime detection

---

Here is the refined **Installation & Access** section, rewritten clearly and professionally to reflect that the system is already hosted.

You can replace your existing Installation section with this:

---

## Deployment & Access

The Bank Risk Early Warning Engine is already deployed and live.

Hosted backend endpoint:
[https://news-automation-jv0f.onrender.com](https://news-automation-jv0f.onrender.com)

Access is restricted and available only with permission.

This is a controlled research deployment and not a public API.

---

## Running Locally (Development / Authorized Use)

If you have been granted access and want to run the backend locally:

### 1. Clone the Repository

```bash
git clone https://github.com/BUVI-2006/bank_risk_engine_backend.git
cd evaluator.py
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend

```bash
uvicorn evaluator:app --reload
```

The `--reload` flag enables live reloading during development.

This allows you to:

* Trigger real-time risk evaluations
* Retrieve updated news-aligned predictions
* Inspect full pipeline outputs locally

---

## Author

Built and architected by Buvanesh Pulugarajan . 

This project represents two months of focused research and implementation in real time financial risk intelligence systems.

---

