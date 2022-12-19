function Tweet(data) {
    this.id = ko.observable(data.id);
    this.username = ko.observable(data.username);
    this.body = ko.observable(data.body);
    this.timestamp = ko.observable(data.timestamp);
}

function TweetListViewModel() {
    var self = this;
    self.tweets_list = ko.observableArray([]);
    self.username= ko.observable();
    self.body= ko.observable();
    self.addTweet = function() {
	self.save();
	self.username("");
	self.body("");
    };

    $.getJSON('/api/v3/tweets', function(tweetModels) {
	var t = $.map(tweetModels.tweets_list, function(item) {
		//alert(JSON.stringify(item))
	    return new Tweet(item);
	});
	self.tweets_list(t);
    });
	
    self.save = function() {
	var uname = self.username();
	var tbody = self.body()
	$.getJSON('/api/v3/tweets', function(tweetModels) {
	var t = $.map(tweetModels.tweets_list, function(item) {
	    return new Tweet(item);
	});
	self.tweets_list(t);
    });
	return $.ajax({
	    url: '/api/v3/tweets',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'username': uname,
		'body': tbody,
	    }),
	    success: function(data) {
          alert("success")
		      console.log("Pushing to users array");
			  self.tweets_list.push(new Tweet({username: uname,body: tbody, timestamp: "now"}));
		      return;
	    },
	    error: function() {
		return console.log("Failed");
	    }
	});
    };
}

ko.applyBindings(new TweetListViewModel());
