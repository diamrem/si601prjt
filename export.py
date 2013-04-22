import time
import sqlite3 as sql

con = sql.connect('./wiki_text.db')
cur = con.cursor()

con_dict = sql.connect('./wiki_text.db')
con_dict.row_factory = sql.Row
cur_dict = con_dict.cursor()

def export_revision():
    with open('./unique_page_id.txt') as f, \
         open('./all_fields_complete.tsv', 'w') as output:
        header = '\t'.join(['page_id', 'page_title', 'revision_id',
                           'contributor_id', 'contributor_name',
                           'timestamp','diff_score']) + '\n'
        output.write(header)
        for line in f:
            count = 0
            p_id, re_count  = [int(item.strip()) for item in line.split('|')]
            print p_id
            for fields in cur.execute('''select page_id, page_title, revision_id,
                                         contributor_id, contributor_name,
                                         timestamp,diff_score from wiki
                                         where page_id = ?''', (p_id,)):
                if not all(fields[:-1]):
                    continue
                if not count:
                    print fields[1]
                count += 1
                fields_list = list(fields)
                contributor_name = fields[4].encode('utf8')
                fields_list[4] = contributor_name
                page_title = fields[1].encode('utf8')
                fields_list[1] = page_title
                line = '\t'.join([str(item) for item in fields_list]) + '\n'
                output.write(line)
                if count%1000 == 0:
                    print line
                    print count, ' are written so far...'

def export_gource_log():
    with open('gource_log_fresh', 'w') as output, \
         open('./unique_page_id.txt') as f:
        for line in f:
            count = 0
            p_id, re_count  = [int(item.strip()) for item in line.split('|')]
            print p_id
            for row in cur_dict.execute('''select page_id, page_title, revision_id,
                                         contributor_id, contributor_name,
                                         timestamp,diff_score from wiki
                                         where page_id = ? order by timestamp
                                   ''', (p_id,)):
                if not row['page_title'] or not row['contributor_name']:
                    continue
                if not count:
                    filename = row['page_title'].encode('utf8')
                    print filename
                    action_t = 'A'
                else:
                    action_t = 'M'
                count += 1
                timestamp = time.mktime(time.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'))
                username = row['contributor_name'].encode('utf8')
                line = '|'.join([str(int(timestamp)), username, action_t, filename]) + '\n'
                output.write(line)
                if count%1000 == 0:
                    print count, ' are written for ', filename, line


if __name__ == "__main__":
    start = time.time()
    export_gource_log()
    end = time.time()
    print 'total ', (end-start)/60
