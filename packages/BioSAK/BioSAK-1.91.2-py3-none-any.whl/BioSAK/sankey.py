import os
import argparse


sankey_usage = '''
=============================== sankey example commands ===============================

BioSAK sankey -p demo -i sankey_matrix.txt

# Requires R and its packages optparse, tools and googleVis.
# Format of input file: tab separated, non column header, first column as sample id.

=======================================================================================
'''


def unique_list_elements(list_input):

    list_output = []
    for each_element in list_input:
        if each_element not in list_output:
            list_output.append(each_element)

    return list_output


def sankey(args):

    input_datamatrix_txt = args['i']
    output_prefix        = args['p']
    plot_width           = args['x']
    plot_height          = args['y']

    pwd_self              = os.path.realpath(__file__)
    self_path             = '/'.join(pwd_self.split('/')[:-1])
    pwd_get_sankey_plot_R = '%s/get_sankey_plot.R' % self_path
    output_file_txt       = '%s.txt' % output_prefix

    paired_taxon_list_all = []
    genome_number = 0
    max_col_num = 0
    for each_line in open(input_datamatrix_txt):
        each_line_split = each_line.strip().split('\t')
        print(each_line_split)
        genome_number += 1

        if (len(each_line_split) - 1) > max_col_num:
            max_col_num = (len(each_line_split) - 1)

        n = 1
        while n < (len(each_line_split) - 1):
            print()
            paired_taxon_list_all.append('%s,%s' % (each_line_split[n], each_line_split[n+1]))
            n += 1

    paired_taxon_list_uniq = unique_list_elements(paired_taxon_list_all)
    paired_taxon_list_uniq_count_dict = {}
    for each_key in paired_taxon_list_uniq:
        paired_taxon_list_uniq_count_dict[each_key] = paired_taxon_list_all.count(each_key)

    output_file_handle = open(output_file_txt, 'w')
    output_file_handle.write('C1,C2,Number\n')
    for each_genome_taxon in paired_taxon_list_uniq_count_dict:
        for_out = '%s,%s\n' % (each_genome_taxon, paired_taxon_list_uniq_count_dict[each_genome_taxon])
        output_file_handle.write(for_out)
    output_file_handle.close()

    # run R script
    if plot_width is None:
        if max_col_num <= 5:
            plot_width = (max_col_num - 1) * 300
        else:
            plot_width = (max_col_num - 1) * 250

    if plot_height is None:
        plot_height = genome_number * 2
        if plot_height < 600:
            plot_height = 600

    os.system('Rscript %s -f %s -x %s -y %s' % (pwd_get_sankey_plot_R, output_file_txt, plot_width, plot_height))


if __name__ == '__main__':

    sankey_parser = argparse.ArgumentParser(description='', add_help=True)
    sankey_parser.add_argument('-i', required=True,             help='input datamatrix')
    sankey_parser.add_argument('-p', required=True,             help='output prefix')
    sankey_parser.add_argument('-x', required=False, type=int,  help='plot width')
    sankey_parser.add_argument('-y', required=False, type=int,  help='plot height')
    args = vars(sankey_parser.parse_args())
    sankey(args)
