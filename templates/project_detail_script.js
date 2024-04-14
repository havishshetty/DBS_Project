document.addEventListener("DOMContentLoaded", function () {
  // Get project ID from URL query parameters
  const urlParams = new URLSearchParams(window.location.search);
  const projectId = urlParams.get("id");

  // Fetch project details from server
  fetch(`http://127.0.0.1:5000/api/projects/${projectId}`)
    .then((response) => response.json())
    .then((data) => {
      // Populate project details on the page
      document.getElementById("project-name").textContent += data.ProjectName;
      document.getElementById("description").textContent += data.Description;
      document.getElementById("due-date").textContent += data.DueDate;
      document.getElementById("creator-user-id").textContent +=
        data.CreatorUserID;

      // Fetch comments for the project
      fetch(`http://127.0.0.1:5000/api/comment_project/${projectId}`)
        .then((response) => response.json())
        .then((commentsData) => {
          // Populate comments on the page
          document.getElementById("comments").textContent +=
            commentsData.CommentText;

          // Fetch task status for the project
          fetch(`http://127.0.0.1:5000/api/task_status/${projectId}`)
            .then((response) => response.json())
            .then((progressData) => {
              // Populate task status on the page
              document.getElementById("progress").textContent +=
                progressData.Status;
            })
            .catch((error) => console.error("Error fetching progress:", error));
        })
        .catch((error) => console.error("Error fetching comments:", error));
    })
    .catch((error) => console.error("Error fetching project details:", error));
});
