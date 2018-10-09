output = document.getElementById("sample_data")

var data = {
 Jack: {
    comment: 3,
    create: 5,
    edit: 9,
    empty: 2,
    move: 7,
    permissionChange: 8,
    rename: 23,
    trash: 2,
    unknown: 0,
    untrash: 0,
    upload: 0
 }
}

output.innerHTML = data.Jack.comment
