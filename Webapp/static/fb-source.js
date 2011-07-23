


var stream = "";
var sortedStream = {};

function loginFB() {
	FB.login(function(response) {
	  if (response.session) {
	    // user successfully logged in
		document.getElementById('fb-login').style = "display:none;";
		getStream();
		
	  } else {
	    // user cancelled login
	  }}, {perms: 'read_stream, offline_access'});
}

// download and prepare stream
function getStream () {
    document.elementById('loading-info').style = 'display:block';
	FB.api('/me/home', 'GET', {'limit':500, 'date_format': 'U'}, function(response) {
		stream = response['data'];
		for (x in stream) {
			sortedStream[cleanName(stream[x]['from']['name'])] = stream[x];
		}
		// Loaded FB data
		document.elementById('loading-info').style = 'display:none';
	});
}

// users is array of user IDs of which posts should be shown
function postsWithUsers (users) {
	// Loop over sorted stream and get the posts
	posts = [];
	for (x in users) {
		posts.push(sortedStream[cleanName(users[x])]);
	}
	return posts.sort(postsSorter);
}

// Sorts entries based on their publish dates
function postsSorter (a, b) {
	if (a.created_time > b.created_time)
		return -1;
	else if (a.created_time == b.created_time)
		return 0;
	else
		return 1;
} 

function cleanName (name) {
	return name.replace(/ /g, '');
}

// Renders a post
function renderPost(post) {
	if (post != undefined) {
		html = '<div style="margin-top: 40px; min-height: 45px;"><div style="float:left;"><img src="https://graph.facebook.com/'+post.from.id+'/picture"></div><div style="margin-left: 60px;"><a href="http://www.facebook.com/profile.php?id='+post.from.id+'">'+post.from.name+'</a><br>';
		if (post.message != undefined) {
			html = html+'<p style="margin-top: 5px;">'+post.message+'</p>';
		}
		
		if (post.picture != undefined) {
			html = html + '<img src="'+post.picture+'" style="margin-top: 10px;">';
		}
		
		html = html+'</div></div>';
	}
	return html;
}