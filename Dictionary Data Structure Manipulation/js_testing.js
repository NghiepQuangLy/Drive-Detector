let output = document.getElementById("try")
//output.innerHTML = "hello"

var data = {
 Jack: {
    comment: 3,
    create: 5,
    edit: 9
 }
};

for(var key in data) {
  var value = data[key];
 	//output.innerHTML += key + " = " + value + "x"
  //output.innerHTML += key
  for(var key2 in value){
  	var value2 = value[key2]
    //output.innerHTML += typeof value2
    output.innerHTML += value2
  }
}
