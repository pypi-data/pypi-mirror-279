from textwrap import fill
import datetime
import matplotlib.ticker as ticker
import matplotlib.dates as mdate
import sklearn.metrics as metrics
from itertools import product
from tqdm import tqdm
from matplotlib import cm
from matplotlib import pyplot as plt
from scipy.stats import norm
import numpy as np
import pickle
from .KitNET.KitNET import KitNET
import matplotlib
import socket
from .feature_squeeze import squeeze_features
import multiprocessing as mp
import csv
matplotlib.use('Agg')
np.set_printoptions(threshold=np.inf)
# matplotlib.rcParams['timezone']="Pacific/Auckland"


def train_normal(params):
    """
    trains kitsune on normal traffic

    Args:
        params (dict): set of training parameters.

    Returns:
        type: None, model is saved in model_path


    """
    # Build Kitsune
    K = KitNET(100, params["maxAE"], params["FMgrace"],
               params["ADgrace"], 0.1, 0.75, normalize=params["normalize"])

    input_file = open(params["path"], "r")
    input_file.readline()
    count = 0
    tbar = tqdm()
    rmse = []
    while True:
        feature_vector = input_file.readline()
        # check EOF via empty string
        if not feature_vector:
            break
        fv = feature_vector.rstrip().split(",")
        fv = fv[:100]
        fv = np.array(fv, dtype="float")
        K.process(fv)
        count += 1
        tbar.update(1)
        if count > params["FMgrace"] + params["ADgrace"]:
            break
    tbar.close()
    # save
    with open(params["model_path"], "wb") as of:
        pickle.dump(K, of)

# This method is added after the code review to solve the issue 9
def calc_threshold(path, model_path, ignore_index=-1):
    """
    calculates threshold value for kitsune model

    Args:
        path (string): path to traffic feature file.
        model_path (string): path to trained kitsune model.
        ignore_index (int): number of features to ignore at the start. Defaults to -1.

    Returns:
        float: threshold value

    """
    with open(model_path, "rb") as m:
        kitsune = pickle.load(m)

    counter = 0
    input_file = open(path, "r")
    input_file.readline()
    rmse_array = []

    feature_vector = input_file.readline()
    while feature_vector is not '':

        if counter < ignore_index:
            feature_vector = input_file.readline()
            counter += 1
            continue

        fv = feature_vector.rstrip().split(",")
        fv = fv[:100]
        fv = np.array(fv, dtype="float")

        try:
            if kitsune.input_precision is not None:
                fv = squeeze_features(fv, kitsune.input_precision)
        except AttributeError as e:
            pass

        rmse = kitsune.process(fv)

        if rmse == 0:

            rmse_array.append(1e-2)
        else:

            rmse_array.append(rmse)
        counter += 1

        feature_vector = input_file.readline()

    # threshold is min(mean+3std, max)
    benignSample = np.log(rmse_array)
    mean = np.mean(benignSample)
    std = np.std(benignSample)
    threshold_std = np.exp(mean + 3 * std)
    threshold_max = max(rmse_array)
    threshold = min(threshold_max, threshold_std)
    return threshold

