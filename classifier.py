import os

# Deve vir ANTES do import tensorflow
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tensorflow as tf
import numpy as np
from PIL import Image


def get_class(model_path, labels_path, image_path):

    # Carrega o modelo
    model = tf.keras.models.load_model(
        model_path,
        compile=False
    )

    # Carrega os labels
    with open(labels_path, "r", encoding="utf-8") as file:
        labels = [line.strip() for line in file.readlines()]

    # Abre a imagem
    image = Image.open(image_path).convert("RGB")

    # Redimensiona
    image = image.resize((224, 224))

    # Converte para array
    image_array = np.asarray(image)

    # Normaliza os pixels
    image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    # Adiciona dimensão do batch
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Faz a previsão
    prediction = model.predict(
        image_array,
        verbose=0
    )

    # Maior probabilidade
    index = np.argmax(prediction[0])

    confidence = prediction[0][index]

    return (
        f"{labels[index]} "
        f"({confidence * 100:.2f}%)"
    )
