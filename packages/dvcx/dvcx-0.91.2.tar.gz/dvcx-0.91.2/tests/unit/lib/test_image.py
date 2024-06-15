import open_clip
import pytest
from PIL import Image
from torch import Tensor
from torchvision.transforms import ToTensor

from dvcx.lib.image import CLIPScoreMapper, ImageFile, ImageReader, convert_image


def test_convert_image(tmp_path):
    file_name = "img.jpg"
    file_path = tmp_path / file_name

    img = Image.new(mode="RGB", size=(64, 64))
    img.save(file_path)

    converted_img = convert_image(
        img,
        mode="RGBA",
        size=(32, 32),
        transform=ToTensor(),
    )
    assert isinstance(converted_img, Tensor)
    assert converted_img.size() == (4, 32, 32)


def test_image_file(tmp_path, catalog):
    file_name = "img.jpg"
    file_path = tmp_path / file_name

    img = Image.new(mode="RGB", size=(64, 64))
    img.save(file_path)

    file = ImageFile(name=file_name, source=f"file://{tmp_path}")
    file.set_catalog(catalog)

    with open(file_path, "rb") as fd:
        file.set_file(fd, caching_enabled=False)
        assert isinstance(file.get_value(), Image.Image)


def test_image_file_reader(mocker):
    img = Image.new(mode="RGB", size=(64, 64))

    kwargs = {
        "mode": "RGBA",
        "size": (32, 32),
        "transform": ToTensor(),
        "open_clip_model": None,
    }
    reader = ImageReader(**kwargs)

    convert_image = mocker.patch("dvcx.lib.image.convert_image")

    reader(img)
    assert len(convert_image.call_args.args) == 1
    assert isinstance(convert_image.call_args.args[0], Image.Image)
    assert convert_image.call_args.kwargs == kwargs


@pytest.mark.parametrize("text", ["caption text", ["text1", "text2"]])
@pytest.mark.parametrize("prob", [True, False])
def test_clip_score_mapper(text, prob):
    img = Image.new(mode="RGB", size=(64, 64))

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k"
    )
    tokenizer = open_clip.get_tokenizer("ViT-B-32")

    kwargs = {
        "model": model,
        "preprocess": preprocess,
        "tokenizer": tokenizer,
        "text": "text",
        "output": "scores",
        "prob": prob,
    }
    mapper = CLIPScoreMapper(**kwargs)
    assert "text" in mapper.params
    assert list(mapper.output.keys()) == ["scores"]
    assert mapper.output["scores"].to_dict() == {
        "type": "Array",
        "item_type": {"type": "Float"},
    }

    scores = mapper.similarity_scores(img, text)
    assert isinstance(scores, list)
    if isinstance(text, str):
        assert len(scores) == 1
    else:
        assert len(scores) == len(text)
    if prob:
        assert sum(scores) == pytest.approx(1)
