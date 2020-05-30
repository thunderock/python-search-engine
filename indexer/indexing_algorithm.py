import warnings
from indexer import document
from tqdm import tqdm
import re
import os


class IndexingAlgo(object):
    """
    super class for indexing algos
    very easy to add other algos
    """

    __name = 'general_indexing_algo'

    @property
    def name(self):
        assert self.__name
        return self.__name

    def __init__(self, *args, **kwargs):
        super(IndexingAlgo, self).__init__(*args, **kwargs)

    def index(self, docs, threads=2):
        """

        :param docs: list of documents
        :param threads: extent of parallelism
        :return: true if no error else false
        """
        raise NotImplementedError

    def pickle(self):
        """
        should be able to store data in indexed form somewhere
        :return:
        """
        raise NotImplementedError

    def load(self, file_path):
        """
        should be able to load from a file
        :param file_path: pkl file
        :return: algo object
        """
        raise NotImplementedError

    def docs(self, token):
        raise NotImplementedError

    def search_docs(self, query):
        """
        supposed to return set of relevant docs given string
        :param query: string
        :return:
        """
        raise NotImplementedError

    def __preprocess_sent(self, doc):
        raise NotImplementedError


class InvertedIndex(IndexingAlgo):

    __name = 'default'

    @staticmethod
    def __basic_doc_sanity(doc):
        assert isinstance(doc, document.Document), "doc shd be of Document type"
        return True

    def __init__(self):
        super(IndexingAlgo, self).__init__()
        self.__word_to_index = {}
        self.__index_to_word = []
        self._inverted_index = {}
        self.__index_to_doc = []
        self.__doc_to_index = {}
        self.max_doc_length = int(os.environ.get("max_tokens", "8"))

    def __preprocess_sent(self, sent):
        """
        same for both indexing and search time
        :param sent:
        :return:
        """
        sent = sent.strip()
        sent = re.sub(r"[^a-zA-Z0-9]+", ' ', sent).lower().split()
        return sent

    def index(self, docs, threads=1):
        warnings.warn("currently implemented only with one thread")

        for doc in tqdm(docs):
            if not self.__basic_doc_sanity(doc): continue
            if doc not in self.__doc_to_index:
                doc_index = len(self.__index_to_doc)
                self.__doc_to_index[doc] = doc_index
                self.__index_to_doc.append(doc)
                tokens = self.__preprocess_sent(doc.transformed_string)
                doc.tokens = tokens
                if len(tokens) > self.max_doc_length:
                    warnings.warn("sorry we can't have doc of size more than " + str(self.max_doc_length))
                    continue
                for token in tokens:

                    if token not in self.__word_to_index:
                        token_index = len(self.__index_to_word)
                        self.__word_to_index[token] = token_index
                        self.__index_to_word.append(token)
                        self._inverted_index[token_index] = {doc_index}
                    else:
                        token_index = self.__word_to_index[token]
                        self._inverted_index[token_index].add(doc_index)

        return True

    def search_docs(self, query):
        docs = set()
        tokens = self.__preprocess_sent(query)
        if len(tokens) > self.max_doc_length:
            warnings.warn("sorry we can't have doc of size more than " + str(self.max_doc_length))
            return tokens, set()
        for token in tokens:
            if token in self.__word_to_index:
                feature_set = self._inverted_index[self.__word_to_index[token]]
                for i in feature_set:
                    docs.add(self.__index_to_doc[i])
        return tokens, list(docs)









