function submitForm() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  let headersList = {
    "Content-Type": "application/json",
  };
  let bodyContent = JSON.stringify({
    username: username,
    password: password,
  });
  try {
    let response = fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      body: bodyContent,
      headers: headersList,
    });

    if (response.ok) {
      const responseData = response.json();
      console.log(responseData);
      if (responseData) {
        window.location.href = 'http://127.0.0.1:8000/templates/home.html';
        console.log(responseData);
      } else {
        console.error("Failed to log in");
        // Handle error appropriately, e.g., show error message to user
      }
    } else {
      console.error("Failed to log in:", response.statusText);
      // Handle error appropriately, e.g., show error message to user
    }
  } catch (error) {
    console.error("Error:", error);
    // Handle error appropriately, e.g., show error message to user
  }
}
