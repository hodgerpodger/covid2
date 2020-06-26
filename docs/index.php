<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="style.css">

    <title>Covid Graphs</title>
  </head>

  <body>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>

  <div class="container-fluid">

    <h2>Daily New Cases</h2>

<?php
// usage: php index.php > index.html

$str = file_get_contents("../counties.json");
$counties = json_decode($str, true);

echo "<ul>\n";
foreach ($counties as $index => $array) {
    $county = $array[0];
    $state = $array[1];
    $label = $array[2];

    echo "<li><a href=\"#{$label}\"> {$county} County </a></li>\n";


}
echo "</ul>\n";

foreach ($counties as $index => $array) {
    $county = $array[0] . " County";
    $label = $array[2];

    echo "
    <div class=\"row\"><h4>$county</h4></div>
    <div class=\"row\">
        <a name=\"{$label}\"></a>
        <div class=\"col-6\"><a href=\"images/{$label}_1.png\"><img src=\"images/{$label}_1.png\"></a></div>
        <div class=\"col-6\"><a href=\"images/{$label}_2.png\"><img src=\"images/{$label}_2.png\"></a></div>
    </div>
    ";
}

?>

  </div>
  </body>
</html>