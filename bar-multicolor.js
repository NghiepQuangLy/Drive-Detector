$(document).ready(function () {
function create_histogram(drive_name, file_name, users, insertions, deletions, comments)
    {
	var ctx = $("#bar-chartcanvas");

	var data = {
		labels : users,
		datasets : [
			{
				label : "Insertions",
				data : insertions,
                backgroundColor : "lime",
				
				borderWidth : 1
			},
			{
				label : "Deletions",
				data : deletions,
				
                backgroundColor : "aqua",
				
				borderWidth : 1
			},
            {
				label : "Comments",
				data : comments,
				
                backgroundColor : "mintcream",
				
				borderWidth : 1
			}
		]
	};

	var options = {
		title : {
			display : true,
			position : "top",
			text : "User Contributions for " + file_name + " in Drive " + drive_name,
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
    }
// test case
    create_histogram('Test_Drive', 'Test_File', ['Jack', 'Manvendra', 'Tito', 'Vibhas', 'Mike'], [14, 9, 32, 4, 18],[78, 39, 12, 40, 8],[50, 79, 22, 44, 88]);

});