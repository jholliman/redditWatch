google.charts.load('current', {packages: ['corechart', 'line', 'timeline']});

function WallStreetBots() {
	this.checkSetup();
	this.initFirebase();

	this.database.ref('/').once('value').then(function(data) {
		var val = data.val();
		console.log(val);
	}.bind(this));
};

WallStreetBots.prototype.initFirebase = function() {
	firebase.auth().onAuthStateChanged(this.onAuthStateChanged.bind(this));
	this.auth = firebase.auth();
	this.database = firebase.database();
};

WallStreetBots.prototype.checkSetup = function() {
	if (!window.firebase || !(firebase.app instanceof Function) || !window.config) {
	  window.alert('Firebase SDK missing');
	} else if (config.storageBucket === '') {
	  window.alert('Your Firebase Storage bucket has not been enabled.');
	}
};

WallStreetBots.prototype.onAuthStateChanged = function(user) {
	/*
	if (user) {
		  this.button_signin.style.display = 'none';
		  this.data_section.style.display = '';
		  
		  this.updateDataRange();
	  } else {
		  this.button_signin.style.display = '';
		  this.data_section.style.display = 'none';
	}
	*/
};

window.onload = function() {
  window.WallStreetBots = new WallStreetBots();
};
