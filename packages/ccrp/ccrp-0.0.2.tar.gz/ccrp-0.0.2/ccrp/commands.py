from .utils import split_two_bytes


def debug_print_commands(commands):
    print([hex(c) for c in commands])


def reset():
    return [0x1B, 0x40]


def lf():
    return [0x0A]


def lf_cr():
    return [0x0A, 0x0D]


def font(*, compressed=False, bold=False, double_height=False, double_width=False, underline=False):
    """
    compressed true: 9x17, compressed false: 12x24
    """
    font_code = (
        0b00000000
        + 0b00000001 * compressed
        + 0b00001000 * bold
        + 0b00010000 * double_height
        + 0b00100000 * double_width
        + 0b01000000 * underline
    )
    return [0x1B, 0x21, font_code]


def text(t):
    return bytes(t, encoding="cp437")


def line(t):
    return bytes(t, encoding="cp437") + bytes([0x0A, 0x0D])


def raw(data: bytes):
    # for hacky printer mostly
    return data


def align(align="left"):
    # in order
    aligns = ["left", "center", "right"]
    assert align in aligns, "Invalid align mode"
    return [0x1B, 0x61, aligns.index(align)]


def feed(lines):
    # print buffer and feed lines
    assert lines >= 0 and lines < 2**8
    return [0x1B, 0x64, lines]


def cut(*, partial=False):
    # autocutter
    return [0x1D, 0x56, 0x01 * partial]


def std_cut(lines=6):
    return feed(lines) + cut()


def raw_code128(data, *, width=2, height=50, text_above=False, text_below=True, text_compressed=False):
    """
    text_above and text_below control whether a human readable interpretation (HRI) is printed above and/or below the
    barcode
    """
    commands = []
    # set width
    assert width >= 2 and width <= 6
    commands += [0x1D, 0x77, width]
    # set height
    assert height >= 1 and height <= 255
    commands += [0x1D, 0x68, height]
    # set HRI above and/or below
    commands += [0x1D, 0x48, 0x0 + 0x01 * text_above + 0x02 * text_below]
    # set HRI compressed or not
    commands += [0x1D, 0x66, 0x01 * text_compressed]
    assert len(data) >= 2 and len(data) <= 255
    # now actual barcode, 73 is code 128
    commands += [0x1D, 0x6B, 73, len(data)]
    commands += data
    return commands


def code128(text, *args, **kwargs):
    """
    text_above and text_below control whether a human readable interpretation (HRI) is printed above and/or below the
    barcode

    TODO: this currently only support code page B, which is suboptimal for some things and can't represent everything
    """
    data = bytes("{B" + text, "ascii")
    assert all((c >= 32 and c <= 126) for c in data)
    return raw_code128(data, *args, **kwargs)


def qr_code(text, *, version=0, err_level="M", pixel_size=6):
    commands = []
    # select QR code
    commands += [0x1D, 0x5A, 0x02]
    # check version (size), version = 0 is automatic
    assert version >= 0 and version <= 40
    # check error correction level was valid
    err_levels = {
        "L": 76,
        "M": 77,
        "Q": 81,
        "H": 72,
    }
    r = err_levels.get(err_level, None)
    assert r is not None, "Invalid error correction level"
    # err_levels = ["L", "M", "Q", "H"]
    # assert err_level in err_levels
    # r = err_levels.index(err_level)
    assert pixel_size >= 1 and pixel_size <= 6
    if isinstance(text, bytes):
        data = text
    else:
        data = bytes(text, "iso-8859-1")
    # length of data
    n = len(data)
    assert n >= 1 and n <= 65535
    nH, nL = split_two_bytes(n)
    commands += [0x1B, 0x5A, version, r, pixel_size, nL, nH]
    commands += data
    return commands


