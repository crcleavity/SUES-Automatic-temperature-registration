import tensorflow as tf
import train


def test():
    (x_test, y_test) = train.get_datasets("./test")

    test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    test_db = test_db.map(train.preprocess).batch(1)

    model = tf.keras.models.load_model('model.h5', compile=False)
    for step, (x, y) in enumerate(test_db):
        logits = model(x)
        logits = tf.nn.softmax(logits)
        pred = tf.cast(tf.argmax(logits, axis=2), dtype=tf.int32)
        print(f"pred: {pred[0].numpy()}, ground truth: {y[0].numpy()}, is same: {int(tf.reduce_sum(tf.cast(tf.equal(pred, y), dtype=tf.int32))) == 4}")


if __name__ == '__main__':
    test()