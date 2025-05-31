# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from functools import partial
from pathlib import Path

import torch

from ultralytics.utils.checks import check_yaml
from ultralytics.utils import IterableSimpleNamespace, yaml_load

from .byte_tracker import BYTETracker


traj_store = dict()

def on_predict_start(predictor: object, persist: bool = True) -> None:
    """
    Initialize trackers for object tracking during prediction.

    Args:
        predictor (object): The predictor object to initialize trackers for.
        persist (bool): Whether to persist the trackers if they already exist.

    Raises:
        AssertionError: If the tracker_type is not 'bytetrack' or 'botsort'.
        ValueError: If the task is 'classify' as classification doesn't support tracking.

    Examples:
        Initialize trackers for a predictor object:
        >>> predictor = SomePredictorClass()
        >>> on_predict_start(predictor, persist=True)
    """
    if hasattr(predictor, "trackers") and persist:
        return

    cfg = IterableSimpleNamespace(**yaml_load('./trackers/bytetrack.yaml'))

    trackers = []
    for _ in range(predictor.dataset.bs):
        tracker = BYTETracker(args=cfg, frame_rate=30)
        trackers.append(tracker)
    predictor.trackers = trackers
    predictor.vid_path = [None] * predictor.dataset.bs  # for determining when to reset tracker on new video


def on_predict_postprocess_end(predictor: object, persist: bool = True) -> None:
    """
    Postprocess detected boxes and update with object tracking.

    Args:
        predictor (object): The predictor object containing the predictions.
        persist (bool): Whether to persist the trackers if they already exist.

    Examples:
        Postprocess predictions and update with tracking
        >>> predictor = YourPredictorClass()
        >>> on_predict_postprocess_end(predictor, persist=True)
    """
    for i, result in enumerate(predictor.results):
        tracker = predictor.trackers[i]
        vid_path = predictor.save_dir / Path(result.path).name

        det = (result.obb).cpu().numpy()
        if len(det) == 0:
            continue
        tracks = tracker.update(det, result.orig_img)
        if len(tracks) == 0:
            continue

        # Get multi-step look-ahead predictions
        traj = tracker.multi_step_look_ahead()
        traj_store[i] = traj

        idx = tracks[:, -1].astype(int)
        predictor.results[i] = result[idx]

        update_args = {"obb": torch.as_tensor(tracks[:, :-1])}
        predictor.results[i].update(**update_args)


def register_tracker(model: object, persist: bool) -> None:
    """
    Register tracking callbacks to the model for object tracking during prediction.

    Args:
        model (object): The model object to register tracking callbacks for.
        persist (bool): Whether to persist the trackers if they already exist.

    Examples:
        Register tracking callbacks to a YOLO model
        >>> model = YOLOModel()
        >>> register_tracker(model, persist=True)
    """
    model.add_callback("on_predict_start", partial(on_predict_start, persist=persist))
    model.add_callback("on_predict_postprocess_end", partial(on_predict_postprocess_end, persist=persist))
