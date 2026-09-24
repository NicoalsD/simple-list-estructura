async function fetchTasks() {
  const res = await fetch("/api/tasks");
  const tasks = await res.json();
  const list = document.getElementById("tasks");
  list.innerHTML = "";
  tasks.forEach(t => {
    const li = document.createElement("li");
    if (t.completed) li.className = "completed";
    const check = document.createElement("div");
    check.className = "check";
    check.textContent = t.completed ? "✔" : "";
    check.onclick = () => updateTask(t.id, { completed: !t.completed });
    const label = document.createElement("span");
    label.className = "label";
    label.textContent = t.title;
    label.title = "Double-click to edit";
    label.ondblclick = () => {
      const title = prompt("Edit task", t.title);
      if (title && title.trim()) updateTask(t.id, { title: title.trim() });
    };
    const del = document.createElement("button");
    del.className = "del";
    del.textContent = "×";
    del.onclick = () => deleteTask(t.id);
    li.append(check, label, del);
    list.appendChild(li);
  });
}

async function addTask() {
  const input = document.getElementById("newTitle");
  if (!input.value.trim()) return;
  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: input.value.trim() })
  });
  input.value = "";
  fetchTasks();
}

async function updateTask(id, data) {
  await fetch("/api/tasks/" + id, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  fetchTasks();
}

async function deleteTask(id) {
  await fetch("/api/tasks/" + id, { method: "DELETE" });
  fetchTasks();
}

document.getElementById("newTitle").addEventListener("keydown", e => {
  if (e.key === "Enter") addTask();
});
fetchTasks();
