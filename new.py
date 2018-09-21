tags = ['{:21}'.format('Name:'),'{:21}'.format('ID:'),'{:21}'.format('Trashed:'),'{:21}'.format('Last Modifying User:')]
values = ['hello world', '18', 'True', 'Mike']
separator=', '
print(separator.join(values))