$(document).ready(function(){

    $('#generate').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/generate',
            function(data) {
                console.log(data)
        });
      });

    $('#server').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/server',
            function(data) {
                console.log(data)
        });
      });
});