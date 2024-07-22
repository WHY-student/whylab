from typing import Union, Tuple

from mmengine.config import Config
from mmengine.runner.checkpoint import (_load_checkpoint,
                                        _load_checkpoint_to_model)
from mmengine.dataset import Compose
from mmcv.transforms import LoadImageFromFile

from mmdet.utils import ConfigType
from mmdet.registry import MODELS
from mmdet.registry import TRANSFORMS

def model_init(config_path, checkpoint=None, device="cpu"):
    cfg = Config.fromfile(config_path)
    model = MODELS.build(cfg.model)
    model.cfg = cfg
    if isinstance(checkpoint, str):
        checkpoint = _load_checkpoint(checkpoint, map_location='cpu')
    _load_checkpoint_to_model(model, checkpoint)
    model.to(device)
    model.eval()
    return model

def init_pipeline(cfg: ConfigType) -> Compose:
    """Initialize the test pipeline."""
    pipeline_cfg = cfg.test_dataloader.dataset.pipeline

    # For inference, the key of ``img_id`` is not used.
    if 'meta_keys' in pipeline_cfg[-1]:
        pipeline_cfg[-1]['meta_keys'] = tuple(
            meta_key for meta_key in pipeline_cfg[-1]['meta_keys']
            if meta_key != 'img_id')

    load_img_idx = _get_transform_idx(
        pipeline_cfg, ('LoadImageFromFile', LoadImageFromFile))
    if load_img_idx == -1:
        raise ValueError(
            'LoadImageFromFile is not found in the test pipeline')
    pipeline_cfg[load_img_idx]['type'] = 'mmdet.InferencerLoader'
    transforms = []
    for transform in pipeline_cfg:
        transform = TRANSFORMS.build(transform)
        if not callable(transform):
            raise TypeError(f'transform should be a callable object, '
                            f'but got {type(transform)}')
        transforms.append(transform)
    return Compose(transforms)

def _get_transform_idx(pipeline_cfg: ConfigType,
                        name: Union[str, Tuple[str, type]]) -> int:
    """Returns the index of the transform in a pipeline.

    If the transform is not found, returns -1.
    """
    for i, transform in enumerate(pipeline_cfg):
        if transform['type'] in name:
            return i
    return -1