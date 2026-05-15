function ChartCard({ src }) {
  return (
    <div className="chart-card">
      <img src={`http://127.0.0.1:8000${src}`} alt="chart" />
    </div>
  );
}

export default ChartCard;