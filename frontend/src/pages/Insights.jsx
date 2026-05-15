import ChartCard from "../components/ChartCard";

function Insights({ charts }) {
  return (
    <div>
      <h1>EDA Visual Intelligence</h1>

      <div className="charts-layout">
        {charts.map((chart, i) => (
          <ChartCard key={i} src={chart} />
        ))}
      </div>
    </div>
  );
}

export default Insights;