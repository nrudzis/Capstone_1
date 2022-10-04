/*
// FOR WORK ON REGULAR MULTIPLE SEARCH FORM
$(document).on("click", ".remove-condition", function() {
  $(this).parent().remove();
});

$("#new-condition").click(function() {
  const $newConditionSelect = $("form").children().first().clone();
  $newConditionSelect.insertBefore($("#new-condition"));
  if($("form div").length > 17) {
    $("#new-condition").prop("disabled", true);
  }
});
*/

// FOR WORK ON WTFORMS MULTIPLE SEARCH FORM
$("#multiple-search-form > ul > li").append(
  `<li>
    <table id="searchfield-1">
      <tbody>
        <tr>
          <th>
            <label for="searchfield-1-attribute">Attribute</label>
          </th>
          <td>
            <select id="searchfield-1-attribute" name="searchfield-1-attribute">
              <option value="q_eps_growth_first">Latest Quarterly EPS Growth</option>
              <option value="q_eps_growth_next">1 Quarter Ago Quarterly EPS Growth</option>
              <option value="q_eps_growth_last">2 Quarters Ago Quarterly EPS Growth</option>
              <option value="a_eps_growth_first">Latest Annual EPS Growth</option>
              <option value="a_eps_growth_next">1 Year Ago Annual EPS Growth</option>
              <option value="a_eps_growth_last">2 Years Ago Annual EPS Growth</option>
              <option value="institutional_holders">Institutional Holders</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>
            <label for="searchfield-1-relation">Relation</label>
          </th>
          <td>
            <select id="searchfield-1-relation" name="searchfield-1-relation">
              <option value="greater">></option>
              <option value="less"><</option>
              <option value="equal">=</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>
            <label for="searchfield-1-amount">Amount</label>
          </th>
          <td>
            <input id="searchfield-1-amount" name="searchfield-1-amount" step="any" type="number" value="">
          </td>
        </tr>
      </tbody>
    </table>
  </li>
  <li>
    <table id="searchfield-2">
      <tbody>
        <tr>
          <th>
            <label for="searchfield-2-attribute">Attribute</label>
          </th>
          <td>
            <select id="searchfield-2-attribute" name="searchfield-2-attribute">
              <option value="q_eps_growth_first">Latest Quarterly EPS Growth</option>
              <option value="q_eps_growth_next">1 Quarter Ago Quarterly EPS Growth</option>
              <option value="q_eps_growth_last">2 Quarters Ago Quarterly EPS Growth</option>
              <option value="a_eps_growth_first">Latest Annual EPS Growth</option>
              <option value="a_eps_growth_next">1 Year Ago Annual EPS Growth</option>
              <option value="a_eps_growth_last">2 Years Ago Annual EPS Growth</option>
              <option value="institutional_holders">Institutional Holders</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>
            <label for="searchfield-2-relation">Relation</label>
          </th>
          <td>
            <select id="searchfield-2-relation" name="searchfield-2-relation">
              <option value="greater">></option>
              <option value="less"><</option>
              <option value="equal">=</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>
            <label for="searchfield-2-amount">Amount</label>
          </th>
          <td>
            <input id="searchfield-2-amount" name="searchfield-2-amount" step="any" type="number" value="">
          </td>
        </tr>
      </tbody>
    </table>
  </li>`)


$('#ticker-search-form-section-show').click(() => {
  $('#multiple-search-form-section').hide();
  $('#ticker-search-form-section').show();
});

$('#multiple-search-form-section-show').click(() => {
  $('#ticker-search-form-section').hide();
  $('#multiple-search-form-section').show();
});
