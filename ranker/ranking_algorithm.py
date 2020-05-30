import os
import warnings

class RankingAlgo(object):
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
        super(RankingAlgo, self).__init__(*args, **kwargs)

    def get_ordered_results(self, query_tokens, docs):
        raise NotImplementedError

    def __ranking_function(self, doc, query_tokens):
        """
        score a doc and query calculate score of a doc,
        assumption is that all features can be extracted from query tokens and docs
        :param doc:
        :param query_tokens:
        :return:
        """


class DefaultRankingAlgo(RankingAlgo):

    __name = 'default'

    def __init__(self):
        super(RankingAlgo, self).__init__()
        self.max_tokens = int(os.environ.get("max_tokens", "8"))

    def __score_query(self, query_tokens):
        j = self.max_tokens
        ret = {}
        for i in range(len(query_tokens)):
            if query_tokens[i] in ret:

                ret[query_tokens[i]].append(j)
            else:
                ret[query_tokens[i]] = [j]
            j -= 1
        return ret

    def __ranking_function(self, doc, scored_query):

        j = self.max_tokens
        score = 0
        for i in doc.tokens:
            if i in scored_query:
                lt = scored_query[i]
                for ii in lt:
                    score += ii * j
            j -= 1
        return score

    def get_ordered_results(self, query_tokens, docs):
        assert isinstance(docs, list), "doc should be list of relevant docs"
        if len(query_tokens) > self.max_tokens:
            warnings.warn("sorry we can't have doc of size more than " + str(self.max_tokens))
            return []
        ordered_docs = []
        for doc in docs:
            ordered_docs.append((doc.name, self.__ranking_function(doc, self.__score_query(query_tokens))))
        ordered_docs = sorted(ordered_docs)
        return (sorted(ordered_docs, key = lambda x: x[1], reverse=True))





