/*
user_data should be of the following format:
dictionary = {
  dictionary1,
  dictionary2...
}

SAMPLE INPUT DATA FORMAT:
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
  Vibhas: {
     comment: 5,
     create: 5,
     edit: 5,
     emptyTrash: 5,
     move: 5,
     permissionChange: 5,
     rename: 5,
     trash: 5,
     unknown: 5,
     untrash: 5,
     upload: 5
   },
  Jack: {
    comment: 5,
    create: 5,
    edit: 5,
    emptyTrash: 5,
    move: 5,
    permissionChange: 5,
    rename: 5,
    trash: 5,
    unknown: 5,
    untrash: 5,
    upload: 5
   },
   Mike: {
     comment: 5,
     create: 5,
     edit: 5,
     emptyTrash: 5,
     move: 5,
     permissionChange: 5,
     rename: 5,
     trash: 5,
     unknown: 5,
     untrash: 5,
     upload: 5
    },
    Tito: {
      comment: 5,
      create: 5,
      edit: 5,
      emptyTrash: 5,
      move: 5,
      permissionChange: 5,
      rename: 5,
      trash: 5,
      unknown: 5,
      untrash: 5,
      upload: 5
     },
   Manvendra: {
     comment: 5,
     create: 5,
     edit: 5,
     emptyTrash: 5,
     move: 5,
     permissionChange: 5,
     rename: 5,
     trash: 5,
     unknown: 5,
     untrash: 5,
     upload: 5
    }
};

$(document).ready(function () {
function create_histogram(drive_user_data)
    {
	var ctx = $("#bar-chartcanvas");

  // Creating arrays to store the number of the actions performed by the user
  // for each type of action
  comment_count = [];
  create_count = [];
  edit_count = [];
  emptyTrash_count = [];
  move_count = [];
  permissionChange_count = [];
  rename_count = [];
  trash_count = [];
  unknown_count = [];
  untrash_count = [];
  upload_count = [];

  user_names = [];


  // Looping through the outer dictionary items in drive_user_data
  // With respect to the sample input data provided at the top of the file,
  // this loop would iterate through Jack, Tito, ...
  for(var key in drive_user_data) {
    // key would store the individual dictionary initializers inside drive_user_data
    // for example, for the first iteration, key = "Jack"
    // value variable below stores the dictionary objects present inside drive_user_data
    var value = drive_user_data[key];

    // Storing the user names in an array
    user_names.push(key)

    for(var key2 in value){
    	var value2 = value[key2]

      // If the key2 value is insert, the value corresponding to key2
      // would be pushed into the inserts array
      // (Similar for all the other actions)
      if (key2 == "comment"){
        comment_count.push(value2)
      }
      else if (key2 == "create"){
        create_count.push(value2)
      }
      else if (key2 == "edit"){
        edit_count.push(value2)
      }
      else if (key2 == "emptyTrash"){
        emptyTrash_count.push(value2)
      }
      else if (key2 == "move"){
        move_count.push(value2)
      }
      else if (key2 == "permissionChange"){
        permissionChange_count.push(value2)
      }
      else if (key2 == "rename"){
        rename_count.push(value2)
      }
      else if (key2 == "trash"){
        trash_count.push(value2)
      }
      else if (key2 == "unknown"){
        unknown_count.push(value2)
      }
      else if (key2 == "untrash"){
        untrash_count.push(value2)
      }
      else if (key2 == "upload"){
        upload_count.push(value2)
      }
    }
  };

	var data = {
		labels : user_names,
		datasets : [
      {
				label : "Comments",
        data: comment_count,
        backgroundColor : "lime",
				borderWidth : 1
			},
      {
				label : "Create",
        data: create_count,
        backgroundColor : "aqua",
				borderWidth : 1
			},
      {
				label : "Edit",
        data: edit_count,
        backgroundColor : "skyblue",
				borderWidth : 1
			},
      {
				label : "Empty Trash",
        data: emptyTrash_count,
        backgroundColor : "springgreen",
				borderWidth : 1
			},
      {
				label : "Move",
        data: move_count,
        backgroundColor : "pink",
				borderWidth : 1
			},
      {
				label : "Permission Change",
        data: permissionChange_count,
        backgroundColor : "silver",
				borderWidth : 1
			},
      {
				label : "Rename",
        data: rename_count,
        backgroundColor : "salmon",
				borderWidth : 1
			},
      {
				label : "Trash",
        data: trash_count,
        backgroundColor : "brown",
				borderWidth : 1
			},
      {
				label : "Unknown",
        data: unknown_count,
        backgroundColor : "gray",
				borderWidth : 1
			},
      {
				label : "Untrash",
        data: untrash_count,
        backgroundColor : "crimson",
				borderWidth : 1
			},
      {
				label : "Upload",
        data: upload_count,
        backgroundColor : "skyblue",
				borderWidth : 1
			}
		]
	};

	var options = {
		title : {
			display : true,
			position : "top",
      text : "User Contributions",
			fontSize : 18,
			fontColor : "#111"
		},
		legend : {
			display : true
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
    create_histogram(temp_user_data);
});
