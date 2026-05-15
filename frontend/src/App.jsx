import { useEffect, useState } from "react";
import axios from "axios";
import {
  FaChartLine, FaRobot, FaBrain, FaLightbulb, FaGithub,
  FaChartPie, FaBolt, FaShieldAlt, FaWifi, FaMoneyBillWave,
  FaTrophy, FaCrosshairs, FaHandshake, FaCreditCard,
  FaHeadset, FaGift, FaChartBar, FaUsers
} from "react-icons/fa";
import "./App.css";

const API = "http://127.0.0.1:8000";

const FIELD_OPTIONS = {
  gender: ["Male", "Female"],
  SeniorCitizen: [0, 1],
  Partner: ["Yes", "No"],
  Dependents: ["Yes", "No"],
  PhoneService: ["Yes", "No"],
  MultipleLines: ["Yes", "No", "No phone service"],
  InternetService: ["DSL", "Fiber optic", "No"],
  OnlineSecurity: ["Yes", "No", "No internet service"],
  OnlineBackup: ["Yes", "No", "No internet service"],
  DeviceProtection: ["Yes", "No", "No internet service"],
  TechSupport: ["Yes", "No", "No internet service"],
  StreamingTV: ["Yes", "No", "No internet service"],
  StreamingMovies: ["Yes", "No", "No internet service"],
  Contract: ["Month-to-month", "One year", "Two year"],
  PaperlessBilling: ["Yes", "No"],
  PaymentMethod: ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
};

const INITIAL_FORM = {
  gender: "Female", SeniorCitizen: 0, Partner: "Yes", Dependents: "No",
  tenure: 5, PhoneService: "Yes", MultipleLines: "No",
  InternetService: "Fiber optic", OnlineSecurity: "No", OnlineBackup: "No",
  DeviceProtection: "No", TechSupport: "No", StreamingTV: "Yes",
  StreamingMovies: "Yes", Contract: "Month-to-month", PaperlessBilling: "Yes",
  PaymentMethod: "Electronic check", MonthlyCharges: 89.5, TotalCharges: 447.5,
};

/* ── Gauge ── */
function RiskGauge({ value }) {
  const r = 70, cx = 90, cy = 90;
  const circumference = Math.PI * r;
  const offset = circumference - (value / 100) * circumference;
  const color = value > 60 ? "#ef4444" : value > 35 ? "#f59e0b" : "#10b981";
  return (
    <div className="gauge-wrap">
      <svg className="gauge-svg" viewBox="0 0 180 110">
        <path d={`M 20 90 A ${r} ${r} 0 0 1 160 90`} className="gauge-bg" />
        <path d={`M 20 90 A ${r} ${r} 0 0 1 160 90`} className="gauge-fill"
          style={{ stroke: color, strokeDasharray: circumference, strokeDashoffset: offset }} />
        <text x={cx} y="78" className="gauge-text">{value}%</text>
        <text x={cx} y="98" className="gauge-label-text">Risk Score</text>
      </svg>
    </div>
  );
}

/* ── Fields ── */
function Field({ label, name, value, options, onChange }) {
  return (
    <div className="field-group">
      <label htmlFor={`field-${name}`}>{label}</label>
      <select id={`field-${name}`} value={value} onChange={(e) => onChange(name, e.target.value)}>
        {options.map((o, i) => <option key={i} value={o}>{name === "SeniorCitizen" ? (o === 0 ? "No" : "Yes") : o}</option>)}
      </select>
    </div>
  );
}

