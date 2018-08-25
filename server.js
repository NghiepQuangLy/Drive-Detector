// PASTE YOUR CODE HERE
function objectToHTML(object)
  {
    	let output = "";
    	let str = Object.keys(object);
    	let length = Object.keys(object).length;
    	for (let i = 0; i<length; i++)
      	{
          let x = str[i];

			    if ((typeof object[x] === "object") && (Array.isArray(object[x]) === false))
          {
					    output += x +":"+objectToHTML(object[x]) + " ";

          }
          else {

              output += x+": "+object[x]+"<br/>";

          }
      	}

    	return output;
  }

let testObj = {
      number: 1,
      string: "abc",
      array: [5, 4, 3, 2, 1],
      boolean: true,
      trial: {a1: 1, a2: 2}
  };

let output = objectToHTML(testObj);
let outputAreaRef = document.getElementById("outputArea");
outputAreaRef.innerHTML = output;
