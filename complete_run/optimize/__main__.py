import sys
import time
import numpy as np
import torch
from torch import device, cuda
from torch.optim import Adam

from generator.constants import NZ

from .optimize import SequenceTuner
from .vectors import TuningVectors


# THIS IS ALL TEMPORARY
from generator.models import snp_generator
from classifier.models import conv_net, conv_net_one_layer

def optimize(vector_id, target_class):
    dev = device("cuda" if cuda.is_available() else "cpu")

    generator_params = {
        'nz': NZ,
        'num_filters': 320,
        'len_filters': 15,
        'transpose_size': 10,
    }
    generator = snp_generator(**generator_params).to(dev)
    GENERATOR_PATH = '/home/pbromley/synth-seqs-models/generator-len-200/generator.pth'
    generator.load_state_dict(torch.load(GENERATOR_PATH, map_location=dev))
    generator.train(False)

    model_params = {           
        'filters': 100,
        'pool_size': 100,
        'fully_connected': 100,
        'drop': 0.5,
    }
 
    classifier = conv_net_one_layer(**model_params).to(dev)
    MODEL_PATH = '/home/pbromley/synth-seqs-models/classifier-len-200/classifier.pth'
    classifier.load_state_dict(torch.load(MODEL_PATH, map_location=dev))
    classifier.train(False)

    classifier.eval()
    generator.eval()

    optimizer_params = {
        'lr': 0.017,
        'betas': (0.8, 0.59)
    }

    tuner = SequenceTuner(generator,
                          classifier,
                          optimizer_params,
                          dev)

    vector_path = '/home/pbromley/projects/synth_seqs/tuning/initial/vectors-len-100.npy'
    vectors = TuningVectors()
    opt_zs = vectors.load_fixed(vector_path, slice(0, vector_id))
    iters = 10000
    save_dir = f'/home/pbromley/projects/synth_seqs/tuning/global_penalty_len200/{target_class}/'

    start = time.time()
    tuner.optimize_multiple(opt_zs,
                            target_class,
                            iters,
                            save_dir) 
                   
    elapsed = time.time() - start

    #tuner.save_training_history(save_dir, vector_id)

def initialize_fixed_vectors(num_vectors, len_vectors, path, seed=None):
    tv = TuningVectors()
    tv.save_fixed(num_vectors, len_vectors, path, seed=seed)

if __name__ == '__main__':
    #assert len(sys.argv) == 2, 'Wrong number of arguments given (exactly 1 required)'

    c = int(sys.argv[1])
    #vector_id = args % 1000
    #target_component = args // 1000

    optimize(1000, c)

