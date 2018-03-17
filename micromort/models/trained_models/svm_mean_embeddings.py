import pickle
import nltk
import numpy as np
from sklearn.externals import joblib

class MyTokenizer:
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        transformed_X = []
        for document in X:
            tokenized_doc = []
            for sent in nltk.sent_tokenize(document):
                tokenized_doc += nltk.word_tokenize(sent)
            transformed_X.append(np.array(tokenized_doc))
        return np.array(transformed_X)
    
    def fit_transform(self, X, y=None):
        return self.transform(X)

class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.wv.syn0[0])

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = MyTokenizer().fit_transform(X)
        
        return np.array([
            np.mean([self.word2vec.wv[w] for w in words if w in self.word2vec.wv]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])
    
    def fit_transform(self, X, y=None):
        return self.transform(X)


class Classifier:
    
    def __init__(self):
        base_path = "../resources/trained_models/oneVsAll_linear_SVM_mean_embeddings/"
        classifier_model = base_path + "svmWithEmbeddings.sav"
        mean_embedding_vectorizer_model = base_path + "mean_embedding_vectorizer.sav"
        mlb_model = base_path + "mlb"
        self.classifier = pickle.load(open(classifier_model, 'rb'))
        self.mean_embedding_vectorizer = joblib.load(mean_embedding_vectorizer_model)
        self.mlb = pickle.load(open(mlb_model, 'rb'))

        self.class_mapping = {
                      91: 'health', 92: 'safety_security', 93 : 'environment',
                      94 : 'social_relations', 95 : 'meaning_in_life', 96 : 'achievement',
                      97 : 'economics', 98 : 'politics', 99 : 'not_applicable', 0 : 'skip' }


    def predict_single(self, article, with_label = False):

        pred = self.mlb.inverse_transform(
            self.classifier.predict(
                self.mean_embedding_vectorizer.fit_transform([article])
            )
        )[0]
        if with_label:
            return self.convertToLabels(pred)
        else:
            return list(pred)

    def predict_all(self, articles, with_label = False):
        result = []
        for article in articles:
            pred = self.predict_single(article, with_label)
            result.append((article, pred))
        return result
        

    def convertToLabels(self, tup):
        labels = []
        for t in tup:
            labels.append(self.class_mapping.get(t, ""))
        return labels


if __name__ == "__main__":
    c = Classifier()
    news_article = "LONDON (NYTIMES) - The anonymous letters arrived this weekend in plain white envelopes with second-class stamps, and were sent to people in at least six communities in England.\n\nInside was a message so hateful that it sent ripples of alarm across the country and prompted a national counterterrorism investigation.\n\nThe message said April 3 would be \"Punish a Muslim Day\", and points would be awarded for acts of violence: 25 for pulling a woman's head scarf, 500 for murdering a Muslim and 1,000 for bombing a mosque.\n\nRiaz Ahmed, a Liberal Democrat councillor in Bradford, in West Yorkshire County, told The Mirror on Saturday that he had received one of the letters at his business address.\n\n\"It seems strange that anyone would send something like this to an address in a predominantly Muslim area,\" Ahmed was quoted as saying. \"When I opened it and saw the content, I was horrified.\"\n\nPeople in Birmingham, Cardiff, Leicester, London and Sheffield have also reported receiving the notes, according to the authorities, a member of Parliament and an organisation that monitors anti-Muslim activity.\n\nThe Metropolitan Police of London and other officials have warned Britons to be vigilant, and counterterrorism officials are investigating.\n\nNaz Shah, a member of Parliament from Bradford West, said on Twitter and in a Facebook post that members of her community had received the letters and that the situation had become \"very distressful, not only those who have received the letter but also for the wider communities\". Shah said the North East Counter Terrorism Unit, which is coordinating the investigation, had informed her that the letters appeared to be linked.\n\n\"I would appeal to the wider community to remain vigilant and report any suspicious activity to the police,\" she said.\n\nThe significance of April 3, 2018, was not immediately clear. Some neo-Nazi groups use the number 18 to signify the letters of Hitler's first and last names in the alphabet.\n\nTell Mama, an organisation that tracks anti-Muslim crimes, said in a Twitter post that the hate letters sent out in Britain numbered in the \"double figures\" and that it was working with the police.\n\nAt least some letters appeared to have been mailed out of Sheffield, the group said."

    print(c.predict_single(news_article, True))