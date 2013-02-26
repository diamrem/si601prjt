# -*- coding: utf-8 -*-

from igraph import *
from db import DB_PATH
import sqlite3 as sqlite

def fetch_user_article(cursor):
    print 'constructing sql...'
    pair_sql = '''
               select contributor_id, page_id from wiki
               where timestamp > '2012-07-01 00:00:00' 
               and timestamp < '2012-12-31 23:59:59'
               '''
    user_sql = '''
               select distinct contributor_id from wiki
               where timestamp > '2012-07-01 00:00:00' 
               and timestamp < '2012-12-31 23:59:59'
               '''
    page_sql = '''
               select distinct page_id from wiki
               where timestamp > '2012-07-01 00:00:00' 
               and timestamp < '2012-12-31 23:59:59'
               '''

    print 'fetching use_article pair...'
    cursor.execute(pair_sql)
    rows_pair = cursor.fetchall()

    print 'fetching distinct contributor_id...'
    cursor.execute(user_sql)
    rows_user = cursor.fetchall()

    print 'fetching distinct page_id...'
    cursor.execute(page_sql)
    rows_article = cursor.fetchall()

    return rows_pair, rows_user, rows_article


def build_graph(pair, users, articles):
    u_list = [id for id, in users]
    a_list = [id for id, in articles]
    total_u = len(u_list)
    total_a = len(a_list)
    edges = []
    print 'building edges..'
    count = 0
    for user_id, article_id in pair:
        count += 1
        if (u_list.index(user_id), a_list.index(article_id)+total_u)not in edges:
            edges.append((u_list.index(user_id),
                a_list.index(article_id)+total_u))
        if count%1000 == 0:
            print count
    print 'building a bipartite graph...'

    G = Graph.Bipartite([0]*total_u+[1]*total_a, edges)
    G.vs['id'] = ['']*(total_u + total_a)

    print 'adding user nodes...'
    for idx, id in enumerate(u_list):
        G.vs[idx]['u_id'] = id
        # add numeric property
        G.vs[idx]['index'] = idx

    print 'adding article nodes...'
    for idx, id in enumerate(a_list):
        G.vs[idx+total_u]['u_id'] = id
        # add numeric property
        G.vs[idx+total_u]['index'] = idx+total_u

    print 'writing to graphml file...'
    G.write_graphml(open('wiki_network.graphml','w'))
    G1, G2 = G.bipartite_projection()
    G1.write_graphml(open('wiki_network_user.graphml','w'))
    G2.write_graphml(open('wiki_network_page.graphml','w'))

if __name__ == "__main__":
    con = sqlite.connect(DB_PATH)
    cur = con.cursor()
    build_graph(*fetch_user_article(cur))
