//MULTIPLE SEARCH FORM ADD/REMOVE SEARCHFIELDS
const $searchfields = $('.searchfields');

function reindex() {
  const $inputGroup = $searchfields.find('.input-group');
  $inputGroup.each(function(i) {
    const selectedVals = [];
    $(this).children('select').each(function() {
      selectedVals.push($(this).children('option:selected').val());
    });
    const inputVal = $(this).children('input').val();
    const reindexed = $(this).html().replace(/searchfield-[0-9]+/g, `searchfield-${i}`);
    $(this).html(reindexed);
    $(this).children('select').each(function(i) {
      $(this).val(selectedVals[i]);
    });
    $(this).children('input').val(inputVal);
  });
}

function appendRemoveBtn() {
  const $lis = $searchfields.children('li');
  if ($lis.length===2) {
    $lis.each(function() {
      $(this).append(`
        <button type="button" class="remove-searchfield-btn btn btn-outline-danger position-relative ms-3">
          <span class="material-symbols-outlined position-absolute top-50 start-50 translate-middle">close</span>
        </button>
      `);
    });
  }
}

function addNewSearchfield() {
  const $newSearchfield = $searchfields.children().first().clone();
  $newSearchfield.find('input').val('');
  const $firstOptions = $newSearchfield.find('option:first-child');
  makePlaceholder($firstOptions);
  $searchfields.append($newSearchfield);
  appendRemoveBtn();
  reindex();
}

$('#add-searchfield-btn')
  .on('click', () => {
    addNewSearchfield();
  });

$(document)
  .on('click', '.remove-searchfield-btn', function() {
    $(this).parent().remove();
    const $lis = $searchfields.children('li');
    if ($lis.length<2) {
      $('.remove-searchfield-btn').remove();
    }
    reindex();
  });
