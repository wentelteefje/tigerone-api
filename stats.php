<html>
<style>
table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    text-align: left;
    padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
    background-color: #4CAF50;
    color: white;
}
</style>
<body>

<?php
$mysqli = new mysqli("localhost", "mgiapi", "INV.api", "MMU3");

/* check connection */
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}


    $result = mysqli_query($mysqli,"SELECT * FROM stats");

    echo "<table>"; // start a table tag in the HTML
    echo "<tr><th>IP</th><th>Nethash, shares, rejected shares</th><th>Hashes</th><th>Temperatures and Fanspeeds (T,f)</th></tr>";
    while($row = mysqli_fetch_array($result))
      {
      echo "<tr><td><a href=\"http://" . $row['IP'] . ":3333/\">" . $row['IP'] . "</a></td><td>" . $row['NETHASH'] . "</td><td>" . $row['HASHES'] . "</td><td>" . $row['TEMPSFANS'] . "</td>";
      echo "</tr>";
      }
    echo "</table>";


$mysqli->close();
?>

</body>
</html>
