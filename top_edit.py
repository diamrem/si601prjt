import sqlite3 as lite
import sys
import csv

con=None
con=lite.connect('wiki.db')
cur=con.cursor()
outfile=csv.writer(open('top_articles.txt','w'),delimiter='\t')
outfile.writerow(['article','number of edits'])

#cur.execute("SELECT contributor_id, contributor_name FROM wiki")
cur.execute("SELECT page_id FROM wiki")
rows=cur.fetchall()

#editor={}
articles={}
"""
for line in rows:
    if line[1] not in editor:
        editor[line[1]]=1
    else:
        editor[line[1]]+=1
"""
for line in rows:
    if line not in articles:
        articles[line]=1
    else:
        articles[line]+=1

sorted_articles=sorted(articles.items(),key=lambda x:x[1], reverse=True)

#sort_editor=sorted(editor.items(), key=lambda x: x[1], reverse=True)
#for item in sort_editor:
print len(articles)
"""
for key, value in articles.items():
    outfile.writerow([key,value])
"""
for item in sorted_articles[0:20]:
    outfile.writerow(item)
con.close()
