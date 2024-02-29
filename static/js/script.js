// static/signup.js

document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signupForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const submitButton = document.querySelector('button[type="submit"]');

    function validatePassword() {
        const email = emailInput.value;
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // Validate email format
        const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

        // Validate password length
        const isLengthValid = password.length >= 8;

        // Validate password match
        const doPasswordsMatch = password === confirmPassword;

        // Enable or disable submit button based on conditions
        submitButton.disabled = !(isEmailValid && isLengthValid && doPasswordsMatch);

        // Display error messages with Bootstrap classes
        document.getElementById('emailError').innerHTML = isEmailValid ? '' : '<small class="text-danger">Enter a valid email address</small>';
        document.getElementById('passwordError').innerHTML = isLengthValid ? '' : '<small class="text-danger">Password must be at least 8 characters long</small>';
        document.getElementById('confirmPasswordError').innerHTML = doPasswordsMatch ? '' : '<small class="text-danger">Passwords do not match</small>';
    }

    // Attach the validatePassword function to all relevant input events
    emailInput.addEventListener('input', validatePassword);
    passwordInput.addEventListener('input', validatePassword);
    confirmPasswordInput.addEventListener('input', validatePassword);

    // Form submission validation
    signupForm.addEventListener('submit', function (event) {
        const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
        const isLengthValid = passwordInput.value.length >= 8;
        const doPasswordsMatch = passwordInput.value === confirmPasswordInput.value;

        if (!isEmailValid || !isLengthValid || !doPasswordsMatch) {
            event.preventDefault(); // Prevent form submission
            alert('Please fix the form issues before submitting.');
        }
    });
});
