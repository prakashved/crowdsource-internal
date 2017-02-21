# Data Preparation for crowd sourcing app


from __future__ import division
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import os
import sys
import csv
import argparse

class Data_Prep():

	'''
	Preprocesses the data from the crowd sourcing app into a csv file
	'''

	def __init__(self, folder, isdns=[]): 
		''' 
		PARAM: folder is the relative path of the folder which contains all the log files. 
				MSISDN is the list of MSISDNs to process. If empty list, will
				consider all the MSISDNs present in the folder

		OUTPUT: csv file in VAR folder, subdirectory csv_files
		'''

		self.folder = folder
		self.MSISDN = self._get_dates()

		if isdns ==[]:
			self.isdns =self.MSISDN.keys()

		else:
			assert(set(isdns).issubset(self.MSISDN.keys()))
			self.isdns = isdns


		return None

	@staticmethod 
	def convert_epoch_time(t):
		'''
		Convert epoch time to utc time
		PARAM: t is the epoch time either in seconds or milliseconds. Type : str
		OUTPUT : t in datetime.datetime format
		'''

		if len(t)> 12: # time is in milliseconds
			date_time = time.gmtime(int(t)/1000)
		else:
			date_time = time.gmtime(int(t))
			
		# convert to datetime.datetime format
		return datetime(*date_time[:6])

	def _get_dates(self):
		# Private method
		'''
		Obtains a dictionary where key is the MSISDN and the values are the date and time of the journey
		'''
		MSIDSN={}
		files = os.listdir(self.folder)
		files = [x for x in files if x.endswith('.log')]
		for f in files:
			isdn = f.split('_')[0]
			f_path =  os.path.join(self.folder, f)
			if isdn in MSIDSN:
				MSIDSN[isdn].append(f_path)
			else:
				MSIDSN[isdn]=[f_path]

		return MSIDSN

	def _convert_csv(self, df, msisdn):

		'''
		Print the dataframe df into csv file

		PARAMS: df is the dataframe to print to csv 

		OUTPUT: csv file under VAR folder, subfolder csv_files
		'''

		directory = os.path.join(self.folder, "csv_files")
		if not os.path.exists(directory):
			os.makedirs(directory)

		f_path = os.path.join(directory, str(msisdn)+ ".csv")
		df.to_csv(f_path, index_label="Time")

		return None


	def obtain_dataframe(self, msisdn, print_out=True):
		'''
		Obtain the dataframe by MSISDN level.
		PARAMS: msisdn is the isdn to create the dataframe for
		 		meta_data is the name of the columns to add to dataframe
				print_out is boolean. If True, will print the output of this file into a csv file 
				loc of file is in class VAR folder, subfolder csv_logs
		OUTPUT: pandas dataframe indexed by the timestamp of the location
		'''

		msisdn_df=pd.DataFrame()

		assert msisdn in self.MSISDN.keys() 

		for log in self.MSISDN[msisdn]: 
			# load the file to memory
			f=open(log)
			try:
				data=json.load(f)
				f.close()

			except:
				print "Error loading json file %s" %log
				continue

			meta_data = data.keys()
			meta_data.remove('locations')

			#<TODO>: check if msisdn found in data is consistent with that found in the log file name

			try:
				df = pd.DataFrame.from_records(data['locations'], index='ts')

			except KeyError:
				print "timestamp not present in log_file %s" %log
				continue

			# Convert epoch time(index of the dataframe) to datetime.datetime format 
			df.index =  df.index.map(self.convert_epoch_time)

			#insert the other metadata
			for x in meta_data:
				df[x] = str(data[x])

			msisdn_df = msisdn_df.append(df)

		if print_out:
			self._convert_csv(msisdn_df, msisdn)

		else:
			pass

		return None



	def generate_summary(self):

		'''
		Generates the csv files for the VARS ISDNS
		'''

		for num in self.isdns:
			self.obtain_dataframe(num)

		return None





def main(folder, ISDN=[]):

	# main file for cobverting to csv file

	prep = Data_Prep(folder, isdns=ISDN)
	d = prep.generate_summary()



if __name__ == '__main__':


	parser = argparse.ArgumentParser()
	parser.add_argument("folder", type=str,
                    help="relative path of the folder which contains all the log file")
	parser.add_argument('-i', '--imsi', nargs='+', type=str, default =[], help="list of IMSIs to consider only")

	args = parser.parse_args()

	main(args.folder, ISDN=args.imsi)
	












