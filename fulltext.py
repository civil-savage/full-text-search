#!/usr/local/bin/python3

import cgi
import cgitb
cgitb.enable()
import mysql.connector as mysql
from mysql.connector import errorcode
import os
from string import Template
from opdc import util, tmpl

cnx = mysql.connect(host='localhost',
                    user='root',
                    password=None,
                    database='rhohman')
form = cgi.FieldStorage()
terms = form.getvalue("terms", '')
# Look in how to handle ajax requests likely using some sort of request.form or sometihng or other.

def main():
    template(search()[0], search()[1])
    cnx.close()


def format_terms():
# Not perfect but a workable multisearch term string format.
    terms_list = (terms)
    temp_list = []
    clean_terms = set()
    and_tog = ''
    not_tog = ''
    for words in terms_list.split():
        temp_list.append(words)
        if words == 'not':
            not_tog = 1
        elif words == 'and':
            and_tog = 1
            if len(temp_list) < 3:
                clean_terms.add('+' + temp_list[-2])
            elif temp_list[-3] != 'not':
                clean_terms.add('+' + temp_list[-2])
        elif not_tog:
            clean_terms.add('-' + words)
            not_tog = ''
        elif and_tog:
            if words != 'not':
                clean_terms.add('+' + words)
                and_tog = ''
        elif temp_list[0] != words:
            if words != 'or':
                clean_terms.add(words)
        else:
            clean_terms.add(words)
    return(' '.join(clean_terms))


def search():
    cursor = cnx.cursor()
    query = Template("""select $arg from edgar_poems WHERE MATCH (txt)"""
                     """AGAINST ('$sterms' $boole);""")
    query_items = ['name', 'count(*)']
    query_stack = []
    all_results = []
    for item in query_items:
        if len(terms.split()) > 1: # Multiterm seach
            query_stack.append(query.substitute(arg=item,
                                                boole='IN BOOLEAN MODE',
                                                sterms=format_terms()))
        else:# single item search(general search)
            query_stack.append(query.substitute(arg=item,
                                                boole='',
                                                sterms=terms))
    for queries in query_stack:
        cursor.execute(queries)
        results = cursor.fetchall()
        for result in results:
            all_results.append(str(result).strip('\'(),'))
    cursor.close()
    count = all_results.pop()  # Count should always be the last item.
    return(all_results, count)


def template(results, count):
    print('Content-type: text/html\n')
    with open('astf.tmpl') as tfile:
        t = tmpl.prepare(tfile, 'astf.tmpl')
        print(t.render({'results': results,
                        'count': count,
                        'terms': terms}))

if __name__ == '__main__':
    main()
