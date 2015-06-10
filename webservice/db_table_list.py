#!/usr/bin/env python
import json
import sqlite3
from mako.template import Template
from xml.dom import minidom
import urllib
import re
import time
import cgi

url_str = "http://localhost//category?action=getxml&date=" + time.strftime('%Y-%m-%d') + "&time" + time.strftime('%H:%M')
#print url_str
xml_str = urllib.urlopen(url_str).read()
xmldoc = minidom.parseString(xml_str)

module_name = []
for node in xmldoc.getElementsByTagName('module'):
    nodelist = node.getElementsByTagName('name')
    for i in nodelist:
        #node_name =  i.toxml().split("<name>")
        node_name = re.search('<name>(.+?)</name>', i.toxml())
        if node_name:
           node_name = node_name.group(1)
          # print node_name[1].split("</name>")
          # print node_name 
           module_name.append(node_name)

#print module_name 

connection = sqlite3.connect('../HappyFace.db')
cursor = connection.cursor()

db_table_list = []

for table_name in module_name:
  #str = "SELECT name FROM sqlite_master WHERE type='table' and name like '%" + table_name + "%';"
  #print str
  if table_name != 'ddm':
     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name like '%" + table_name + "%';")
     tables = cursor.fetchall()
  else:
     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name like '%" + table_name + "%' and name not like '%deletion%';")
     tables = cursor.fetchall()

 
  for table in tables:
    table_dict = {}
    table_dict['module_name'] = table_name
        
    table_dict['table_name'] = table[0]
    table_dict['table_columns'] = []
    cursor.execute("PRAGMA table_info(" + table[0] + ");")
    columns = cursor.fetchall()
    for column in columns:
       table_dict['table_columns'].append(column[1])
    
    db_table_list.append(table_dict)


j = json.dumps(db_table_list, indent = 4)
#output_file = 'db_table_list_Output.json'
#f = open(output_file, 'w')
#print >> f, j
print 'Content-type:text/plain'
print
print j

connection.close()

