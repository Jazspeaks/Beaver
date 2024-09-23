document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.form');
  
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      // Example of handling form submission
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
  
      console.log('Email:', email);
      console.log('Password:', password);
  
      // Here you could add logic to send the form data to a server or show a success message
    });
  });
  