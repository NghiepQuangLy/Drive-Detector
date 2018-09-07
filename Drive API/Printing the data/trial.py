
outfile = open("features.html", "w")

print(outfile, """<html>
<head>
 <title>Feature information</title>
</head>
<body>
<table border="1">""")

print(outfile, "<tr><th>Feature</th><th>Start</th><th>End</th></tr>")

for i in range(10):
    print(outfile, "%s" % i)

print(outfile, """</table>
</body></html>""")