def eval_kitsune(path, model_path, threshold, ignore_index=-1, out_image=None, meta_file=None, record_scores=False, y_true=None, record_prediction=False, load_prediction=False, plot_with_time=False):
    """
    evaluates trained kitsune model on some traffic.

    Args:
        path (string): path to traffic feature file.
        model_path (string): path to trained kitsune model.
        threshold (float): anomaly threshold value, if None it calculates the threshold value as 3 std away from mean. Defaults to None.
        ignore_index (int): number of features to ignore at the start. Defaults to -1.
        out_image (string): path to output anomaly score image. Defaults to None.
        meta_file (string): path to metadata file, used to calculate evasion metrics. Defaults to None.
        record_scores (boolean): whether to record anomaly scores in a seperate csv file. Defaults to False.

    Returns:
        if has_meta: return number of positive samples and positive samples that are not craft packets.
        else: return number of positive samples

    """
    # the pcap, pcapng, or tsv file to process.
    print("evaluting", path)
    print("meta", meta_file)
    print("kitsune model path ", model_path)
    # if(threshold is not None):
    #     t = open(threshold, "r")
    #     threshold = t.readline() 
    # else:
    #     t = threshold 
    t = threshold 

    roc_auc = 1
    label_map = []

    with open(model_path, "rb") as m:
        kitsune = pickle.load(m)

    if out_image == None:

        out_image = path[:-4] + "_kitsune_rmse.png"

    if meta_file is not None:
        meta = open(meta_file, "r")
        meta.readline()
        meta_row = meta.readline()
        has_meta = True
        pos_craft = 0
        pos_mal = 0
        pos_ignore = 0
    else:
        has_meta = False
        pos = 0

    labels = []
    times = []
    colours = []
    tbar = tqdm()
    if load_prediction:
        rmse_array = np.genfromtxt(
            path[:-4] + "_kitsune_score.csv", delimiter=",")
    else:
        counter = 0
        input_file = open(path, "r")
        input_file.readline()
        rmse_array = []

        if not has_meta:
            colours = None

        feature_vector = input_file.readline()
        while feature_vector is not '':

            if counter < ignore_index:
                feature_vector = input_file.readline()

                if meta_file is not None:
                    meta_row = meta.readline()

                counter += 1
                continue

            fv = feature_vector.rstrip().split(",")

            if len(fv) == 102:
                label = fv[-2]
                if label.isdigit():
                    try:
                        label = socket.getservbyport(int(label))
                    except OSError:
                        label = "udp"
                if label not in label_map:
                    label_map.append(label)

                labels.append(label_map.index(label))
                times.append(mdate.epoch2num(float(fv[-1])) + 1)
                fv = fv[:100]

            fv = np.array(fv, dtype="float")

            try:
                if kitsune.input_precision is not None:
                    fv = squeeze_features(fv, kitsune.input_precision)
            except AttributeError as e:
                pass

            rmse = kitsune.process(fv)

            if rmse == 0:

                rmse_array.append(1e-2)
            else:

                rmse_array.append(rmse)
            counter += 1
            tbar.update(1)

            feature_vector = input_file.readline()
            # set colours
            if has_meta:
                comment = meta_row.rstrip().split(",")[-1]
                if comment == "craft":
                    colours.append([67 / 255., 67 / 255., 67 / 255., 0.8])

                elif comment == "malicious":
                    colours.append([1, 0, 0, 1])
                else:
                    colours.append([204 / 255., 243 / 255., 1, 0.5])

            if threshold is not None and rmse > float(threshold):
                if has_meta:
                    comment = meta_row.rstrip().split(",")[-1]
                    if comment == "craft":
                        pos_craft += 1
                    elif comment == "malicious":
                        pos_mal += 1
                    elif comment == "attacker_low":
                        pos_ignore += 1
                    else:
                        print(meta_row)
                        print(rmse)
                        raise Exception
                else:
                    pos += 1

            if has_meta:
                meta_row = meta.readline()

    # if no threshold, calculate threshold
    # Comented this out after the code review .
                

    # if threshold == None:
    #     # threshold is min(mean+3std, max)
    #     benignSample = np.log(rmse_array)
    #     mean = np.mean(benignSample)
    #     std = np.std(benignSample)
    #     threshold_std = np.exp(mean + 3 * std)
    #     threshold_max = max(rmse_array)
    #     threshold = min(threshold_max, threshold_std)
    #     pos = (rmse_array > threshold).sum()

    # record prediction scores/rmse
    if record_scores:
        score_path = "_kitsune_score.csv"
        threshold_path = "_kitsune_threshold.csv"
        # print("max_rmse",np.max(rmse_array))
        np.savetxt(score_path, rmse_array, delimiter=",")
        np.savetxt(threshold_path, [float(threshold)], delimiter=",")
        print("score saved to", score_path)

    # record prediction labels
    if record_prediction:
        pred_path = "_kitsune_prediction.csv"
        np.savetxt(pred_path, rmse_array > threshold, delimiter=",")
        print("kitsune prediction saved to", pred_path)
    
    print("port scan examples over threshold:", pos)

    tbar.close()

    return rmse_array 