def data_matrix(text, *, image_height=0, image_width=8, pixel_size=6):
    # TODO: figure out encoding
    if isinstance(text, bytes):
        data = text
    else:
        data = bytes(text, "ascii")
    commands = []
    # select data matrix
    commands += [0x1D, 0x5A, 0x01]
    # 0 is auto
    assert image_height >= 0 and image_height <= 144
    assert image_width >= 8 and image_width <= 144
    assert pixel_size >= 1 and pixel_size <= 6
    # length of data
    n = len(data)
    assert n >= 1 and n <= 65535
    nH, nL = split_two_bytes(n)
    commands += [0x1B, 0x5A, image_height, image_width, pixel_size, nL, nH]
    commands += data
    return commands


def set_horizontal_tabs(positions):
    # set horizontal tabs to positions given by the list
    assert all((p >= 1 and p <= 255) for p in positions)
    return [0x1B, 0x44] + positions + [0x00]


def tab(number=1):
    return [0x09] * number


def set_code_page(n=0):
    """
    n is number or string from below
    """
    known_cps = {
        "CP437": 0,
        "ISO-8859-1": 23,
    }
    if isinstance(n, str):
        n = known_cps.get(n)
        if n is None:
            raise AttributeError("Unknown code page")
    assert n >= 0 and n <= 255
    return [0x1B, 0x74, n]


def checkbox(compressed=False, filled=False):
    if not compressed:
        # define normal checkbox chars
        # ESC &
        # define 0x20 to be left one, 0x21 as right one
        commands = [0x1B, 0x26, 3, 0x20, 0x21]
        # left bracket
        filled_column = [0x7F, 0xFF, 0xFE]
        if not filled:
            column = [0x80, 0x0, 0x01]
        else:
            column = [0xFF, 0xFF, 0xFF]
        commands += [12] + filled_column + column * 11
        # right bracket
        commands += [12] + column * 11 + filled_column
    else:
        # define compressed checkbox chars
        empty_column = [0x00, 0x00, 0x00]
        filled_column = [0x00, 0xFF, 0xFE]
        if not filled:
            column = [0x01, 0x00, 0x01]
        else:
            column = [0x01, 0xFF, 0xFF]
        commands = [0x1B, 0x26, 3, 0x20, 0x21]
        commands += [9] + empty_column + filled_column + column * 7
        commands += [9] + column * 7 + filled_column + empty_column

    # print them
    # set self-defined character set
    commands += [0x1B, 0x25, 0x1]
    # print our chars
    commands += [0x20, 0x21]
    # undo self-defined chars
    commands += [0x1B, 0x25, 0x0]
    return commands


normal_char_width = 47
double_char_width = 24
compressed_char_width = 64


def _bits_to_stripe_bytes(bits, width, height):
    # takes a list of 0/1 bits and produces a striped bitmap, where every 8 running binary pixels turn into a byte
    assert width % 8 == 0
    assert len(bits) == width * height
    out = [[0x0] * (width // 8) for _ in range(height)]
    for y in range(height):
        for x in range(width // 8):
            byte = bits[width * y + x * 8 : width * y + (x + 1) * 8]
            out[y][x] = sum([b << (7 - n) for n, b in enumerate(byte)])
    return out, width // 8, height


def print_bits_bitmap(bits, width, height):
    # takes a list of 0/1 bits and produces bitmap commands
    bytes_, bytes_width, bytes_height = _bits_to_stripe_bytes(bits, width, height)
    commands = [0x1D, 0x44, 0x01]
    for row in bytes_:
        commands += [0x15, 0x01, 0x16, len(row)] + row
    commands += [0x1D, 0x44, 0x00]
    return commands


def write_user_defined_bitmap(position, bits, width, height):
    assert width % 8 == 0
    assert len(bits) == width * height
    bytes_, bytes_width, bytes_height = _bits_to_stripe_bytes(bits, width, height)
    wH, wL = split_two_bytes(bytes_width)
    hH, hL = split_two_bytes(bytes_height)
    assert position >= 0 and position < 8
    commands = [0x1B, 0xFE, position, wL, wH, hL, hH]
    for row in bytes_:
        commands += row
    return [0x1B, 0x09] + commands + [0x1B, 0x15]


def user_defined_bitmap(position):
    assert position >= 0 and position < 8
    commands = [0x1C, 0x50, position]
    return commands
