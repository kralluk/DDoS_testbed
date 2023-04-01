$(document).ready(function () {
     
  $("#slowloris_form").on("submit", function (e) {
    e.preventDefault();
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/slowloris",
      data: formData,
      success: function (data) {
        console.log(data);
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  $("#slow_read_form").on("submit", function (e) {
    e.preventDefault();
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/slow_read",
      data: formData,
      success: function (data) {
        console.log(data);
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  $("#icmp_flood").on("submit", function (e) {
    e.preventDefault();
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/icmp_flood",
      data: formData,
      success: function (data) {
        console.log(data);
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  $("#udp_flood_form").on("submit", function (e) {
    e.preventDefault();
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/udp_flood",
      data: formData,
      success: function (data) {
        console.log(data);
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });

  $("#stop_attack").on("click", function (e) {
    e.preventDefault();
    $.getJSON("/stop_attack", function (data) {
      console.log(data);
    });
  });

  $("#attack_option").change(function () {
    // Get the selected value and associated form element
    var selectedOption = $(this).val();
    var formElement = $("#" + $(this).find("option:selected").data("form"));

    // Hide all form elements and show the selected form element
    $(".option-form").hide();
    formElement.show();
  });

  document
    .getElementById("spoof_select")
    .addEventListener("change", function () {
      var inputDiv = document.getElementById("ip_address_input");
      if (this.value === "yes") {
        inputDiv.style.display = "block";
      } else {
        inputDiv.style.display = "none";
      }
    });
});

