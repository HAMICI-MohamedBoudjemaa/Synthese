<!doctype html>
<meta charset="utf-8">
<title>Tweet</title>

<meta name="twitter:widgets:conversation" content="none">
<meta name="twitter:widgets:cards" content="hidden">
<meta name="twitter:widgets:link-color" content="#cc0000">
<meta name="twitter:widgets:theme" content="light">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">


<body>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">WebSiteName</a>
    </div>
    <ul class="nav navbar-nav">
      <li class="active"><a href="#">Home</a></li>
      <li><a href="#">Page 1</a></li>
      <li><a href="#">Page 2</a></li>
      <li><a href="#">Page 3</a></li>
    </ul>
  </div>
</nav>
<?php

function convertTimestamp($t){
	$parts=array();
	$parts = explode(" ", $t);
	$monthes = ['Janvier', 'Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'];
	$days = ['Lundi','Mardi','Jeudi','Vendredi','Samedi','Dimanche'];
	switch($parts[0]) {
		case "Mon":$jour=$days[0];break;
		case "Tue":$jour=$days[1];break;
		case "Wed":$jour=$days[2];break;
		case "Thu":$jour=$days[3];break;
		case "Fri":$jour=$days[4];break;
		case "Sat":$jour=$days[5];break;
		case "Sun":$jour=$days[6];break;
		default:
	}
	switch($parts[1]) {
		case "Jan":$mois=$monthes[0];break;
		case "Feb":$mois=$monthes[1];break;
		case "Mar":$mois=$monthes[2];break;
		case "Apr":$mois=$monthes[3];break;
		case "May":$mois=$monthes[4];break;
		case "Jun":$mois=$monthes[5];break;
		case "Jul":$mois=$monthes[6];break;
		case "Aug":$mois=$monthes[7];break;
		case "Sep":$mois=$monthes[8];break;
		case "Oct":$mois=$monthes[9];break;
		case "Nov":$mois=$monthes[10];break;
		case "Dec":$mois=$monthes[11];break;
		default:
	}
	$number = $parts[2];
	$time = $parts[3];
	$year = $parts[5];
	return $jour.' '.$number.' '.$mois.' '.$year.' - '.$time;
}
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
/////////////////////////////////////////////STATS//////////////////////////////////////////
/**** obtenir la date du 1er tweet ****/
$filter =["tendance"=>$tendance];
$options = ["sort" => ["created"=>-1],"limit" => 1];
$query = new MongoDB\Driver\Query($filter, $options);
$cursor = $manager->executeQuery('benoit.tweets', $query);
foreach ($cursor as $document) {
	$document = json_decode(json_encode($document),true);
	$premiere_date = convertTimestamp($document['created']);	
}

/**** obtenir nombre d'utilisateurs differents ******/
$filter =["tendance"=>$tendance];
$options = ["sort" => ["screen_name"=>1]];
$query = new MongoDB\Driver\Query($filter, $options);
$cursor = $manager->executeQuery('benoit.tweets', $query);
$i=0;
$count_tweets=0;
$count_retweets=0;
$count_different_users=0;
$last_user="";
foreach ($cursor as $document) {
	$document = json_decode(json_encode($document),true);
	if($i!=0){
		if($document['screen_name']!=$last_user){
			$count_different_users++;
		}
	}
	else{$count_different_users++;}
	$count_tweets++;
	$count_retweets += $document['retweet_count'];
	$last_user = $document['screen_name'];
	$i++;	
}
echo '<h1 style="font-size: 30px;line-height: 20px; font-family: Garamond, cursive;"> Statistiques de l\'événement '.$tendance.'</h3>
<div id="stats">
<p>Date premier tweet : '.$premiere_date.'</p>
<p>Nombre de tweets : '.$count_tweets.'</p>
<p>Nombre de retweets : '.$count_retweets.'<p>
<p>Personnes qui parlent à ce sujet : '.$count_different_users.'<p>
</div>';

$filter =["followers"=>['$gt' => 100000],"tendance"=>$tendance];
$options = ["sort" => ["created"=>1]];
$query = new MongoDB\Driver\Query($filter, $options);
$cursor = $manager->executeQuery('benoit.tweets', $query);

$ids=array();

echo('<h1 style="font-size: 30px;line-height: 20px; font-family: Garamond, cursive;"> Tweets majeurs de l\'événement '.$tendance.'</h3>
<div id="tweet_container">');
foreach ($cursor as $document) {
	$document = json_decode(json_encode($document),true);
	$ids[]= $document['tweet_id'];
	echo '<h3 style="font-size: 16px;line-height: 20px; font-family: Garamond, cursive;">'.convertTimestamp($document['created']).'</h3>';
	echo '<div style ="border:3px solid skyblue;display:inline-block;">';
	echo $document['username'].' <b>@'.$document['screen_name'].'</b> ('.$document['followers'].' followers) :';
	echo '<br />&nbsp;';
	echo '<br />&nbsp;';
	echo $document['tweet_text'];
	echo '</div>';
	echo '<br />&nbsp;';
	echo '<br />&nbsp;';
}
echo('</div>');
?>

<div id="tweets"></div>
</body>


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
