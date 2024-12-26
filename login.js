const allowedUsernames = ["user1", "user2", "user3"];  // Add allowed usernames here
const standardPassword = "SAKEC123";  // Standard password

function validateLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (allowedUsernames.includes(username) && password === standardPassword) {
        alert("Login successful!");
        // Redirect to another page or perform any action
        window.location.href = "wow2_1_1.html";  // Example redirection
        return false;
    } else {
        document.getElementById("error-message").style.display = "block";
        return false; // Prevent form submission
    }
}
