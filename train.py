import tensorflow as tf
import matplotlib.pyplot as plt
model_chose=''

def display_learning_curves(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.ylim([min(plt.ylim()), 1])
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.ylim([0, 1.0])
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.show()


def train_model(classes, train_generator, val_generator, epochs, img_shape=(224, 224, 3)):

    if  model_chose =='mobilenetv2':                                              
        base_model = tf.keras.applications.MobileNetV2(input_shape=img_shape,
                                                    include_top=False,
                                                    weights='imagenet')
        print('使用的模型为mobilenetv2（适用于移动端模型）')  
    if  model_chose =='inceptionv3':
        base_model = tf.keras.applications.InceptionV3(input_shape=img_shape,
                                                    include_top=False,
                                                    weights='imagenet') 
        print('使用的模型为inceptionv3（高精度模型）')                                                                                            
    # base_model.trainable = True
    base_model.trainable = False
    model = tf.keras.Sequential([
        base_model,
        # tf.keras.layers.Conv2D(32, 3, activation='relu'),
        # tf.keras.layers.Dropout(0.2),
        # tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(classes, activation='softmax')
    ])
    # fine_tune_at = 100
    # for layer in base_model.layers[:fine_tune_at]:
    #    layer.trainable =  False
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss='categorical_crossentropy',
                  metrics=['acc'])
    history = model.fit(train_generator,
                                  epochs=epochs,
                                  validation_data=val_generator)

    model.save('my_model.h5')

       
    print('训练结束,标签已更新')
    print(history.history)
    display_learning_curves(history)
