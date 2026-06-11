import { useState } from "react";

function TaskForm({ addTask }) {
  const [taskName, setTaskName] = useState("");

  return (
    <div className="task-form">
      <input
        type="text"
        placeholder="Task Name"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
      />

      <button
        onClick={() => {
          if (taskName.trim() !== "") {
            addTask(taskName);
            setTaskName("");
          }
        }}
      >
        Assign Task
      </button>
    </div>
  );
}

export default TaskForm;