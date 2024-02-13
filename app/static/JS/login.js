// FORGOT PASSWORD SECTION
function showForgotPasswordSection() {
  console.log('Function called');
  document.getElementById('forgot-password-section').style.display = 'block';
}

window.onload = function () {
  // Get the exit icon element
  var exitIcon = document.getElementById('exit-icon');

  // Add a click event listener to the exit icon
  exitIcon.addEventListener('click', function () {
    // Get the "Forgot Password" section
    var forgotPasswordSection = document.getElementById('forgot-password-section');

    // Hide the "Forgot Password" section
    forgotPasswordSection.style.display = 'none';
  });

}