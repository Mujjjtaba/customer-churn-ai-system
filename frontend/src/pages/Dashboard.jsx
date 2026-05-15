import MetricCard from "../components/MetricCard";

function Dashboard({ metrics }) {
  const modelNames = Object.keys(metrics);

  if (modelNames.length === 0) return <div>Loading Dashboard...</div>;

  const bestAccuracy = Math.max(
    ...modelNames.map((m) => metrics[m]["Accuracy"] * 100)
  ).toFixed(2);

  const avgRoc = (
    modelNames.reduce((acc, m) => acc + metrics[m]["ROC AUC"], 0) /
    modelNames.length *
    100
  ).toFixed(2);

  return (
    <div>
      <h1>Executive Dashboard Overview</h1>

      <div className="dashboard-grid">
        <MetricCard title="Models Trained" value={modelNames.length} />
        <MetricCard title="Best Accuracy" value={`${bestAccuracy}%`} />
        <MetricCard title="Average ROC AUC" value={`${avgRoc}%`} />
        <MetricCard title="ML Status" value="Production Ready" />
      </div>
    </div>
  );
}

export default Dashboard;