#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/2022 10:04 PM
# @Author  : Runsheng     
# @File    : bedbin6.py


from __future__ import print_function
import sys
# get a script to make the bin sized histogram
# prepare a bed file like:
#
# I\t\t1000\n
# I\t1000\t2000\n
# to use as the bed.a
# and use the bedtools coverage -a bed.a -b bam to get the interval wig file

# example, the length of C. elegans genome
"""
chrI     15072423
chrII     15279345
chrIII     13783700
chrIV     17493793
chrV     20924149
chrX     17718866
"""

def get_chrlist(chrsize_txt):
    with open(chrsize_txt, "r") as f:
        chr_list=[]
        for line in f.readlines():
            chro=line.split("\t")[0]
            length=int(line.strip().split("\t")[-1])
            chr_list.append((chro,length))
    return chr_list


def bed_generate(chr_list,binsize=50):
    """
    generate a bin file in bed format using bin size and steps
    still using 0 based [start end) coding for the output
    output: bed6 with chro, start, end, name, . strand
    """
    for line in chr_list:
        chro,length=line
        ### for oen chro
        for i in range(0,length/binsize+1):
            start=(i)*binsize
            end=(i+1)*binsize
            if end <= length:
                end=end
            else:
                end=length
            name_l=[str(x) for x in [chro, start, end]]
            name="_".join(name_l)
            bed6_l=[str(x) for x in [chro, start, end, name, ".", "+"]]
            sys.stdout.write("\t".join(bed6_l))
            sys.stdout.write("\n")

    return 0


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--fa_size",
                        help="the size file for the fasta")
    parser.add_argument("-b", "--bin", default=100000,
                        help="the bin size used")

    args = parser.parse_args()

    # make a file using the functions
    chr_list=get_chrlist(chrsize_txt=args.fa_size)
    bed_generate(chr_list=chr_list, binsize=int(args.bin))
