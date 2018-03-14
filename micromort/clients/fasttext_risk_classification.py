from micromort.datasets.risk_dataset import RiskDataset
from tqdm import tqdm
import os
import micromort.constants as constants
import numpy as np
from micromort.models.risk_classification.multilabel_classification import \
    FastTextMultiLabelClassifier

FILE_PATHS = constants.PATHS
OUTPUTS_DIR = FILE_PATHS['OUTPUTS_DIR']

if __name__ == '__main__':

    MAX_SENTENCE_LENGTH = 200
    risk_train_dataset = RiskDataset(use_headlines_only=False,
                                     max_sentence_length=MAX_SENTENCE_LENGTH)
    risk_test_dataset = RiskDataset(train=False, use_headlines_only=False,
                                    max_sentence_length=MAX_SENTENCE_LENGTH)

    ###########################################################################
    #                   SETUP THE HYPER-PARAMETERS                            #
    ###########################################################################
    VOCAB_SIZE = risk_train_dataset.get_vocab_size()
    LEARNING_RATE = 1e-03
    NUM_EPOCHS = 80
    LEARNING_TYPE = 'adam'
    BATCH_SIZE = 64
    REG = 1e-01
    NUM_HIDDEN = 1024
    EMBEDDING_DIMENSION = 300
    MULTILABEL = True
    LOGS_FOLDER = os.path.join(OUTPUTS_DIR, 'fastext_risk_classification', 'logs')
    TEST_LOGS_FOLDER = os.path.join(OUTPUTS_DIR, 'fastext_risk_classification', 'logs',
                                    'train')
    TRAIN_LOGS_FOLDER = os.path.join(OUTPUTS_DIR, 'fastext_risk_classification',
                                     'logs', 'test')
    MODELS_FOLDER = os.path.join(OUTPUTS_DIR, 'fastext_risk_classification', 'models')
    NUM_TRAIN = len(risk_train_dataset)
    NUM_TEST = len(risk_test_dataset)

    ###########################################################################
    #                   PREPARE THE DATASET                          #
    ###########################################################################
    train_data = []
    train_labels = []
    for i in tqdm(range(NUM_TRAIN), total=NUM_TRAIN, desc="Collecting the training data"):
        sentence, label = risk_train_dataset[i]
        train_data.append(sentence)
        train_labels.append(label)

    test_data = []
    test_labels = []
    for j in range(NUM_TEST):
        sentence, label = risk_test_dataset[j]
        test_data.append(sentence)
        test_labels.append(label)

    train_data = np.array(train_data)
    train_labels = np.array(train_labels)
    test_data = np.array(test_data)
    test_labels = np.array(test_labels)

    ###########################################################################
    #                  CONFIG AND RIG THE CLASSIFIER                          #
    ###########################################################################
    config = dict(learning_rate=LEARNING_RATE,
                  learning_type=LEARNING_TYPE,
                  num_epochs=NUM_EPOCHS,
                  batch_size=BATCH_SIZE,
                  reg=REG,
                  num_hidden=NUM_HIDDEN,
                  embedding_dimension=EMBEDDING_DIMENSION,
                  vocab_size=VOCAB_SIZE,
                  multilabel=MULTILABEL,
                  log_folder=LOGS_FOLDER,
                  test_log_folder=TEST_LOGS_FOLDER,
                  train_log_folder=TRAIN_LOGS_FOLDER,
                  models_folder=MODELS_FOLDER
                  )

    classifier = FastTextMultiLabelClassifier(train_data, train_labels,
                                              test_data, test_labels,
                                              config)

    classifier.train(print_every=10, log_summary=True)

    (one_err, coverage_, ap, mi_p, mi_r, mi_fscore, ma_p, ma_r,
     ma_fscores, _, _, _) = classifier.test(test_data,
                                            test_labels)

    scores = {'one_err': one_err,
              'coverage': coverage_,
              'average_precision': ap,
              'micro_precision': mi_p,
              'micro recall': mi_r,
              'micro fscore': mi_fscore,
              'macro precision': ma_p,
              'macro recall': ma_r,
              'macro fscore': ma_fscores}
    print('*' * 80)
    print('SCORES MULTILABEL PREDICT {0}'.format(scores))
    print('*' * 80)

    class_labels = ['health', 'safety_security', 'environment',
                    'social_relations', 'meaning_in_life', 'achievement',
                    'economics', 'politics', 'not_applicable']

    class_accuracy_report = classifier.get_report(test_data, test_labels, class_labels)
    print(class_accuracy_report)

    # get the examples that have false positives for a given class name
    false_positive_examples = {}

    for class_label in class_labels:
        false_positive_idxs = classifier.get_false_positive_examples(test_data,
                                                                     test_labels,
                                                                     class_label)

        false_positive_examples[class_label] = []
        for idx in false_positive_idxs:
            false_positive_examples[class_label].append(
                (risk_test_dataset.test_annotated_data[idx]
                 ['article_headline'],
                 risk_test_dataset.test_annotated_data[idx]['article_id']))

        print('*' * 80)
        print("False positive for class {0}".format(class_label))
        print('*' * 80)
        print(false_positive_examples[class_label])

    false_negative_examples = {}
    for class_label in class_labels:
        false_negative_idxs = classifier.get_false_negative_examples(test_data,
                                                                     test_labels,
                                                                     class_label)
        false_negative_examples[class_label] = []
        for idx in false_negative_idxs:
            false_negative_examples[class_label].append(
                (risk_test_dataset.test_annotated_data[idx]
                 ['article_headline'],
                 risk_test_dataset.test_annotated_data[idx]['article_id']))

        print('*' * 80)
        print("False negative for class {0}".format(class_label))
        print('*' * 80)
        print(false_negative_examples[class_label])




