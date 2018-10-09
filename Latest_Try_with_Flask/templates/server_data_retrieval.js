let outputAreaRef = document.getElementById('actual_content');
var user_data = {{account_data|tojson}};
console.log(user_data);
for (var i = 0; i < user_data.length; i++)
    {
        var drive_contents_html = outputAreaRef.createElement("BUTTON");
        drive_contents_html.innerHTML = user_data[i].name;
        drive_contents_html.setAttribute("id", "Drive " + user_data[i].name);




        var drive_contents = user_data[i].contents;

        for (var j = 0; j < drive_contents.length; j++)
            {
                if (drive_contents[j].type === 'folder')
                    {
                        var folder_contents_html = outputAreaRef.createElement("BUTTON");

                        folder_contents_html.innerHTML = drive_contents[j].name;

                        var folder_contents = drive_contents[j].files;

                        for (var z = 0; z < folder_contents.length; z++)
                            {
                                var file_in_folder = document.createElement("BUTTON");
                                file_in_folder.innerHTML = folder_contents[z].name;

                                folder_contents_html.appendChild(file_in_folder);
                            }

                        drive_contents_html.appendChild(folder_contents_html);
                    }
                else
                    {
                        var file_not_in_folder = document.createElement("BUTTON");
                        file_not_in_folder.innerHTML = user_data[i].contents[j].name;
                        drive_contents_html.appendChild(file_not_in_folder);
                    }
            }
        outputAreaRef.innerHTML = drive_contents_html;
        //document.body.appendChild(drive_contents_html);

    }
