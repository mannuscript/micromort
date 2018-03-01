"""
This gives the user functions that are necessary to evaluate
multi-label classification

One error, coverage and average precision are called rank measures
which operate on the scores calculate by the classifier on different labels

Then there are bi-partition measures that operate on the labels that
are produced by the classifier
For bi-partition measure refer to the book
Introduction to information retrieval book by Manning
Pg.282
"""
import numpy as np


def one_error(scores, labels):
    """

    Args:
        scores: Type:ndarray
                shape: N * Nc
                N - Number of training examples
                Nc - Number of classes
        labels: Type: ndarray
                shape: N * Nc
                N - Number of training examples
                Nc - Number of classes
    Returns: error
             Type: float

    """
    assert scores.shape == labels.shape
    N, Nc = scores.shape
    accuracy = 0.0
    num_no_right_classes = 0
    for i in range(0, N):
        scores_row = scores[i]
        label_row = labels[i]
        positions_label_row_where_one = np.where(label_row == 1)[0]
        if len(positions_label_row_where_one) == 0:
            num_no_right_classes += 1
        else:
            position_max = np.argmax(scores_row)
            label = label_row[position_max]
            accuracy += label

    if N == num_no_right_classes:
        accuracy = 1.0
    else:
        accuracy /= (N - num_no_right_classes)

    return 1 - accuracy


def coverage(scores, labels):
    """
    Coverage measures how far along the ranked list of scores
    should we traverse to achieve maximum precision

    For examples if the ranked list of labels is given below
    [[0.8, 1.0, 0.7, 0.9]]
    and the true label for this data point is
    [[1, 0, 1, 0]]

    Then the rank is 3 i.e
    The scores corresponding to the correct labels are 0.8 and 0.7
    Now consider the descending order of scores which is
    [1.0, 0.9, 0.8, 0.7]
    The rank of 0.8 is 2 and that of 0.7 is 3
    So the maximum rank is is 3 which is the rank of the data point

    In case of tied scores for two labels (irrespective of the scores
     corresponding to positive or negative labels) they
     are taken to be the maximum one.. See the test cases for example

    Paste the formula below in latex it .
    coverage_{S}(H) = \frac{1}{m} \sum_{i=1}^{m} \max_{l \in Y_i}rank_f(x_i,l) -1

    H is the hypothesis from the input space to the output space
    m is the number of training examples
    Y_i is the labels that are assigned to the training example x_i
    S = [(x1, Y1)....(xm, Ym)]
    every Y is a subset(say 1, 2) of the total label set(say 1, 2, 3, 4)


    Args:
        scores: Type:ndarray
                shape: N * Nc
                N - Number of training examples
                Nc - Number of classes
        labels: Type: ndarray
                shape: N * Nc
                N - Number of training examples
                Nc - Number of classes
    Returns: error
             Type: float
    """
    assert scores.shape == labels.shape
    N, Nc = scores.shape

    scores_ascending = np.sort(scores, axis=1)
    average_rank = 0.0

    for i in range(N):
        right_labels_index = np.where(labels[i] == 1)[0]

        # When there are no right_labels in the datum, max_rank is 0
        if len(right_labels_index) == 0:
            max_rank = 0
        else:
            scores_corresponding_to_right_labels = scores[i][right_labels_index]
            inverse_rank = np.searchsorted(scores_ascending[i],
                                           scores_corresponding_to_right_labels)
            rank = (Nc) - inverse_rank
            max_rank = np.max(rank)
        average_rank += max_rank

    average_rank /= float(N)

    return average_rank


def average_precision(scores, labels):
    """

    The formula for calculating average precision is as follows
    avgprec_s(H) = \frac{1}{m}
                \sum_{i = 1}^{m}
                  \frac{1}{|Y_i|}
                  \sum_{y \in Y_i} \frac{|l' \in Y_i| rank_f(x_i, l') \le rank_f(x_i, l)}{rank_f(x,l)}
    Args:
        scores: Type:ndarray
                shape: N * N_c
                N - Number of training examples
                Nc - Number of classes
        labels: Type: ndarray
                shape: N * N_c
                N - Number of training examples
                N_c - Number of classes
    Returns: precision
             Type: float
    """
    assert scores.shape == labels.shape
    N, Nc = scores.shape

    precision = 0.0
    scores_ascending = np.sort(scores, axis=1)

    for i in range(0, N):
        right_labels_index = np.where(labels[i] == 1)[0]
        wrong_labels_index = np.where(labels[i] == 0)[0]
        scores_positive_labels = scores[i][right_labels_index]
        scores_negative_labels = scores[i][wrong_labels_index]

        if len(right_labels_index) == 0:
            precision = 1.0

        else:
            inverse_rank_positive_scores = np.searchsorted(scores_ascending[i],
                                                           scores_positive_labels)

            inverse_rank_negative_scores = np.searchsorted(scores_ascending[i],
                                                           scores_negative_labels)

            rank_positive_scores = Nc - inverse_rank_positive_scores
            rank_negative_scores = Nc - inverse_rank_negative_scores

            sum_over_right_labels = 0.0
            for each_rank in rank_positive_scores:
                sum_over_right_labels += len(np.where(rank_negative_scores <=
                                                      each_rank)[0]) / float(each_rank)

            precision += (sum_over_right_labels) / float(len(right_labels_index))

    precision /= N

    return round(precision, 4)


