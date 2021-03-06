#!/usr/bin/env python
# Script to render text as a PNG image.

# texttopng

# Example (all ASCII glyphs):
"""
printf $(printf '\\%s' $(seq 40 176 | grep -v '[89]')) |
  fold -w 32 |
  python3 texttopng.py > ascii.png
"""

import binascii
import itertools

import png


def usage(fil):
    fil.write("texttopng [-h|--help] text\n")


font = {
    32: '0000000000000000',
    33: '0010101010001000',
    34: '0028280000000000',
    35: '0000287c287c2800',
    36: '00103c5038147810',
    37: '0000644810244c00',
    38: '0020502054483400',
    39: '0010100000000000',
    40: '0008101010101008',
    41: '0020101010101020',
    42: '0010543838541000',
    43: '000010107c101000',
    44: '0000000000301020',
    45: '000000007c000000',
    46: '0000000000303000',
    47: '0000040810204000',
    48: '0038445454443800',
    49: '0008180808080800',
    50: '0038043840407c00',
    51: '003c041804043800',
    52: '00081828487c0800',
    53: '0078407804047800',
    54: '0038407844443800',
    55: '007c040810101000',
    56: '0038443844443800',
    57: '0038443c04040400',
    58: '0000303000303000',
    59: '0000303000301020',
    60: '0004081020100804',
    61: '0000007c007c0000',
    62: '0040201008102040',
    63: '0038440810001000',
    64: '00384c545c403800',
    65: '0038447c44444400',
    66: '0078447844447800',
    67: '0038444040443800',
    68: '0070484444487000',
    69: '007c407840407c00',
    70: '007c407840404000',
    71: '003844405c443c00',
    72: '0044447c44444400',
    73: '0038101010103800',
    74: '003c040404443800',
    75: '0044487048444400',
    76: '0040404040407c00',
    77: '006c545444444400',
    78: '004464544c444400',
    79: '0038444444443800',
    80: '0078447840404000',
    81: '0038444444443c02',
    82: '0078447844444400',
    83: '0038403804047800',
    84: '007c101010101000',
    85: '0044444444443c00',
    86: '0044444444281000',
    87: '0044445454543800',
    88: '0042241818244200',
    89: '0044443810101000',
    90: '007c081020407c00',
    91: '0038202020202038',
    92: '0000402010080400',
    93: '0038080808080838',
    94: '0010284400000000',
    95: '000000000000fe00',
    96: '0040200000000000',
    97: '000038043c443c00',
    98: '0040784444447800',
    99: '0000384040403800',
    100: '00043c4444443c00',
    101: '000038447c403c00',
    102: '0018203820202000',
    103: '00003c44443c0438',
    104: '0040784444444400',
    105: '0010003010101000',
    106: '0010003010101020',
    107: '0040404870484400',
    108: '0030101010101000',
    109: '0000385454444400',
    110: '0000784444444400',
    111: '0000384444443800',
    112: '0000784444784040',
    113: '00003c44443c0406',
    114: '00001c2020202000',
    115: '00003c4038047800',
    116: '0020203820201800',
    117: '0000444444443c00',
    118: '0000444444281000',
    119: '0000444454543800',
    120: '0000442810284400',
    121: '00004444443c0438',
    122: '00007c0810207c00',
    123: '0018202060202018',
    124: '0010101000101010',
    125: '003008080c080830',
    126: '0020540800000000',
}


def char(i):
    """Get image data for the character `i` (a one character string).
    Returned as a list of rows.
    Each row is a tuple containing the packed pixels.
    """

    i = ord(i)
    if i not in font:
        return [(0,)] * 8
    return [(row,) for row in binascii.unhexlify(font[i])]


def texttoraster(m):
    """
    Convert the string *m* to a raster image.
    Any newlines in *m* will cause more than one line of output.
    The resulting raster will be taller.
    Prior to rendering each line,
    it is padded on the right with
    enough spaces to make all lines the same length.
    """

    lines = m.split('\n')
    maxlen = max(len(line) for line in lines)
    justified = [line.ljust(maxlen) for line in lines]
    rasters = [linetoraster(line) for line in justified]
    x, = set(r[0] for r in rasters)
    y = sum(r[1] for r in rasters)
    raster = itertools.chain(*(r[2] for r in rasters))
    return x, y, raster


def linetoraster(m):
    """
    Convert a single line of text *m* to a raster image,
    by rendering it using the font in *font*.

    A triple of (*width*, *height*, *pixels*) is returned;
    *pixels* is in boxed row packed pixel format.
    """

    # Assumes monospaced font.
    x = 8 * len(m)
    y = 8
    return x, y, [itertools.chain(*row) for row in zip(*map(char, m))]


def render(message, out):
    x, y, pixels = texttoraster(message)
    w = png.Writer(x, y, greyscale=True, bitdepth=1)
    w.write_packed(out, pixels)
    out.flush()


def main(argv=None):
    import sys

    if argv is None:
        argv = sys.argv
    for a in argv:
        if a.startswith('-'):
            if a in ('-h', '--help'):
                usage(sys.stdout)
                sys.exit(0)
            else:
                sys.stderr.write("Unknown option: %s\n" % a)
                usage(sys.stderr)
                sys.exit(4)
    arg = argv[1:]
    if len(arg) > 0:
        message = arg[0]
        out = open("%s.png" % message, 'wb')
    else:
        message = sys.stdin.read()
        out = png.binary_stdout()

    render(message, out)


if __name__ == '__main__':
    main()
