from micromort.newstweets import classify
from micromort.models.trained_models.svm_mean_embeddings import Classifier, MeanEmbeddingVectorizer, PolarityClassifier


def main():
    clf = classify.Classify()


if __name__ == "__main__":
    main()