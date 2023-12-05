$(document).ready(function () {
  var socket = io.connect("http://127.0.0.1:5000");
  socket.on("connect", function () {
    var username = $("#username").val();
    if (message_sent) {
      socket.emit(username + " connected!");
      message_sent = true;
    }
  });
  socket.on("message", function (data) {
    var sender = data.split(":")[0];
    var message = data.split(":")[1];
    var chatMessage = message; // Menghilangkan username dari pesan yang dikirim

    // Cek apakah pengguna adalah pengirim pesan atau bukan
    if (sender === $("#username").val()) {
      // Menampilkan pesan pengguna sendiri tanpa username
      $("#chat-box").append($("<div class='button-47 sent-message'>").text(chatMessage));
    } else {
      // Menampilkan pesan pengguna lain dengan username
      $("#chat-box").append($("<div class='button-47 received-message'>").text(sender + " : " + chatMessage));
    }
  });

  $("form").submit(function (event) {
    event.preventDefault();
    var message_text = $("#messagecht").val();
    var username = $("#username").val();
    socket.send(username + ": " + message_text);
    console.log("Pesan terkirim:", username + ": " + message_text);
    $("#messagecht").val("");
  });
});
