// Handle form submission to add a new to-do
document.getElementById("addTodoForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  const todo = {
    id: Date.now(), // Unique ID (using timestamp)
    title: title,
    description: description,
    done: false,
  };

  // Send POST request to create new to-do
  fetch("/todos/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(todo),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      fetchTodos(); // Refresh the to-do list
    });
});

// Fetch and display all to-dos
function fetchTodos() {
  fetch("/todos/all")
    .then((response) => response.json())
    .then((data) => {
      const todos = data.todos;
      const todoList = document.getElementById("todoList");
      todoList.innerHTML = "";
      todos.forEach((todo) => {
        const li = document.createElement("li");
        li.innerHTML = `
          ${todo.title} - ${todo.description || "No description"}
          <button onclick="markAsDone(${todo.id}, ${!todo.done})">${todo.done ? "Undo" : "Mark as Done"}</button>
          <button onclick="deleteTodo(${todo.id})">Delete</button>
        `;
        todoList.appendChild(li);
      });
    });
}

// Mark a to-do as done or undone
function markAsDone(id, doneStatus) {
  fetch(`/todos/${id}/done`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ done: doneStatus }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      fetchTodos(); // Refresh the to-do list
    })
    .catch((error) => {
      console.error("Error marking to-do as done:", error);
    });
}

// Delete a to-do
function deleteTodo(id) {
  fetch(`/todos/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      fetchTodos(); // Refresh the to-do list
    })
    .catch((error) => {
      console.error("Error deleting to-do:", error);
    });
}

// Fetch and display incomplete to-dos
function fetchIncompleteTodos() {
  fetch("/todos")
    .then((response) => response.json())
    .then((data) => {
      const incompleteTodos = data.incomplete_todos;
      const todoList = document.getElementById("todoList");
      todoList.innerHTML = "";
      incompleteTodos.forEach((todo) => {
        const li = document.createElement("li");
        li.textContent = `${todo.title} - ${todo.description || "No description"}`;
        todoList.appendChild(li);
      });
    });
}

// Fetch and display completed to-dos
function fetchDoneTodos() {
  fetch("/todos/done")
    .then((response) => response.json())
    .then((data) => {
      const doneTodos = data.done_todos;
      const todoList = document.getElementById("todoList");
      todoList.innerHTML = "";
      doneTodos.forEach((todo) => {
        const li = document.createElement("li");
        li.textContent = `${todo.title} - ${todo.description || "No description"}`;
        todoList.appendChild(li);
      });
    });
}
