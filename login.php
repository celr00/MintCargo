<?php

  // Credenciales
  define("DB_SERVER", "localhost:3307");
  define("DB_USERNAME", "root");
  define("DB_PASSWORD", "");
  define("DB_NAME", "mintcargo");

  // Conectar a la base de datos
  $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
  if ($link === false) {
    die("Error..." . mysqli_connect_error());
    header("Location: index.html?msg=Database not connected");
  }

  // Correo y contraseña
  $email = $_POST["email"];
  $pass = $_POST["pass"];

  $sql = "SELECT 1 FROM users WHERE email = '$email' and password = '$pass';";
  $result = mysqli_query($link, $sql);
  if (mysqli_num_rows($result) > 0) {
    header("Location: home.html");
  } else {
    header("Location: index.html?msg=Wrong credentials...");
  }

  mysqli_close($link);
?>