import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# PAGE CONFIGURATION


st.set_page_config(
    page_title="Diabetes Detection System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# CUSTOM CSS
# IMPORTANT: Streamlit widgets are NOT placed inside raw HTML divs.
# This prevents HTML/code from appearing on the page.


st.markdown(
    """
<style>
/* -------------------- GLOBAL -------------------- */
.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(112, 75, 255, .09), transparent 28%),
        radial-gradient(circle at 94% 12%, rgba(0, 190, 220, .10), transparent 28%),
        #f6f9ff;
    color: #10275d;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.1rem;
    padding-bottom: 1.5rem;
}

#MainMenu, header, footer { visibility: hidden; }

/* -------------------- TOP NAV -------------------- */
.top-nav {
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255,255,255,.96);
    border: 1px solid #e3eaf6;
    border-radius: 18px;
    padding: 0 22px;
    box-shadow: 0 8px 28px rgba(34,67,125,.08);
    margin-bottom: 18px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #173d92;
    font-size: 1.35rem;
    font-weight: 850;
}

.brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg,#6347ef,#087cf0);
    color: white;
    font-size: 1.25rem;
}

.nav-links {
    display: flex;
    gap: 8px;
    align-items: center;
}

.nav-link {
    padding: 10px 15px;
    border-radius: 12px;
    color: #263b68;
    font-weight: 750;
    font-size: .95rem;
}

.nav-link.active {
    color: #0876ed;
    background: #edf5ff;
}

/* -------------------- HERO -------------------- */
.hero-card {
    min-height: 300px;
    border: 1px solid #e0e9f7;
    border-radius: 28px;
    background: linear-gradient(120deg,#ffffff 0%,#f0f8ff 100%);
    box-shadow: 0 16px 42px rgba(43,76,137,.09);
    padding: 32px 38px;
    margin-bottom: 18px;
}

.hero-title {
    font-size: clamp(2.3rem, 4.2vw, 3.45rem);
    line-height: 1.05;
    margin: 4px 0 10px;
    letter-spacing: -2px;
    font-weight: 900;
    color: #102c69;
}

.hero-title .purple {
    background: linear-gradient(90deg,#7b45eb,#4168ef);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #314873;
    font-size: 1.18rem;
    font-weight: 750;
    margin-bottom: 10px;
}

.hero-text {
    color: #5a6f96;
    font-size: 1rem;
    line-height: 1.55;
    max-width: 650px;
}

.feature-row {
    display: flex;
    gap: 28px;
    margin-top: 22px;
    flex-wrap: wrap;
}

.feature {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #123574;
    font-weight: 800;
}

.feature-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e6f4ff;
    font-size: 1.35rem;
}

.feature small {
    color: #71809c;
    font-weight: 550;
}

.hero-art {
    height: 300px;
    border-radius: 28px;
    border: 1px solid #e0e9f7;
    background: linear-gradient(135deg,#ffffff,#edf8ff);
    box-shadow: 0 16px 42px rgba(43,76,137,.09);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}

.hero-art::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 190px;
    border-radius: 50%;
    background: radial-gradient(circle,rgba(54,198,238,.18),transparent 68%);
}

.art-wrap {
    position: relative;
    text-align: center;
    z-index: 1;
}

.glucose {
    width: 105px;
    height: 125px;
    border-radius: 28px;
    background: linear-gradient(160deg,#28a8dd,#0874b8);
    border: 7px solid #d8f4ff;
    box-shadow: 0 15px 28px rgba(22,112,173,.22);
    margin: 0 auto 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: white;
    font-weight: 900;
}

.glucose-screen {
    width: 68px;
    height: 48px;
    border-radius: 9px;
    background: #dff7ff;
    color: #17608a;
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-size: 1.2rem;
    line-height: 1.05;
}

.glucose-screen small { font-size: .6rem; }

.stethoscope {
    position: absolute;
    left: 78px;
    top: 4px;
    font-size: 4.7rem;
    transform: rotate(-7deg);
}

.heart-art {
    position: absolute;
    right: 55px;
    bottom: 42px;
    font-size: 4.8rem;
    filter: drop-shadow(0 8px 10px rgba(210,60,60,.18));
}

.art-caption {
    color: #0876dc;
    font-weight: 850;
    font-size: .95rem;
    line-height: 1.15;
}

/* -------------------- SECTION HEADERS -------------------- */
.card-head {
    background: rgba(255,255,255,.97);
    border: 1px solid #e1e9f5;
    border-radius: 22px;
    padding: 18px 22px;
    box-shadow: 0 9px 28px rgba(40,73,130,.07);
    margin-bottom: 13px;
}

.card-head-inner {
    display: flex;
    align-items: center;
    gap: 14px;
}

.card-icon {
    width: 54px;
    height: 54px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg,#e8f2ff,#dcecff);
    font-size: 1.55rem;
}

.card-icon.green { background: #e4f8ef; }
.card-icon.blue { background: #e5efff; }

.card-title {
    color: #122f6c;
    font-size: 1.48rem;
    font-weight: 900;
    margin: 0;
}

.card-subtitle {
    color: #647697;
    margin: 3px 0 0;
    font-size: .93rem;
}

/* -------------------- STREAMLIT INPUTS -------------------- */
.stSelectbox label,
.stNumberInput label {
    color: #253b69 !important;
    font-weight: 750 !important;
    font-size: .92rem !important;
}

div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] > div {
    border-radius: 11px !important;
    border-color: #dbe5f2 !important;
    background: #fbfcff !important;
    min-height: 42px;
}

input {
    color: #1e2e4d !important;
}

/* Make the two main columns visually close to the reference design. */
div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
    gap: 18px;
}

/* -------------------- PREDICT BUTTON -------------------- */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border: none !important;
    border-radius: 13px !important;
    background: linear-gradient(90deg,#137ff2 0%,#8b38f2 100%) !important;
    color: white !important;
    font-size: 1.08rem !important;
    font-weight: 850 !important;
    box-shadow: 0 10px 25px rgba(92,75,222,.25);
}

.stButton > button:hover {
    box-shadow: 0 14px 30px rgba(92,75,222,.34);
    transform: translateY(-1px);
}

/* -------------------- RESULT -------------------- */
.result-card {
    background: rgba(255,255,255,.98);
    border: 1px solid #e1e9f5;
    border-radius: 22px;
    padding: 20px 24px 22px;
    box-shadow: 0 9px 28px rgba(40,73,130,.07);
}

.result-box {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
}

.result-box.good {
    border: 1px solid #83e0b1;
    background: linear-gradient(135deg,#effdf6,#e7faef);
}

.result-box.risk {
    border: 1px solid #ffb2b2;
    background: linear-gradient(135deg,#fff6f6,#ffeded);
}

.result-icon {
    width: 68px;
    height: 68px;
    min-width: 68px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 2.15rem;
    font-weight: 900;
    background: linear-gradient(135deg,#31c98d,#0eaa72);
}

.result-icon.risk {
    background: linear-gradient(135deg,#ff756e,#dc4047);
}

.result-title {
    margin: 0;
    font-size: 1.45rem;
    font-weight: 900;
    color: #11794f;
}

.result-title.risk { color: #b4232c; }

.result-description {
    margin: 5px 0 0;
    color: #536783;
}

.probability-row {
    display: flex;
    align-items: end;
    justify-content: space-between;
    margin-top: 25px;
}

.probability-label {
    color: #394e75;
    font-weight: 800;
    font-size: 1rem;
}

.probability-value {
    color: #142b63;
    font-size: 2rem;
    font-weight: 950;
}

.progress {
    height: 18px;
    background: #e7ebf2;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 5px;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg,#2bc88d,#13a972);
}

.progress-fill.risk {
    background: linear-gradient(90deg,#ff7b72,#e5484d);
}

.advice {
    margin-top: 14px;
    padding: 16px 18px;
    border-radius: 14px;
    background: #eafaf1;
    color: #315d4b;
    line-height: 1.5;
}

.advice.risk { background: #fff0f0; color: #713c40; }
.advice strong { color: #137b50; display:block; margin-bottom:3px; }
.advice.risk strong { color:#b4232c; }

/* -------------------- SUMMARY -------------------- */
.summary-card {
    background: rgba(255,255,255,.98);
    border: 1px solid #e1e9f5;
    border-radius: 22px;
    padding: 20px 24px 22px;
    box-shadow: 0 9px 28px rgba(40,73,130,.07);
    margin-top: 16px;
}

.summary-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;
    border: 1px solid #dce5f2;
    border-radius: 12px;
    margin-top: 13px;
}

.summary-table th,
.summary-table td {
    padding: 10px 9px;
    border-right: 1px solid #e2e8f1;
    border-bottom: 1px solid #e2e8f1;
    text-align: center;
    font-size: .82rem;
}

.summary-table th {
    background: #f8faff;
    color: #435577;
    font-weight: 850;
}

.summary-table td {
    color: #1e3156;
    font-weight: 650;
}

.summary-table th:last-child,
.summary-table td:last-child { border-right: 0; }
.summary-table tr:last-child td { border-bottom: 0; }

/* -------------------- INFO NOTE -------------------- */
.info-note {
    margin-top: 14px;
    padding: 13px 16px;
    border-radius: 13px;
    background: #eaf4ff;
    color: #466287;
    font-size: .88rem;
    line-height: 1.45;
}

/* -------------------- FOOTER -------------------- */
.footer {
    border-top: 1px solid #dce5f1;
    margin-top: 20px;
    padding: 17px 4px 4px;
    display: flex;
    justify-content: space-between;
    gap: 30px;
    color: #667795;
    font-size: .83rem;
}

.footer-brand {
    color: #173b88;
    font-weight: 900;
}

/* -------------------- MOBILE -------------------- */
@media (max-width: 850px) {
    .top-nav { padding: 0 13px; }
    .nav-link:not(.active) { display: none; }
    .hero-card, .hero-art { min-height: 0; }
    .hero-card { padding: 25px; }
    .hero-art { height: 260px; }
    .feature-row { gap: 16px; }
    .footer { flex-direction: column; }
}
</style>
""",
    unsafe_allow_html=True,
)

# LOAD MODEL

MODEL_PATH = Path(__file__).resolve().parent / "diabetes_model_balanced.pkl"

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}\n"
            "Keep diabetes_model.pkl in the same folder as this Streamlit file."
        )
    return joblib.load(MODEL_PATH)

