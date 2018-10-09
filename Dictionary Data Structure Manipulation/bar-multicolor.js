/*
user_data should be of the following format:
user_data = {
  Jack: {
     create: 5,
     edit: 9,
     empty: 2.....,
},
  Tito: {
    create: 5,
    edit: 9,
    empty: 2.....,
}
}
*/

var temp_user_data = {
  Jack: {
     insert: 5,
     delete: 9,
     comment: 2
   },
   Manvendra: {
      insert: 4,
      delete: 1,
      comment:0
    },
    Tito: {
       insert: 5,
       delete: 9,
       comment: 2
     },
     Vibhas: {
        insert: 6,
        delete: 7,
        comment: 8
      },
      Mike: {
         insert: 6,
         delete: 7,
         comment: 8
       }
};
'Jack', 'Manvendra', 'Tito', 'Vibhas', 'Mike'
$(document).ready(function () {
function create_histogram(drive_name, file_name, users, insertions, deletions, comments, temp_user_data)
    {
	var ctx = $("#bar-chartcanvas");

  //var drive_file_data = {
    //drive: drive_name,
    //file: file_name
  //}

  temp_insertions = []
  temp_deletions = []
  temp_comments = []

  var printing_data = {

  }

	var data = {
		labels : users,
		datasets : [
			{
				label : "Insertions",
				//data : insertions,
        data: temp_user_data.
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
			//text : "User Contributions for " + file_name + " in Drive " + drive_name,
      text : "User Contributions for " + drive_file_data.file + " in Drive " + drive_file_data.drive,
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
    //create_histogram('Test_Drive', 'Test_File', ['Jack', 'Manvendra', 'Tito', 'Vibhas', 'Mike'], [78, 39, 12, 40, 8],[50, 79, 22, 44, 88]);
});
