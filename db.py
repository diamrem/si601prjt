# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
import sqlite3 as sqlite
import sys


DB_PATH = 'wiki.db'

def create_db():
    con = sqlite.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('drop table if exists wiki')
    cur.execute('''create table wiki
                   (page_id integer,
                    page_title text,
                    revision_id integer,
                    contributor_id integer,
                    contributor_name text,
                    timestamp date)''')
    con.commit()
    return con, cur

def write_database(cur, con, source):
    with open(source, 'r') as f:
        tree = et.parse(f)
        root = tree.getroot()
        print root.findall('page')
        for page in root.findall('page'):
            if int(page[1].text) == 0:
                page_title = page.find('title').text
                page_id = page.find('id').text
                print page_id, page_title
                for revision in page.findall('revision'):
                    try:
                        revision_id = revision.find('id').text
                        timestamp = revision.find('timestamp').text.replace('T', ' ')\
                                                            .replace('Z', '')
                        contributor =  revision.find('contributor')
                        if contributor.find('ip') is None:
                            contributor_id = contributor.find('id').text
                            contributor_name = contributor.find('username').text
                        else:
                            contributor_id = contributor_name = contributor.find('ip').text

                        cur.execute('''insert into wiki values
                                    (?, ?, ?, ?, ?, ?)''', 
                                    (page_id, page_title, revision_id,
                                        contributor_id, contributor_name,
                                        timestamp))
                        con.commit()
                    except:
                        print "something is wrong, continue"
                        continue

        


if __name__ == "__main__":
    con, cur = create_db()
    
    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: db.py <file_path>'
    sys.exit(1)
    source = args[0] # file name of the input file

    write_database(cur, con, source)
