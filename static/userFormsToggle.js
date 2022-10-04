//Keep form section visible if there is a form error
Array.from(
  document.querySelectorAll('[id$="-form-section"]'))
  .forEach(i => $(i).has(".form-error").show());

//Form section behavior - needs refactoring
$('#email-form-section-show').click(() => {
  $('#email-form-section-show').hide();
  $('#username-form-section-show').show();
  $('#password-form-section-show').show();
  $('#username-form-section').hide();
  $('#password-form-section').hide();
  $('#email-form-section').show();
});

$('#username-form-section-show').click(() => {
  $('#username-form-section-show').hide();
  $('#email-form-section-show').show();
  $('#password-form-section-show').show();
  $('#email-form-section').hide();
  $('#password-form-section').hide();
  $('#username-form-section').show();
});

$('#password-form-section-show').click(() => {
  $('#password-form-section-show').hide();
  $('#email-form-section-show').show();
  $('#username-form-section-show').show();
  $('#email-form-section').hide();
  $('#username-form-section').hide();
  $('#password-form-section').show();
});

$('#email-form-section-hide').click(() => {
  $('#email-form-section').hide();
  $('#email-form-section-show').show();
});

$('#username-form-section-hide').click(() => {
  $('#username-form-section').hide();
  $('#username-form-section-show').show();
});

$('#password-form-section-hide').click(() => {
  $('#password-form-section').hide();
  $('#password-form-section-show').show();
});
