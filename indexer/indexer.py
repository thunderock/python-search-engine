from indexer import indexing_algorithm


class Indexer(object):
    """
    main indexer class
    """

    def __init__(self, indexing_algo):
        assert isinstance(indexing_algo, indexing_algorithm.IndexingAlgo)
        self.indexing_algo = indexing_algo
        self.indexed = False

    def index(self, docs, threads=None):
        self.indexed = True
        if threads:
            return self.indexing_algo.index(docs, threads)

        return self.indexing_algo.index(docs)

    def search(self, query):
        return self.indexing_algo.search_docs(query)
