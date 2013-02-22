#!/usr/bin/env python

'''
SkyMap module

Auxiliary functions to plot the SkyMap
____________________________

This module is part of the PyASB project, 
created and maintained by Miguel Nievas [UCM].
____________________________
'''

__author__ = "Miguel Nievas"
__copyright__ = "Copyright 2012, PyASB project"
__credits__ = ["Miguel Nievas"]
__license__ = "GNU GPL v3"
__shortname__ = "PyASB"
__longname__ = "Python All-Sky Brightness pipeline"
__version__ = "1.99.0"
__maintainer__ = "Miguel Nievas"
__email__ = "miguelnr89[at]gmail[dot]com"
__status__ = "Prototype" # "Prototype", "Development", or "Production"

# NOTE: The following 2 functions should be moved to separate file or at least to a new class
# NOTE: Maybe should be rewrite as follows?:
# 1.) Create the file with the header
# 2.) Iterative add lines

class Summary():
	def __init__(self,Image,InputOptions,ImageAnalysis,InstrumentCalibration,ImageSkyBrightness):
		self.summarize_results(InputOptions, Image, ImageAnalysis,\
			InstrumentCalibration, ImageSkyBrightness)
		self.save_summary_to_file(Image.ImageInfo)

	def summarize_results(self,InputOptions, Image, ImageAnalysis,\
	InstrumentCalibration, ImageSkyBrightness):

		sum_date   = str(Image.ImageInfo.fits_date)
		sum_filter = str(Image.ImageInfo.used_filter)
		sum_stars  = str(InstrumentCalibration.BouguerFit.Regression.Nstars_initial)
		sum_gstars = str("%.1f"%float(InstrumentCalibration.BouguerFit.Regression.Nstars_rel))
		sum_zpoint = \
			str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.mean_zeropoint))+' +/- '+\
			str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.error_zeropoint))
		sum_extinction = \
			str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.extinction))+' +/- '+\
			str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.error_extinction))
		sum_skybrightness = \
			str("%.3f"%float(ImageSkyBrightness.SBzenith))+' +/- '+\
			str("%.3f"%float(ImageSkyBrightness.SBzenith_err))
			
		self.summary_content = \
			[sum_date, sum_filter,sum_stars, sum_gstars, \
			sum_zpoint, sum_extinction, sum_skybrightness]

	def save_summary_to_file(self,ImageInfo):
		try:
			assert(ImageInfo.summary_path!=False)
		except:
			print('Skipping write summary to file')
		else:
			print('Write summary to file')
			def summary_filename(ImageInfo):
				filename = ImageInfo.photometry_table_path +\
					"/Summary_"+ImageInfo.obs_name+"_"+ImageInfo.fits_date+"_"+\
					ImageInfo.used_filter+".txt"
				return(filename)
			
			photfile = open(summary_filename(ImageInfo),'w+')
			
			content = ['#Date, Filter, Stars, % Good Stars, ZeroPoint, Extinction, SkyBrightness\n']
			for line in self.summary_content:
				content_line = ""
				for element in line:
					content_line += element + ", "
				content_line += "\n"
				content.append(content_line)
			
			photfile.writelines(content)
			photfile.close()
		