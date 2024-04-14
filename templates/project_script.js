window.onload = async function fetchProjects() {
  try {
    let response = await fetch("http://127.0.0.1:5000/api/users/1/projects");
    if (response.ok) {
      let data = await response.json();
      let projData = data.projects;
    //   console.log(projData);
      let projectDisplay = document.querySelector(".project_display");

      projData.forEach((project) => {
        // Get the ProjectID dynamically for each project
        let PROJECT_ID = project.ProjectID;

        // Create anchor tag for each card
        let cardLink = document.createElement("a");
        cardLink.href = `project_detail.html?id=${PROJECT_ID}`;

        // Create card element
        let card = document.createElement("div");
        card.classList.add("card", "mb-3");

        // Create card body
        let cardBody = document.createElement("div");
        cardBody.classList.add(
          "card-body",
          "d-flex",
          "flex-column",
          "align-items-start"
        );

        // Create project name
        let projectName = document.createElement("h5");
        projectName.classList.add("card-title", "mb-1");
        projectName.textContent = project.ProjectName;

        // Create project description
        let description = document.createElement("p");
        description.classList.add("card-text", "mb-1");
        description.textContent = project.Description;

        // Create due date
        let dueDate = document.createElement("p");
        dueDate.classList.add("card-text", "text-muted", "small");
        dueDate.textContent =
          "Due Date: " + new Date(project.DueDate).toLocaleDateString();

        // Append elements to card body
        cardBody.appendChild(projectName);
        cardBody.appendChild(description);
        cardBody.appendChild(dueDate);

        // Append card body to card
        card.appendChild(cardBody);

        // Append card to anchor tag
        cardLink.appendChild(card);

        // Append anchor tag to project display
        projectDisplay.appendChild(cardLink);
      });
    } else {
      console.error("Failed to fetch projects:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};
