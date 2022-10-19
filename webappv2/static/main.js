$(document).ready(function(){

    $('#info').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/info',
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
    $('#add_attacker').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/add_attacker',
            function(data) {
                console.log(data)
        });
      });
    $('#remove_attacker').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/remove_attacker',
            function(data) {
                console.log(data)
        });
      });
});