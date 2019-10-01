<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
 
// database connection will be here
// include database 
include_once 'con.php';

// get posted data
$data = json_decode(file_get_contents("php://input"));

if(!empty($data->name)){
    $db=new DB();
    $conn=$db->connect();
    $sql="select * from mentor where fname='".$data->name."'";
    $result=$db->get_data($conn,$sql);
    $records_arr=array();
    $records_arr["records"]=array();
    if (mysqli_num_rows($result) > 0) {
        while( $row =mysqli_fetch_assoc($result)){
            extract($row);
            $record_item=array(
                "name" => $fname,
                "email" => $email,
                "nic" =>$nic,
                "mobile" => $mobile
            );
            array_push($records_arr["records"], $record_item);
        }
        // set response code - 200 OK
        http_response_code(200);
    
        // show products data in json format
        echo json_encode($records_arr);
    }else{
         // set response code - 404 Not found
        http_response_code(404);
    
        // tell the user no products found
        echo json_encode(
            array("message" => "No products found.")
        );
    }
    $db->disconnect($conn);
   
}else{
    http_response_code(404);
}