function NumberField({ label, name, value, onChange, readOnly }) {
  return (
    <div className="field-group">
      <label htmlFor={`field-${name}`}>{label}</label>
      <input id={`field-${name}`} type="number" value={value}
        onChange={(e) => onChange(name, e.target.value)} readOnly={readOnly} />
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState("dashboard");
  const [metrics, setMetrics] = useState({});
  const [edaImages, setEdaImages] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState(INITIAL_FORM);
  const [pageKey, setPageKey] = useState(0);

  useEffect(() => {
    axios.get(`${API}/metrics`).then(r => setMetrics(r.data || {})).catch(() => {});
    axios.get(`${API}/eda-images`).then(r => setEdaImages(r.data.charts || [])).catch(() => {});
  }, []);

  const switchTab = (id) => { setTab(id); setPageKey(k => k + 1); };

  const updateField = (name, value) => {
    const next = { ...form, [name]: value };
    if (name === "tenure" || name === "MonthlyCharges") {
      next.TotalCharges = Number(next.tenure) * Number(next.MonthlyCharges);
    }
    setForm(next);
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const payload = {
        ...form,
        SeniorCitizen: Number(form.SeniorCitizen),
        tenure: Number(form.tenure),
        MonthlyCharges: Number(form.MonthlyCharges),
        TotalCharges: Number(form.TotalCharges),
      };
      const res = await axios.post(`${API}/predict`, payload);
      setPrediction(res.data);
    } catch (err) {
      console.error("Prediction Error:", err.response?.data || err.message);
      alert("Prediction failed. Check if backend is running.");
    }
    setLoading(false);
  };

  const modelNames = Object.keys(metrics);
  const bestModel = modelNames.length > 0
    ? Object.entries(metrics).reduce((a, b) => a[1]["F1 Score"] > b[1]["F1 Score"] ? a : b)
    : null;

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: <FaChartLine /> },
    { id: "analytics", label: "Analytics", icon: <FaBrain /> },
    { id: "prediction", label: "Prediction", icon: <FaRobot /> },
    { id: "insights", label: "Insights", icon: <FaChartPie /> },
    { id: "recommendations", label: "Strategies", icon: <FaLightbulb /> },
  ];

  /* ── DASHBOARD ── */
  const renderDashboard = () => (
    <div className="page-enter" key={pageKey}>
      <div className="hero stagger-in">
        <h2>Customer Churn Intelligence</h2>
        <p>Enterprise-grade telecom retention platform powered by multi-model
          machine learning. Predict churn probability, analyze behavior, and get
          AI-driven retention strategies.</p>
      </div>

      <div className="bento-grid">
        <div className="bento-card stagger-in">
          <div className="card-icon purple"><FaBrain /></div>
          <div className="card-label">Models Benchmarked</div>
          <div className="card-value">{modelNames.length}</div>
        </div>
        <div className="bento-card stagger-in">
          <div className="card-icon pink"><FaTrophy /></div>
          <div className="card-label">Best Model</div>
          <div className="card-value small">{bestModel ? bestModel[0] : "—"}</div>
        </div>
        <div className="bento-card stagger-in">
          <div className="card-icon amber"><FaCrosshairs /></div>
          <div className="card-label">Peak Accuracy</div>
          <div className="card-value">{bestModel ? (bestModel[1]["Accuracy"] * 100).toFixed(1) + "%" : "—"}</div>
        </div>
        <div className="bento-card stagger-in">
          <div className="card-icon emerald"><FaChartBar /></div>
          <div className="card-label">Best F1 Score</div>
          <div className="card-value">{bestModel ? (bestModel[1]["F1 Score"] * 100).toFixed(1) + "%" : "—"}</div>
        </div>
      </div>

      {modelNames.length > 0 && (
        <div className="chart-section stagger-in">
          <h3>Model Accuracy Comparison</h3>
          <div className="bar-chart">
            {Object.entries(metrics)
              .sort((a, b) => b[1]["Accuracy"] - a[1]["Accuracy"])
              .map(([name, vals]) => (
              <div className="bar-row" key={name}>
                <div className="bar-label">{name}</div>
                <div className="bar-track">
                  <div className="bar-fill" style={{width: `${vals["Accuracy"] * 100}%`}} />
                </div>
                <div className="bar-value">{(vals["Accuracy"] * 100).toFixed(1)}%</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="info-card stagger-in">
        <h3>Platform Overview</h3>
        <p>ChurnAI Pro benchmarks 10 classification models — from Logistic Regression
          to CatBoost — against telecom customer data to identify customers at highest
          cancellation risk. The system uses feature engineering, label encoding, and
          standard scaling to deliver production-ready churn probability scores with
          actionable retention recommendations.</p>
      </div>
    </div>
  );

  /* ── ANALYTICS ── */
  const renderAnalytics = () => (
    <div className="page-enter" key={pageKey}>
      <div className="page-header">
        <h2>Model Performance Analytics</h2>
        <p>Detailed metrics across all trained classification models</p>
      </div>
      <div className="analytics-grid">
        {Object.entries(metrics).map(([name, vals], i) => (
          <div className="model-card stagger-in" key={i}>
            <div className="model-card-header">
              <h3>{name}</h3>
              {bestModel && bestModel[0] === name && <span className="model-badge best">Best</span>}
            </div>
            <div className="metric-row"><span className="label">Accuracy</span><span className="value">{(vals["Accuracy"] * 100).toFixed(2)}%</span></div>
            <div className="metric-row"><span className="label">Precision</span><span className="value">{(vals["Precision"] * 100).toFixed(2)}%</span></div>
            <div className="metric-row"><span className="label">Recall</span><span className="value">{(vals["Recall"] * 100).toFixed(2)}%</span></div>
            <div className="metric-row"><span className="label">F1 Score</span><span className="value">{(vals["F1 Score"] * 100).toFixed(2)}%</span></div>
            <div className="metric-row"><span className="label">ROC AUC</span><span className="value">{(vals["ROC AUC"] * 100).toFixed(2)}%</span></div>
            <div className="metric-row"><span className="label">Training Time</span><span className="value">{vals["Training Time"].toFixed(3)}s</span></div>
          </div>
        ))}
      </div>
    </div>
  );

  /* ── PREDICTION ── */
  const renderPrediction = () => (
    <div className="page-enter" key={pageKey}>
      <div className="page-header">
        <h2>Churn Risk Prediction</h2>
        <p>Enter customer profile details to generate an AI-powered churn risk assessment</p>
      </div>
      <div className="prediction-layout">
        <div className="form-panel">
          <div className="form-section">
            <h3><FaShieldAlt /> Demographics</h3>
            <div className="form-grid">
              <Field label="Gender" name="gender" value={form.gender} options={FIELD_OPTIONS.gender} onChange={updateField} />
              <Field label="Senior Citizen" name="SeniorCitizen" value={form.SeniorCitizen} options={FIELD_OPTIONS.SeniorCitizen} onChange={updateField} />
              <Field label="Partner" name="Partner" value={form.Partner} options={FIELD_OPTIONS.Partner} onChange={updateField} />
              <Field label="Dependents" name="Dependents" value={form.Dependents} options={FIELD_OPTIONS.Dependents} onChange={updateField} />
              <NumberField label="Tenure (months)" name="tenure" value={form.tenure} onChange={updateField} />
            </div>
          </div>

          <div className="form-section">
            <h3><FaWifi /> Services</h3>
            <div className="form-grid">
              <Field label="Phone Service" name="PhoneService" value={form.PhoneService} options={FIELD_OPTIONS.PhoneService} onChange={updateField} />
              <Field label="Multiple Lines" name="MultipleLines" value={form.MultipleLines} options={FIELD_OPTIONS.MultipleLines} onChange={updateField} />
              <Field label="Internet Service" name="InternetService" value={form.InternetService} options={FIELD_OPTIONS.InternetService} onChange={updateField} />
              <Field label="Online Security" name="OnlineSecurity" value={form.OnlineSecurity} options={FIELD_OPTIONS.OnlineSecurity} onChange={updateField} />
              <Field label="Online Backup" name="OnlineBackup" value={form.OnlineBackup} options={FIELD_OPTIONS.OnlineBackup} onChange={updateField} />
              <Field label="Device Protection" name="DeviceProtection" value={form.DeviceProtection} options={FIELD_OPTIONS.DeviceProtection} onChange={updateField} />
              <Field label="Tech Support" name="TechSupport" value={form.TechSupport} options={FIELD_OPTIONS.TechSupport} onChange={updateField} />
              <Field label="Streaming TV" name="StreamingTV" value={form.StreamingTV} options={FIELD_OPTIONS.StreamingTV} onChange={updateField} />
              <Field label="Streaming Movies" name="StreamingMovies" value={form.StreamingMovies} options={FIELD_OPTIONS.StreamingMovies} onChange={updateField} />
            </div>
          </div>

          <div className="form-section">
            <h3><FaMoneyBillWave /> Billing</h3>
            <div className="form-grid">
              <Field label="Contract" name="Contract" value={form.Contract} options={FIELD_OPTIONS.Contract} onChange={updateField} />
              <Field label="Paperless Billing" name="PaperlessBilling" value={form.PaperlessBilling} options={FIELD_OPTIONS.PaperlessBilling} onChange={updateField} />
              <Field label="Payment Method" name="PaymentMethod" value={form.PaymentMethod} options={FIELD_OPTIONS.PaymentMethod} onChange={updateField} />
              <NumberField label="Monthly Charges ($)" name="MonthlyCharges" value={form.MonthlyCharges} onChange={updateField} />
              <NumberField label="Total Charges ($)" name="TotalCharges" value={form.TotalCharges} readOnly />
            </div>
          </div>

          <button id="predict-btn" className="predict-btn" onClick={handlePredict} disabled={loading}>
            {loading ? "Analyzing Customer Risk..." : "Run Churn Prediction"}
          </button>
        </div>

        <div className="result-panel">
          <h3><FaCrosshairs /> Prediction Result</h3>
          {prediction ? (
            <>
              <RiskGauge value={prediction.churn_probability} />
              <div className="result-verdict">
                <div className={`verdict-text ${prediction.churn_probability > 50 ? "danger" : "safe"}`}>
                  {prediction.prediction}
                </div>
              </div>
              <div className="result-recommendation">
                <h4>AI Recommendation</h4>
                <p>{prediction.recommendation}</p>
              </div>
            </>
          ) : (
            <div className="result-empty">
              <div className="empty-icon"><FaRobot /></div>
              <p>Fill the form and run prediction to see results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  /* ── INSIGHTS ── */
  const renderInsights = () => (
    <div className="page-enter" key={pageKey}>
      <div className="page-header">
        <h2>Data Insights</h2>
        <p>Exploratory data analysis charts from the Telco customer dataset</p>
      </div>
      <div className="eda-grid">
        {edaImages.map((img, i) => {
          const name = img.split("/").pop().replace(".png", "").replace(/_/g, " ");
          return (
            <div className="eda-card stagger-in" key={i}>
              <img src={`${API}${img}`} alt={name} loading="lazy" />
              <div className="eda-label">{name}</div>
            </div>
          );
        })}
      </div>
    </div>
  );

  /* ── RECOMMENDATIONS ── */
  const recommendations = [
    { icon: <FaHandshake />, color: "purple", title: "Convert Month-to-Month Users",
      desc: "Prioritize month-to-month customers for loyalty conversion with discounted annual contracts." },
    { icon: <FaCreditCard />, color: "cyan", title: "Electronic Check Risk",
      desc: "Customers using electronic check show elevated churn. Incentivize automatic payment methods." },
    { icon: <FaUsers />, color: "emerald", title: "Onboarding Stabilization",
      desc: "Low tenure customers (< 6 months) need onboarding campaigns to reduce early-stage attrition." },
    { icon: <FaHeadset />, color: "rose", title: "Support Service Gaps",
      desc: "Missing online security and tech support correlate with dissatisfaction clusters." },
    { icon: <FaGift />, color: "amber", title: "Bundle Services",
      desc: "Bundle technical support, device protection, and security services to reduce churn intent." },
  ];

  const renderRecommendations = () => (
    <div className="page-enter" key={pageKey}>
      <div className="page-header">
        <h2>Retention Strategies</h2>
        <p>AI-driven intervention strategies to reduce customer attrition</p>
      </div>
      <div className="rec-grid">
        {recommendations.map((r, i) => (
          <div className="rec-card stagger-in" key={i}>
            <div className={`rec-icon ${r.color}`}>{r.icon}</div>
            <div>
              <h4>{r.title}</h4>
              <p>{r.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="app-shell">
      <nav className="topnav">
        <a className="topnav-brand" href="#">
          <div className="brand-dot"><FaBolt /></div>
          ChurnAI
        </a>
        <div className="topnav-tabs">
          {navItems.map(n => (
            <button key={n.id} className={tab === n.id ? "active" : ""} onClick={() => switchTab(n.id)}>
              {n.icon} {n.label}
            </button>
          ))}
        </div>
        <a className="topnav-github" href="https://github.com/Mujjjtaba/customer-churn-ai-system" target="_blank" rel="noreferrer">
          <FaGithub /> GitHub
        </a>
      </nav>

      <main className="main-content">
        {tab === "dashboard" && renderDashboard()}
        {tab === "analytics" && renderAnalytics()}
        {tab === "prediction" && renderPrediction()}
        {tab === "insights" && renderInsights()}
        {tab === "recommendations" && renderRecommendations()}
      </main>
    </div>
  );
}