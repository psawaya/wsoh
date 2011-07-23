<?PHP
// fb-import.php

// JSON: FB ID, full name, FB image

session_start();
require 'FB-SDK/facebook.php';

// Get new Facebook instance
$fb = new Facebook (array (
	'appId' => '259190380763066',
	'secret' => '3638f662872fba7fb1afe4a59b350f50'
	));
	
// Catch OAuth
if ($mode="oauth-login") {
	// Get access token from code
	try {
		$accesToken = $fb->getAccessTokenFromCode($_GET['code']);
		if ($accessToken != false)
			$_SESSION['accessToken'] = $accessToken;
	} catch (Exception $e) {
		die ('Exception when trying to convert code to accessToken: '.print_r($e, true));
	}
}

// Check whether the user is logged in, if not redirect to login
if ($fb->getUser() == 0) {
	$params = array(
		'redirect_uri' => 'http://localhost/FBCircles/fb-import.php?mode=oauth-login',
		'scope' => ''
	);
	header('Location:'.$fb->getLoginUrl($params));
}

$myUserID = $fb->getUser();

$users = array();
$edges = array();

// Get friends of user
$friends = $fb->api('me/friends');

$me = $fb->api('me');
$users[] = array('uid' => $me['id'],
				 'name' => $me['name'],
				 'pic' => 'https://graph.facebook.com/'.$me['uid'].'/picture?access_token='.$fb->getAccessToken());

// Loop over friends and get their friends
$cnt = 0;
$batch = array();
foreach ($friends['data'] as $friend) {
	
	// Add edge
	$edges[][$myUserID] = $friend['id'];
	$batch[] = $friend['id'];
	
	if ($cnt >= 100) {
		// create FQL batch query
		
	}
	
	$cnt++;
	
	/*// Get friend's info
	$friendInfo = $fb->api($friend['id']);
	$users[] = array('uid' => $friend['id'],
					 'name' => $friendInfo['name'],
					 'pic' => 'https://graph.facebook.com/'.$friend['id'].'/picture?access_token='.$fb->getAccessToken());
	
	// Get friend's friends
	$secondDegreeFriends = $fb->api('fql.query', array('query' => 'SELECT uid2 FROM friend WHERE uid1 = '.$friend['id']));
	
	foreach ($secondDegreeFriends as $secondFriend) {
		$edges[][$friend['id']] = $secondFriend['uid2'];
		
		// Get info about second degree friend
		$secondFriendInfo = $fb->api($secondFriend['uid2']);
		$users[] = array('uid' => $secondFriend['uid2'],
						 'name' => $secondFriendInfo['name'],
						 'pic' => 'https://graph.facebook.com/'.$secondFriend['uid2'].'/picture?access_token='.$fb->getAccessToken());
	}*/
}

$finalArray = array('users' => $users, 'edges' => $edges);
print_r($finalArray);

?>