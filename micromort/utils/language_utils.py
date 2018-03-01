import numpy as np


def thresholding(scores, labels):
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

    Returns:

    """
    assert scores.shape == labels.shape
    N, Nc = scores.shape

    # Sort by descending order of the scores
    scores_ = scores.copy()
    scores_ = np.fliplr(np.sort(scores_, axis=1))

    # Get the indices by which every row in the score gets sorted
    labels_sort_indices = np.fliplr(np.argsort(scores, axis=1))

    # re arrange the labels according to these indices
    labels_sorted = np.array([labels[i][labels_sort_indices[i]] for i in range(0, N)])

    tms = []
    # You have to go through every data point now
    for i in range(N):
        labels_row = labels_sorted[i]
        scores_row = scores_[i]

        # Find the places where 1 changes to 0
        boundary_indices = np.where(labels_row == 1)[0]

        # Now you know the boundaries between the right class and
        # the wrong class
        # Find the candidate tms by adding them up
        candidate_tms = []
        for index in boundary_indices:
            if index != (len(labels_row) - 1):
                candidate_tms.append(
                    (scores_row[index] + scores_row[index + 1]) / 2)

        # For every candidate tm find the F measure
        positive_scores = scores_row[np.where(labels_row == 1)[0]]
        negative_scores = scores_row[np.where(labels_row == 0)[0]]

        best_tm = None
        best_fscore = -np.inf

        # This handles the cases of the form [0, 0, 0, 1]
        # What should be chosen as the candidate tm here?
        if len(candidate_tms) == 0:
            if len(boundary_indices) == 1 \
                    and boundary_indices[0] == len(labels_row) - 1:
                best_tm = scores_row[boundary_indices[0]]

            # If all the classes are zero [0, 0, 0, 0]
            # Then pick the score that is the lowest as the threshold
            if len(boundary_indices) == 0:
                best_tm = scores_row[len(scores_row) - 1] # since scores row is arranged in the descending order

        for tm in candidate_tms:
            num_true_positives = len(positive_scores[positive_scores >= tm])
            num_true_negatives = len(negative_scores[negative_scores >= tm])
            precision = float(num_true_positives) / (num_true_positives + num_true_negatives)
            recall = float(num_true_positives) / len(positive_scores)
            fscore = (2 * precision * recall)/ (precision + recall)

            if fscore > best_fscore:
                best_tm = tm

        best_tm  = round(best_tm, 4)
        tms.append(best_tm)

    return np.array(tms)
