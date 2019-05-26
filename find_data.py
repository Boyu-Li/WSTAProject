import lucene
from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, BooleanClause, BooleanQuery
from org.apache.lucene.index import DirectoryReader
from org.apache.pylucene.queryparser.classic import PythonMultiFieldQueryParser
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer

class Searcher():

    def __init__(self):
        indexdir = './IndexFiles.index'
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        search_dir = SimpleFSDirectory(Paths.get(indexdir))
        self.searcher = IndexSearcher(DirectoryReader.open(search_dir))
        self.searcher.setSimilarity(BM25Similarity())
        self.analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
    def repalcer(self, text):
        chars = '/\\`*_{}[]()>#+-.!$‘"'
        for c in chars:
            if c in text:
                text = text.replace(c, ' ')
        return text

    def search(self, query, topk=20):
        print(query)
        query = self.repalcer(query)
        query = PythonMultiFieldQueryParser.escape(query)
        qp = PythonMultiFieldQueryParser(['name', 'contents'], self.analyzer)
        query = qp.parse(query, ['name', 'contents'],
                         [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST], self.analyzer)
        print(query)
        scores = self.searcher.search(query, topk).scoreDocs
        docnames = []
        doccontents = []
        for score in scores:
            doc = self.searcher.doc(score.doc)
            docnames.append(doc.get('docname'))
            doccontents.append(doc.get('contents'))
        return docnames, doccontents

    def retrieve(self, term, sid):
        query = term + ' ' + str(sid)
        query = self.repalcer(query)
        query = QueryParser.escape(query)
        query = QueryParser('docname', self.analyzer).parse(query)
        score = self.searcher.search(query, 1).scoreDocs
        doc = self.searcher.doc(score[0].doc)
        return doc.get('docname'), doc.get('contents')

    def search_scores(self, query, topk=10):
        query = self.repalcer(query)
        qp = PythonMultiFieldQueryParser(['name', 'contents'], self.analyzer)
        query = qp.parse(query, ['name', 'contents'],
                         [BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD], self.analyzer)
        scores = self.searcher.search(query, topk).scoreDocs

        docnames = []
        doccontents = []
        s = []
        for score in scores:
            doc = self.searcher.doc(score.doc)
            docnames.append(doc.get('docname'))
            doccontents.append(doc.get('contents'))
            s.append(score.score)
        return docnames, doccontents, s


    def search2(self, query, topk=10):
        query = self.repalcer(query)
        query = QueryParser.escape(query)
        query1 = QueryParser('name', self.analyzer).parse(query)
        query2 = QueryParser('name-contents', self.analyzer).parse(query)
        scores1 = self.searcher.search(query1, 30).scoreDocs
        scores2 = self.searcher.search(query2, 30).scoreDocs
        name1 = []
        name2 = []
        for score1 in scores1:
            doc1 = self.searcher.doc(score1.doc)
            t = doc1.get('name')
            if t not in name1:
                name1.append(t)
            if len(name1)>2:
                break
        print(name1)
        name2.append(name1[0])
        for score2 in scores2:
            doc2 = self.searcher.doc(score2.doc)
            name2.append(doc2.get('name-sid'))
        print(set(name2))
        name = set(name1)&set(name2)
        print(list(name))
        # query2 = QueryParser('name-sid', self.analyzer).parse(docname)
        # print('query2:', query2)
        # scores2 = self.searcher.search(query2, topk).scoreDocs
        # print(scores2)

        # for score in scores2:
        #     doc = self.searcher.doc(score.doc)
        #     docnames2.append(doc.get('name-sid'))
        #     doccontents2.append(doc.get('contents'))
        # print(docnames2, doccontents2)
        # #return docnames2, doccontents2



a = Searcher()
c = "Zach Galifianakis was featured in Puss in Boots."
b = a.search2(c)
print(b)