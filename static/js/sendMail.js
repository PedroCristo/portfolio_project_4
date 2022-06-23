// Emailjs script
function sendMail(contactForm) {
    emailjs.send("service_jui1hv6", "tasty_blog_contact", {
        "from_name": contactForm.name.value,
        "surname": contactForm.surname.value,
        "subject": contactForm.subject.value,
        "email": contactForm.email.value,
        "message": contactForm.message.value,
    })
    .then(
        function(response) {
            document.getElementById('email_alert').innerHTML = `<h4 class="email-sent-message alert-success">Thanks for your email!
            <br> We will contact you as soon as possible!</h4>`;
        },
        function(error) {
            document.getElementById('email_alert').innerHTML = `<h4 class="email-sent-message alert-danger">Sorry, something went wrong!
            <br> Try to send the email again.</h4>`;
        }
    );
    return false;  // To block from loading a new page
}