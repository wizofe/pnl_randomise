# fsl_randomise

FSL randomise related scripts.

## TODO
- Write a complete test for randomise_summary.py
- Write up `README.md`


Table of Contents
=================
    * [randomise_summary.py](#randomise_summary.py)
    * [merge_images_and_make_design.py](#merge_images_and_make_design.py)


## randomise_summary.py
This script could be used to summarize outputs from FSL randomise. 


## Usage

> Simplest use

It automatically finds `design.mat` and `design.con` in the current directory,
along with `*corrp*nii.gz` images when ran without any options.

```sh
cd RANDOMISE/LOCATION/stats
randomise_summary.py
```



> Individual `*corrp*nii.gz`

Also individual `*corrp*nii.gz` images, `design.mat` and `design.con` in 
different location could be specified with options.

```sh
randomise_summary.py -i stats/tbss_corrp_tstat1.nii.gz

# you can also specify design matrices if they have different naming
randomise_summary.py -i stats/tbss_corrp_tstat1.nii.gz \
                     -d stats/this_is_design_file.mat \
                     -c stats/this_is_contrast_file.mat \

```


> Control p-value threshold

The p-value for significance could be altered, if higher threshold is rquired
by adding extra option `-t` or `--threshold`

```sh
randomise_summary.py -t 0.99
```


> Run FSL's atlas query with the significant cluster

FSL's atlas query returns information about the location of the cluster. If
`-a` or `--atlas` option is given, the script will run atlas query on the 
significant cluster and print the summarized output on screen

```sh
randomise_summary.py -a
```

> Extract values for the significant cluster in each subject

It is a common practice to look at the correlation between the values of each
subject in the significant cluster and their clinical scales.  Simply add `--subject_values` option for this.

```sh
randomise_summary.py --subject_values
```

If your randomise directory does not have the `all_*.nii.gz` (4d merged image), 
specify the directory where the 4d merged images are, with `--merged_img_dir`

```sh
randomise_summary.py --subject_values \
                     --merged_img_dir /DIRECTORY/WITH/all_4D_skeleton.nii.gz
```

> Create png file -- **under development : link kcho_figure.py**

```sh
randomise_summary.py --figure
```


> All options

```sh
usage: randomise_summary.py [-h] [--directory DIRECTORY]
                            [--input INPUT [INPUT ...]]
                            [--threshold THRESHOLD] [--contrast CONTRAST]
                            [--matrix MATRIX] [--subject_values]
                            [--merged_img_dir MERGED_IMG_DIR] [--atlasquery]
                            [--figure]

        randomise_summary.py --dir /example/randomise/output/dir/
        

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Specify randomise out dir. This this option is given,
                        design.mat and design.con within the directory are
                        read by default.
  --input INPUT [INPUT ...], -i INPUT [INPUT ...]
                        Specify randomise out corrp files. If this option is
                        given, --directory input is ignored
  --threshold THRESHOLD, -t THRESHOLD
                        Threshold for the significance
  --contrast CONTRAST, -c CONTRAST
                        Contrast file used for the randomise.
  --matrix MATRIX, -m MATRIX
                        Matrix file used for the randomise
  --subject_values, -s  Print average in the significant cluster for all
                        subjects
  --merged_img_dir MERGED_IMG_DIR, -p MERGED_IMG_DIR
                        Directory that contains merged files
  --atlasquery, -a      Run atlas query on significant corrp files
  --figure, -f          Create figures

Kevin Cho Thursday, August 22, 2019
```

## Example output
```
[kc244@rgs09:/data/pnl/kcho/Lupus/TBSS/final/ANOVA]$ python /data/pnl/kcho/PNLBWH/fsl_randomise/randomise_summary.py
/data/pnl/kcho/Lupus/TBSS/final/ANOVA None None
--------------------------------------------------------------------------------
* Matrix summary
/data/pnl/kcho/Lupus/TBSS/final/ANOVA
/data/pnl/kcho/Lupus/TBSS/final/ANOVA/design.con
/data/pnl/kcho/Lupus/TBSS/final/ANOVA/design.mat
total number of data point : 79
Group columns are : col 0, col 1, col 2
+--------+---------+---------+---------+
|        | col 0   | col 1   | col 2   |
|--------+---------+---------+---------|
| mean   | 0.25    | 0.32    | 0.43    |
| std    | 0.44    | 0.47    | 0.5     |
| min    | 0.0     | 0.0     | 0.0     |
| max    | 1.0     | 1.0     | 1.0     |
| unique | Group 1 | Group 2 | Group 3 |
| count  | 20      | 25      | 34      |
+--------+---------+---------+---------+
--------------------------------------------------------------------------------
* Result summary
+-----------------------------------+------------+--------+------------+------------+----------------+---------+-------------------+-------------+--------------+------------------------+----------+-----------+
| file name                         | contrast   | Test   | Modality   |   Stat num | Significance   |   Max P | contrast_text     |    Sig mean |      Sig std |   % significant voxels |   % left |   % right |
|-----------------------------------+------------+--------+------------+------------+----------------+---------+-------------------+-------------+--------------+------------------------+----------+-----------|
| tbss_FA_tfce_corrp_fstat1.nii.gz  | * 1 1 1    | f      | FA         |          1 | False          |  0.8302 | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FA_tfce_corrp_tstat1.nii.gz  | 1. -1.  0. | t      | FA         |          1 | False          |  0.9392 | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FA_tfce_corrp_tstat2.nii.gz  | 1.  0. -1. | t      | FA         |          2 | True           |  0.9758 | Group 1 > Group 3 |   0.0353768 |   0.00701967 |                   19.8 |     13.7 |      28.8 |
| tbss_FA_tfce_corrp_tstat3.nii.gz  | 0.  1. -1. | t      | FA         |          3 | False          |  0.7114 | Group 2 > Group 3 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FAt_tfce_corrp_fstat1.nii.gz | * 1 1 1    | f      | FAt        |          1 | False          |  0.8788 | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FAt_tfce_corrp_tstat1.nii.gz | 1. -1.  0. | t      | FAt        |          1 | True           |  0.9608 | Group 1 > Group 2 |   0.0444185 |   0.00322326 |                    0.9 |      0   |       2.1 |
| tbss_FAt_tfce_corrp_tstat2.nii.gz | 1.  0. -1. | t      | FAt        |          2 | True           |  0.9984 | Group 1 > Group 3 |   0.0153723 |   0.0132404  |                   51.2 |     50.6 |      57.1 |
| tbss_FAt_tfce_corrp_tstat3.nii.gz | 0.  1. -1. | t      | FAt        |          3 | False          |  0.8374 | Group 2 > Group 3 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FW_tfce_corrp_fstat1.nii.gz  | * 1 1 1    | f      | FW         |          1 | False          |  0.8172 | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FW_tfce_corrp_tstat1.nii.gz  | 1. -1.  0. | t      | FW         |          1 | False          |  0.2646 | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FW_tfce_corrp_tstat2.nii.gz  | 1.  0. -1. | t      | FW         |          2 | False          |  0.0838 | Group 1 > Group 3 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_FW_tfce_corrp_tstat3.nii.gz  | 0.  1. -1. | t      | FW         |          3 | False          |  0.5842 | Group 2 > Group 3 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_MD_tfce_corrp_fstat1.nii.gz  | * 1 1 1    | f      | MD         |          1 | False          |  0.7704 | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_MD_tfce_corrp_tstat1.nii.gz  | 1. -1.  0. | t      | MD         |          1 | False          |  0.401  | Group 1 > Group 2 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_MD_tfce_corrp_tstat2.nii.gz  | 1.  0. -1. | t      | MD         |          2 | False          |  0.2036 | Group 1 > Group 3 | nan         | nan          |                  nan   |    nan   |     nan   |
| tbss_MD_tfce_corrp_tstat3.nii.gz  | 0.  1. -1. | t      | MD         |          3 | False          |  0.6076 | Group 2 > Group 3 | nan         | nan          |                  nan   |    nan   |     nan   |
+-----------------------------------+------------+--------+------------+------------+----------------+---------+-------------------+-------------+--------------+------------------------+----------+-----------+
```
