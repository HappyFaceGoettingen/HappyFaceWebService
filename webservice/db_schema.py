import sqlite3
import json

connection = sqlite3.connect('../HappyFace.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM module_instances;")
modules = cursor.fetchall()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

#cursor.execute("""
#    SELECT id
#    FROM hf_runs
#    """)

# Convert query to objects of key-value pairs

db_structure = []
for module in modules:
    #module_table_name = module[1].replace('_','__')
    #module_table_name_split = module_table_name.split()
    #module_table_name = ''
    #for character in module_table_name_split:
    #    if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    #        module_table_name += '_' + character.lower()
    #    else:
    #        module_table_name += character
    #module_table_name = 'mod_' + module_table_name

    module_table_name = module[1]
    module_table_name = 'mod_' + module_table_name.lower().replace('_','__')
    #print module_table_name
    module_name = module[1]
    cursor.execute("PRAGMA table_info(" + module_table_name + ");")
    columns = cursor.fetchall()
    table_dict = {}
    table_dict['module_name'] = module_name
    table_dict['module_table_name'] = module_table_name
    table_dict['module_table_columns'] = []
    for column in columns:
        table_dict['module_table_columns'].append(column[1])
    table_dict['subtables'] = []
    for table in tables:
        if table[0].startswith('sub_' + module[0].replace('_','__')):
            subtable = {}
            subtable['subtable_name'] = table[0]
            subtable['subtable_columns'] = []
            cursor.execute("PRAGMA table_info(" + table[0] + ");")
            subtable_columns = cursor.fetchall()
            for column in subtable_columns:
                subtable['subtable_columns'].append(column[1])
            table_dict['subtables'].append(subtable)
            
    db_structure.append(table_dict)

j = json.dumps(db_structure, indent = 4)
structure_file = 'db_structure.json'
f = open(structure_file, 'w')
print >> f, j

connection.close()
