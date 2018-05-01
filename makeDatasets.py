from utils.generate_test_splits import generate_hold_out_split
from utils.dataset import DataSet
#from utils import dataset, generate_test_splits

dataset = DataSet()
generate_hold_out_split(dataset, training=0.8, base_dir="splits/")

