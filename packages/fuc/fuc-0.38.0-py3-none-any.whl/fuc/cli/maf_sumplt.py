from .. import api

import matplotlib.pyplot as plt

description = """
Create a summary plot with a MAF file.

The format of output image (PDF/PNG/JPEG/SVG) will be automatically
determined by the output file's extension.
"""

epilog = f"""
[Example] Output a PNG file:
  $ fuc {api.common._script_name()} in.maf out.png

[Example] Output a PNG file:
  $ fuc {api.common._script_name()} in.maf out.pdf
"""

def create_parser(subparsers):
    parser = api.common._add_parser(
        subparsers,
        api.common._script_name(),
        description=description,
        epilog=epilog,
        help=
"""Create a summary plot with a MAF file."""
    )
    parser.add_argument(
        'maf',
        help=
"""Input MAF file."""
    )
    parser.add_argument(
        'out',
        help=
"""Output image file."""
    )
    parser.add_argument(
        '--figsize',
        metavar='FLOAT',
        type=float,
        default=[15, 10],
        nargs=2,
        help=
"""Width, height in inches (default: [15, 10])."""
    )
    parser.add_argument(
        '--title_fontsize',
        metavar='FLOAT',
        type=float,
        default=16,
        help=
"""Font size of subplot titles (default: 16)."""
    )
    parser.add_argument(
        '--ticklabels_fontsize',
        metavar='FLOAT',
        type=float,
        default=12,
        help=
"""Font size of tick labels (default: 12)."""
    )
    parser.add_argument(
        '--legend_fontsize',
        metavar='FLOAT',
        type=float,
        default=12,
        help=
"""Font size of legend texts (default: 12)."""
    )

def main(args):
    mf = api.pymaf.MafFrame.from_file(args.maf)
    mf.plot_summary(
        figsize=args.figsize,
        title_fontsize=args.title_fontsize,
        ticklabels_fontsize=args.ticklabels_fontsize,
        legend_fontsize=args.legend_fontsize
    )
    plt.savefig(args.out)
