##############################################
# 01 - Loading libraries and packages
##############################################
import os
import pandas as pd

os.chdir('/indicator/src')

import tools.manage_files as mf
import tools.download as dl

import raw_data.fao as fao

##############################################
# 02 - Setting configuration
##############################################
print("02 - Setting configuration")
# Setting global parameters
root = "/indicator"
data_folder = os.path.join(root, "data")
conf_folder = os.path.join(data_folder, "conf")
# Inputs
inputs_folder = os.path.join(data_folder, "inputs")
inputs_f_downloads = os.path.join(inputs_folder, "01_downloads")
inputs_f_raw = os.path.join(inputs_folder, "02_raw")
# Logs
logs_folder = os.path.join(data_folder, "logs")

# Creating folders
print("Creating folders")
mf.mkdir(inputs_folder)
mf.mkdir(inputs_f_downloads)
mf.mkdir(inputs_f_raw)
mf.mkdir(logs_folder)

# Loading configurations
print("Loading configurations")
conf_xls = pd.ExcelFile(os.path.join(conf_folder,"conf.xlsx"))
conf_downloads = conf_xls.parse("downloads")
conf_metrics = conf_xls.parse("metrics")

countries_xls = pd.ExcelFile(os.path.join(conf_folder,"countries.xlsx"))
countries_list = countries_xls.parse("countries")
#crops = pd.read_csv(os.path.join(conf_folder, "crops.csv"), encoding = "UTF-8")

##############################################
# 03 - Downloading data from sources
##############################################
print("03 - Downloading data from sources")

# Getting data from faostat
print("Getting data from faostat")
conf_downloads["output"] = conf_downloads.apply(lambda x: dl.download_url(x.url, inputs_f_downloads), axis=1)


##############################################
# 04 - Processing downloaded data
##############################################
print("04 - Processing downloaded data")

# Processing fao data
fao_downloaded_files = conf_downloads.loc[conf_downloads["database"] == "fao","output"]
fao.create_workspace(inputs_f_raw)
fao.create_merge_countries(countries_list, fao_downloaded_files, inputs_f_raw)
#import raw_data.fao as fao
