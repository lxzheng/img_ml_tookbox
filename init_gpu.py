import os
import tensorflow as tf
import random


def init_gpu(vis_dev):
    if 'GPU_SET' not in os.environ:
        os.environ['GPU_SET'] = '1'
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            if vis_dev not in range(len(gpus)):
                vis_dev = random.randint(0, len(gpus) - 1)
            os.environ["CUDA_VISIBLE_DEVICES"] = str(vis_dev)
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
