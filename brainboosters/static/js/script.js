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
      const welcomeMessage = authButtons.querySelector("p");
      navItems.insertBefore(welcomeMessage, navItems.firstChild);
      navItems.appendChild(mobileAuthButtons);

      // Welcome Name! message change color, emoji, and font-weight for the  when mobile menu is active
      welcomeMessage.style.color = "#C63D9F";
      welcomeMessage.style.fontWeight = "700";
      welcomeMessage.style.fontSize = "18px";
      welcomeMessage.style.marginBottom = "18px";

      // Emoji
      welcomeMessage.innerHTML = "👋 " + welcomeMessage.innerText.trim();
    } else {
      const welcomeMessage = authButtons.querySelector("p");
      navItems.appendChild(welcomeMessage);
      mobileAuthButtons.remove();

      // Reset styles when mobile menu is inactive
      welcomeMessage.style.color = "";
      welcomeMessage.style.fontWeight = "";
      welcomeMessage.style.fontSize = "";
      welcomeMessage.style.marginBottom = "";
      // Emoji correctly placed
      welcomeMessage.innerHTML = welcomeMessage.innerText.trim();
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
  userTypeInputs.forEach((input) => {
    if (input.checked) {
      input.parentElement.classList.add("active");
    }
    input.addEventListener("change", function () {
      userTypeInputs.forEach((inp) =>
        inp.parentElement.classList.remove("active")
      );
      if (this.checked) {
        this.parentElement.classList.add("active");
      }
    });
  });

  const observerOptions = {
    root: null, // viewport
    threshold: 0.2, // Trigger when 20% of the section is visible
  };

  const aboutSection = document.querySelector(".about");

  if (aboutSection) {
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          aboutSection.querySelector(".left").classList.add("show");
          aboutSection.querySelector(".right").classList.add("show");
          observer.unobserve(entry.target); 
        }
      });
    }, observerOptions);

    observer.observe(aboutSection);
  }

  const tutorLeftSide = document.querySelector(".tutor .left");
  const tutorRightSide = document.querySelector(".tutor .right");
  const parentLeftSide = document.querySelector(".parents .left");
  const parentRightSide = document.querySelector(".parents .right");

  // Create the IntersectionObserver to trigger animations
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
        }
      });
    },
    { threshold: 0.2 }  // Trigger when 20% of the element is visible
  );

  // Observe the left and right sides for animation trigger
  observer.observe(tutorLeftSide);
  observer.observe(tutorRightSide);
  observer.observe(parentLeftSide);
  observer.observe(parentRightSide);

});
// Responsive Menu End

// Initialize EmailJS
emailjs.init("Sov9QXcN7STkhherR");

// Handle form submission
document
  .getElementById("contactForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const form = event.target;

    // Collect form data
    // const templateParams = {
    //   name: form.name.value,
    //   email: form.email.value,
    //   message: form.message.value,
    // };
    const templateParams = {
      from_name: form.name.value,
      to_name: "",
      message: form.message.value,
      reply_to: form.email.value,
    };

    // Send the email using EmailJS
    emailjs
      .send("service_4l3agts", "template_tcz0sbg", templateParams)
      .then((response) => {
        alert("Your message has been sent successfully!");
        form.reset();
      })
      .catch((error) => {
        console.error("Error sending email:", error);
        alert("Failed to send your message. Please try again later.");
      });
  });
