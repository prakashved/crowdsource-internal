This module will convert the log files obtained from the crowdsourcing app into a csv file.

Allows us to easily analyse the dataset

The first line of the csv file are the names of the columns.

Output: csv files by MSIDSN level, i.e. for each MSIDSN, we have a csv file
The csv files will appear in the folder where the log files are found, under the sub-directory csv_files

How to run:

Used the argparse module which explains what the variables represent

I) Output csv files for all the MSISDNs present:

   python Data_preparation.py ./data/crowdsource-internal/


II) Output csv files for MSISDN x and MSIDSN y

    python Data_preparation.py ./data/crowdsource-internal/ -i 6598282016 6598636442

