$("#new-condition").click(function() {
  const $newConditionSelect = $("form").children().first().clone();
  $newConditionSelect.insertBefore($("#new-condition"));
  if($("form div").length > 17) {
    $("#new-condition").prop("disabled", true);
  }
});
