# -*- coding: utf-8 -*-

import lxml.etree as et
from WikiExtractor import clean, compact
from time import sleep
import sqlite3 as sqlite
import sys


DB_PATH = 'wiki_text.db'
PREFIX = '{http://www.mediawiki.org/xml/export-0.8/}'

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
                    re_text text,
                    timestamp date)''')
    con.commit()
    return con, cur

def insert_to_db(page, cur, con):
    if int(page[1].text) == 0:
        page_title = page.find(PREFIX+'title').text
        page_id = page.find(PREFIX+'id').text
        print "dealing with page: ", page_id, "\npage title: ", page_title
        print '===================='
        for revision in page.findall(PREFIX+'revision'):
            try:
                revision_id = revision.find(PREFIX+'id').text
                print 'revision', revision_id, "found:"
                timestamp = revision.find(PREFIX+'timestamp').text.replace('T', ' ')\
                                                    .replace('Z', '')
                contributor =  revision.find(PREFIX+'contributor')
                if contributor.find(PREFIX+'ip') is None:
                    contributor_id = contributor.find(PREFIX+'id').text
                    contributor_name = contributor.find(PREFIX+'username').text
                else:
                    contributor_id = contributor_name = contributor.find(PREFIX+'ip').text
                text = revision.find(PREFIX+'text').text
                if text:
                    text = clean(text)
                    text = '\n'.join(compact(text))
                else:
                    text = ' '
                print 'clear text is:\n>>>>', text

                cur.execute('''insert into wiki values
                            (?, ?, ?, ?, ?, ?, ?)''', 
                            (page_id, page_title, revision_id,
                                contributor_id, contributor_name,
                                text, timestamp))
                con.commit()
            except:
                print "something is wrong, continue"
                continue
            print '===================='

if __name__ == "__main__":
    print 'start...'
    con, cur = create_db()
    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: db_text.py <file_path>'
        sys.exit(1)
    source = args[0] # file name of the input file
    print 'with file ', source
    sleep(0.2)
    context = et.iterparse(source, events=('end',), tag=PREFIX+'page') 
    page_count = 0
    for event, page in context:
        page_count += 1
        insert_to_db(page, cur, con)
        page.clear()
        while page.getprevious() is not None:
            del page.getparent()[0]
        if page_count == 400:
            break

