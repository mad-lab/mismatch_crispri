#!/usr/bin/env python
# Author: John Hawkins (jsh) [really@gmail.com]

import argparse
import logging
import pathlib
import shutil
import sys

from matplotlib import pyplot as plt
import pandas as pd
import scipy.stats as st
import seaborn as sns

import eval_lib as el

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s') 

_PACKAGEDIR = pathlib.Path(__file__).parent
TESTDIR = _PACKAGEDIR / 'testdata'
_CODEFILE = pathlib.Path(__file__)


def parse_args():
  """Read in the arguments for the sgrna library construction code."""
  logging.info('Parsing command line.')
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--xgammas', type=str,
      help='file: unique entries for gamma by variant -- x axis',
      required=True)
  parser.add_argument(
      '--xname', type=str,
      help='str: label name for x axis',
      required=True)
  parser.add_argument(
      '--ygammas', type=str,
      help='file: unique entries for gamma by variant -- y axis',
      required=True)
  parser.add_argument(
      '--yname', type=str,
      help='str: label name for y axis',
      required=True)
  parser.add_argument(
      '--pngfile', type=str,
      help='directory: directory for plots (WARNING: will be created and cleared)',
      required=True)
  args = parser.parse_args()
  return args


def main():
  args = parse_args()
  template = 'Reading X: {args.xname} from {args.xgammas}...'
  logging.info(template.format(**locals()))
  xdata = pd.read_csv(args.xgammas, sep='\t')
  xprs = el.pearsons_by_gene(xdata)

  template = 'Reading Y: {args.yname} from {args.ygammas}...'
  logging.info(template.format(**locals()))
  ydata = pd.read_csv(args.ygammas, sep='\t')
  yprs = el.pearsons_by_gene(ydata)

  data = pd.concat([xprs, yprs], axis='columns')
  data.columns = [args.xname, args.yname]

  fig = plt.figure(figsize=(6,6))
  sns.scatterplot(args.xname, args.yname, data=data,
                  s=5, alpha=0.5, edgecolor='none')

  template = 'Pearson R Comparison\n{args.xname} vs {args.yname}'
  plt.title(template.format(**vars()))
  plt.xlim(-1.1, 1.1)
  plt.ylim(-1.1, 1.1)
  plt.xlabel(args.xname)
  plt.ylabel(args.yname)
  plt.tight_layout()
  plt.savefig(args.pngfile, dpi=300)
  plt.close('all')

##############################################
if __name__ == "__main__":
  sys.exit(main())
