$(document).ready(function () {
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
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  $("#remove_botnet").click(function (e) {
    e.preventDefault();

    $.ajax({
      // type: "POST",
      url: "/remove_botnet",
      success: function (data) {
        console.log(data);
        alert("Botnet was removed");
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  // $("#remove_botnet").on("click", function (e) {
  //   e.preventDefault();
  //   $.getJSON("/remove_botnet", function (data) {
  //     console.log(data);
  //   });
  // });
  $("#ping").on("click", function (e) {
    e.preventDefault();
    $.getJSON("/ping", function (data) {
      console.log(data);
    });
  });
  $("#icmp_flood").on("click", function (e) {
    e.preventDefault();
    $.getJSON("/icmp_flood", function (data) {
      console.log(data);
    });
  });
  $("#stop_attack").on("click", function (e) {
    e.preventDefault();
    $.getJSON("/stop_attack", function (data) {
      console.log(data);
    });
  });
});
