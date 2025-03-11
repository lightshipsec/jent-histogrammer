"""The one and only main script for this python package"""
import argparse
import sys
from importlib.metadata import PackageNotFoundError, version

import matplotlib.pyplot as plt
import numpy as np
from halo import Halo

try:
    PACKAGE_VERSION = version("jent_histogrammer")
except PackageNotFoundError:
    PACKAGE_VERSION = "dev"


def create_histogram(data, lower_limit, upper_limit, bin_width, output_file):
    """Function which creates a histogram from the provided data"""
    spinner = Halo(text=f"Creating histogram: {output_file}", spinner="line")
    spinner.start()

    plt.title("JENT Histogram")

    legend_text = f'''Lower: {lower_limit}
Upper: {upper_limit}
Bin Width: {bin_width}
Sample: {data.size}'''

    plt.figtext(0.15, 0.75, legend_text, fontsize=6, bbox=dict(facecolor='lightgray', alpha=0.5))

    plt.hist(data,
            bins=range(lower_limit, upper_limit, bin_width),
            histtype='bar',
            color='g')
    plt.savefig(output_file, format="jpg", dpi=300)
    spinner.succeed()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description=f"JEnt Histogrammer ({PACKAGE_VERSION})",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version', action='version', version=f'{PACKAGE_VERSION}', default=None)
    parser.add_argument("input_file", type=str, help="Input file")
    parser.add_argument("output_file", type=str, help="Output file")
    parser.add_argument("--file-type", type=str,
                        choices=["binary", "ascii"],
                        help="Input file format",
                        default="binary")
    parser.add_argument("--bin-width", type=int, help="Bin/bucket width", default=5)
    parser.add_argument("--sample-size", type=str, default="32",
                        help="Sample size in bits", choices=["8", "32"])
    parser.add_argument("--lower", type=int, help="Lower bounds of histogram")
    parser.add_argument("--upper", type=int, help="Upper bounds of histogram")

    args = parser.parse_args()

    dtype = np.uint32
    if args.sample_size == "8":
        dtype = np.uint8
    elif args.sample_size == "32":
        dtype = np.uint32

    if args.version:
        print(f"{PACKAGE_VERSION}")
        sys.exit(0)

    spinner = Halo(text=f"Loading {args.file_type} sample file: {args.input_file}", spinner="line")
    spinner.start()
    data = None
    if args.file_type == "binary":
        data = np.fromfile(args.input_file, dtype=dtype)
    elif args.file_type == "ascii":
        data = np.loadtxt(args.input_file, dtype=dtype)
    else:
        print("ERROR: Unknown file type:", args.file_type)
        sys.exit(1)

    spinner.succeed()

    lower_limit = args.lower
    if lower_limit is None:
        lower_limit = np.min(data)

    upper_limit = args.upper
    if upper_limit is None:
        upper_limit = np.max(data)

    create_histogram(data, lower_limit, upper_limit, args.bin_width, args.output_file)
