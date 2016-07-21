#!/usr/local/bin/python3

import cgi
import cgitb
cgitb.enable()
import mysql.connector as mysql
from mysql.connector import errorcode
import os
from opdc import util, tmpl

cnx = mysql.connect(host ='localhost', user = 'root', password = None, database = 'rhohman')

def main():
    table = showtable()
    template(table)
    cnx.close()
    
def showtable():
    cursor = cnx.cursor()
    tablequery = ("""select name from edgar_poems;""")
    cursor.execute(tablequery)
    results = cursor.fetchall()
    table = []
    for result in results:
        table.append(str(result).strip('\'(),'))
    cursor.close()
    return(table)

# def search():
#     cursor = cnx.cursor()
#     titlequery = ("""select name form edgar_poems WHERE MATCH (txt) AGAISNT ('""" + userquery + """');""") 
#     cursor.execute(tablequery)
#     results = cursor.fetchall()
#     clean_results = []
#     for result in results:
#         clean_results.append(str(result).strip('\'(),'))
#     cursor.close()
#     return(clean_results)


def template(table):
    print('Content-type: text/html\n')
    with open('sft.tmpl') as tfile:
        t = tmpl.prepare(tfile,'stf.tmpl')
        print(t.render({'table': table}))
           
main()


#### Use this sort of thing to proccess a tmpl doc and what not also look at the other listman proj for further proccess.
# def print_records(cust, proj, cc):
#   print(tmpl.render(info['doc_head'],info))
#   for r in legacy.records(cust, proj + cc):
#     if (r['svstat'] == '1'
#         and r['svtype'] == '1'
#         and r['Q22.1'] == '2'):
#       print(tmpl.render(info['rec_head'],
#                         {'ident': r['Ident'],
#                          'cc': cc.upper(),
#                          'title': info['title']}))
#       print_resp(r)
#   print(tmpl.render(info['doc_foot'], info))

# def print_resp(r):
#   for q in qs:
#     name = q['name']
#     ques = info[name]
#     resp =  q['resp'](r)
#     if resp is not None:
#       print(tmpl.render(info['ques'],
#                         { 'ques': ques,
#                           'resp': resp,
#                           'name': name}))








   

     
      




