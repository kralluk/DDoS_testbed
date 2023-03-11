$(document).ready(function () {
  // Load bot count on page load
  updateBotCount();

  $("#generate_botnet_form").on("submit", function (e) {
    e.preventDefault();
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/generate_botnet",
      data: formData,
      success: function (data) {
        console.log(data);
        alert(data);
        updateBotCount(); //Updating bot count after generating new ones
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  $("#remove_botnet").click(function (e) {
    e.preventDefault();

    $.ajax({
      url: "/remove_botnet",
      success: function (data) {
        console.log(data);
        updateBotCount(); // updating bot count after removing
        alert("Botnet was removed");
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  
  $("#ping").on("click", function (e) {
    e.preventDefault();
    $.getJSON("/ping", function (data) {
      console.log(data);
    });
  });

  function updateBotCount() {
    $.getJSON('/bot_count', function(data) {
      $('#bot-count').text(data.bot_count);
    });
  }
});


