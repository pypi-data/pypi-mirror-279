import csv
import numpy as np
from sklearn import metrics

def evaluation_metrics(scores_path, threshold_path):
    # Calulate the F1 score for Model using ground labels
    # Actual outputs from kitsune_score.csv
    y_output = csv.reader(open(scores_path, 'r'))
    y_output = list(y_output)
    y_output = [float(i[0]) for i in y_output]

    # let ground labels be 0(benign) for all pkts
    y_true = np.ones(len(y_output))

    # Threshold for F1 score
    threshold = csv.reader(open(threshold_path, 'r'))
    threshold = list(threshold)
    threshold = float(threshold[0][0])

    # Predicted labels
    y_pred = np.array([0 if i > threshold else 1 for i in y_output])

    # 0 -> benign and 1 -> malicious

    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2*(precision*recall)/(precision+recall)

    print("True Negatives: ", tn)
    print("False Positives: ", fp)
    print("False Negatives: ", fn)
    print("True Positives: ", tp)

    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 score: ", f1)

    return f1
