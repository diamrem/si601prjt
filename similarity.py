from gensim import corpora, models, similarities
import nltk
from nltk.corpus import stopwords

from difflib import SequenceMatcher
import string, time, os.path
import sqlite3 as sql


con = sql.connect('./wiki_text.db')
cur = con.cursor()
sw = stopwords.words('english')


def modify_db():
    print 'updating db..'
    cur.execute('alter table wiki add column diff_score real default null')
    con.commit()

def clean_doc(text):
    stemmer = nltk.PorterStemmer()
    tokens = nltk.WordPunctTokenizer().tokenize(text)
    return [stemmer.stem(word.lower()) for word in
            tokens if word.lower() not in sw]

def sim():
    with open('./unique_page_id.txt') as id_counts:
        for id_c in id_counts:
            p_id, re_count  = [int(item.strip()) for item in id_c.split('|')]
            print p_id
            if re_count < 5000:
                print "done!"
                break

            dict_name = './tmp/%d.dict' % p_id
            corpus_name = './tmp/%d.mm' % p_id
            if os.path.isfile(dict_name):
                dictionary = corpora.dictionary.Dictionary.load(dict_name)
            else:
                docs = []
                count = 0
                print 'building dict...'
                for page_title, text in cur.execute('''select page_title, re_text from wiki where
                                                    page_id=? order by random() limit
                                                    ?''', (p_id, re_count/50)):
                    if count == 0:
                        print page_title
                    count += 1
                    if count%100 == 0:
                        print count, 'done'
                    docs.append(clean_doc(text))
                dictionary = corpora.Dictionary(docs)
                dictionary.save(dict_name)
            print dictionary

            if os.path.isfile(corpus_name):
                corpus = corpora.MmCorpus(corpus_name)
            else:
                print 'building corpus...'
                corpus = [dictionary.doc2bow(doc) for doc in docs]
                corpora.MmCorpus.serialize(corpus_name, corpus)

            print 'computing similarities...'
            lsi_m = models.LsiModel(corpus, id2word=dictionary, num_topics=150)
            previous = None
            count = 0
            re_diff = []
            for revision_id, re_text in cur.execute('''select revision_id,
                                                       re_text from wiki 
                                                       where page_id=? 
                                                       order by timestamp
                                                    ''', (p_id,)):
                count += 1
                if not previous:
                    previous = clean_doc(re_text)
                    previous_id = revision_id
                else:
                    current = clean_doc(re_text)
                    previous_vec = dictionary.doc2bow(previous)
                    current_vec = dictionary.doc2bow(current)
                    current_lsi = lsi_m[current_vec]
                    try:
                        index = similarities.MatrixSimilarity([previous_vec,])
                        diff = 1 - (index[current_lsi] + 1 )/2.0
                    except:
                        print 'error!, set diff -1'
                        diff  = -1
                    if count%100 == 0:
                        print count
                        print revision_id, ' ', str(round(diff,5))+' diff to ', previous_id
                        print '\n =========== \n'
                    re_diff.append((float(round(diff,5)), revision_id))
                    previous = current
                    previous_id = revision_id
            print 'updating database for page', p_id
            cur.executemany('''update wiki set diff_score = ? where
                               revision_id = ?''', re_diff)
            con.commit()

            

if __name__ == '__main__':
    start = time.time()
    # modify_db()
    sim()
    end = time.time()
    print 'total ', (end-start)/60

