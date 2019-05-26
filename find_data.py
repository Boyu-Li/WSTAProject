import lucene
from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, BooleanClause
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

    def search(self, query, topk=10):
        query = self.repalcer(query)
        query = PythonMultiFieldQueryParser.escape(query)
        qp = PythonMultiFieldQueryParser(['name', 'contents'], self.analyzer)
        query = qp.parse(query, ['name', 'contents'],
                         [BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD], self.analyzer)
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

# a = Searcher()
# c = "Keith Stanfield's entire name is LaKeith Lee \"Keith'' Stanfield "
# b = a.search(c)
# print(b)