import os 

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small



def skint_type_model():
    weights = os.path.join(os.getcwd(), "AI_Model", "skintypemodel_v1.weights.h5")

    cnn = MobileNetV3Small(include_top=False, input_shape=(180, 180, 3), pooling="avg", include_preprocessing=True)
    for layer in cnn.layers:
        layer.trainable = False

    for layer in cnn.layers[60:]:
        layer.trainable = True

    drop1 = tf.keras.layers.Dropout(0.6)(cnn.output)
    output = tf.keras.layers.Dense(3, activation="softmax")(drop1)



    model = tf.keras.Model(inputs=[cnn.input], outputs=[output])

    micro_f1 = tf.keras.metrics.F1Score(average="micro", name="micro_f1")
    macro_f1 = tf.keras.metrics.F1Score(average="macro", name="macro_f1")

    optimizer = tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.9, nesterov=True)

    checkpoint_cb = tf.keras.callbacks.ModelCheckpoint("./checkpoints/msmall60.weights.h5", 
                                                    save_weights_only=True,
                                                    save_best_only=True, 
                                                    monitor="val_micro_f1",
                                                    mode="max", 
                                                    verbose=1
                                                    )


    model.compile(loss="categorical_crossentropy", optimizer=optimizer,
                metrics=[micro_f1, macro_f1])
    
    model.load_weights(weights)

    return model