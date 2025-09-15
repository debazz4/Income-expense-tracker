
const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn")


//To toggle password
const handleToggleInput = (e)=>{
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password",)
    }
};
showPasswordToggle.addEventListener("click", handleToggleInput);

const handleToggleInputs = (e) => {
    if (showPasswordToggles.textContent === "SHOW") {
        showPasswordToggles.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordFields.setAttribute("type", "password",)
    }
};
showPasswordToggles.addEventListener("click", handleToggleInputs);

