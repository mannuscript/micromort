from micromort.datasets.risk_annotated_base import RiskAnnotatedBase
import numpy as np
from pydash.collections import at as pluck_at


class RiskDataset(RiskAnnotatedBase):
    def __init__(self,
                 max_sentence_length=15,
                 train=True,
                 train_proportion=0.8,
                 use_headlines_only=True):

        RiskAnnotatedBase.__init__(self,
                                   use_headlines_only)
        self.max_sentence_length = max_sentence_length
        self.train = train
        self.train_proportion = train_proportion
        self.train_indices, self.test_indices = self.get_train_test_indices()
        (self.train_annotated_data, self.test_annotated_data), \
        (self.train_tokenized_article_texts,
         self.test_tokenized_article_texts), (self.train_tokenized_article_headlines,
                                              self.test_tokenized_article_headlines), \
        (self.train_risk_labels, self.test_risk_labels), (self.train_sentiment_labels,
                                                          self.test_sentiment_labels) = \
            self.get_train_test_split()

        # sanity checks
        assert len(self.train_annotated_data) == len(
            self.train_tokenized_article_texts) == len(
            self.train_tokenized_article_headlines) == len(self.train_risk_labels) == len(
            self.train_sentiment_labels)

        assert len(self.test_annotated_data) == len(self.test_tokenized_article_texts) \
               == len(self.test_tokenized_article_headlines) == len(
            self.test_risk_labels) == len(self.test_sentiment_labels)

    def __len__(self):
        if self.train:
            return len(self.train_indices)
        else:
            return len(self.test_indices)

    def __getitem__(self, index):
        if self.train:
            if self.use_headlines_only:
                tokens = self.train_tokenized_article_headlines[index]
            else:
                tokens = self.train_tokenized_article_headlines[index] + \
                         self.train_tokenized_article_texts[index]

            risk_label = self.train_risk_labels[index]
        else:
            if self.use_headlines_only:
                tokens = self.test_tokenized_article_headlines[index]
            else:
                tokens = self.test_tokenized_article_headlines[index] + \
                         self.test_tokenized_article_texts[index]

            risk_label = self.test_risk_labels[index]

        if len(tokens) >= self.max_sentence_length:
            tokens = tokens[:self.max_sentence_length]
        else:
            difference = self.max_sentence_length - len(tokens)
            tokens.extend(['<PAD>'] * difference)

        # convert the tokens to indexes
        token_indices = [self.words_to_idx.get(token, 0) for token in tokens]

        # convert the indices into onehot format

        # 90 comes from the fact that the labels are from 91 to 99
        labels = list(map(lambda x: (x % 90) - 1, risk_label))
        one_hot = np.zeros(9)
        one_hot[labels] = 1

        return token_indices, one_hot

    def get_train_test_indices(self):
        num_data = len(self.annotated_data)
        num_train = int(np.ceil(self.train_proportion * num_data))
        num_test = num_data - num_train

        print("Train proportion: {0}, Number of train {1}, Number of test {2}".format(
            self.train_proportion, num_train, num_test))

        # Get random indices
        np.random.seed(1729)
        train_indices = np.random.choice(np.arange(num_data), size=num_train,
                                         replace=False)
        test_indices = list(set(np.arange(num_data)).difference(set(train_indices)))

        return train_indices, test_indices

    def get_train_test_split(self):

        train_data = pluck_at(self.annotated_data, *self.train_indices)
        test_data = pluck_at(self.annotated_data, *self.test_indices)
        train_tokenized_article_texts = pluck_at(self.tokenized_article_texts,
                                                 *self.train_indices)

        test_tokenized_article_texts = pluck_at(self.tokenized_article_texts,
                                                *self.test_indices)

        train_tokenized_article_headlines = pluck_at(self.tokenized_article_headlines,
                                                     *self.train_indices)

        test_tokenized_article_headlines = pluck_at(self.tokenized_article_headlines,
                                                    *self.test_indices)

        train_risk_labels = pluck_at(self.risk_labels, *self.train_indices)
        train_sentiment_labels = pluck_at(self.sentiment_labels, *self.train_indices)

        test_risk_labels = pluck_at(self.risk_labels, *self.test_indices)
        test_sentiment_labels = pluck_at(self.sentiment_labels, *self.test_indices)

        return (train_data, test_data), (train_tokenized_article_texts,
                                         test_tokenized_article_texts), (
                   train_tokenized_article_headlines, test_tokenized_article_headlines), \
               (train_risk_labels, test_risk_labels), (train_sentiment_labels,
                                                       test_sentiment_labels)

    def indices_to_tokens(self, indices):
        tokens = [self.idx_to_words[index] for index in indices]
        return tokens


if __name__ == '__main__':
    risk_dataset = RiskDataset()
    sentence, label = risk_dataset[1]
    print(sentence)
    print(risk_dataset.indices_to_tokens(sentence))
    print(risk_dataset.test_annotated_data[0])
