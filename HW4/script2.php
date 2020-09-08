<?php

// make sure browsers see this page as utf-8 encoded HTML
header('Content-Type: text/html; charset=utf-8');

$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;

if ($query)
{
$choice = isset($_REQUEST['sort'])? $_REQUEST['sort'] : "Lucene";
  // The Apache Solr Client library should be on the include path
  // which is usually most easily accomplished by placing in the
  // same directory as this script ( . or current directory is a Lucene
  // php include path entry in the php.ini)

  require_once('solr-php-client-master/Apache/Solr/Service.php');

  // create a new solr service instance - host, port, and webapp
  // path (all Lucenes in this example)
  $solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample');

  //if ( $solr->ping() ) {
  //   echo 'Solr Server Responding.';
      // your code
  //  }else{
  //    echo "Solr Server is not Running";
  //  }
	
  // if magic quotes is enabled then stripslashes will be needed
  if (get_magic_quotes_gpc() == 1)
  {
    $query = stripslashes($query);
  }

  // in production code you'll always want to use a try /catch for any
  // possible exceptions emitted  by searching (i.e. connection
  // problems or a query parsing error)
  try
  {
  if($choice == "Lucene")
     $additionalParameters=array('sort' => '');
    else{

    $additionalParameters=array('sort' => 'pageRankFile desc');
	
}
    $results = $solr->search($query, 0, $limit, $additionalParameters);
	
  }
  catch (Exception $e)
  {

    // in production you'd probably log or email this error to an admin
    // and then show a special message to the user but for this example
    // we're going to show the full exception
    die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
  }
}

?>
<html>
  <head>
    <title>Homework 4</title>
  </head>
  <body>
    <form  accept-charset="utf-8" method="get" >
      <label for="q">Search:</label>
      <input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/>
      <input type="submit" value="Submit"/>
<br/>
    <input type="radio" name="sort" value="pagerank" <?php if(isset($_REQUEST['sort']) && $choice == "pagerank") { echo 'checked="checked"';} ?>>Page Rank
    <input type="radio" name="sort" value="Lucene" <?php if(isset($_REQUEST['sort']) && $choice == "Lucene") { echo 'checked="checked"';} ?>>Lucene
    </form>
<?php


$arrFromCSV =  array_map('str_getcsv', file('URLtoHTML_latimes_news.csv'));
if ($results)
{
  $total = (int) $results->response->numFound;
  $start = min(1, $total);
  $end = min($limit, $total);
  $stack = [];
echo "  <div>Results $start -  $end of $total :</div> <ol>";

foreach ($results->response->docs as $doc)
  {  
    $id = $doc->id;
    $title = $doc->title;
   $des = $doc->description;

   if($title=="" ||$title==null){
     $title = $doc->dc_title;
     if($title=="" ||$title==null)
       $title="N/A";
   }
	if($des=="" ||$des==null)
{
       $des="N/A";
   }
   
   $id1 = $id;
   $id = str_replace("/home/ananya/Desktop/SolrHW/latimes/","",$id);
   foreach($arrFromCSV as $row)
   {
    if($id==$row[0])
    {
      $url = $row[1];
      break;
    }
   }
   unset($row);
   //derror_reporting(E_ALL ^ E_NOTICE);  
    echo " <li>   
	Title: <a href='$url' target='_blank'>$title</a> </br>
	URL: <a href='$url' target='_blank'>$url</a> </br>
	Description: $des</br>
	ID: $id2 </br>
	</br></li>";
  array_push($stack,$id1);

}
  echo "</ol>";
  
}				
?>

  </body>
</html>
