let output = document.getElementById("try")
//output.innerHTML = "hello"

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

var data = {
 Jack: {
    comment: 3,
    create: 5,
    edit: 9
 }
};

inserts = [];
deletes = [];
commentss = [];
names = [];
for(var key in temp_user_data) {
  var value = temp_user_data[key];
  output.innerHTML += value
  names.push(key)
  for(var key2 in value){
  	var value2 = value[key2]

    if (key2 == "insert"){
      inserts.push(value2)
    }
    else if (key2 == "delete"){
      deletes.push(value2)
    }
    else if (key2 == "commentss"){
      commentss.push(value2)
    }
  }
};
///output.innerHTML += inserts
//output.innerHTML += names
