$(function() {
  $("#button").click(function() {
    $("#button").addClass("onclic", 100, validate);
  });
function validate() {
    setTimeout(function() {
      $("#button").removeClass("onclic");
      $("#button").addClass("validate", 100, callback);
    }, 2250);
  }
  function callback() {
    setTimeout(function() {
      $("#button").removeClass("validate");
    }, 1250);
  }
});
