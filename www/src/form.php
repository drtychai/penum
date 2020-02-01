$api_endpoint = $_ENV["API_ENDPOINT"] ?: "http://localhost:5000/api";
$host = "";
$data = "";
// For single host via form
if(isset($_POST["host"]))
{
    $host = $_POST["host"];
    $data = array('hosts' => array("".$host));
    $opts = array(
        'http' => array(
            'method'  => 'POST',
            'content' => json_encode($data),
            'header'=>  "Content-Type: application/json\r\n"
            )
        );

    $context  = stream_context_create($opts);
    $result = file_get_contents($api_endpoint, false, $context);
    $response = $result;
}

// For file of hosts

