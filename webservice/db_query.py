#!/usr/bin/env python
import sqlite3
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import json
import cgi
import os

form = cgi.FieldStorage()
form_dict = {}
called_directly = False
if form.getvalue('data') == None:
    # Called via URL directly
    called_directly = True
    input = form.getvalue('data')
    input.split('&').split
else:
    # Called via web interface
    for key in form.keys():
        if isinstance(form[key], list):
            list_values = []
            for entry in form[key]:
                list_values.append(entry.value)
            form_dict[key] = list_values
        else:
            form_dict[key] = form[key].value

print 'Content-type:text/plain'
print

parameters_ok = 1
if not ('table_name' in form_dict and 'columns' in form_dict and 'timestamp_from' in form_dict and 'timestamp_to' in form_dict):
    print
    print 'Please specify ALL parameters: ?table_name=table1&columns=col1,col2&table_name=table2&columns=col3,col4&timestamp_from=YYYY-MM-DD HH:mm&timestamp_to=YYYY-MM-DD HH:mm'
    parameters_ok = 0
if not isinstance(form_dict['table_name'], list):
    if not (form_dict['table_name'].startswith('mod_') or form_dict['table_name'].startswith('sub_')):
        print
        print 'The chosen table ' + form_dict['table_name'] + ' is not a proper table or subtable. These start with "mod_" or "sub_", accordingly.'
        parameters_ok = 0
else:
    if len(form_dict['table_name']) != len(form_dict['columns']):
        print
        print 'Please specify table columns for each table exactly once.'
        parameters_ok = 0
    for table in form_dict['table_name']:
        if not (table.startswith('mod_') or table.startswith('sub_')):
            print
            print 'The chosen table ' + table + ' is not a proper table or subtable. These start with "mod_" or "sub_", accordingly.'
            parameters_ok = 0

if parameters_ok == 1:
    # connect to HappyFace database
    db_engine = create_engine('sqlite:///../HappyFace.db')
    db_engine.echo = False
    metadata = MetaData(db_engine)
    Session = sessionmaker(bind=db_engine)
    session = Session()

    if not isinstance(form_dictionary['table_name'], list):
        form_dictionary['table_name'] = [form_dictionary['table_name']]
        form_dictionary['columns'] = [form_dictionary['columns']]

    for index, table in enumerate(form_dictionary['table_name']):
        columns = form_dictionary['columns'][index].split(',')
        for index1, column in enumerate(columns):
            columns[index1] = column.strip()
            if columns[index1] == '':
                del columns[index1]
        for index1, column in enumerate(columns):
            columns[index1] = table + '.' + column
        table_ref = Table(table, metadata, autoload=True)
        table_cursor = table_ref.select(['hf_runs.id', 'hf_runs.time,'] + columns)

        try:
            table_cursor.execute()
        except SQLAlchemyError as ex:
            print 'SQLAlchemyError:', ex

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



if called_directly:
    print 'Here it is: query_result.json'
else:
    print 'query_result.json'

#db = create_engine('sqlite:///HappyFace.db')
#db.echo = False
#metadata = MetaData(db)
#Session = sessionmaker(bind=db)
#session = Session()
#hf_runs = Table('hf_runs', metadata, autoload=True)
