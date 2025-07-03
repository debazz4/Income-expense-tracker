const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#emailField");
const emailFeedbackArea = document.querySelector(".emailFeedbackArea");
const usernamesuccess = document.querySelector(".usernamesuccess");
const emailsuccess = document.querySelector(".emailsuccess");


usernameField.addEventListener("keyup", (e) => {

    const usernameval = e.target.value;

    usernamesuccess.style.display = "block";

    usernamesuccess.textContent = `Checking ${usernameval}`;

    usernameField.classList.remove("is-invalid");

    feedbackArea.style.display = "none";

    if (usernameval.length > 0) {
        fetch("/auth/validate-username", {
            body: JSON.stringify({ username: usernameval }),
            method: "POST",
        }) 
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            usernamesuccess.style.display = "none";
            if (data.username_error) {
                usernameField.classList.add("is-invalid");

                feedbackArea.style.display = "block";
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
            }
    });
    }
});

emailField.addEventListener("keyup", (e) => {

    const emailval = e.target.value;

    emailsuccess.style.display = "block";

    emailsuccess.textContent = `Checking ${emailval}`;

    emailField.classList.remove("is-invalid");

    emailFeedbackArea.style.display = "none";

    if (emailval.length > 0) {
        fetch("/auth/validate-email", {
            body: JSON.stringify({ email: emailval }),
            method: "POST",
        }) 
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            emailsuccess.style.display = "none"
            if (data.email_error) {
                emailField.classList.add("is-invalid");

                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
            }
    });
    }
});