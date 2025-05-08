document.addEventListener("DOMContentLoaded", function () {
    // Get UI elements
    const clientBtn = document.getElementById("clientBtn");
    const staffBtn = document.getElementById("staffBtn");
    const clientForm = document.getElementById("clientform");
    const staffForm = document.getElementById("staffform");
    
    // Hide staff form by default
    staffForm.style.display = "none";
    
    // Setup event listeners for tab switching
    clientBtn.addEventListener("click", function () {
        // Show client form, hide staff form
        clientForm.style.display = "block";
        staffForm.style.display = "none";
        
        // Update active states
        clientBtn.classList.add("active");
        staffBtn.classList.remove("active");
        
        // Smooth transition
        clientForm.style.opacity = 0;
        setTimeout(() => {
            clientForm.style.opacity = 1;
        }, 50);
    });
    
    staffBtn.addEventListener("click", function () {
        // Hide client form, show staff form
        clientForm.style.display = "none";
        staffForm.style.display = "block";
        
        // Update active states
        staffBtn.classList.add("active");
        clientBtn.classList.remove("active");
        
        // Smooth transition
        staffForm.style.opacity = 0;
        setTimeout(() => {
            staffForm.style.opacity = 1;
        }, 50);
    });
    
    // Add smooth transitions to forms
    clientForm.style.transition = "opacity 0.3s ease";
    staffForm.style.transition = "opacity 0.3s ease";
});