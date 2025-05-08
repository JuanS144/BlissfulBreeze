document.addEventListener("DOMContentLoaded", () => {
  const logodropdown = document.getElementById("logo-dropdown");
  const content = document.getElementById("main-content");

  // Set initial styles
  content.style.opacity = 0;
  content.style.display = "none";

  // Wait 1.5 seconds before starting transition
  setTimeout(() => {
    logodropdown.style.transition = "opacity 1s ease";
    logodropdown.style.opacity = 0;

    // After fade-out, switch display and fade in content
    setTimeout(() => {
      logodropdown.style.display = "none";
      content.style.display = "block";

      // Fade in the content
      requestAnimationFrame(() => {
        content.style.transition = "opacity 1s ease";
        content.style.opacity = 1;
      });
    }, 500); // match fade-out duration
  }, 500); // delay before starting transition
});

function setupArrowNavigation(form) {
  const inputs = form.querySelectorAll('.form-field');

  inputs.forEach((input, index) => {
      input.addEventListener('keydown', function (event) {
          if (event.key === "ArrowDown") {
              event.preventDefault();
              if (index < inputs.length - 1) {
                  inputs[index + 1].focus();
              }
          } else if (event.key === "ArrowUp") {
              event.preventDefault();
              if (index > 0) {
                  inputs[index - 1].focus();
              }
          } else if (event.key === "Enter") {
              event.preventDefault();
              if (index < inputs.length - 1) {
                  inputs[index + 1].focus();
              } else {
                  form.requestSubmit();
              }
          }
      });
  });
}


// Flash message animation
document.addEventListener("DOMContentLoaded", () => {
  // Logo animation code you already have...

  // Flash message animation
  const flashMessages = document.querySelectorAll('.flash');
  
  if (flashMessages.length > 0) {
    flashMessages.forEach(flash => {
      // Show the message
      setTimeout(() => {
        flash.classList.add('show');
      }, 1200);
      
      // Hide after 5 seconds
      setTimeout(() => {
        flash.classList.remove('show');
        
        // Remove from DOM after transition completes
        setTimeout(() => {
          if (flash.parentNode) {
            flash.parentNode.removeChild(flash);
          }
        }, 500);
      }, 7000);
    });
  }
});