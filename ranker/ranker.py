from ranker import ranking_algorithm


class Ranker(object):
    """
    ranking abstract class
    """

    def __init__(self, ranking_algo):
        assert isinstance(ranking_algo, ranking_algorithm.RankingAlgo)
        self.ranking_algo = ranking_algo

    def get_ordered_results(self, tokens, docs):
        return self.ranking_algo.get_ordered_results(tokens, docs)
