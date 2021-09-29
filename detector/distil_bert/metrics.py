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

    antisem_preds = preds[[mapper(l) for l in labels]]
    no_antisem_preds = preds[[mapper(l) for l in 1 - labels]]

    return {
      'acc_antisemitism': accuracy_score(antisem_preds, np.ones_like(antisem_preds)),
      'acc_notantisemitism': accuracy_score(no_antisem_preds, np.zeros_like(no_antisem_preds)),
      'acc_all': accuracy_score(labels, preds),
    }