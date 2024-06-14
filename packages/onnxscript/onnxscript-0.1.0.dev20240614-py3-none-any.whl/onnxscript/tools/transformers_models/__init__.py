# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
# pylint: disable=import-outside-toplevel
from __future__ import annotations

import random
from typing import Any, Sequence

import torch


def has_transformers():
    """Tells if transformers is installed."""
    try:
        import transformers

        assert transformers
        return True  # noqa
    except ImportError:
        return False


def ids_tensor(
    shape: Sequence[int],
    vocab_size: int,
    rng: random.Random | None = None,
    name: str | None = None,
):
    """Creates a random int32 tensor of the shape within the vocab size."""
    del name  # unused

    if rng is None:
        rng = random.Random()

    total_dims = 1
    for dim in shape:
        total_dims *= dim

    values = []
    for _ in range(total_dims):
        values.append(rng.randint(0, vocab_size - 1))

    return torch.tensor(data=values, dtype=torch.long).view(shape).contiguous()


def get_input_dims_for_llm(
    dynamic_shapes: bool, warmup: int, repeat: int
) -> list[tuple[int, int]]:
    """Returns input dimensions for model such as llama, phi, ..."""
    if not dynamic_shapes:
        return [(2, 1024)] * (warmup + repeat)
    w = [(2, 1024), (3, 1024), (2, 1096)] * warmup
    w = w[:warmup]
    r = [(2, 1024), (3, 1024), (4, 1024), (2, 1096), (2, 1112)] * repeat
    r = r[:repeat]
    return w + r


def get_model_and_inputs(
    model: str,
    config: str,
    dynamic_shapes: bool,
    device: str = "cpu",
    num_hidden_layers: int = 1,
    with_mask: bool = True,
    implementation: str = "eager",
    dtype: str | None = None,
    warmup: int = 5,
    repeat: int = 10,
) -> tuple[Any, list[tuple[torch.Tensor, ...]], dict | None]:
    """
    Returns a model and a couple of dummy inputs.

    Args:
        model: model name, 'phi', 'llama', ...
        config: 'small', 'medium', 'large', ...
        dynamic_shapes: dynamic or static shapes
        device: 'cpu' or 'cuda'
        num_hidden_layers: number of hidden layers
        with_mask: one input or two inputs
        implementation: eager or sdpa
        warmup: number of inputs to generate
        repeat: number of inputs to generate for repeat
        dtype: if specified, cast the model and the inputs into this type

    Returns:
        model and list of inputs
    """
    if model == "phi":
        import onnxscript.tools.transformers_models.phi as m

        tmodel, inputs, dynamic_shapes_def = m.get_phi_model_config(
            warmup=warmup,
            repeat=repeat,
            implementation=implementation,
            with_mask=with_mask,
            num_hidden_layers=num_hidden_layers,
            dynamic_shapes=dynamic_shapes,
            config=config,
        )

    else:
        raise AssertionError(f"Model {model!r} is unknown.")

    if dtype is not None:
        dt = getattr(torch, dtype)
        tmodel = tmodel.to(dt)
        inputs = [
            tuple((i if i.dtype in {torch.int64, torch.int32} else i.to(dt)) for i in inp)
            for inp in inputs
        ]

    if device == "cuda":
        tmodel = tmodel.to("cuda")
        inputs = [tuple(i.to("cuda") for i in inp) for inp in inputs]

    return tmodel, inputs, dynamic_shapes_def
