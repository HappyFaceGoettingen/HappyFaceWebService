#!/usr/bin/env python
import sqlite3
import json
import cgi
import base64
import os

def query_database(is_cgi = 0):
    # Called as CGI script
    if is_cgi == 1:
        print 'Content-type:text/html'
        print
        form = cgi.FieldStorage()
        input = form.getvalue('data')
        f = open('query_string', 'w')
        f.write(input)
        f.close()
    # Called regularly
    else:
        f = open('query_string', 'r')
        input = f.read()
        f.close()

    # test input
    #input = "SELECT hf_runs.id, hf_runs.time, sub_panda_site_details.id, sub_panda_site_details.queue_link FROM hf_runs INNER JOIN sub_panda_site_details ON hf_runs.id = sub_panda_site_details.parent_id WHERE '2013-01-01 14:45:00.000000' < hf_runs.time AND '2013-7-22 14:45:00.000000' > hf_runs.time; SELECT hf_runs.id, hf_runs.time, sub_apel_details_table.id FROM hf_runs INNER JOIN sub_apel_details_table ON hf_runs.id = sub_apel_details_table.parent_id WHERE '2013-01-01 14:45:00.000000' < hf_runs.time AND '2013-7-22 14:45:00.000000' > hf_runs.time; "
    queries = input.split(';')[0:-1]

    connection = sqlite3.connect('../HappyFace.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM module_instances;")
    modules = cursor.fetchall()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    query_result = []
    for query in queries:
        query = query.strip()
        result = {}
        if query[0:6].lower() == 'select':
            module_name = ''
            columns = (query.split('FROM')[0])[7:].split(',')
            for index, column in enumerate(columns):
                columns[index] = column.strip()
                columns[index], module_name = columns[index], columns[index].split('.')[0]
            columns = ','.join(columns) 
            result['table_name'] = module_name
            result['table_columns'] = columns
            #print query
            try:
                cursor.execute(query);
            except sqlite3.OperationalError, msg:
                print msg
            content = cursor.fetchall()
            result['content'] = content
            query_result.append(result)
        else:
            pass

    j = json.dumps(query_result, indent = 4)
    structure_file = 'query_result.json'
    f = open(structure_file, 'w')
    print >> f, j
    #print j
    #print base64.b64encode(j)
    if is_cgi == 1:
        print structure_file

    connection.close()

if __name__ == '__main__':
    query_database(1)
