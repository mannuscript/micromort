from micromort.models.trained_models.svm_mean_embeddings import Classifier, MeanEmbeddingVectorizer, PolarityClassifier

class Classify:

    """
        Note:
        Loading of model is a memory and time extensive operation, it has to be done 
        one time and the object of the Classifier should be retained in the memory of the pipeline.
    """
    def __init__(self):
            self.life_domain_classifier = Classifier(base_path="/Users/mannumalhotra/code/work/micromort/micromort/resources/trained_models/oneVsAll_linear_SVM_mean_embeddings/")
            self.life_domain_classifier = PolarityClassifier()


    def apply_classifiers(self, articleBody, articleTitle):
        labels = {
            "life_domains" : self.getLifeDomains(),
            "polarity" : self.getPolarity(),
        }
        return labels

    def getLifeDomains(self, articleBody, articleTitle):
        labels = self.life_domain_classifier.predict_single(articleTitle + articleBody, True)
        return labels

    def getPolarity(self, articleBody, articleTitle):
        polarity = self.polarity_classifier.predict(articleTitle + articleBody)