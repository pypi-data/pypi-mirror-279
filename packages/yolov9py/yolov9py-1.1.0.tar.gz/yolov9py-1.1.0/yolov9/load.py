from yolov9.models.experimental import attempt_load
from yolov9.models.yolo import DetectionModel
from yolov9.utils.general import LOGGER, intersect_dicts, logging


def load_model(cfg_path, weights=None, channels=3, classes=80, fuse=True, device=None, dtype=None):
    """
    Creates or loads a YOLO model.

    Arguments:
        cfg_path (str): path to configuration file
        weight (bool): path to model checkpoint
        channels (int): number of input channels
        classes (int): number of model classes
        fuse (bool): apply YOLO autoshape wrapper to model
        device (str, torch.device, None): device to use for model parameters
        dtype (str, torch.dtype, None): type used for model parameters

    Returns:
        YOLO model
    """

    model = DetectionModel(cfg_path, channels, classes)  # create model

    if weights:
        # Model checkpoint as pretrained from COCO
        ckpt = attempt_load(weights, device=device, fuse=fuse)

        # Model with new output configuration
        if not (channels == 3 and classes == 80):
            csd = ckpt.float().state_dict()  # checkpoint state_dict as FP32
            csd = intersect_dicts(csd, model.state_dict(), exclude=['anchors'])  # intersect
            model.load_state_dict(csd, strict=False)  # load
        else:
            model = ckpt

        if len(ckpt.names) == classes:
            model.names = ckpt.names  # set class names attribute

    return model.to(device=device).to(dtype=dtype)