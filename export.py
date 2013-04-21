import time
import sqlite3 as sql

con = sql.connect('./wiki_text.db')
cur = con.cursor()


def export_revision():
    with open('./unique_page_id.txt') as f, \
         open('./all_fields.tsv', 'w') as output:
        header = '\t'.join(['page_id', 'page_title', 'revision_id',
                           'contributor_id', 'contributor_name',
                           'timestamp','diff_score']) + '\n'
        output.write(header)
        for line in f:
            count = 0
            p_id, re_count  = [int(item.strip()) for item in line.split('|')]
            if re_count < 5000:
                print "done"
                break
            print p_id
            for fields in cur.execute('''select page_id, page_title, revision_id,
                                         contributor_id, contributor_name,
                                         timestamp,diff_score from wiki
                                         where page_id = ?''', (p_id,)):
                if not all(fields):
                    continue
                if not count:
                    print fields[1]
                count += 1
                contributor_name = fields[4].encode('utf8')
                fields_list = list(fields)
                fields_list[4] = contributor_name
                line = '\t'.join([str(item) for item in fields_list]) + '\n'
                output.write(line)
                if count%1000 == 0:
                    print line
                    print count, ' are written so far...'

if __name__ == "__main__":
    start = time.time()
    export_revision()
    end = time.time()
    print 'total ', (end-start)/60
