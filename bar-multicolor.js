$(document).ready(function () {

	var ctx = $("#bar-chartcanvas");

	var data = {
		labels : ["Jack", "Manvendra", "Mike", "Tits", "Vibhas"],
		datasets : [
			{
				label : "Insertions",
				data : [10, 50, 25, 70, 40],
                backgroundColor : "lime",
				
				borderWidth : 1
			},
			{
				label : "Deletions",
				data : [20, 35, 40, 60, 50],
				
                backgroundColor : "aqua",
				
				borderWidth : 1
			},
            {
				label : "Comments",
				data : [56, 95, 11, 23, 50],
				
                backgroundColor : "mintcream",
				
				borderWidth : 1
			}
		]
	};

	var options = {
		title : {
			display : true,
			position : "top",
			text : "Contributions Histogram",
			fontSize : 18,
			fontColor : "#111"
		},
		legend : {
			display : false
		},
		scales : {
			 xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: true
            }]
		}
	};

	var chart = new Chart( ctx, {
		type : "horizontalBar",
		data : data,
		options : options
	});

});