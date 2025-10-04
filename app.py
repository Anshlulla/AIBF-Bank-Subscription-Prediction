import pandas as pd
import streamlit as st
import yaml
from sklearn.preprocessing import StandardScaler
from src.utils.utils import load_pickle
import streamlit as st
import gdown

#MODEL_PATH = "artifacts/model_trainer/model/model.pkl"
MODEL_PATH = "https://drive.google.com/uc?id=1NeeDjcgRLvXGPAYDZG_L6EtX4976J66Q"

# --- Styled title with markdown ---
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50; font-size: 48px;'>
        🏦 Bank Subscription Prediction
    </h1>
    <p style='text-align: center; color: #555; font-size: 18px;'>
        Predict whether a client will subscribe to a term deposit
    </p>
    """,
    unsafe_allow_html=True
)

placeholder = st.empty()
placeholder.markdown(
    """
    <div style='text-align:center;'>
        <h2>⏳ Initializing Application...</h2>
        <p>Downloading model. Please wait a few moments.</p>
    </div>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def load_model():
    url = MODEL_PATH
    output = "model.pkl"
    gdown.download(url, output, quiet=False)
    model = load_pickle(output)
    return model

# --- Load Model ---
try:
    model = load_model()
    placeholder.empty()  # Remove loading message once done
    st.success("✅ Model loaded successfully!")
except Exception as e:
    placeholder.empty()
    st.error(f"Error loading model: {e}")
    st.stop()

# --- Model features (from training pipeline) ---
MODEL_FEATURES = [
    'age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous',
    'job_blue-collar','job_entrepreneur','job_housemaid','job_management',
    'job_retired','job_self-employed','job_services','job_student','job_technician',
    'job_unemployed','job_unknown','marital_married','marital_single',
    'education_secondary','education_tertiary','education_unknown',
    'default_yes','housing_yes','loan_yes','contact_telephone','contact_unknown',
    'month_aug','month_dec','month_feb','month_jan','month_jul','month_jun',
    'month_mar','month_may','month_nov','month_oct','month_sep',
    'poutcome_other','poutcome_success','poutcome_unknown'
]

def get_schema_columns(schema_path="schema.yaml"):
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)
    return list(schema["columns"].keys())

def preprocess_input(df):
    # One-hot encode categorical columns (except target)
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if "y" in categorical_cols:
        categorical_cols.remove("y")
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    # Map target if present
    if "y" in df.columns:
        df["y"] = df["y"].map({"no": 0, "yes": 1})
    # Convert all columns to int where possible
    df = df.apply(lambda x: x.astype(int) if x.dtype == "bool" or x.dtype == "object" else x)
    # Add missing columns as zeros
    for col in MODEL_FEATURES:
        if col not in df.columns:
            df[col] = 0
    # Reorder columns
    df = df[MODEL_FEATURES]
    # Scale numeric columns
    num_cols = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df

# --- Step 1: Input method ---
input_method = st.radio("Select Input Method", ["Upload Excel", "Manual Input"])
df = None

# --- Step 2a: Excel Upload ---
if input_method == "Upload Excel":
    st.markdown("#### Upload your Excel or CSV file below")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            schema_cols = get_schema_columns()
            if set(df.columns) != set(schema_cols):
                st.warning("Uploaded file columns do not match the expected schema.")
                st.info(f"Expected columns ({len(schema_cols)}): {', '.join(schema_cols)}")
                df = None
            else:
                st.success("File uploaded successfully!")
                df = df.drop("y", axis=1)
                st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")

# --- Step 2b: Manual Input ---
elif input_method == "Manual Input":
    num_features = {
        "age": st.slider("Age:", 18, 95, 50),
        "balance": st.slider("Balance:", -8019, 81204, 0),
        "day": st.slider("Day:", 1, 31, 5),
        "duration": st.slider("Duration:", 0, 4918, 20),
        "campaign": st.slider("Campaign:", 1, 63, 1),
        "pdays": st.slider("Pdays:", -1, 871, 5),
        "previous": st.slider("Previous:", 0, 37, 1)
    }

    job = st.selectbox("Job", [
        "blue-collar", "entrepreneur", "housemaid", "management",
        "retired", "self-employed", "services", "student",
        "technician", "unemployed", "unknown"
    ])
    marital = st.selectbox("Marital Status", ["married", "single", "divorced"])
    education = st.selectbox("Education", ["primary", "secondary", "tertiary", "unknown"])
    contact = st.selectbox("Contact", ["telephone", "unknown", "cellular"])
    month = st.selectbox("Month", [
        "jan","feb","mar","apr","may","jun","jul",
        "aug","sep","oct","nov","dec"
    ])
    poutcome = st.selectbox("Poutcome", ["other", "success", "unknown"])

    default_yes = st.checkbox("Default")
    housing_yes = st.checkbox("Housing Loan")
    loan_yes = st.checkbox("Personal Loan")

    # Build a single-row DataFrame for manual input
    manual_dict = {**num_features,
        "job": job,
        "marital": marital,
        "education": education,
        "contact": contact,
        "month": month,
        "poutcome": poutcome,
        "default_yes": int(default_yes),
        "housing_yes": int(housing_yes),
        "loan_yes": int(loan_yes)
    }
    df = pd.DataFrame([manual_dict])
    st.dataframe(df)

# --- Step 3: Preprocess and Predict ---
if df is not None:
    df_proc = preprocess_input(df)
    if st.button("Predict"):
        try:
            predictions = model.predict(df_proc)
            df['Prediction'] = ["Subscribed" if p == 1 else "Not Subscribed" for p in predictions]
            st.header("Predictions:")
            #df = df.drop("y", axis=1)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Prediction error: {e}")