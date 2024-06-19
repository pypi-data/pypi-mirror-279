from typing import Union

import torch
from check_shapes import check_shapes
from torch import nn

from ..networks.transformer import ISTEncoder, PerceiverEncoder
from ..utils.helpers import preprocess_observations
from .base import ConditionalNeuralProcess
from .tnp import TNPDecoder


class PTTNPEncoder(nn.Module):
    def __init__(
        self,
        transformer_encoder: Union[PerceiverEncoder, ISTEncoder],
        xy_encoder: nn.Module,
    ):
        super().__init__()

        self.transformer_encoder = transformer_encoder
        self.xy_encoder = xy_encoder

    @check_shapes(
        "xc: [m, nc, dx]", "yc: [m, nc, dy]", "xt: [m, nt, dx]", "return: [m, nq, dz]"
    )
    def forward(
        self,
        xc: torch.Tensor,
        yc: torch.Tensor,
        xt: torch.Tensor,
    ) -> torch.Tensor:
        yc, yt = preprocess_observations(xt, yc)

        zc = torch.cat((xc, yc), dim=-1)
        zc = self.xy_encoder(zc)

        zt = torch.cat((xt, yt), dim=-1)
        zt = self.xy_encoder(zt)

        zt = self.transformer_encoder(zc, zt)
        return zt


class PTTNP(ConditionalNeuralProcess):
    def __init__(
        self,
        encoder: PTTNPEncoder,
        decoder: TNPDecoder,
        likelihood: nn.Module,
    ):
        super().__init__(encoder, decoder, likelihood)
