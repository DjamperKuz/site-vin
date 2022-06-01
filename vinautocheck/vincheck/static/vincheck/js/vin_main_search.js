$(document).ready(
  $('#vin').submit(function(e){
    e.preventDefault();
    var serializedData = $(this).serialize();

    $.ajax({
      type:"POST",
      url: "",
      data:  serializedData,
      success: function(data){
        $("#vin").text(data["vin"]);
      }
    });
  })
);
