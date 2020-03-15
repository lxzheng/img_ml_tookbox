# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import random
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from init_gpu import init_gpu

# 初始化GPU分配
init_gpu(random.randint(0, 2))


def plot_images(images_arr, labels, label_names):
    img_couts = images_arr.shape[0]
    if img_couts > 5:
        img_couts = 5
    fig, axes = plt.subplots(1, img_couts, figsize=(20, 20))

    if img_couts > 1:
        axes = axes.flatten()
        for img, ax, label in zip(images_arr, axes, labels):
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(label_names[np.argmax(label)])
    elif img_couts == 1:
        plt.imshow(images_arr[0])
        plt.title(label_names[np.argmax(labels[0])])
    plt.tight_layout()
    plt.show()


def load_data(data_dir, batch_size=4, img_size=(224, 224), validation_perc=0.10, data_aug=False):
    if data_aug:
        image_generator = ImageDataGenerator(rescale=1. / 255,
                                             validation_split=validation_perc,
                                             rotation_range=45,
                                             width_shift_range=.15,
                                             height_shift_range=.15,
                                             horizontal_flip=True,
                                             zoom_range=0.5)
    else:
        image_generator = ImageDataGenerator(rescale=1. / 255,
                                             validation_split=validation_perc)

    train_generator = image_generator.flow_from_directory(directory=data_dir,
                                                          # class_mode='binary',
                                                          batch_size=batch_size,
                                                          target_size=img_size,
                                                          subset='training')
    val_generator = image_generator.flow_from_directory(directory=data_dir,
                                                        # class_mode='binary',
                                                        batch_size=batch_size,
                                                        target_size=img_size,
                                                        subset='validation')
    classes = len(train_generator.class_indices)

    label_names = list(train_generator.class_indices.keys())

    # sample_training_images, sample_training_labels = next(train_generator)
    # print("Some image examples:")
    # plotImages(sample_training_images[:5],sample_training_labels[:5],label_names)

    return train_generator, val_generator, classes, label_names
