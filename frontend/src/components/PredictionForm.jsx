import { useState } from "react";
import { predictCustomer } from "../services/api";

function PredictionForm() {
  const [result, setResult] = useState(null);

  const [formData, setFormData] = useState({
    gender: "Female",
    SeniorCitizen: 0,
    Partner: "Yes",
    Dependents: "No",
    tenure: 5,
    PhoneService: "Yes",
    MultipleLines: "No",
    InternetService: "Fiber optic",
    OnlineSecurity: "No",
    OnlineBackup: "No",
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "Yes",
    StreamingMovies: "Yes",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: 89.5,
    TotalCharges: 450.2
  });

  const handlePredict = async () => {
    const res = await predictCustomer(formData);
    setResult(res);
  };

  return (
    <div>
      <div className="predict-grid">
        {Object.keys(formData).map((key) => (
          <input
            key={key}
            value={formData[key]}
            onChange={(e) =>
              setFormData({ ...formData, [key]: e.target.value })
            }
            placeholder={key}
          />
        ))}
      </div>

      <button onClick={handlePredict}>Run Churn Prediction</button>

      {result && (
        <div className="result-box">
          <h3>{result.prediction}</h3>
          <p>Probability: {result.churn_probability}%</p>
          <p>{result.recommendation}</p>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;