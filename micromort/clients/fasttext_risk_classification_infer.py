import os
from micromort.models.risk_classification.multilabel_classification import \
    FastTextMultiLabelClassifier
from micromort.datasets.risk_dataset import RiskDataset
import numpy as np
import copy
from micromort.resources.configs.mongodbconfig import mongodb_config
import pymongo
import datetime

if __name__ == '__main__':
    config_file = os.path.join('.', 'coarse_aspect_config.pkl')

    classifier = FastTextMultiLabelClassifier(config_file=config_file,
                                              load_model_from_file=True)

    MAX_SENTENCE_LENGTH = 200
    risk_test_dataset = RiskDataset(train=False, use_headlines_only=False,
                                    max_sentence_length=MAX_SENTENCE_LENGTH)
    NUM_TEST = len(risk_test_dataset)
    class_labels = ['health', 'safety_security', 'environment',
                    'social_relations', 'meaning_in_life', 'achievement',
                    'economics', 'politics', 'not_applicable']
    class_labels = np.array(class_labels)

    MONGO_URL = mongodb_config['onespace_host']
    MONGO_PORT = mongodb_config['port']
    MONGO_DB = mongodb_config['db']

    client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db['risk_categorized_news']
    labeling_collection = db['news_labeling']


    test_data = []
    test_labels = []
    for j in range(NUM_TEST):
        sentence, label = risk_test_dataset[j]
        test_data.append(sentence)
        test_labels.append(label)

    test_data = np.array(test_data)
    test_labels = np.array(test_labels)

    scores, predicted_labels = classifier.multilabel_predict(test_data)
    print(predicted_labels.shape)

    annotated_data = copy.deepcopy(risk_test_dataset.test_annotated_data)
    for idx, data in enumerate(annotated_data):
        _ = data.pop('risk_category', None)
        labels = predicted_labels[idx]
        labels = class_labels[np.where(labels == 1)[0].astype(int)].tolist()
        data['risk_category'] = labels
        doc = labeling_collection.find_one({'url': data['article_url']})
        try:
            date = int(doc['date'])
            date = datetime.datetime.fromtimestamp(date)
        except ValueError:
            date = doc['date']
            date = datetime.datetime.strptime(date, '%a %d %B %Y %H:%M:%S %z')
        data['date'] = date

    collection.insert_many(annotated_data)


