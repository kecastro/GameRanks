$('#search-input-user').keyup(function (event) {
  var query =($('#search-input-user').val());

  if (query != '' || query != ' ') {
    $.ajax({
       type: 'GET',
       url: '/searchuser/',
       data: {'query': query },
       success: function(data) {
          $('#main-results-search-user').html(data);
       },
       error: function(data) {
          console.log(data);
       }
     });
  }
});


$(document).click(function(event) {
  $is_inside = $(event.target).closest('#main-results-search-user').length;

  if( event.target.id == 'search-input-user' || $is_inside ) {
    return;
  }else {
    $('#results-search-user').remove();
  }
});