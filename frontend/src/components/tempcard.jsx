function TaskCard({ title, status }) {
  return (
    <div className="task-card">
      <h3>{title}</h3>
      <p>Status: {status}</p>
    </div>
  );
}

export default TaskCard;