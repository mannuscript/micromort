import numpy as np
import tensorflow as tf
import time
import random

from micromort.utils.general_utils import partition_lists


class ClassifyBaseModel(object):
    """
        This models the base class that is required for
        all the classifications in Tensor flow

        Tensorflow classifications model
        Inputs as placeholders
        Output labels as placeholder
    """

    def __init__(self, training_features, train_labels,
                 validation_features, validation_labels,
                 config):
        print("Initialising the session in the base classify model")
        self.train_data = training_features
        self.validation_data = validation_features
        if train_labels.ndim == 1:
            self.train_labels = self.make_it_hot(train_labels)
        elif train_labels.ndim == 2:
            self.train_labels = train_labels

        if validation_labels.ndim == 1:
            self.validation_labels = self.make_it_hot(validation_labels)
        elif validation_labels.ndim == 2:
            self.validation_labels = validation_labels
        self.config = config
        self.num_train, self.num_tokens = training_features.shape
        self.num_train, self.num_classes = self.train_labels.shape
        self.session = tf.Session()

        print("Number of training examples %d" % self.num_train)

    def add_loss(self):
        """
        THE TRUE DISTRIBUTION WILL BE A PLACEHOLDER
        Returns: loss - scalar

        """
        raise NotImplementedError

    def add_summaries_operation(self):
        pass

    def add_placeholder(self):
        """
        Add all the placeholder that are required for the model here
        Returns:
        """
        raise NotImplementedError

    def calculate_accuracy(self):
        """
        Add the operation to calculate the accuracy for your model
        Returns:

        """
        raise NotImplementedError

    def calculate_scores(self):
        """
        Return the scores of the model
        If it is convolutional neural networks or neural networks
        calculate the activations and final scores before the softmax loss is
        added
        """
        raise NotImplementedError

    def get_batch(self, batch_size):
        """
        Args:
            batch_size: an integer
        Returns: The next batch of training data and training labels
        and all that is needed for training the minibatch

        """
        # 1. Shuffle the indices
        # 2. Randomly pick batch_size number of integers from the shuffled set of indices
        # 3. Get the corresponding data
        # 4. Convert the ys into a one hot vector for calculating the loss
        indices = np.arange(self.num_train)
        np.random.seed(1729)
        np.random.shuffle(indices)
        num_partitions = int(np.ceil(float(self.num_train) / batch_size))
        partitions = partition_lists(indices.tolist(), num_partitions)
        processed_training_examples = 0

        for partition in partitions:
            processed_training_examples += len(partition)
            train_data = self.train_data[partition]
            train_labels = self.train_labels[partition]
            assert np.isnan(np.sum(train_data)) == False
            assert np.isnan(np.sum(train_labels)) == False
            yield train_data, train_labels
        assert processed_training_examples == self.num_train

    def get_random_batch(self, batch_size):

        random.seed(time.time())
        indices = np.arange(self.num_train)
        np.random.shuffle(indices)
        num_partitions = int(np.ceil(float(self.num_train) / batch_size))
        partitions = partition_lists(indices.tolist(), num_partitions)

        random_partition_index = np.random.randint(0, high=len(partitions), size=1)
        random_partition = partitions[random_partition_index]
        train_data = self.train_data[random_partition]
        train_labels = self.train_labels[random_partition]
        assert np.isnan(np.sum(train_data)) == False
        assert np.isnan(np.sum(train_labels)) == False
        return train_data, train_labels

    def get_placeholder(self, size, dtype=tf.float32):
        """
        SHOULD NOT BE CHANGED IN THE INHERITED CLASS
        Args:
            size: The size of the placeholder to be created
            dtype: Data type for the placeholder

        Returns: tf.placeholder
        """
        return tf.placeholder(dtype, size)

    def initialize_parameters(self):
        """
        Initialize the parameters of the model
        Returns:

        """
        raise NotImplementedError

    def make_it_hot(self, labels):
        num_examples = labels.shape[0]
        one_hot_labels = np.zeros((num_examples, self.num_classes), dtype=np.float32)
        one_hot_labels[range(num_examples), labels] = 1.0
        return one_hot_labels

    def test(self, test_features, test_labels):
        """
        Calculates the accuracy on the test data set that is passed
        Args:
            test_features: Test features of shape (N, D)
            test_labels: : Test labels of shape (N)

        Returns: test_accuracy

        """
        raise NotImplementedError

    def train(self):
        """

        Args:
            session: The tensor flow session on which the various operations can be run
            in parallel

        Returns:
        """
        raise NotImplementedError

    def close_session(self):
        self.session.close()
