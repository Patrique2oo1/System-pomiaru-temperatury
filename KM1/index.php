<!DOCTYPE html>
<html>

<script>
    setInterval(function() {
        location.reload();
    }, 5000);
</script>
<head>
<style>
body
{
	background-color: rgb(32, 32, 32);
	font-family: Consolas;
}
h1
{
	text-align: center;
	color: white;
}
table
{
	width:100%; 
	text-align: center
}
th, tr, td 
{
	font-size: 30px;
	color: white;
	background-color: rgb(128, 128, 128);
	border: 1px solid rgb(128, 128, 128);
	border-radius: 10px;
}
</style>
</head>
<body>

<h1>Projekt bezpiecznego systemu monitoringu temperatury w domu</h1>
<?php
	$minimum_row = null;
	$maksimum_row = null;
	$aktualna_row = null;
	$blad_bazy = false;
	try
	{
		$conn = mysqli_connect("localhost", "root", "");
		mysqli_select_db($conn, "iot_projekt_km1");

		$minimum = "SELECT temperatura, data FROM pomiar WHERE temperatura = (SELECT MIN(temperatura) FROM pomiar) ORDER BY data ASC, pomiar_id ASC LIMIT 1;";
		$minimum_result = mysqli_query($conn, $minimum);
		$minimum_row = mysqli_fetch_assoc($minimum_result);
	
		$maksimum = "SELECT temperatura, data FROM pomiar WHERE temperatura = (SELECT MAX(temperatura) FROM pomiar) ORDER BY data ASC, pomiar_id ASC LIMIT 1;";
		$maksimum_result = mysqli_query($conn, $maksimum);
		$maksimum_row = mysqli_fetch_assoc($maksimum_result);
	
		$aktualna = "SELECT temperatura FROM pomiar ORDER BY data DESC, pomiar_id DESC LIMIT 1;";
		$aktualna_result = mysqli_query($conn, $aktualna);
		$aktualna_row = mysqli_fetch_assoc($aktualna_result);
	}
	catch (mysqli_sql_exception $e)
	{
		$blad_bazy = true;
		error_log($e -> getMessage());
	}
?>
<table>
  <tr>
    <th>Minimalna temperatura</th>
    <th>Aktualna temperatura</th>
    <th>Maksymalna temperatura</th>
  </tr>
  <tr>
    <td><?php echo $minimum_row ? $minimum_row['temperatura']. " *C" : "brak danych";?></td>
    <td rowspan="2"><?php echo $aktualna_row ? $aktualna_row['temperatura']. " *C" : "brak danych";?></td>
    <td><?php echo $maksimum_row ? $maksimum_row['temperatura']. " *C" : "brak danych";?></td>
  </tr>
  <tr>
    <td><?php echo $minimum_row ? $minimum_row['data'] : "brak danych";?></td>

    <td><?php echo $maksimum_row ? $maksimum_row['data'] : "brak danych";?></td>
  </tr>
</table>

</body>
</html>