def plot_kitsune(rmse_array, threshold, out_image=None, meta_file=None, plot_with_time=False):
    if out_image is not None:
        cmap = plt.get_cmap('Set3')
        
        f, ax1 = plt.subplots(constrained_layout=True, figsize=(10, 5), dpi=200)

        if plot_with_time:
            x_val = range(len(rmse_array))
            ax1.xaxis.set_major_locator(ticker.MultipleLocator(0.85))
            ax1.tick_params(labelrotation=90)
        else:
            x_val = range(len(rmse_array))

        if meta_file:
            ax1.scatter(x_val, rmse_array, s=1, c='#00008B')
        else:
            ax1.scatter(x_val, rmse_array, s=1, alpha=1.0, c='#FF8C00')

        ax1.axhline(y=threshold, color='r', linestyle='-')
        ax1.set_yscale("log")
        ax1.set_title("Anomaly Scores from Kitsune Execution Phase")
        ax1.set_ylabel("RMSE (log scaled)")
        ax1.set_xlabel("packet index")

        f.savefig(out_image)
        print("plot path:", out_image)
        plt.close()




# def evaluation_metrics(scores_path, threshold):

#     # Calulate the F1 score for Model using ground labels
#     # Actual outputs from kitsune_score.csv
#     y_output = csv.reader(open(scores_path, 'r'))
#     y_output = list(y_output)
#     y_output = [float(i[0]) for i in y_output]

#     # let ground labels be 0(benign) for all pkts
#     y_true = np.ones(len(y_output))
#     # print(y_true)

#     # Threshold for F1 score
#     # threshold = csv.reader(open(threshold_path, 'r'))
#     # threshold = list(threshold)
#     # threshold = float(threshold[0][0])

#     # Predicted labels
#     y_pred = np.array([0 if i > threshold else 1 for i in y_output])
#     # print(y_pred)
#     # 0 -> benign and 1 -> malicious
#     tp = fp = tn = fn = 0
#     for i in range(len(y_true)):
#         if y_true[i] == 1 and y_pred[i] == 1:
#             tp += 1
#         elif y_true[i] == 0 and y_pred[i] == 1:
#             fp += 1
#         elif y_true[i] == 0 and y_pred[i] == 0:
#             tn += 1
#         else:
#             fn += 1
#     # print(metrics.confusion_matrix(y_true, y_pred).ravel())
#     # m = metrics.confusion_matrix(y_true, y_pred)
#     # tn = m[0][0]
#     # fp = m[0][1]
#     # fn = m[1][0]
#     # tp = m[1][1]
#     # tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
#     precision = tp/(tp+fp)
#     recall = tp/(tp+fn)
#     f1 = 2*(precision*recall)/(precision+recall)

#     print("True Negatives: ", tn)
#     print("False Positives: ", fp)
#     print("False Negatives: ", fn)
#     print("True Positives: ", tp)

#     print("Precision: ", precision)
#     print("Recall: ", recall)
#     print("F1 score: ", f1)

#     # Add the code to calculate the Confusion Matrix, ROC curve, and AUC score in this function


def evaluation_metrics(rmse_array, threshold):
    # Calculate the F1 score for Model using ground labels
    # y_output = csv.reader(open(scores_path, 'r'))
    y_output = list(rmse_array)
    y_output = [float(i) for i in y_output]

    # let ground labels be 0(benign) for all pkts
    y_true = np.ones(len(y_output))

    # Predicted labels
    y_pred = np.array([0 if i > threshold else 1 for i in y_output])

    # Confusion Matrix
    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    print("Confusion Matrix: ")
    print("True Negatives: ", tn)
    print("False Positives: ", fp)
    print("False Negatives: ", fn)
    print("True Positives: ", tp)

    # Precision, Recall and F1 Score
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2*(precision*recall)/(precision+recall)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 score: ", f1)

    # ROC Curve and AUC Score
    fpr, tpr, _ = metrics.roc_curve(y_true, y_pred)
    print("False Positive Rate: ", fpr)
    print("True Positive Rate: ", tpr)
    auc_score = metrics.auc(fpr, tpr)
    print("AUC Score: ", auc_score)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % auc_score)
    plt.plot(fpr, tpr, color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig('roc_curve.png')
    print("ROC curve saved as roc_curve.png in the current directory.")