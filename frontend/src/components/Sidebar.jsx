function Sidebar({ setPage, currentPage }) {
  const menus = [
    "Dashboard",
    "Analytics",
    "PredictionStudio",
    "Insights",
    "Recommendations"
  ];

  return (
    <div className="sidebar">
      <h2>Menu</h2>
      {menus.map((item) => (
        <button
          key={item}
          className={currentPage === item ? "active-menu" : ""}
          onClick={() => setPage(item)}
        >
          {item}
        </button>
      ))}
    </div>
  );
}

export default Sidebar;