def macro_precision(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape: N * Nc
                          N - Number of training examples
                          Nc - NUmber of classes
        true_labels: Type: ndarray
                     shape: N * Nc
                     N - Number of training examples
                     Nc - Number of classes
    Returns: macros_precision
    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    tp = true_positives(predicted_labels, true_labels).astype("float64")
    fp = false_positives(predicted_labels, true_labels).astype("float64")
    sum_tp_fp = tp + fp
    # If true positives are zero, irrespective of the denominator
    # the precision is zero
    tp_zero_location = np.where(tp == 0.0)
    if len(tp_zero_location[0]) > 0:
        sum_tp_fp[tp_zero_location] = 1.0
    precision = np.sum(tp / sum_tp_fp) / float(Nc)
    return round(precision, 4)


def macro_recall(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape: N * Nc
                          N - Number of training examples
                          Nc - NUmber of classes
        true_labels: Type: ndarray
                     shape: N * Nc
                     N - Number of training examples
                     Nc - Number of classes
    Returns: macros_precision
    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    tp = true_positives(predicted_labels, true_labels).astype("float64")
    fn = false_negatives(predicted_labels, true_labels).astype("float64")
    sum_tp_fn = tp + fn
    tp_zero_locations = np.where(tp == 0.0)
    if len(tp_zero_locations[0]) > 0:
        sum_tp_fn[tp_zero_locations] = 1.0
    recall = np.sum(tp / sum_tp_fn) / float(Nc)
    return round(recall, 4)


def macro_fscore(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape: N * Nc
                          N - Number of training examples
                          Nc - NUmber of classes
        true_labels: Type: ndarray
                     shape: N * Nc
                     N - Number of training examples
                     Nc - Number of classes
    Returns: macros_precision
    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    tp = true_positives(predicted_labels, true_labels).astype("float64")
    fp = false_positives(predicted_labels, true_labels).astype("float64")
    fn = false_negatives(predicted_labels, true_labels).astype("float64")

    tp_zero_locations = np.where(tp == 0)
    denominator = (2 * tp) + fp + fn
    if len(tp_zero_locations[0]) > 0:
        denominator[tp_zero_locations] = 1
    macro_fscore = (1.0 / Nc) * (np.sum((2 * tp) / denominator))
    return round(macro_fscore, 4)


def micro_precision(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: micro precision
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    tp = true_positives(predicted_labels, true_labels).astype("float64")
    fp = false_positives(predicted_labels, true_labels).astype("float64")

    numerator = np.sum(tp)
    denominator = np.sum(tp + fp)

    numerator_zero_positions = np.where(numerator == 0.0)
    if len(numerator_zero_positions[0]) > 0:
        denominator[numerator_zero_positions] = 1.0
    precision = numerator / denominator
    return round(precision, 4)


def micro_recall(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: micro precision
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    tp = true_positives(predicted_labels, true_labels).astype("float64")
    fn = false_negatives(predicted_labels, true_labels).astype("float64")
    numerator = np.sum(tp)
    denominator = np.sum(tp + fn)
    numerator_zero_positions = np.where(numerator == 0.0)
    if len(numerator_zero_positions[0]) > 0:
        denominator[numerator_zero_positions] = 1.0
    recall = numerator / denominator
    return round(recall, 4)


def micro_fscore(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: micro precision
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    tp = true_positives(predicted_labels, true_labels).astype(np.float64)
    fp = false_positives(predicted_labels, true_labels).astype(np.float64)
    fn = false_negatives(predicted_labels, true_labels).astype(np.float64)
    numerator = np.sum(2 * tp)
    denominator = np.sum((2 * tp) + fp + fn)
    numerator_zero_positions = np.where(numerator == 0.0)
    if len(numerator_zero_positions[0]) > 0:
        denominator[numerator_zero_positions] = 1.0
    fscore = numerator / denominator
    return round(fscore, 4)


def true_positives(predicted_labels, true_labels):
    """
    Predicted condition positive
    True condition positive
    Get the number of true positives for all the classes
    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: true_positives for all classes
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    true_positives_array = []

    for i in range(Nc):
        location_true_ones = np.where(true_labels[:, i] == 1)[0]
        predicted_labels_at_location = predicted_labels[:, i][location_true_ones]
        true_positives_array.append(len(np.where(predicted_labels_at_location == 1)[0]))

    return np.array(true_positives_array)


def false_positives(predicted_labels, true_labels):
    """
    True condition is negative
    Predicted condition is positive
    Get the number of true positives for all the classes
    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: false positives for all classes
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    false_positives_array = []

    for i in range(Nc):
        location_true_zeros = np.where(true_labels[:, i] == 0)[0]
        predicted_labels_at_location = predicted_labels[:, i][location_true_zeros]
        false_positives_array.append(len(np.where(predicted_labels_at_location == 1)[0]))
    return np.array(false_positives_array)


def true_negatives(predicted_labels, true_labels):
    """
    True condition is negative
    Predicted condition is negative
    Get the number of true positives for all the classes
    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: true_negatives for all classes
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    true_negatives = []

    for i in range(Nc):
        location_true_zeros = np.where(true_labels[:, i] == 0)[0]
        predicted_labels_at_location = predicted_labels[:, i][location_true_zeros]
        true_negatives.append(len(np.where(predicted_labels_at_location == 0)[0]))
    return np.array(true_negatives)


def false_negatives(predicted_labels, true_labels):
    """
    True condition is positive
    Predicted condition negative

    Get the number of true positives for all the classes
    Args:
        predicted_labels: Type: ndarray
                          shape: N * N_c
                          N - Number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * N_c
                     N - Number of training examples
                     N_c - Number of classes

    Returns: false_negatives for all classes
             Type:float number

    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    false_negatives = []

    for i in range(Nc):
        location_true_ones = np.where(true_labels[:, i] == 1)[0]
        predicted_labels_at_location = predicted_labels[:, i][location_true_ones]
        false_negatives.append(len(np.where(predicted_labels_at_location == 0)[0]))
    return np.array(false_negatives)


def semeval_measures(predicted_labels, true_labels):
    """

    Args:
        predicted_labels: Type: ndarray
                          shape N * Nc
                          N - number of training examples
                          Nc - Number of classes
        true_labels: Type: ndarray
                     shape: N * Nc
                     N - Number of training exaamples
                     Nc - Number of classes

    Returns: F-score

    The semeval_2016 2016 challenge evaluation checks the Fscores for every sentence
    (For Slot1 tasks)
    """
    assert predicted_labels.shape == true_labels.shape
    N, Nc = predicted_labels.shape
    precision_score = 0.0
    recall_score = 0.0

    for i in range(0, N):
        # Find the true positives
        predicted_labels_row = predicted_labels[i]
        true_labels_row = true_labels[i]
        locations_true_labels_where_one = np.where(true_labels_row == 1)[0]
        locations_true_labels_where_zero = np.where(true_labels_row == 0)[0]

        true_positives = len(np.where(predicted_labels_row[
                                          locations_true_labels_where_one] == 1)[0])
        false_positives = len(np.where(predicted_labels_row[
                                           locations_true_labels_where_zero] == 1)[0])
        false_negatives = len(np.where(predicted_labels_row[
                                           locations_true_labels_where_one] == 0)[0])

        # There are no right classes
        if len(locations_true_labels_where_one) == 0:
            precision = 0 if len(locations_true_labels_where_one) > 0 else 1
            recall = 1

        # You predicted no true positives
        elif true_positives == 0:
            precision = 0
            recall = 0

        # Everything is normal here
        else:
            precision = float(true_positives) / (true_positives + false_positives)
            recall = float(true_positives) / (true_positives + false_negatives)

        precision_score += precision
        recall_score += recall

    precision_score /= N
    recall_score /= N
    fmeasure = (2 * precision_score * recall_score) / (precision_score + recall_score)
    return precision_score, recall_score, fmeasure


if __name__ == "__main__":
    # true_labels = np.array([[0, 0, 0, 0]])
    # predicted_labels = np.array([[0, 0, 0, 0]])
    # fscore = semeval_measures(predicted_labels, true_labels)
    # print(fscore)
    pass
