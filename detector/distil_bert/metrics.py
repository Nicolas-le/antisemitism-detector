from transformers import EvalPrediction
from sklearn.metrics import accuracy_score
import numpy as np


def antisem_metrics(pred: EvalPrediction):
    """
    Compute 3 accuracies: all labels, antisemitic, notantisemitic.
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    mapper = lambda n: True if n == 1 else False

    hatePreds = preds[[mapper(l) for l in labels]]
    noHatePreds = preds[[mapper(l) for l in 1 - labels]]

    return {
      'acc_antisemitism': accuracy_score(hatePreds, np.ones_like(hatePreds)),
      'acc_notantisemitism': accuracy_score(noHatePreds, np.zeros_like(noHatePreds)),
      'acc_all': accuracy_score(labels, preds),
    }