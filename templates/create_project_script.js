// JavaScript code
document
  .getElementById("create-project-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    // Collect input values into separate variables
    let projectName = document.getElementById("project-name").value;
    let description = document.getElementById("description").value;
    let dueDate = document.getElementById("due-date").value;
    let userId = document.getElementById("user-id").value;

    let jsonData = {
      ProjectName: projectName,
      Description: description,
      DueDate: dueDate,
      CreatorUserID: userId,
    };

    try {
      let response = await fetch("http://127.0.0.1:5000//api/projects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      });

      if (response.ok) {
        let data = await response.json();
        console.log(data);
        alert("Project created successfully with ID: " + data.ProjectID);
        // Redirect to another page or update UI as needed
      } else {
        alert("Failed to create project: " + response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });
