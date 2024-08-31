import torch

from typing import Optional
from omegaconf import OmegaConf
from huggingface_hub import hf_hub_download
from .allinone import AllInOne
from .ensemble import Ensemble
from ..typings import PathLike

NAME_TO_FILE = {
    "harmonix-fold0": "harmonix-fold0-0vra4ys2.pth",
    "harmonix-fold1": "harmonix-fold1-3ozjhtsj.pth",
    "harmonix-fold2": "harmonix-fold2-gmgo0nsy.pth",
    "harmonix-fold3": "harmonix-fold3-i92b7m8p.pth",
    "harmonix-fold4": "harmonix-fold4-1bql5qo0.pth",
    "harmonix-fold5": "harmonix-fold5-x4z5zeef.pth",
    "harmonix-fold6": "harmonix-fold6-x7t226rq.pth",
    "harmonix-fold7": "harmonix-fold7-qwwskhg6.pth",
    "all-fold0": "all-fold0-40pa2vpn.pth",
    "all-fold1": "all-fold1-ixhnrlbv.pth",
    "all-fold2": "all-fold2-b9yx1jtt.pth",
    "all-fold3": "all-fold3-ri1y9ns9.pth",
    "all-fold4": "all-fold4-u6l5vhox.pth",
    "all-fold5": "all-fold5-m7dx7spr.pth",
    "all-fold6": "all-fold6-4j7nqihf.pth",
    "all-fold7": "all-fold7-f0qjbkoz.pth",
}

ENSEMBLE_MODELS = {
    "harmonix-all": [
        "harmonix-fold0",
        "harmonix-fold1",
        "harmonix-fold2",
        "harmonix-fold3",
        "harmonix-fold4",
        "harmonix-fold5",
        "harmonix-fold6",
        "harmonix-fold7",
    ],
    "all": [
        "all-fold0",
        "all-fold1",
        "all-fold2",
        "all-fold3",
        "all-fold4",
        "all-fold5",
        "all-fold6",
        "all-fold7",
    ],
}


def load_pretrained_model(
    model_name: Optional[str] = None,
    cache_dir: Optional[PathLike] = None,
    device=None,
):
    if model_name in ENSEMBLE_MODELS:
        return load_ensemble_model(model_name, cache_dir, device)

    model_name = model_name or list(NAME_TO_FILE.keys())[0]
    assert (
        model_name in NAME_TO_FILE
    ), f"Unknown model name: {model_name} (expected one of {list(NAME_TO_FILE.keys())})"

    if device is None:
        if torch.cuda.device_count():
            device = "cuda"
        else:
            device = "cpu"

    filename = NAME_TO_FILE[model_name]
    checkpoint_path = hf_hub_download(
        repo_id="taejunkim/allinone", filename=filename, cache_dir=cache_dir
    )

    checkpoint = torch.load(checkpoint_path, map_location=device)
    config = OmegaConf.create(checkpoint["config"])

    model = AllInOne(config).to(device)
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    return model


def load_ensemble_model(
    model_name: Optional[str] = None,
    cache_dir: Optional[PathLike] = None,
    device=None,
):
    models = []
    for model_name in ENSEMBLE_MODELS[model_name]:
        model = load_pretrained_model(model_name, cache_dir, device)
        models.append(model)

    ensemble = Ensemble(models).to(device)
    ensemble.eval()

    return ensemble
