import torch
from torch import nn
from gxl_ai_utils.utils import utils_file


class Transducer(nn.Module):
    def __init__(self,
                 encoder,
                 decoder,
                 joiner):
        """"""
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.joiner = joiner

    def forward(self,
                x: torch.Tensor,
                x_lens: torch.Tensor,
                y: torch.Tensor,
                y_lens: torch.Tensor):
        """"""
        assert x.ndim == 3, x.ndim
        assert x_lens.ndim == 1, x_lens.ndim
        assert y.ndim == 2, y.shape[-1]
        assert y_lens.ndim == 1, y_lens.ndim
        x, x_lens = self.joiner(x, x_lens)
        assert torch.all(x_lens >= 0), x_lens
        blank_id = self.decoder.blank_id
        sos = torch.ones(x.shape[0], 1, dtype=torch.long) * blank_id
        sos_y = torch.cat([sos, y], dim=1)
        sos_y_padded = utils_file.do_padding_ids_by_lens(sos_y, x_lens, blank_id)
        decoder_out,_ = self.decoder(sos_y_padded)






def test_transducer():
    """"""
    input_tensor = torch.randint(0, 1023, size=(3, 12))
    lengths = torch.randint(5, 12, size=(3,))

    print()
    print(input_tensor)
    print(lengths)
    output_y = utils_file.do_padding_ids_by_lens(input_tensor, lengths, 120)
    print()
    print(output_y)
    input_tensor = torch.randn(3,5,8)
    lengths = torch.randint(2, 6, size=(3,))
    print(lengths)
    output_y = utils_file.do_padding_embeds_by_lens(input_tensor, lengths, 10)
    print(output_y)



if __name__ == '__main__':
    print('haha')
