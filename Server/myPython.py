#!/usr/bin/python
 # -*- coding: UTF-8 -*-

import cgi
import sys
import json

 def output(content):
 	sys.stdout.write('Content-Type: text/plain\n\n')
 	sys.stdout.write(content)

 form = cgi.FieldStorage()

 fail=0
 try:
 	myData = str(form['myData'].value)
 except:
 	fail=1
 else:
 	if myData == "":
 		fail=1

 if fail == 1:
 	output('Who are you?')
 	raise SystemExit

 output('Hello, '+myData)
 raise SystemExit

  pyObject = json.loads(jsonString) # now you can use the data in Python

#output(json.dumps(pythonObject)) # sends the Python variable content to javascript as JSON
output(json.dumps("Hello")) # sends the Python variable content to javascript as JSON