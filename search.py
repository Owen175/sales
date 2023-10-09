import spacy


class Search:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def similarity(self, w1, w2):
        words = w1 + ' ' + w2
        tokens = self.nlp(words)
        token1, token2 = tokens[0], tokens[1]
        return token1.similarity(token2)

    def search(self, search_term, keywords_list):
        item_similarity = []
        ls = search_term.split(' ')
        for keywords in keywords_list:
            ls_similarity = []
            for keyword in keywords:
                for term in ls:
                    ls_similarity.append(self.similarity(term, keyword))
            sorted_similarity = sorted(ls_similarity, reverse=True)
            count = 0
            total_similarity = 0
            while count < 5 and count < len(sorted_similarity):
                total_similarity += sorted_similarity[count]
                count += 1
            item_similarity.append(total_similarity)
        return item_similarity


search_function_ranker = Search()


