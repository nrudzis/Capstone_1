//Confirmation message to send
function deleteMessage($dForm) {
  if($dForm.is('#wlc-delete')) {
    const wlcCompany = $dForm.parent().siblings().find('.lg-item-heading').text();
    const wlcWatchlist = $('h1').text();
    return `Remove ${wlcCompany} from '${wlcWatchlist}'?`;
  }
  if($dForm.hasClass('wl-delete')) {
    if($dForm.is('#wl-delete-dpage')) {
      const wlDPageWatchlist = $('h1').text();
      return `Delete '${wlDPageWatchlist}'?`;
    } else {
      const wlLPageWatchlist= $dForm.parent().siblings().find('.lg-item-heading').text();
      return `Delete '${wlLPageWatchlist}'?`;
    }
  }
  if($dForm.is('#u-delete')) {
    return 'Delete your account? Your login credentials and watchlists will be permanently deleted. This cannot be undone.';
  }
}

//Prompt user to confirm delete
$('.delete-form').submit(function(e) {
  let dMessage = deleteMessage($(this));
  if (window.confirm(dMessage)) {
    return;
  } else {
    e.preventDefault();
  }
});
