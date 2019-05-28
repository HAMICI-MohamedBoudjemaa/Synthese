<!doctype html>
<meta charset="utf-8">
<title>Tweet</title>

<meta name="twitter:widgets:conversation" content="none">
<meta name="twitter:widgets:cards" content="hidden">
<meta name="twitter:widgets:link-color" content="#cc0000">
<meta name="twitter:widgets:theme" content="light">


<body>
<?php
$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");

$filter =[];
$options = [];
$query = new MongoDB\Driver\Query($filter, $options);
$cursor = $manager->executeQuery('benoit.trends', $query);

$trends=array();
foreach ($cursor as $document) {
	$document = json_decode(json_encode($document),true);
	$trends[]=$document['id'];	
}

echo '<form action="#" method="get">
  <select name="trends" size=8 multiple> onchange="onTrendChanged(this)"';
for ($i=0;$i<count($trends);$i++){
	if($i==0) echo '<option value="'.$trends[$i].'" selected>'.$trends[$i].'</option>';
	else echo '<option value="'.$trends[$i].'">'.$trends[$i].'</option>';
}
echo'</select>
<input type="submit" value="Send">
</form>';


if(!isset($_GET['trends'])) {
	//$tendance = $trends[0];
	$tendance = "Batman";
}
else {
	$tendance = $_GET['trends'];
}

$filter =["retweet_count"=>['$gt' => 0],"tendance"=>$tendance];
$options = [];
$query = new MongoDB\Driver\Query($filter, $options);
$cursor = $manager->executeQuery('benoit.tweets', $query);

$ids=array();
foreach ($cursor as $document) {
	$document = json_decode(json_encode($document),true);
	$ids[]= $document['tweet_id'];
	//echo $document['tweet_id'];
}
?>
</body>
<div id="tweets"></div>

<script src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<script>
	var ids = [];
	<?php
	for ($i=0;$i<count($ids);$i++){
		echo 'ids.push('.$ids[$i].');';
	}
	?>
	window.addEventListener('load', function() {
	  twttr.events.bind('rendered', function (event) {
	    //var footer = event.target.contentDocument.querySelector('.footer');
	    //footer.parentNode.removeChild(footer);
	    //var follow = event.target.contentDocument.querySelector('.follow-button');
	    //follow.parentNode.removeChild(follow);
	  });
	  for (var i = 0; i<ids.length ; i++){
		console.log(ids[i]);
	  	twttr.widgets.createTweet(ids[i].toString(), document.getElementById('tweets'));
	  }
	})
</script>
