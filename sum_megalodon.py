#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/4/2022 3:11 PM
# @Author  : Runsheng     
# @File    : sum_megalodon.py

"""
parsers for megalodon bed11 file
generate summary for all sites and regional level (promoter or gene)
"""
import pandas
import os

from utils import myexe

import logger
LOGGER=logger.get_logger()

def sum_5mc_ratio(d0):
    """
    d0 is a df from the megalodon bed dfile
    print is (methylated C number, unmethylated C number)
    return methylated C number
    """
    # print((d0[10]/100*d0[9]).sum()/d0[9].sum(),
    #     ( (1-d0[10]/100)*d0[9] ).sum()/d0[9].sum())

    return (d0[10] / 100 * d0[9]).sum() / d0[9].sum()


def sum_inter_promoter(in_filename, out_filename):
    """
    return the gene:mean propotion in promoter info
    """
    df_inter = pandas.read_csv(in_filename, sep="\t", header=None)
    last_col=len(df_inter.columns)
    df = df_inter.groupby([3])[last_col-1].mean()
    df.to_csv(out_filename, header=False)


def sum_5mc_promoter(in_csv):
    df = pandas.read_csv(in_csv, sep=",", header=None)
    return df[[1]].mean()[1]


def flow_process_megalodon(in_file, promoter_file, sample="WT", wkdir=os.getcwd()):
    """
    infile is a megalodon bed file
    out: sample_promoter.csv: gene, proportion (gene is the region defined in promoter_file)
    out: sample_overall.csv: sample, all, promoter_all
    """
    print("wkdir", wkdir)
    df1 = pandas.read_csv(in_file, sep="\t", header=None)
    number_all = sum_5mc_ratio(df1)

    # outfile names
    inter_file = sample + "_inter.bed"
    sum_file = sample + "_sum.txt"
    sum_promoter_file = sample + "_promoter.csv"

    # main code
    cmd_bedtools = """
    cd {wkdir}
    bedtools intersect -a {promoter_file} -b {in_file} -wa -wb > {inter_file}""".format(
        wkdir=wkdir, promoter_file=promoter_file, in_file=in_file, inter_file=inter_file)
    print(cmd_bedtools)
    myexe(cmd_bedtools)

    # write one file
    sum_inter_promoter(in_filename=inter_file, out_filename=sum_promoter_file)
    number_promoter = sum_5mc_promoter(sum_promoter_file)

    # write sum file
    with open(sum_file, "w") as fw:
        fw.write(sample + "\t" + str(number_all) + "\t" + str(number_promoter))
        fw.write("\n")
    # clean
    clean_cmd = """rm {inter_file}""".format(inter_file=inter_file)
    myexe(clean_cmd)

    return 0


if __name__=="__main__":
    import argparse
    example_text = '''example:
    ### example to run the sum_megalodon.py 
    sum_megalodon.py --i modified_bases.6mA.bed -a gene.bed -s sample 
    The script will generate sample_sum.txt and sample_promoter.csv as the result
    ####
    out: sample_promoter.csv: gene, proportion (gene is the region defined in gene.bed)
    out: sample_sum.txt: sample, all, gene_all
    #### 
    input of modified_bases.6mA.bed is a 11 col megalodon result
    input of gene.bed is a 6 col annotation bed with "chr start end name coverage strand" information, the coverage column can be empty
    '''
    parser = argparse.ArgumentParser(prog='sum_megaladon',
                                     description='megalodon bed parser, generate the overall sum for proportion and the regional summary for a givien region, like the promoter region',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-i", "--input", help="the megalodon bed file with 11 cols, the bed follows the bedtool bedgraph format, with strand information in col6, name information in col4, coverage information in col5")
    parser.add_argument("-a", "--annotation", help="the annotation bed file, with at least 6 cols following the bedtool format, with strand information in col6, name information in col4")
    parser.add_argument("-p", "--prefix", default="sample", help="the prefix of the output files")

    args = parser.parse_args()
    flow_process_megalodon(in_file=args.input, promoter_file=args.annotation, sample=args.prefix)
