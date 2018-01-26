#!/usr/bin/env python
# encoding=utf8
'''
    File name: set_time_to_gpx.py
    Description: set new date and time offset to a gpx file.
    Python Version: 2.7.13
'''
__author__ = "Alberto Andrés"
__license__ = "GPL"

filename='torija-prueba-recorrido-largo.gpx'

import re
import os

# New date to update 'YYYY-MM-DD'
gpx_date = '2017-09-15'
new_date = '2016-09-18'
# New time to add 'HH-MM-SS'
time_offset = '05-42-00'
# Add 0 or Subtract 1
operation = 1

fdr = open(filename, "r")
fdw = open(filename+'mod', "w")

file = fdr.read()
#new_file = file.replace(gpx_date, new_date)
#fdw.write(new_file)
fdw.write(file)

# Constants 
len_timetag_and_date_c = 16
len_time_c = 8

def time2secs(hh,mm,ss):

    segundostotales = (hh * 3600) + (mm * 60) + ss
    return segundostotales
    
def secs2hhmmss(segundostotales):

        hh = segundostotales // 3600
        mm = (segundostotales % 3600) // 60
        ss = (segundostotales %3600) % 60
        return hh,mm,ss

def replace( filePath, text, subs, flags=0 ):
    with open( filePath, "r+" ) as file:
        fileContents = file.read()
        textPattern = re.compile( re.escape( text ), flags )
        fileContents = textPattern.sub( subs, fileContents )
        file.seek( 0 )
        file.truncate()
        file.write( fileContents )

fdr.seek(0)
num_lines = len(fdr.readlines())
print num_lines
#num_lines = 20
fdr.seek(0)
fdw.seek(0)	

for i_line in range(1,num_lines-2):
	line = fdr.readline()
	if 'time' in line:
		offset_time = line.find('time')
		start_time  = offset_time + len_timetag_and_date_c
		end_time    = start_time + len_time_c
		time = str(line[start_time:end_time])

		#Get HH_MM_SS
		hh = int(time[0:2])
		mm = int(time[3:5])
		ss = int(time[6:8])
		
		#Get HH_MM_SS from new time to add
		new_hh = int(time_offset[0:2])
		new_mm = int(time_offset[3:5])
		new_ss = int(time_offset[6:8])

		# Calculate the new time:
		# Convert the time to seconds
		time_in_secs = time2secs(hh, mm, ss)
		new_time_in_secs = time2secs(new_hh, new_mm, new_ss)
		if operation == 0:
			# Sum the time with the new time
			time_in_secs = time_in_secs + new_time_in_secs
		else:
			# Sum the time with the new time
			time_in_secs = time_in_secs - new_time_in_secs
		
		# Convert the time in seconds to HH-MM-SS
		(hh,mm,ss) = secs2hhmmss(time_in_secs)
		new_time = str(hh).zfill(2) + ':' + str(mm).zfill(2) + ':' + str(ss).zfill(2)
		new_line = line.replace(time, new_time)
		replace(filename+'mod', line, new_line, 0)

fdw.close()
fdr.close()

# Update the date
fdr = open(filename+'mod', "r")
fdw = open(filename.rstrip('.gpx')+'_new.gpx', "w")

file = fdr.read()
new_file = file.replace(gpx_date, new_date)
fdw.write(new_file)

fdw.close()
fdr.close()

os.remove(filename+'mod')


