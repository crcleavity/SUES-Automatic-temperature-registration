import os
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, optimizers, Sequential


def get_datasets(filePath):
    file_name_list = os.listdir(filePath)

    x_data = []
    y_data = []

    for selected_file_name in file_name_list:
        if selected_file_name.endswith('.png'):
            captcha_image = Image.open(os.path.join(filePath, selected_file_name))

            captcha_image = captcha_image.convert('L')
            captcha_image_np = np.array(captcha_image)

            img_np = np.array(captcha_image_np)
            x_data.append(img_np)
            y_data.append(np.array(list(selected_file_name.split('.')[0])).astype(np.int))

    x_data = np.array(x_data).astype(np.float)
    y_data = np.array(y_data)
    return x_data, y_data


def preprocess(x, y):
    x = 2 * tf.cast(x, dtype=tf.float32) / 255. - 1
    x = tf.expand_dims(x, -1)
    y = tf.cast(y, dtype=tf.int32)
    return x, y


def train():
    (x, y) = get_datasets("./train")
    print(x.shape, y.shape)

    train_db = tf.data.Dataset.from_tensor_slices((x, y))
    train_db = train_db.map(preprocess).batch(10)

    model = Sequential([
        layers.Conv2D(32, kernel_size=[3, 3], padding="same", activation=tf.nn.relu),
        layers.MaxPool2D(pool_size=[2, 2], strides=2, padding='same'),

        layers.Conv2D(64, kernel_size=[3, 3], padding="same", activation=tf.nn.relu),
        layers.MaxPool2D(pool_size=[2, 2], strides=2, padding='same'),
        layers.Flatten(),

        layers.Dense(128),
        layers.Dense(40),
        layers.Reshape([4, 10])
    ])

    model.build(input_shape=[None, 32, 70, 1])
    model.summary()
    optimizer = optimizers.Adam(lr=1e-3)

    for epoch in range(5):
        for step, (x, y) in enumerate(train_db):
            with tf.GradientTape() as tape:
                logits = model(x)
                y_one_hot = tf.one_hot(y, depth=10)
                loss_ce = tf.losses.MSE(y_one_hot, logits)
                loss_ce = tf.reduce_mean(loss_ce)

            grads = tape.gradient(loss_ce, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

            if step % 10 == 0:
                print(f"epoch: {epoch}, step: {step}, loss: {float(loss_ce)}")

    model.save('model.h5')


if __name__ == '__main__':
    train()
