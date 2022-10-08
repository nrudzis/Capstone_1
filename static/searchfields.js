//MULTIPLE SEARCH FORM ADD/REMOVE SEARCHFIELDS
const $searchfields = $('.searchfields');

function reindex() {
  let $lis = $searchfields.children('li');
  $lis.each(function(i) {
    let $reindexed = $(this).html().replace(/searchfield-[0-9]+/g, `searchfield-${i}`);
    $(this).html($reindexed);
  });
}

function appendRemoveBtn() {
  let $lis = $searchfields.children('li');
  if ($lis.length===2) {
    $lis.each(function() {
      $(this).append(`<button type="button" class="remove-searchfield-btn">X</button>`);
    });
  }
}

function addNewSearchfield() {
  let $newSearchfield = $searchfields.children().first().clone();
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
    let $lis = $searchfields.children('li');
    if ($lis.length<2) {
      $('.remove-searchfield-btn').remove();
    }
    reindex();
  });
