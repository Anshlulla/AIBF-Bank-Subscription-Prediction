# Bank Subscription Prediction AIBF Project

## 📋 Project Overview

This project is an end-to-end MLOps pipeline for predicting whether a bank client will subscribe to a term deposit, based on their demographic and historical banking data. The pipeline is modular, reproducible, and production-ready, leveraging tools like DVC for data and pipeline versioning, Docker for containerization, and Streamlit for interactive model inference.

You can test it out at: [streamlit deployment](https://ai-bank-subscription-prediction.streamlit.app/)


Find the report at: [`Project Report`](CA2_22070126013.pdf)

---

## 📁 Project Structure

```
├── data/
│   └── bank_subscription.xlsx
├── artifacts/
│   └── ... (pipeline outputs)
├── src/
│   ├── components/
│   ├── config/
│   ├── constants/
│   ├── entity/
│   ├── logging/
│   ├── pipeline/
│   └── utils/
├── schema.yaml
├── dvc.yaml
├── requirements.txt
├── Dockerfile
├── app.py
├── main.py
```

---

## 📋Methodology Diagram
<img width="759" height="564" alt="image" src="https://github.com/user-attachments/assets/4d7d01bb-8160-4dbd-93c6-987e88058ba4" />

---

## 📊 Dataset Description

- **Source:** `data/bank_subscription.xlsx`
- **Features:**
  - **Numerical:** `age`, `balance`, `day`, `duration`, `campaign`, `pdays`, `previous`
  - **Categorical:** `job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `poutcome`
  - **Target:** `y` (yes/no - whether the client subscribed to a term deposit)
- **Schema:** See [`schema.yaml`](schema.yaml) for column names and types.

---

## 🏗️ Pipeline Stages

### 1. Data Ingestion
- Reads the raw dataset from `data/bank_subscription.xlsx`.
- Saves a clean CSV copy.

### 2. Data Transformation
- Performs one-hot encoding on categorical columns.
- Normalizes numerical columns using `StandardScaler`.
- Splits the data into train and test sets.
- Saves processed data.

### 3. Model Training
- Uses a `RandomForestClassifier`.
- Handles class imbalance with SMOTE oversampling.
- Trains the model on the processed training data.
- Saves the trained model and SMOTE object.

### 4. Model Evaluation
- Evaluates the trained model on the test set.
- Computes metrics like accuracy, precision, recall, F1-score.
- Saves evaluation metrics in a JSON format.

---

## ⚙️ DVC Pipeline Steps

1. **Initialize DVC (once):**
   ```bash
   dvc init
   ```

2. **Run the pipeline:**
   ```bash
   dvc repro
   ```

3. **Track data and models:**
   ```bash
   dvc add data/bank_subscription.xlsx
   dvc add artifacts/model_trainer/model/model.pkl
   ```

4. **Push data and models to remote (optional):**
   ```bash
   dvc remote add -d myremote <remote-url>
   dvc push
   ```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Anshlulla/AIBF-Bank-Subscription-Prediction
cd AIBF-Bank-Subscription-Prediction
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install dvc
```

### 3. Run the Pipeline

```bash
dvc repro
```

---

## 🌐 Streamlit App

The project includes a Streamlit app for interactive predictions:
You can test it out at [streamlit deployment](https://ai-bank-subscription-prediction.streamlit.app/)

- **Features:**
  - Upload Excel/CSV files or manually input client data.
  - Get instant predictions on whether a client will subscribe.
  - Schema validation for uploaded files.

**To launch the app:**
```bash
streamlit run app.py
```

---

## 🐳 Docker Support

The project includes a `Dockerfile` for easy containerization and deployment.

**Build the Docker image:**
```bash
docker build -t anshlulla/aibf-project:latest .
```

**Run the container:**
```bash
docker run --rm -p 8501:8501 aibf-project:latest
```

## 📝 Notes

- The pipeline is fully modular and can be extended or modified for other tabular classification tasks.
- All experiment artifacts and data versions are tracked with DVC for reproducibility.
- The Streamlit app provides an interactive interface for predictions using the trained model.
- Docker support ensures consistent deployment across environments.

---



