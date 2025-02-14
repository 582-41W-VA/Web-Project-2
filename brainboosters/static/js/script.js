// Responsive Menu
document.addEventListener("DOMContentLoaded", function () {
  const burgerMenu = document.createElement("div");
  burgerMenu.classList.add("burger-menu");
  burgerMenu.innerHTML = `
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
  `;

  const navContainer = document.querySelector("nav .container");
  const navItems = document.querySelector("nav .nav-items");
  const logoAndNav = document.querySelector(".logo-and-nav");
  const authButtons = document.querySelector("nav .auth-buttons");

  if (logoAndNav) {
    navContainer.insertAdjacentElement("beforeend", burgerMenu);
  }

  const mobileAuthButtons = document.createElement("div");
  mobileAuthButtons.classList.add("mobile-auth-buttons");

  if (authButtons) {
    const loginBtn = authButtons
      .querySelector(".btn-secondary")
      .cloneNode(true);
    const signupBtn = authButtons.querySelector(".btn-primary").cloneNode(true);

    mobileAuthButtons.appendChild(loginBtn);
    mobileAuthButtons.appendChild(signupBtn);
  }

  burgerMenu.addEventListener("click", function () {
    this.classList.toggle("active");
    navItems.style.display = this.classList.contains("active")
      ? "flex"
      : "none";

    const dropdowns = navItems.querySelectorAll(".dropdown");
    dropdowns.forEach((dropdown) => {
      dropdown.addEventListener("click", function (e) {
        if (window.innerWidth <= 1024) {
          e.preventDefault();
          this.classList.toggle("active");
        }
      });
    });

    if (this.classList.contains("active")) {
      navItems.appendChild(mobileAuthButtons);
    } else {
      mobileAuthButtons.remove();
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 1024) {
      navItems.style.display = "";
      burgerMenu.classList.remove("active");
    }
  });

/*  const userTypeLabels = document.querySelectorAll('.user-type-label');

  userTypeLabels.forEach(label => {
    label.addEventListener('click', function() {
      // Remove 'active' class from all labels
      userTypeLabels.forEach(lbl => lbl.classList.remove('active'));

      // Add 'active' class to the clicked label
      this.classList.add('active');
    });
  });*/
  const userTypeInputs = document.querySelectorAll('input[name="user_type"]');
  userTypeInputs.forEach(input => {
      if (input.checked) {
          input.parentElement.classList.add('active');
      }
      input.addEventListener('change', function() {
          userTypeInputs.forEach(inp => inp.parentElement.classList.remove('active'));
          if (this.checked) {
              this.parentElement.classList.add('active');
          }
      });
  });

});
// Responsive Menu End


// Initialize EmailJS
emailjs.init("Sov9QXcN7STkhherR"); 

// Handle form submission
document.getElementById("contactForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const form = event.target;

  // Collect form data
  const formData = {
    name: form.name.value,
    email: form.email.value,
    message: form.message.value,
  };
  const templateParams = {
      from_name: form.name.value,
      to_name: "",
      message: form.message.value,
      reply_to: form.email.value,
  };

  // Send the email using EmailJS
  emailjs.send("service_4l3agts", "template_kgyv5yl", formData)
    .then(response => {
      alert("Your message has been sent successfully!");
      form.reset(); 
    })
    .catch(error => {
      console.error("Error sending email:", error);
      alert("Failed to send your message. Please try again later.");
    });
});