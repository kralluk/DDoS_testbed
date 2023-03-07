$(document).ready(function () {
    $("#edit_victim_form").on("submit", function (e) {
      e.preventDefault();
      var formData = $(this).serialize();
  
      $.ajax({
        type: "POST",
        url: "/edit_victim",
        data: formData,
        success: function (data) {
          console.log(data);
          alert(data);
        },
        error: function (xhr, status, error) {
          console.log("Error: " + error);
        },
      });
    });
});

