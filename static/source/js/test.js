$(document).ready(function () {
  $(".person").on("click", function () {
    $(this).toggleClass("focus").siblings().removeClass("focus");
  });
  $(".person").on("click", function () {
    var username = $(this).find(".title").text();
    $(".name").text(username);
  });
  $(".groups").on("click", function () {
    var username = $(this).find(".title").text();
    $(".name").text(username);
  });

});

$(document).ready(function () {
  var currentURL = window.location.href; // Dapatkan URL saat ini
  var username = currentURL.substring(currentURL.lastIndexOf("/") + 1);
  // Cek apakah URL saat ini sesuai dengan URL tautan
  if (currentURL === "http://localhost:5000/chat/" + username) {
    // Ganti dengan URL tautan yang sesuai
    $("#" + username).removeAttr("href"); // Hapus atribut href untuk menonaktifkan tautan
    $("#" + username).click(function (event) {
      event.preventDefault(); // Mencegah perilaku bawaan klik pada tautan
    });
    
    $(".name").text(username);
  }
});