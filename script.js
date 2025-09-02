document.getElementById("studentForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const age = document.getElementById("age").value;
  const course = document.getElementById("course").value;

  await fetch("/add", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, age, course})
  });

  this.reset();
  loadStudents();
});

async function loadStudents() {
  const res = await fetch("/list");
  const students = await res.json();

  const table = document.getElementById("studentTable");
  table.innerHTML = "";

  students.forEach(s => {
    const row = `<tr>
      <td>${s.id}</td>
      <td>${s.name}</td>
      <td>${s.age}</td>
      <td>${s.course}</td>
    </tr>`;
    table.innerHTML += row;
  });
}

// Load students when page opens
loadStudents();
