import sqlite3
import json

html = """
<html>
<body>
    <p>Available modules:</p>
    <select multiple>
        %s
    </select>
</body>
</html>"""

def application(environ, start_response):

    connection = sqlite3.connect('HappyFace/HappyFace.db')
    cursor = connection.cursor()

    cursor.execute("SELECT module FROM module_instances")
    modules = cursor.fetchall()
    modules_select = ''
    for module in modules:
        modules_select += '<option value=' + module[0] + '>' + module[0] + '</option>\n'

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()
    tables_select = ''
    for table in tables:
        tables_select += '<option value=' + table[0] + '>' + table[0] + '</option>\n'

    cursor.execute("""
        SELECT id
        FROM hf_runs
        """)

    rows = cursor.fetchall()
    #print(rows)
 
    # Convert query to objects of key-value pairs

    objects_list = []
    for row in rows:
        d = {}
        d['id'] = row[0]
        objects_list.append(d)

    j = json.dumps(objects_list, indent=4)
    objects_file = 'objects.js'
    f = open(objects_file,'w')
    print >> f, j

    connection.close()



    status = '200 OK'

    output = html % (modules_select)
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output.encode('utf-8')]
