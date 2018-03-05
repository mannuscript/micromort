import os

import tensorflow as tf
from progressbar import ProgressBar, Bar, Percentage

from micromort.models.classify_base_model import *
from micromort.utils.evaluation_measures_multilabel_classification import *
from micromort.utils.general_utils import load_pickle, save_pickle
from micromort.utils.general_utils import write_array_to_hdf_file, \
    read_array_from_hdf_file
from micromort.utils.language_utils import thresholding
import numpy as np

"""
    This is meant to do multi label classification
    For example: A document may belong to more than one class
    If there is a statement like
    ""The pasta is good but it is costly""
    Then this sentence belongs to both the food and the price category
    The six categories that are considered are
    Food, Service, Price, Ambience, Annotation and Others
    These are the six categories that are present in the literature

    This is done using the fast text paper that is given in the link below
    https://arxiv.org/abs/1607.01759v2(Bag of tricks for efficient
    text classification)

    The implementation of this is available in keras at the following url
    https://github.com/fchollet/keras/blob/master/examples/imdb_fasttext.py

    This implements the paper where the sigmoid activation layer (just one
    hidden layer.. YES one hidden layer only) and the softmax layer with
    cross entropy loss is added.

    For multi label learning you would require the sigmoid cross entropy
    error and Thresholding (to decide how many classes the labels belong
    to) which is done in this classifier.

    Both are supported in this class

    TODO: The word embeddings are actually trained along with other
    training parameters in the paper. However there is no support
    provided for using pre-trained word vectors

"""


