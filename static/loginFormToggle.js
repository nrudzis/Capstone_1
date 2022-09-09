$('#register-section').hide();

$('#register-section-show').click(() => {
  $('#login-section').hide();
  $('#register-section').show();
});

$('#login-section-show').click(() => {
  $('#register-section').hide();
  $('#login-section').show();
});
