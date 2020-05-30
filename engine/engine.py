import yaml
import os
from indexer import document, indexing_algorithm, indexer
from ranker import ranker, ranking_algorithm


class Engine(object):
    """
    this is main search engine class which exposes abstract functions to outer world
    """
    __instance = None

    @staticmethod
    def get_instance(batch_size=4, config_path='config/conf.yml'):
        if not Engine.__instance:
            Engine(batch_size, config_path)
        return Engine.__instance

    @staticmethod
    def _read_yaml(path):
        return yaml.load(open(path))

    def __init__(self, batch_size=4, config_path='config/conf.yml'):
        if Engine.__instance != None:
            raise Exception("Can't create two instances of this class")
        else:
            self.batch_size = batch_size
            self.config = self._read_yaml(config_path)
            os.environ["max_tokens"] = self.config['max_word_length']
            Engine.__instance = self
            self.indexing_algo = None
            self.indexer = None
            self.ranking_algo = None
            self.ranker = None

    def index(self, doc_strings, indexing_algo='default'):
        assert isinstance(doc_strings, list), 'doc strings should be list of strings'
        assert not self.indexer or self.indexer.indexed, "documents already indexed"
        docs = [document.NormalDocument(i[1], i[0]) for i in doc_strings]
        if indexing_algo == 'default':
            self.indexing_algo = indexing_algorithm.InvertedIndex()
        else:
            assert False, "only one indexing algo implimented"
        self.indexer = indexer.Indexer(self.indexing_algo)
        return self.indexer.index(docs)

    def search(self, string):
        assert isinstance(string, str), "please provide search string"
        assert self.indexer.indexed, "indexing is not done yet"

        query_tokens, relevant_docs = self.indexer.search(string)
        # lazy loading
        if not self.ranking_algo:
            self.ranking_algo = ranking_algorithm.DefaultRankingAlgo()
        if not self.ranker:
            self.ranker = ranker.Ranker(self.ranking_algo)
        return [i[0] for i in self.ranker.get_ordered_results(query_tokens, relevant_docs)]