try:
    bundle = load_model()
    model = bundle["pipeline"]
    THRESHOLD = float(bundle["threshold"])  # balanced operating point chosen on training data
except Exception as exc:
    st.error(f"Could not load the model: {exc}")
    st.stop()

# SESSION STATE

if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "last_input" not in st.session_state:
    st.session_state.last_input = None

# TOP NAVIGATION

st.markdown(
    """
<div class="top-nav">
    <div class="brand">
        <span class="brand-icon">♥</span>
        <span>HealthAI</span>
    </div>
    <div class="nav-links">
        <span class="nav-link active">⌂ &nbsp;Home</span>
        <span class="nav-link">ⓘ &nbsp;About</span>
        <span class="nav-link">▱ &nbsp;Project</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# HERO

hero_left, hero_right = st.columns([1.45, 1], gap="large")

with hero_left:
    st.markdown(
        """
<div class="hero-card">
    <div class="hero-title"><span class="purple">Diabetes</span> Detection System</div>
    <div class="hero-subtitle">Predict the likelihood of diabetes using machine learning</div>
    <div class="hero-text">
        Enter the patient's information below to get an instant prediction and
        understand the risk of diabetes.
    </div>
    <div class="feature-row">
        <div class="feature">
            <span class="feature-icon">🛡️</span>
            <span>Fast &amp; Accurate<br><small>ML Powered</small></span>
        </div>
        <div class="feature">
            <span class="feature-icon">📊</span>
            <span>Easy to Use<br><small>Simple Interface</small></span>
        </div>
        <div class="feature">
            <span class="feature-icon">♡</span>
            <span>Better Awareness<br><small>For a Healthier Life</small></span>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
<div class="hero-art">
    <div class="art-wrap">
        <div class="stethoscope">♧</div>
        <div class="glucose">
            <div class="glucose-screen">96<br><small>mg/dL</small></div>
            💧
        </div>
        <div class="heart-art">❤️</div>
        <div class="art-caption">Your Health<br>Our Priority</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

# MAIN CONTENT

input_col, result_col = st.columns([1, 1.28], gap="large")

# -------------------- INPUT SIDE --------------------
with input_col:
    st.markdown(
        """
<div class="card-head">
    <div class="card-head-inner">
        <div class="card-icon">👤</div>
        <div>
            <div class="card-title">Patient Information</div>
            <div class="card-subtitle">Please fill in the details below</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        gender = st.selectbox("♙ Gender", ["Male", "Female", "Other"], index=0)
    with c2:
        age = st.number_input("🗓️ Age", min_value=0.08, max_value=80.0, value=25.0, step=1.0, help="Model was trained on ages 0.08-80.")

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        hypertension = st.selectbox("🩺 Hypertension", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    with c2:
        heart_disease = st.selectbox("♥ Heart Disease", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

    smoking_history = st.selectbox(
        "🚬 Smoking History",
        ["never", "former", "current", "not current", "ever", "No Info"],
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        bmi = st.number_input("⚖️ BMI (Body Mass Index)", min_value=10.0, max_value=95.0, value=22.0, step=0.1, help="Model was trained on BMI 10-95.")
    with c2:
        hba1c = st.number_input("💧 HbA1c Level (%)", min_value=3.5, max_value=9.0, value=5.2, step=0.1, help="Model was trained on HbA1c 3.5-9.0%.")

    blood_glucose = st.number_input(
        "💧 Blood Glucose Level (mg/dL)",
        min_value=80,
        max_value=300,
        value=90,
        step=1,
        help="Model was trained on glucose 80-300 mg/dL.",
    )

    input_data = pd.DataFrame(
        {
            "gender": [gender],
            "age": [age],
            "hypertension": [hypertension],
            "heart_disease": [heart_disease],
            "smoking_history": [smoking_history],
            "bmi": [bmi],
            "HbA1c_level": [hba1c],
            "blood_glucose_level": [blood_glucose],
        }
    )

    if st.button("🔍  Predict Diabetes", use_container_width=True):
        try:
            score = float(model.predict_proba(input_data)[0][1])
            st.session_state.probability = score
            st.session_state.prediction = int(score >= THRESHOLD)
            st.session_state.last_input = input_data.copy()
            # Common diagnostic cut-offs (ADA/WHO): HbA1c >= 6.5 %, glucose >= 126 mg/dL (fasting)
            st.session_state.guard = bool(hba1c >= 6.5 or blood_glucose >= 126)
        except Exception as exc:
            st.error(f"Prediction error: {exc}")

    st.markdown(
        """
<div class="info-note">
    <b style="color:#0876dc;">ⓘ</b>&nbsp;
    Make sure to enter accurate values for better results.<br>
    This tool is for educational purposes only. The risk score is a model output, not a calibrated probability.
</div>
""",
        unsafe_allow_html=True,
    )

# -------------------- RESULT SIDE --------------------
with result_col:
    st.markdown(
        """
<div class="result-card">
    <div class="card-head-inner">
        <div class="card-icon green">📊</div>
        <div>
            <div class="card-title">Prediction Result</div>
            <div class="card-subtitle">Here is the model's prediction based on the provided information.</div>
        </div>
    </div>
""",
        unsafe_allow_html=True,
    )

    prediction = st.session_state.prediction
    probability = st.session_state.probability
    guard = st.session_state.get("guard", False)
    low_desc = ("HbA1c or glucose is at or above common diagnostic cut-offs. Do not rely on this result."
                if guard else "The model predicts a low likelihood of diabetes.")
    low_advice = ("<strong>⚠️ Check your values</strong> An HbA1c of 6.5% or higher, or a fasting glucose of 126 mg/dL or higher, "
                  "meets common diagnostic criteria regardless of this tool's output. Please see a healthcare professional."
                  if guard else "<strong>💡 Good News!</strong> Based on the provided information, the estimated risk is low. "
                  "Maintain healthy habits and routine health check-ups.")

    if prediction is None:
        st.markdown(
            """
<div class="result-box good">
    <div class="result-icon">✓</div>
    <div>
        <div class="result-title">No Prediction Yet</div>
        <div class="result-description">Enter the patient information and click <b>Predict Diabetes</b> to run the model.</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
        display_probability = 0.0
    else:
        display_probability = (probability or 0.0) * 100
        if prediction == 1:
            st.markdown(
                """
<div class="result-box risk">
    <div class="result-icon risk">!</div>
    <div>
        <div class="result-title risk">Elevated Diabetes Risk</div>
        <div class="result-description">Screening flag: follow-up testing is recommended. This is not a diagnosis.</div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
<div class="result-box good">
    <div class="result-icon">✓</div>
    <div>
        <div class="result-title">Lower Diabetes Risk</div>
        <div class="result-description">{low_desc}</div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    fill_class = "risk" if prediction == 1 else ""
    safe_probability = min(max(display_probability, 0), 100)

    st.markdown(
        f"""
<div class="probability-row">
    <div class="probability-label">Model Risk Score</div>
    <div class="probability-value">{display_probability:.2f}%</div>
</div>
<div class="progress">
    <div class="progress-fill {fill_class}" style="width:{safe_probability:.2f}%;"></div>
</div>
""",
        unsafe_allow_html=True,
    )

    if prediction is None:
        st.markdown(
            """
<div class="advice">
    <strong>💡 Ready to Check</strong>
    Complete the patient information on the left to receive a machine-learning prediction.
</div>
""",
            unsafe_allow_html=True,
        )
    elif prediction == 1:
        st.markdown(
            """
<div class="advice risk">
    <strong>⚠️ Important</strong>
    The model indicates an increased likelihood of diabetes. Consider discussing this result and appropriate testing with a qualified healthcare professional.
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
<div class="advice">
    {low_advice}
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- PATIENT SUMMARY --------------------
    st.markdown(
        """
<div class="summary-card">
    <div class="card-head-inner">
        <div class="card-icon blue">📄</div>
        <div>
            <div class="card-title">Patient Summary</div>
            <div class="card-subtitle">Input values used for prediction</div>
        </div>
    </div>
""",
        unsafe_allow_html=True,
    )

    summary_data = st.session_state.last_input
    if summary_data is None:
        summary_data = input_data

    display_summary = summary_data.rename(
        columns={
            "gender": "Gender",
            "age": "Age",
            "hypertension": "Hypertension",
            "heart_disease": "Heart Disease",
            "smoking_history": "Smoking",
            "bmi": "BMI",
            "HbA1c_level": "HbA1c (%)",
            "blood_glucose_level": "Glucose (mg/dL)",
        }
    ).copy()

    display_summary["Hypertension"] = display_summary["Hypertension"].map({0: "0", 1: "1"})
    display_summary["Heart Disease"] = display_summary["Heart Disease"].map({0: "0", 1: "1"})

    row = display_summary.iloc[0]
    st.markdown(
        f"""
<table class="summary-table">
    <thead>
        <tr>
            <th>Gender</th>
            <th>Age</th>
            <th>Hypertension</th>
            <th>Heart<br>Disease</th>
            <th>Smoking</th>
            <th>BMI</th>
            <th>HbA1c (%)</th>
            <th>Glucose<br>(mg/dL)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{row['Gender']}</td>
            <td>{row['Age']:.0f}</td>
            <td>{row['Hypertension']}</td>
            <td>{row['Heart Disease']}</td>
            <td>{row['Smoking']}</td>
            <td>{row['BMI']:.1f}</td>
            <td>{row['HbA1c (%)']:.1f}</td>
            <td>{row['Glucose (mg/dL)']:.0f}</td>
        </tr>
    </tbody>
</table>
</div>
""",
        unsafe_allow_html=True,
    )

# FOOTER

st.markdown(
    """
<div class="footer">
    <div>
        <span style="font-size:1.45rem;">♥</span>
        <span class="footer-brand"> Diabetes Detection System</span><br>
        <span>Early Prediction. Healthier Tomorrow.</span>
    </div>
    <div style="max-width:650px; text-align:right;">
        ⚕️ This application is a machine-learning demonstration and should not be used
        as a substitute for professional medical diagnosis or clinical decision-making.
    </div>
</div>
""",
    unsafe_allow_html=True,
)
