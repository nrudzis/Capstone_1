/*
// FOR WORK ON REGULAR FORM
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

// FOR WORK ON WTFORMS FORM
$("ul").append(
  `<li>
    <label for="search-1">Search-1</label>
    <table id="search-1">
      <tbody>
        <tr>
          <th>
            <label for="search-1-attribute">Attribute</label>
          </th>
          <td>
            <select id="search-1-attribute" name="search-1-attribute">
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
            <label for="search-1-relation">Relation</label>
          </th>
          <td>
            <select id="search-1-relation" name="search-1-relation">
              <option value="greater">></option>
              <option value="less"><</option>
              <option value="equal">=</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>
            <label for="search-1-amount">Amount</label>
          </th>
          <td>
            <input id="search-1-amount" name="search-1-amount" step="any" type="number" value="">
          </td>
        </tr>
      </tbody>
    </table>
  </li>
  <li>
    <label for="search-2">Search-2</label>
    <table id="search-2">
      <tbody>
        <tr>
          <th>
            <label for="search-2-attribute">Attribute</label>
          </th>
          <td>
            <select id="search-2-attribute" name="search-2-attribute">
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
            <label for="search-2-relation">Relation</label>
          </th>
          <td>
            <select id="search-2-relation" name="search-2-relation">
              <option value="greater">></option>
              <option value="less"><</option>
              <option value="equal">=</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>
            <label for="search-2-amount">Amount</label>
          </th>
          <td>
            <input id="search-2-amount" name="search-2-amount" step="any" type="number" value="">
          </td>
        </tr>
      </tbody>
    </table>
  </li>`)
