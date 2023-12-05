document.addEventListener("DOMContentLoaded", () => {
  var socket = io.connect("http://" + "localhost:5000");
  socket.on("connected", () => {
    socket.send("iam connected");
  });

  socket.on("messages", (data) => {
    console.log(`message recieved : ${data}`);
  });
});

$(document).ready(function () {
  var socket = io.connect("http://127.0.0.1:5000/chat/groupchat");
  var socket_messages = io.connect("http://127.0.0.1:5000/chat");
  var currentURL = window.location.href; // Dapatkan URL saat ini
  var reciever = currentURL.substring(currentURL.lastIndexOf("/") + 1);

  // socket.on("connect", function () {
  //   var username = $("#username").val();
  //   if (message_sent) {
  //     socket_messages.emit(username + " connected!");
  //     message_sent = true;
  //   }
  // });

  // $("#adduser_").on("click", function () {
  //   socket_messages.emit("username", reciever);
  // });

  // socket.on("message", function (data) {
  //   var sender = data.split(":")[0];
  //   var message = data.split(":")[1];
  //   var chatMessage = message; // Menghilangkan username dari pesan yang dikirim
  //   console.log(sender, chatMessage);
  //   // Cek apakah pengguna adalah pengirim pesan atau bukan
  //   if (sender === $("#usernames").val()) {
  //     // Menampilkan pesan pengguna sendiri tanpa username
  //     $("#chat-box").append($("<div class='bubble outgoing'>").html("<strong>" + sender + "</strong> : " + chatMessage));
  //   } else {
  //     // Menampilkan pesan pengguna lain dengan username
  //     $("#chat-box").append($("<div class='bubble incoming'>").text(sender + " : " + chatMessage));
  //   }
  // });

  // socket_messages.emit("username", reciever);
  
  // $("form").submit(function (event) {
  //   event.preventDefault();
  //   var message_text = $("#messages").val();
  //   var username = $("#usernames").val();
  //   socket.send(username + ": " + message_text);
  //   // socket.emit(username + ": " + message_text);
  //   console.log("Pesan terkirim:", username + ": " + message_text);

  //   $("#messages").val("");
  // });

document.addEventListener("DOMContentLoaded", () => {
  var socket = io.connect("http://" + "localhost:5000/chat");
  socket.on("connected", () => {
    socket.send("iam connected");
  });

  socket.on("messages", (data) => {
    console.log(`message recieved : ${data}`);
  });
});

$(document).ready(function () {
  var socket = io.connect("http://127.0.0.1:5000");
  var socket_messages = io.connect("http://127.0.0.1:5000/chat");
  var currentURL = window.location.href; // Dapatkan URL saat ini
  var reciever = currentURL.substring(currentURL.lastIndexOf("/") + 1);

  socket.on("connect", function () {
    var username = $("#usersend").val();
    console.log(username, "Has connected");
    socket_messages.emit("connected", username);
  });

  // $("#adduser_").on("click", function () {
  //   socket_messages.emit("username", reciever);
  // });

  socket_messages.emit("username", reciever);

  // Mengambil URL saat ini
  var currentURL = window.location.pathname;

  if (currentURL === "/chat/groupchat") {
    // Kode yang akan dijalankan untuk '/chat/groupchat'
    socket.on("message", function (data) {
      var sender = data.split(":")[0];
      var message = data.split(":")[1];
      var chatMessage = message; // Menghilangkan username dari pesan yang dikirim
      console.log(sender, chatMessage);
      // Cek apakah pengguna adalah pengirim pesan atau bukan
      if (sender === $("#usernames").val()) {
        // Menampilkan pesan pengguna sendiri tanpa username
        $("#chat-box").append($("<div class='bubble outgoing'>").html("<strong>" + sender + "</strong> : " + chatMessage));
      } else {
        // Menampilkan pesan pengguna lain dengan username
        $("#chat-box").append($("<div class='bubble incoming'>").text(sender + " : " + chatMessage));
      }
    });

    $("form").submit(function (event) {
      event.preventDefault();
      var message_text = $("#messages").val();
      var username = $("#usernames").val();
      socket.send(username + ": " + message_text);
      // socket.emit(username + ": " + message_text);
      console.log("Pesan terkirim:", username + ": " + message_text);

      $("#messages").val("");
    });
  } else if (currentURL.startsWith("/chat/")) {
    // Kode yang akan dijalankan untuk '/chat/<username>'


    $("#submited").on("click", function (event) {
      event.preventDefault(); 
      var message_txt = $("#messages").val();
      var username = $("#usernames").val();
      var receiver = currentURL.split("/chat/")[1]; // Mengambil nama penerima dari URL
      function sendPrivateMessage(username, message_txt) {
        var payload = {
          username: username,
          message: message_txt,
        };
        socket_messages.emit("private", payload);
      }
      if (username === $("#usernames").val()) {
        // Menampilkan pesan pengguna sendiri tanpa username
        $("#chat-box").append($("<div class='bubble outgoing'>").html("<strong>" + username + "</strong> : " + message_txt));
      } else {
        // Menampilkan pesan pengguna lain dengan username
        $("#chat-box").append($("<div class='bubble incoming'>").html("<strong>" + username + "</strong> : " + message_txt));
      }
      // console.log(receiver);
      socket_messages.emit("username", receiver);
      sendPrivateMessage(receiver, message_txt);
      console.log("Pesan terkirim:", username + ": " + message_txt, "Ke " + receiver);
      $("#messages").val("");
    });
  }
});

});
