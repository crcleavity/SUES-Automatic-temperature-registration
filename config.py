from PIL import Image
import tensorflow as tf
import numpy as np


user_dict = {
    "Chen.Bai": {
        "account": "",
        "password": "",
        "mail": ""  # user email address
    },

}

smtp_dict = {
    "from_name": "",
    "from_address": "",  # email address
    "from_password": ""  # email smtp password
}


def png2code():
    def preprocess(x):
        x = 2 * tf.cast(x, dtype=tf.float32) / 255. - 1
        x = tf.expand_dims(x, -1)
        return x

    img = Image.open('codeImg.png')
    img = img.convert('L')
    count = 165
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)
    img = img.point(table, '1')
    img.save('codeImg_cache.png')

    model = tf.keras.models.load_model('model.h5', compile=False)

    captcha_image = Image.open('codeImg_cache.png')
    captcha_image = captcha_image.convert('L')
    captcha_image_np = np.array(captcha_image)
    img_np = np.array(captcha_image_np)
    x_data = [img_np]
    x_data = np.array(x_data).astype(float)

    test = tf.data.Dataset.from_tensor_slices(x_data)
    test = test.map(preprocess).batch(1)

    for step, x in enumerate(test):
        logits = model(x)
        logits = tf.nn.softmax(logits)
        pred = tf.cast(tf.argmax(logits, axis=2), dtype=tf.int32)

    code = ""
    for i in pred[0].numpy():
        code += str(i)

    return code


if __name__ == '__main__':
    png2code()
