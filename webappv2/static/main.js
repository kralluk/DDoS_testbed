$(document).ready(function(){

    $('#generate').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/generate',
            function(data) {
                console.log(data)
        });
      });
});