function Analytics({ metrics }) {
  return (
    <div>
      <h1>Model Analytics Laboratory</h1>

      <div className="analytics-grid">
        {Object.keys(metrics).map((model) => (
          <div className="analytic-card" key={model}>
            <h2>{model}</h2>
            <p>Accuracy: {(metrics[model]["Accuracy"] * 100).toFixed(2)}%</p>
            <p>Precision: {(metrics[model]["Precision"] * 100).toFixed(2)}%</p>
            <p>Recall: {(metrics[model]["Recall"] * 100).toFixed(2)}%</p>
            <p>F1 Score: {(metrics[model]["F1 Score"] * 100).toFixed(2)}%</p>
            <p>ROC AUC: {(metrics[model]["ROC AUC"] * 100).toFixed(2)}%</p>
            <p>Training Time: {metrics[model]["Training Time"].toFixed(2)} sec</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Analytics;