class FastTextMultiLabelClassifier(ClassifyBaseModel):
    def __init__(self, train_features=None, train_labels=None, validation_features=None,
                 validation_labels=None, config=None, config_file=None,
                 load_model_from_file=False):
        """
        :param train_features: type:ndarray
                               shape: N * T
                               N - Number of training examples
                               T - Number of tokens
                               All the documents that are sent should
                               have the same number of tokens
        :param train_labels: type: ndarray
                             shape: N * N_c
                             N - Number of training examples
                             N_c: Number of classes
                             One sentence may belong to a number of
                             classes
        :param validation_features: type: ndarray
                                    shape: N * T
                                    N - Number of validation examples
                                    T - Number of tokens
        :param validation_labels: type: ndarray
                                  shape: N * N_c
                                  N - Number of validation examples
                                  N_c - Number of classes
        :param config: type: dictionary
               learning_rate
               learning_type
               num_hidden
               num_epochs
               batch_size
               log_folder
               test_log_folder
               train_log_folder
               model_folder
               reg
               embedding_dimension - embedding dimension of the word vectors
               vocab_size - size of the vocabulary
               multilabel - True or False
               If this is true then multilabel classification is done
               If this is false then the standard multi-class classification
               is done
        """

        # This load_model_from_file is a hot fix
        # This loads everything it needs from the files and initializes the graph
        # Then you have to change it to handle this in a more graceful manner
        # Explicitly mentioning the different parameters that will be used
        self.X = None  # placeholder holding training data
        self.y = None  # placeholder for training labels
        self.W_embed = None  # Embedding weights of the shape |V| * D
        self.W = None  # Weights of the linear classifier
        self.b = None  # biases of the linear classifier
        self.WeightsThreshold = None  # Numpy vector of shape (Nc + 1) that is
        # learned from the trained multi-label
        # classification

        if load_model_from_file and not config_file:
            print("If you want to load the model from the file then please provide" \
                  "a config file where all the model parameters are stored")

        if load_model_from_file and config_file:
            config = load_pickle(config_file)
            self.session = tf.Session()
            self.initialize_from_config(config)
            self.restore_model()

        # Build the graph and execute with a loss function
        # 1. Add the placeholders
        # 2. Initialize the parameters
        # 3. Calculate the scores
        # 4. Add the loss operation
        # 5. Add the accuracy operation
        # 6. Add the accuracy operation
        # 7. Add the SUMMARIES operation
        # 8. Add the summary writers
        # 9. Add the saver object for saving the model parameters

        if not load_model_from_file:
            save_pickle(config, './coarse_aspect_config.pkl')
            self.initialize_from_config(config)
            super(FastTextMultiLabelClassifier, self).__init__(train_features,
                                                               train_labels,
                                                               validation_features,
                                                               validation_labels,
                                                               config)
            self.add_placeholder()
            self.initialize_parameters()
            self.logits = self.calculate_scores()
            self.loss, self.loss_summary = self.add_loss()
            self.train_op = self.add_optimiser()
            self.accuracy_op, self.accuracy_summary = self.calculate_accuracy()
            self.merged = self.add_summaries_operation()
            self.summary_writer = tf.summary.FileWriter(self.log_folder)
            self.train_summary_writer = tf.summary.FileWriter(self.train_log_folder)
            self.test_summary_writer = tf.summary.FileWriter(self.test_log_folder)
            self.saver = tf.train.Saver()

    def initialize_from_config(self, config):
        self.learning_rate = config['learning_rate']
        self.learning_type = config['learning_type']
        self.hidden_size = config['num_hidden']
        self.num_epochs = config['num_epochs']
        self.batch_size = config['batch_size']
        self.log_folder = config['log_folder']
        self.test_log_folder = config['test_log_folder']
        self.train_log_folder = config['train_log_folder']
        self.models_folder = config['models_folder']
        self.reg = config['reg']
        self.embedding_dimension = config['embedding_dimension']
        self.vocab_size = config["vocab_size"]
        self.isMultiLabel = config['multilabel']

    def add_placeholder(self):
        with tf.name_scope("Inputs") as scope:
            self.X = self.get_placeholder([None, self.num_tokens], dtype=tf.int64)
            self.y = self.get_placeholder([None, self.num_classes])

    def add_loss(self):
        with tf.name_scope("Loss") as scope:
            if self.isMultiLabel:
                loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits,
                                                               labels=self.y)
                loss = tf.reduce_mean(tf.reduce_sum(loss, reduction_indices=[1]))
            else:
                loss = tf.reduce_mean(
                    tf.nn.softmax_cross_entropy_with_logits(self.logits, self.y))

            reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
            loss += sum(reg_losses)
        loss_summary = tf.summary.scalar("loss_summary", loss)
        return loss, loss_summary

    def add_optimiser(self):
        """

                Add the optimizer function to perform Gradient Descent
                Returns: None
                """
        if self.learning_type not in ["vanilla", "adam", "adagrad", "rmsprop"]:
            raise ValueError(
                "Please provide any of [vanilla, adam, adagrad, rmsprop] for optimisation")

        with tf.name_scope("gradient_descent") as scope:
            if self.learning_type == "vanilla":
                train_op = tf.train.GradientDescentOptimizer(
                    self.learning_rate).minimize(self.loss)
            elif self.learning_type == "adam":
                train_op = tf.train.AdamOptimizer(self.learning_rate).minimize(
                    self.loss)
            elif self.learning_type == "adagrad":
                train_op = tf.train.AdagradOptimizer(
                    self.learning_rate).minimize(self.loss)
            elif self.learning_type == "rmsprop":
                train_op = tf.train.RMSPropOptimizer(
                    self.learning_rate).minimize(self.loss)
            return train_op

    def add_summaries_operation(self):
        return tf.summary.merge([self.loss_summary, self.accuracy_summary])

    def calculate_accuracy(self):
        with tf.name_scope("accuracy") as scope:
            if not self.isMultiLabel:
                scores = tf.nn.softmax(self.logits)
                correct_predictions = tf.equal(tf.argmax(scores, 1),
                                               tf.argmax(self.y, 1))
                accuracy = tf.reduce_mean(
                    tf.cast(correct_predictions, tf.float32)) * 100
            else:
                scores = tf.nn.sigmoid(self.logits)
                # Have to calculate the one error for the scores here
                error = tf.py_func(one_error, [scores, self.y], [tf.float64])[0]
                accuracy = tf.subtract(tf.constant(1.0, dtype=tf.float64), error)
            accuracy_summary = tf.summary.scalar("accuracy", accuracy)
        return accuracy, accuracy_summary

    def calculate_scores(self):
        # 1. Embed the documents of shape N * T into N * T * D
        # where N is the number of training examples
        # T is the number of tokens(represented as numbers)
        # D is the embedding dimension

        # 2. Average along the second dimension which is T
        # to get N * D which makes sure that every document is represented
        # as a D dimensional vector

        # 3. Then do the affine transform mentioned in the paper as the
        # linear classifier

        # Return the logits. On these logits they use the softmax function

        # -----------------------------------------------------------------------
        # 1. Use the tensorflow embedding lookup to get a tensor of shape
        # N * T * D
        embedding = tf.nn.embedding_lookup(self.W_embed, self.X)

        # 2. Average along the second dimension to get N * D
        embedding_average = tf.reduce_mean(embedding, reduction_indices=[1])

        # 3. Give it an affine transform
        logits = tf.matmul(embedding_average, self.W) + self.b
        # -----------------------------------------------------------------------
        return logits

    def initialize_parameters(self):
        # There is one variable that is of the size |V| * D
        # where V is the size of the vocab and
        # D is the embedding dimension
        # This word embedding is directly learnt during the entire training

        # There is one hidden layer that H hidden units
        # The weights are of the size
        with tf.name_scope("Embedding_weights") as scope:
            self.W_embed = tf.get_variable("W_embed", shape=[self.vocab_size,
                                                             self.embedding_dimension],
                                           initializer=tf.contrib.layers.xavier_initializer(
                                               seed=1729))

        with tf.name_scope("Linear_classifier_weights") as scope:
            self.W = tf.get_variable("W", shape=[self.embedding_dimension,
                                                 self.num_classes],
                                     initializer=tf.contrib.layers.xavier_initializer(
                                         seed=1729),
                                     regularizer=tf.contrib.layers.l2_regularizer(
                                         self.reg))
            self.b = tf.get_variable("b", shape=[self.num_classes],
                                     initializer=tf.constant_initializer(0.0))

    def multilabel_predict(self, test_features):
        """
        Given the test features,
             it calculates the logits, predicts the scores
             Performs the thresholding and returns the
             predicted labels
        Args:
            test_features:  Type: ndarray
                            shape: N * T
                            N - Number of samples
                            T - number of tokens in the sentence
        Returns:
            scores: Type: ndarray
                    shape: N * Nc
                    N - Number of training examples
                    Nc - Number of classes
            predicted_labels: Type: ndarray
                              shape: N * Nc
                              N - Number of test features
                              Nc - Number of examples
        """
        num_test, num_tokens = test_features.shape
        self.X = self.get_placeholder([None, num_tokens], dtype=tf.int64)
        self.logits = self.calculate_scores()
        logits = \
            self.session.run([self.logits], feed_dict={self.X: test_features})[0]
        scores = tf.nn.sigmoid(logits)
        scores = scores.eval(
            session=self.session)  # This should be a numpy array
        threshold_weights = self.WeightsThreshold
        # augment the scores
        scores_ = np.column_stack((scores, np.ones(scores.shape[0])))
        thresholds = np.dot(scores_, threshold_weights)
        thresholds = thresholds.reshape((-1, 1))

        # If the scores are greater than the corresponding threshold
        # then they are set to 1
        predicted_labels = (scores >= thresholds).astype(np.int64)

        return scores, predicted_labels

    def test(self, test_features, test_labels):
        """

        Args:
            test_features: type: ndarray
                           shape: N * T
                           N - Number of training examples
                           T - Number of tokens in each sentence
            test_labels: type: N * Nc
                         N - number of training examples
                         Nc - Number of classes
        Returns: accuracy for multiclass classification
                 The bi-partition scores and ranking scores
                 for multi-label classification
        """
        if not self.isMultiLabel:
            return self.session.run([self.accuracy_op],
                                    feed_dict={self.X: test_features,
                                               self.y: test_labels})
        else:
            # If the scores are greater than the corresponding threshold
            # then they are set to 1
            scores, predicted_labels = self.multilabel_predict(test_features)

            # Calculating the ranking measures
            one_err = one_error(scores, test_labels)
            coverage_ = coverage(scores, test_labels)
            ap = 1 - average_precision(scores, test_labels)

            # calculating the  bi-partition measures
            mi_p = micro_precision(predicted_labels, test_labels)
            mi_r = micro_recall(predicted_labels, test_labels)
            mi_fscore = micro_fscore(predicted_labels, test_labels)
            ma_p = macro_precision(predicted_labels, test_labels)
            ma_r = macro_recall(predicted_labels, test_labels)
            ma_fscores = macro_fscore(predicted_labels, test_labels)

            # semeval_2016 fscores
            semeval_p, semeval_r, semeval_f = semeval_measures(predicted_labels,
                                                               test_labels)

            return (one_err, coverage_, ap, mi_p, mi_r, mi_fscore, ma_p, ma_r,
                    ma_fscores, semeval_p, semeval_r, semeval_f)

    def train(self, print_every=1, log_summary=True):

        if not os.listdir(self.models_folder):
            init_operation = tf.initialize_all_variables()
            self.session.run(init_operation)
            num_iterations = 0

            # For every epoch
            # Pass once through all the training examples
            # At the end of every approach, check the loss and validation accuracy

            for i in range(self.num_epochs):
                total_iterations = np.ceil(self.num_train / self.batch_size)
                pb = ProgressBar(widgets=[Bar('#'), Percentage()],
                                 maxval=total_iterations).start()
                average_loss = 0.0  # average loss for the epoch
                # start of the iterations of the epoch
                for iteration, (train_data, train_labels) in enumerate(
                        self.get_batch(self.batch_size)):
                    _, loss_summary, loss = self.session.run(
                        [self.train_op, self.merged, self.loss],
                        feed_dict={self.X: train_data, self.y: train_labels})
                    average_loss += loss
                    pb.update(iteration)
                    num_iterations += 1
                    self.summary_writer.add_summary(loss_summary, num_iterations)

                pb.finish()

                # end of the iterations of the epoch
                # calculating the validation loss and validation accuracy
                average_loss = average_loss / (iteration + 1)
                print("Loss at the end of epoch %d is %f" % (i + 1, average_loss))

                training_summary, training_accuracy = self.session.run([self.merged,
                                                                        self.accuracy_op],
                                                                       feed_dict={
                                                                           self.X: self.train_data,
                                                                           self.y: self.train_labels})
                print("Training accuracy at the end of epoch %d is %f" % (
                i + 1, training_accuracy))

                validation_summary, validation_accuracy = self.session.run([self.merged,
                                                                            self.accuracy_op],
                                                                           feed_dict={
                                                                               self.X: self.validation_data,
                                                                               self.y: self.validation_labels})
                print("Validation accuracy at the end of epoch %d is %f" % (
                i + 1, validation_accuracy))

                self.train_summary_writer.add_summary(training_summary, i)
                self.test_summary_writer.add_summary(validation_summary, i)

            # Once the model has been trained, if this is being trained for
            # a multi-label classifier then you need to learn the thresholding weights
            if self.isMultiLabel:
                print("THRESHOLDING")
                self.WeightsThreshold = self.__thresholding(self.train_data,
                                                            self.train_labels)
                # Save this array to hdf file for later restoration
                write_array_to_hdf_file(self.models_folder + "weightsThreshold.h5",
                                        'weightsThreshold', self.WeightsThreshold)

                # Store the weights threshold in the models folder as a pickle file

            self.saver.save(self.session, self.models_folder +
                            "coarse_aspect_classification_weights.ckpt")

        else:
            # Load the variables that are stored in the file and
            # the training is done
            self.restore_model()

    def __thresholding(self, training_data, training_labels):
        """
        This Chooses the thresholds.
        Consider a data point x_i that has the following distribution of
        class probabilities
        C_i =[0.1, 0.2, 0.5, 0.9]
        if c^i > t then x_i belongs to the class
        This t is learnt by formulating it is a threshold problem

        Args:
            training_data: Type: ndarray
                           Shape: N * Nc

        Returns: W - Type: ndarray
                 shape: Nc+1, 1
                 Nc - Number of classes
                 +1 for the biases






        """

        # Use this only when doing the multi-label classification
        if not self.isMultiLabel:
            return

        labels = training_labels
        logits = self.session.run([self.logits], feed_dict={self.X: training_data})[0]

        scores = tf.nn.sigmoid(logits)
        scores = scores.eval(session=self.session)
        thresholds = thresholding(scores, labels)
        ones = np.ones((self.num_train, 1))
        X = np.concatenate((scores, ones), axis=1)

        pseudo_inverse = np.linalg.inv(X.T.dot(X))
        W = pseudo_inverse.dot(X.T.dot(thresholds))
        return W

    def restore_model(self):
        print("THE MODEL IS BEING RESTORED")
        new_saver = tf.train.import_meta_graph(self.models_folder +
                                               'coarse_aspect_classification_weights.ckpt.meta')
        new_saver.restore(self.session, self.models_folder +
                          'coarse_aspect_classification_weights.ckpt')
        all_vars = tf.trainable_variables()
        self.W_embed = \
        [variable for variable in all_vars if variable.name == 'W_embed:0'][0]
        self.W = [variable for variable in all_vars if variable.name == 'W:0'][0]
        self.b = [variable for variable in all_vars if variable.name == "b:0"][0]
        self.WeightsThreshold = read_array_from_hdf_file(self.models_folder +
                                                         "weightsThreshold.h5",
                                                         'weightsThreshold')
