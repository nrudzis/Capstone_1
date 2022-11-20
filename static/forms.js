const $formSections = $('[id$="-form-section"]');
const $showFormSectionBtns = $('[id$="-form-section-show"]');
const $hideFormSectionBtns = $('[id$="-form-section-hide"]');

//FORMS SHOW/HIDE
$showFormSectionBtns.click(function(e) {
  $formSections.hide();
  $showFormSectionBtns.show();
  const btnId = e.target.id;
  const formSectionId = btnId.replace('-show', '');
  $('#' + formSectionId).show();
  $('#' + formSectionId)[0].scrollIntoView();
  $('#' + btnId).hide();
});

$hideFormSectionBtns.click(function() {
  $formSections.hide();
  //$(this).parent().hide();
  $showFormSectionBtns.each(function() {
    $(this).show();
  });
});

//Keep form section visible if there is a form error
//Hide other form sections
$formSections.each(function() {
  const $error = $(this).has('.form-error');
  if($error.length>0) {
    const formSectionId = $(this).attr('id');
    $formSections.hide();
    $('#' + formSectionId).show()
    $('#' + formSectionId + '-show').hide();
  }
});

//SELECTS
//Make first option a placeholder
function makePlaceholder(options) {
  options.each(function() {
    $(this)
      .prop('disabled', true)
      .prop('selected', true);
  });
}

const $firstOptions = $('.form-select').find('option:first-child');

makePlaceholder($firstOptions);
