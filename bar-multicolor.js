$(document).ready(function () {
// this function creates a histogram by taking in the drive_name, file_name, users, insertions, deletions, comments as arguments
function create_histogram(drive_name, file_name, users, insertions, deletions, comments)
    {
	var ctx = $("#bar-chartcanvas");
// data structure to hold the information for the histogram
	var data = {
		labels : users,
		datasets : [
			{
				label : "Insertions", // label to be printed
				data : insertions, //data passesto the function
                backgroundColor : "lime", //color
				
				borderWidth : 1 //minimum border width
			},
			{
				label : "Deletions",// label to be printed deletions
				data : deletions, //data passesto the function
				
                backgroundColor : "aqua", //color
				
				borderWidth : 1 //minimum border width
			},
            {
				label : "Comments", // label to be printed
				data : comments, //data passesto the function
				
                backgroundColor : "mintcream", //color
				
				borderWidth : 1 //minimum border width
			}
		]
	};


// data structure to hold the the setting for the histogram        
var options = {
		title : {
			display : true, 
			position : "top", // at the top
			text : "User Contributions for " + file_name + " in Drive " + drive_name, //string to be display
			fontSize : 18, //pretty average sized font
			fontColor : "#111" //black
		},
		legend : {
			display : false
		},
		scales : {
			 xAxes: [{
                stacked: true //making the bar stacked
            }],
            yAxes: [{
                stacked: true // making the bar stacked
            }]
		}
	};

	var chart = new Chart( ctx, {
		type : "horizontalBar", //type of the bar is a horizontally stacked
		data : data,
		options : options
	});
    }
// test case using names of the team members
    create_histogram('Test_Drive', 'Test_File', ['Jack', 'Manvendra', 'Tito', 'Vibhas', 'Mike'], [14, 9, 32, 4, 18],[78, 39, 12, 40, 8],[50, 79, 22, 44, 88]); //drive_name, file_name, users, insertions, deletions, comments

});