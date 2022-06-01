// Get fully year on the footer
$("#year").text(new Date().getFullYear());

//Parallax effect on scrool
$(window).scroll(function () {
  parallax();
})

function parallax() {

  var wScroll = $(window).scrollTop();

  $(".parallax").css("background-position",
    "center " + (wScroll * 0.60) + "px")
}

//Navbar background and color changes on scrooll

$(document).ready(function () {
  $(window).scroll(function () {
    if ($(document).scrollTop() > 20) {
      $(".navbar").addClass("nav-active")
      $(".nav-link").addClass("nav-active")
      $(".navbar-brand img").addClass("nav-active")
    } else {
      $(".navbar").removeClass("nav-active")
      $(".nav-link").removeClass("nav-active")
      $(".navbar-brand img").removeClass("nav-active")
    }
  });
});

