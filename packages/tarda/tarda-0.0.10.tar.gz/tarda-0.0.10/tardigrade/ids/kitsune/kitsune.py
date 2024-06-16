from .kitsune_ids import parse_with_kitsune
from .kitsune_ids.kitsune import *
import os 

from tardigrade.ids.ids import BaseIDS

class KitsuneIDS:
    """
    This is an awesome IDS
    """
    def __init__(self , keep_csv=False ):
        self.keep_csv = keep_csv
        self.model_path = "kitsune.pkl"
        # self.pcap_path = pcap_path
        self.threshold = None
        self.out_image = None


    # This is for parsing the data and extracting the features from the data .
    def feature_extractor (self, pcap_path, add_label=False, write_prob=1, count=float('Inf'), parse_type="scapy", netstat_path=None, save_netstat=None, add_proto=False, add_time=False, netstat_log_file=None):
        pcap_file = pcap_path + ".pcap"
        output_file_name = pcap_path + ".csv"
        return parse_with_kitsune.parse_kitsune(pcap_file, output_file_name, add_label, write_prob, count, parse_type, netstat_path, save_netstat, add_proto, add_time, netstat_log_file)

    # make a function that would train the model and then save the model in a file
    def train_model(self, params):
        # change to solve the code review issue 4
        if 'model_path' not in params:
            params['model_path'] = self.model_path
        train_normal(params) 
        self.threshold = calc_threshold(params['path'] , params['model_path'])
        csv_path = params['path']
        # Delete the file at csv_path
        if(self.keep_csv == False) : 
            if os.path.exists(csv_path):
                os.remove(csv_path)
                print(f"File {csv_path} has been deleted.")
            else:
                print(f"The file {csv_path} does not exist.")

        return self.threshold

    def test_model(self, pcap_path , model_p = None , ignore_index=-1, out_image=None, meta_file=None, record_scores=False, y_true=None, record_prediction=False, load_prediction=False, plot_with_time=False):
        csv_path = pcap_path + ".csv"
        self.out_image = pcap_path.split("/")[-1] + "_kitsune_rmse.png"
        if model_p is None:
            model_p = self.model_path
        result = eval_kitsune(csv_path,model_p ,self.threshold , ignore_index, out_image, meta_file, record_scores, y_true, record_prediction, load_prediction, plot_with_time)

        # Delete the file at csv_path
        if(self.keep_csv == False) : 
            if os.path.exists(csv_path):
                os.remove(csv_path)
                print(f"File {csv_path} has been deleted.")
            else:
                print(f"The file {csv_path} does not exist.")
                
        return result


    def get_plot(self, rmse_array, out_image=None, meta_file=None , plot_with_time=False):
        if out_image == None:
            out_image = self.out_image
        return plot_kitsune(rmse_array, self.threshold, out_image, meta_file, plot_with_time)
    
    def eval_metrics(self, rmse_array):
        return evaluation_metrics(rmse_array, self.threshold)
