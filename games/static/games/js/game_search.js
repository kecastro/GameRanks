$('#search-input').keyup(function (event) {
  var query =($('#search-input').val());

  if (query != '' || query != ' ') {
    $.ajax({
       type: 'GET',
       url: '/search/',
       data: {'query': query },
       success: function(data) {
          $('#main-results-search').html(data);
       },
       error: function(data) {
          console.log(data);
       }
     });
  }
});


$(document).click(function(event) {
  $is_inside = $(event.target).closest('#main-results-search').length;

  if( event.target.id == 'search-input' || $is_inside ) {
    return;
  }else {
    $('#results-search').remove();
  }
});