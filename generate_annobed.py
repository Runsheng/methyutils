#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/4/2022 4:43 PM
# @Author  : Runsheng     
# @File    : generate_annobed.py

"""
give an bed file, try to guess the name col and the name col, and write a 6 col bed out
"""
def main(infile, outfile="out.bed", namecol=5, strandcol=4):
    f=open(infile, "r")
    fw=open(outfile, "w")
    for line in f.readlines():
        line_l=line.strip().split("\t")
        chro, start, end=line_l[:3]
        name=line_l[namecol-1]
        strand=line_l[strandcol-1]
        line_w=[chro, start, end, name, ".", strand]
        fw.write("\t".join(line_w))
        fw.write("\n")
    f.close()
    fw.close()

if __name__=="__main__":
    import argparse

    example_text = """example: 
    ### example to run the generate_annobed.py 
    generate_annobed.py -i /data/zf/ref/promoter.bed -o zebrafish_promoter.bed -n 5 -s 4
    """

    parser = argparse.ArgumentParser(prog='generate_annobed',
                                     description='',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-i", "--input",
                        help="the in bed file")
    parser.add_argument("-o", "--output",default="out.bed",
                        help=" the out bed file")
    parser.add_argument("-n", "--namecol", type=int, help="the col number for the name in the input bed")
    parser.add_argument("-s", "--strandcol", type=int, help="the col number for the strand in the input bed")

    args = parser.parse_args()
    main(infile=args.input,outfile=args.output,namecol=args.namecol, strandcol=args.strandcol)
