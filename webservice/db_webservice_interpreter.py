#!/usr/bin/env python
import cgi
import os
import db_backend

print 'Content-type:text/plain'
print
form = cgi.FieldStorage()
#print form
form_dictionary = {}
for key in form.keys():
    if isinstance(form[key], list):
        list_values = []
        for entry in form[key]:
            list_values.append(entry.value)
        form_dictionary[key] = list_values
    else:
        form_dictionary[key] = form[key].value
#print form_dictionary

parameters_ok = 1
if not ('table_name' in form_dictionary and 'columns' in form_dictionary and 'timestamp_from' in form_dictionary and 'timestamp_to' in form_dictionary):
    print
    print 'Please specify ALL parameters: ?table_name=table1&columns=col1,col2&table_name=table2&columns=col3,col4&timestamp_from=YYYY-MM-DD HH:mm&timestamp_to=YYYY-MM-DD HH:mm'
    parameters_ok = 0
if not isinstance(form_dictionary['table_name'], list):
    if not (form_dictionary['table_name'].startswith('mod_') or form_dictionary['table_name'].startswith('sub_')):
        print
        print 'The chosen table ' + form_dictionary['table_name'] + ' is not a proper table or subtable. These start with "mod_" or "sub_", accordingly.'
        parameters_ok = 0
else:
    if len(form_dictionary['table_name']) != len(form_dictionary['columns']):
        print
        print 'Please specify table columns for each table exactly once.'
        parameters_ok = 0
    for table in form_dictionary['table_name']:
        if not (table.startswith('mod_') or table.startswith('sub_')):
            print
            print 'The chosen table ' + table + ' is not a proper table or subtable. These start with "mod_" or "sub_", accordingly.'
            parameters_ok = 0

if parameters_ok == 1:
    query_string = ''
    if not isinstance(form_dictionary['table_name'], list):
        query = 'SELECT hf_runs.id, hf_runs.time, '
        columns = form_dictionary['columns'].split(',')
        for index, column in enumerate(columns):
            columns[index] = column.strip()
            if columns[index] == '':
                del columns[index]
        for index, column in enumerate(columns):
            columns[index] = form_dictionary['table_name'] + '.' + column
        query += (', ').join(columns)
        query += ' FROM hf_runs INNER JOIN '
        query += form_dictionary['table_name']
        query += ' ON hf_runs.id = '
        query += form_dictionary['table_name']
        if form_dictionary['table_name'].startswith('mod_'):
            query += '.id WHERE \''
        elif form_dictionary['table_name'].startswith('sub_'):
            query += '.parent_id WHERE \''
        query += form_dictionary['timestamp_from']
        query += '\' < hf_runs.time AND \''
        query += form_dictionary['timestamp_to']
        query += '\' > hf_runs.time; '
        query_string += query
    else:
        for index, table in enumerate(form_dictionary['table_name']):
            query = 'SELECT hf_runs.id, hf_runs.time, '
            columns = form_dictionary['columns'][index].split(',')
            for index1, column in enumerate(columns):
                columns[index1] = column.strip()
                if columns[index1] == '':
                    del columns[index1]
            for index1, column in enumerate(columns):
                columns[index1] = table + '.' + column
            query += (', ').join(columns)
            query += ' FROM hf_runs INNER JOIN '
            query += table
            query += ' ON hf_runs.id = '
            query += table
            if table.startswith('mod_'):
                query += '.id WHERE \''
            elif table.startswith('sub_'):
                query += '.parent_id WHERE \''
            query += form_dictionary['timestamp_from']
            query += '\' < hf_runs.time AND \''
            query += form_dictionary['timestamp_to']
            query += '\' > hf_runs.time; '
            query_string += query
    #print query_string
    f = open('query_string', 'w')
    f.write(query_string)
    f.close()
    db_backend.query_database(0)
    f = open('query_result.json', 'r')
    print f.read()
    f.close()
