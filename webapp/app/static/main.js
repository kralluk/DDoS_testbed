$(document).ready(function(){

    $('#generate_botnet_form').on('submit', function(e) {
      e.preventDefault();
      var formData = $(this).serialize();

      $.ajax({
          type: 'POST',
          url: '/generate_botnet',
          data: formData,
          success: function(data) {
              console.log(data);
              alert(data);
          },
          error: function(xhr, status, error) {
              console.log('Error: ' + error);
          }
      });
  });

    // $('#generate_botnet').on('click', function(e) {
    //     e.preventDefault()
    //     $.getJSON('/generate_botnet',
    //         function(data) {
    //             console.log  (data)
    //     });
    //   });
    $('#remove_botnet').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/remove_botnet',
            function(data) {
                console.log(data)
        });
      });
    $('#ping').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/ping',
          function(data) {
              console.log(data)
      });
    });
});