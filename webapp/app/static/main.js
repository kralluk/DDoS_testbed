$(document).ready(function(){

   
    $('#generate_botnet').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/generate_botnet',
            function(data) {
                console.log(data)
        });
      });
    $('#remove_botnet').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/remove_botnet',
            function(data) {
                console.log(data)
        });
      });
});