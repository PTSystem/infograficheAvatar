<?php
if(isset($_GET['citta']) && isset($_GET['tipologia']))
{
  

  //Check e passiamo solo nel caso in cui entrambi i parametri passati
  if (/* VALIDAZIONE INPUT E SANITIZE */)
  {
    //Clear the cache
    clearstatcache();


    $path = /* PDF PATH */;
    $name = $citta.$tipologia;
    //Check the file path exists or not
    if(file_exists($path)) {

      //Define header information
      header('Content-Description: File Transfer');
      header('Content-Type: application/octet-stream');
      header('Content-Disposition: attachment; filename="'.$name."_".date('d/m/y').".pdf");
      header('Content-Length: '.filesize($path));
      header('Pragma: public');

      //Clear system output buffer
      flush();

      //Read the size of the file
      readfile($path,true);

      //Terminate from the script
      die();
    }
    else{
      echo "File not found";
    }
  }
  else if (/* VALIDAZIONE INPUT E SANITIZE */){
    //Clear the cache
    clearstatcache();


    $path = /* PDF PATH */;
    $name = $citta.$tipologia;
    //Check the file path exists or not
    if(file_exists($path)) {

      //Define header information
      header('Content-Description: File Transfer');
      header('Content-Type: application/octet-stream');
      header('Content-Disposition: attachment; filename="'.$name."_".date('d/m/y').".pdf");
      header('Content-Length: '.filesize($path));
      header('Pragma: public');

      //Clear system output buffer
      flush();

      //Read the size of the file
      readfile($path,true);

      //Terminate from the script
      die();
    }
    else{
      echo "File not found";
    }
  }
  else
  {
    echo "File not found";
  }

}
if(isset($_GET['helper'])){
  // Dobbiamo verificare quale dei due file restituire all'utente
  if ($_GET['helper'] == "Presentazione"){
    $path = /* PDF PATH */;
    $name = "Presentazione_Rawgraphs.pdf";
  } else if ($_GET['helper'] == "Documentazione") {
    $path = /* PDF PATH */;
    $name = "Documentazione_Rawgraphs.pdf";
  } else {
    http_response_code(404);
    include('my_404.php'); // provide your own HTML for the error page
    die();
  }
  if(file_exists($path)) {
    //Define header information
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="'.$name);
    header('Content-Length: '.filesize($path));
    header('Pragma: public');

    //Clear system output buffer
    flush();

    //Read the size of the file
    readfile($path,true);
  }
}
http_response_code(404);
include('my_404.php'); // provide your own HTML for the error page
die();

?>
