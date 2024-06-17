"""
Code from https://github.com/Arshdeep-Singh-Boparai/E-PANNs
"""

import numpy as np
import torch
import csv


# -------------------------------------------- IN/OUT --------------------------------------------- #
def load_csv_labels(labels_csv_path):
    """
    """
    with open(labels_csv_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        lines = list(reader)
    idxs, ids, labels = zip(*lines[1:])
    num_classes = len(labels)
    return num_classes, ids, labels


# -------------------------------------------- PYTORCH -------------------------------------------- #
def move_data_to_device(x, device):
    if 'float' in str(x.dtype):
        x = torch.Tensor(x)
    elif 'int' in str(x.dtype):
        x = torch.LongTensor(x)
    else:
        return x

    return x.to(device)


def interpolate(x, ratio):
    """Interpolate the prediction to compensate the downsampling operation in a
    CNN.

    Args:
      x: (batch_size, time_steps, classes_num)
      ratio: int, ratio to upsample
    """
    (batch_size, time_steps, classes_num) = x.shape
    upsampled = x[:, :, None, :].repeat(1, 1, ratio, 1)
    upsampled = upsampled.reshape(batch_size, time_steps * ratio, classes_num)
    return upsampled


def pad_framewise_output(framewise_output, frames_num):
    """Pad framewise_output to the same length as input frames.
    Args:
      framewise_output: (batch_size, frames_num, classes_num)
      frames_num: int, number of frames to pad
    Outputs:
      output: (batch_size, frames_num, classes_num)
    """
    pad = framewise_output[:, -1 :, :].repeat(1, frames_num - framewise_output.shape[1], 1)
    """tensor for padding"""

    output = torch.cat((framewise_output, pad), dim=1)
    """(batch_size, frames_num, classes_num)"""

    return output


def do_mixup(x, mixup_lambda):
    out = x[0::2].transpose(0, -1) * mixup_lambda[0::2] + \
        x[1::2].transpose(0, -1) * mixup_lambda[1::2]
    return out.transpose(0, -1)


# -------------------------------------------- Tracking -------------------------------------------- #
class PredictionTracker:
    def __init__(self, all_labels, allow_list=None, deny_list=None):
        """
        :param all_labels: List with all categories as returned by the model.
        :param allow_list: If not ``None``, contains the allowed categories.
        :param deny_list: If not ``None``, contains the categories ignored.
        """
        self.all_labels = all_labels
        self.all_lbls_to_idxs = {l: i for i, l in enumerate(all_labels)}
        if allow_list is None:
            allow_list = all_labels
        if deny_list is None:
            deny_list = []
        self.labels = [l for l in all_labels
                       if l in allow_list and l not in deny_list]
        self.lbls_to_idxs = {l: self.all_lbls_to_idxs[l] for l in self.labels}
        self.idxs = sorted(self.lbls_to_idxs.values())

    def __call__(self, model_probs, top_k=6, sorted_by_p=True):
        """
        """
        assert top_k >= 1, "Only integer >= 1 allowed for top_k!"
        top_k += 1
        #
        tracked_probs = model_probs[self.idxs]
        top_idxs = np.argpartition(tracked_probs, -top_k)[-top_k:]
        top_probs = tracked_probs[top_idxs]
        top_labels = [self.labels[idx] for idx in top_idxs]
        result = list(zip(top_labels, top_probs))

        if sorted_by_p:
            result = sorted(result, key=lambda elt: elt[1], reverse=True)

        return result
