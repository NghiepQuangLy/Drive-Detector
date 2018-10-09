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

$(document).ready(function () {
//function create_histogram(drive_name, file_name, users, insertions, deletions, comments, temp_user_data)
function create_histogram(drive_user_data)
    {
	var ctx = $("#bar-chartcanvas");

  inserts = [];
  deletes = [];
  commentss = [];
  user_names = [];

  for(var key in drive_user_data) {
    var value = drive_user_data[key];
    user_names.push(key)
    for(var key2 in value){
    	var value2 = value[key2]

      if (key2 == "insert"){
        inserts.push(value2)
      }
      else if (key2 == "delete"){
        deletes.push(value2)
      }
      else if (key2 == "comment"){
        commentss.push(value2)
      }

    }
  };

	var data = {
		labels : user_names,
		datasets : [
			{
				label : "Insertions",
				//data : insertions,
        data: inserts,
        backgroundColor : "lime",
				borderWidth : 1
			},
			{
				label : "Deletions",
				//data : deletions,
        data: deletes,
        backgroundColor : "aqua",
				borderWidth : 1
			},
            {
				label : "Comments",
				data : commentss,
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
      //text : "User Contributions for " + drive_file_data.file + " in Drive " + drive_file_data.drive,
      text : "User Contributions",
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
    //create_histogram('Test_Drive', 'Test_File', ['Jack', 'Manvendra', 'Tito', 'Vibhas', 'Mike'], [14, 9, 32, 4, 18],[78, 39, 12, 40, 8],[50, 79, 22, 44, 88]);
    create_histogram(temp_user_data);
});
