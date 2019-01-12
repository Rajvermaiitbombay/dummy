__author__ = "Dhruv,Rajkumar"
__version__ = "VMA_version_0.4"
__maintainer__ = "Dhruv,Rajkumar"
__status__ = "Development,Production"

#-----------------------------Importing Libraries-----------------------------#
import os
os.chdir(os.path.dirname(__file__))
#wrk_dir = "E:\demo_tina"
#os.chdir(wrk_dir)
import random
#import urllib.parse
import pandas as pd
import numpy as np
import threading
import webbrowser 
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import flask
from flask import request,render_template
#from dash_flask_login import FlaskLoginAuth
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from flask import send_from_directory
import plotly.figure_factory as ff
import mysql.connector as sql
import datetime as dt
import smtplib
import dash_html_components as html
import dash_core_components as dcc
#import grasia_dash_components as gdc
from dash import Dash
#from flask_login import LoginManager, UserMixin, login_user, logout_user
#import dash
#import dash_renderer
#import flask_compress
#import plotly
#import dash_table_experiments as dtt
#import matplotlib.pyplot as plt
#import plotly.plotly as py
#from ipywidgets import widgets
#from IPython.display import display
#from plotly.widgets import GraphWidget
#from apps import app1
#-----------------------------------------------------------------------------#


from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:root@localhost/lsp_master_test',echo = False)
#-----creating empty dataframes to globalize variables for Flask usage--------#
rating=pd.read_excel('rating2.xlsx')
reviewfile=pd.read_excel('lspreview1.xlsx')
#lspoverview=pd.read_excel('client_LSP_sector0.2.xlsx')
new_metadata = pd.DataFrame()
contact_dataframe = pd.DataFrame()
contact = pd.DataFrame()
contact_info = pd.DataFrame()
manpower_dataframe = pd.DataFrame()
overall = pd.DataFrame()
overall1 = pd.DataFrame()
vehicle_dataframe = pd.DataFrame()
reference_dataframe = pd.DataFrame()
finance_dataframe = pd.DataFrame()
vehicle_count = pd.DataFrame()
lsp_unique_lanes = pd.DataFrame()
df_year_sector = pd.DataFrame()
manpower_transpose = pd.DataFrame()
m = pd.DataFrame()
all_options = dict()
lsp = dict()
state = dict()
total = list()
#-----------------------------------------------------------------------------#

#--------------------Getting Branch list and Lane data------------------------#
#cord1=pd.read_excel(r'Branch_list_LSP_v0.4.xlsx')
lane = pd.read_excel('lane_level_datav4.xlsx')
lane = lane.apply(lambda x: x.str.title() if(x.dtype==object) else x)
lane['LSP Name'] = lane['LSP Name'].str.upper()
lane['TruckType'] = lane['TruckType'].str.upper()

unique_lane_lsp = lane[['LSP Name','Country','Sector','OriginName','OriginLatitude','OriginLongitude','OriginState','OriginDirection','DestinationName','DestinationLatitude','DestinationLongitude','DestinationState','DestinationDirection']]
unique_lane_lsp = unique_lane_lsp.drop_duplicates()
count_lsps = round(len(lane['LSP Name'].unique()),0)

count_of_unique_lanes = len(unique_lane_lsp)
spend_sum_lsp = round(lane['Spend(Lakh)'].sum(),0)
volume_sum_lsp = round(lane['AnnualVolume'].sum(),0)

top_vol = lane.groupby('LSP Name')['AnnualVolume'].sum()
top_vol = top_vol.reset_index()
top_vol = top_vol.sort_values(by='AnnualVolume',ascending=0)

top_spend = lane.groupby('LSP Name')['Spend(Lakh)'].sum()
top_spend = top_spend.reset_index()
top_spend = top_spend.sort_values(by='Spend(Lakh)',ascending=0)

major_trucks = lane.groupby('TruckType')['Count'].sum()
major_trucks = major_trucks.reset_index()
count_of_trucks = len(pd.unique(major_trucks['TruckType']))
major_trucks = major_trucks.sort_values(by='Count',ascending=0)
major_trucks = major_trucks[~major_trucks.TruckType.str.contains("str")]


lane_analytics = lane[['OriginName','DestinationName','LSP Name','TruckType','Rate']]
lane = lane.drop_duplicates()
#-----------------------------------------------------------------------------#

#-------------------------Flask App starts from here--------------------------#
server = flask.Flask(__name__)

#@server.route('/log')
#def log():
#   return render_template('login.html')

@server.route('/upload')
def upload():
   return render_template('upload.html')

@server.route('/file', methods = ['GET','POST'])
def file():
    global new_metadata
    global contact_dataframe
    global vehicle_dataframe
    global reference_dataframe
    global finance_dataframe
    global vehicle_count
    global all_options
    global contact_info
    global contact
    global df_year_sector
    global lsp_unique_lanes
    global manpower_dataframe
    global overall
    global overall1
    global manpower_transpose
    global num_unique_lsps
    if request.method == 'POST' and request.files['myfile']:
        print(request.files['myfile'])
        f = request.files['myfile']
        import pandas as pd
        new_metadata = pd.read_excel(f)       
        new_metadata.to_excel('uploadedfile.xlsx')
        new_metadata.to_html('uploadedfile.html')
        
#------------------Changing name of columns for ease of use-------------------#

#        df = pd.read_excel('working_copy_2.xlsx')
#        new_metadata = df
#        new_metadata.rename(columns=lambda x: x.strip())
        new_metadata = df.rename(columns = {'IP':'IP',
                                                  'Submission ID':'Submission_ID',
                                                  'Submission Date':'Submission_Date',
                                                  'transporter_id':'Transporter_ID',
                                                  'a. Company Name':'lspName',
                                                  'b. Website URL (if available)':'website',
                                                  'c. E-mail(s) - separated by comma':'email',
                                                  'd. Headquarter Address':'hqAddress',
                                                  'e. Year of establishment':'yearEstablished',
                                                  'f. Specify if Company is Private/ Public':'companyType',
                                                  '2. Partner/Owner/Director details >> 1 >> Name of the Person':'personName1',
                                                  '2. Partner/Owner/Director details >> 1 >> Position Held in the Company':'designation1',
                                                  '2. Partner/Owner/Director details >> 1 >> Mobile Number':'mobileNo1',
                                                  '2. Partner/Owner/Director details >> 1 >> Phone Number':'phoneNo1',
                                                  '2. Partner/Owner/Director details >> 1 >> Email Address':'email1',
                                                  '2. Partner/Owner/Director details >> 2 >> Name of the Person':'personName2',
                                                  '2. Partner/Owner/Director details >> 2 >> Position Held in the Company':'designation2',                                                      
                                                  '2. Partner/Owner/Director details >> 2 >> Mobile Number':'mobileNo2',                                                      
                                                  '2. Partner/Owner/Director details >> 2 >> Phone Number':'phoneNo2',                                                      
                                                  '2. Partner/Owner/Director details >> 2 >> Email Address':'email2',
                                                  '2. Partner/Owner/Director details >> 3 >> Name of the Person':'personName3',
                                                  '2. Partner/Owner/Director details >> 3 >> Position Held in the Company':'designation3',
                                                  '2. Partner/Owner/Director details >> 3 >> Mobile Number':'mobileNo3',
                                                  '2. Partner/Owner/Director details >> 3 >> Phone Number':'phoneNo3',
                                                  '2. Partner/Owner/Director details >> 3 >> Email Address':'email3',                                                   
                                                  '2. Partner/Owner/Director details >> 4 >> Name of the Person':'personName4',
                                                  '2. Partner/Owner/Director details >> 4 >> Position Held in the Company':'designation4',
                                                  '2. Partner/Owner/Director details >> 4 >> Mobile Number':'mobileNo4',
                                                  '2. Partner/Owner/Director details >> 4 >> Phone Number':'phoneNo4',
                                                  '2. Partner/Owner/Director details >> 4 >> Email Address':'email4',
                                                  '3. Financials Of the Company >> Net Revenue >> 2014-15(INR Cr.)':'netRevenue_2014-15',
                                                  '3. Financials Of the Company >> Net Revenue >> 2015-16(INR Cr.)':'netRevenue_2015-16',
                                                  '3. Financials Of the Company >> Net Revenue >> 2016-17(INR Cr.)':'netRevenue_2016-17',
                                                  '3. Financials Of the Company >> Net Revenue >> 2017-18(INR Cr.)':'netRevenue_2017-18',
                                                  '3. Financials Of the Company >> Cost Of Operations >> 2014-15(INR Cr.)':'operatingCost_2014-15',
                                                  '3. Financials Of the Company >> Cost Of Operations >> 2015-16(INR Cr.)':'operatingCost_2015-16',
                                                  '3. Financials Of the Company >> Cost Of Operations >> 2016-17(INR Cr.)':'operatingCost_2016-17',
                                                  '3. Financials Of the Company >> Cost Of Operations >> 2017-18(INR Cr.)':'operatingCost_2017-18',
                                                  '3. Financials Of the Company >> Interest Payments >> 2014-15(INR Cr.)':'interestPayment_2014-15',
                                                  '3. Financials Of the Company >> Interest Payments >> 2015-16(INR Cr.)':'interestPayment_2015-16',
                                                  '3. Financials Of the Company >> Interest Payments >> 2016-17(INR Cr.)':'interestPayment_2016-17',
                                                  '3. Financials Of the Company >> Interest Payments >> 2017-18(INR Cr.)':'interestPayment_2017-18',
                                                  '3. Financials Of the Company >> Net Profit >> 2014-15(INR Cr.)':'netProfit_2014-15',
                                                  '3. Financials Of the Company >> Net Profit >> 2015-16(INR Cr.)':'netProfit_2015-16',
                                                  '3. Financials Of the Company >> Net Profit >> 2016-17(INR Cr.)':'netProfit_2016-17',
                                                  '3. Financials Of the Company >> Net Profit >> 2017-18(INR Cr.)':'netProfit_2017-18',
                                                  '3. Financials Of the Company >> Value Of Current Assets >> 2014-15(INR Cr.)':'currentAssets_2014-15',
                                                  '3. Financials Of the Company >> Value Of Current Assets >> 2015-16(INR Cr.)':'currentAssets_2015-16',
                                                  '3. Financials Of the Company >> Value Of Current Assets >> 2016-17(INR Cr.)':'currentAssets_2016-17',
                                                  '3. Financials Of the Company >> Value Of Current Assets >> 2017-18(INR Cr.)':'currentAssets_2017-18',
                                                  '3. Financials Of the Company >> Yearly TurnOver Of the Group >> 2014-15(INR Cr.)':'turnover_2014-15',
                                                  '3. Financials Of the Company >> Yearly TurnOver Of the Group >> 2015-16(INR Cr.)':'turnover_2015-16',
                                                  '3. Financials Of the Company >> Yearly TurnOver Of the Group >> 2016-17(INR Cr.)':'turnover_2016-17',
                                                  '3. Financials Of the Company >> Yearly TurnOver Of the Group >> 2017-18(INR Cr.)':'turnover_2017-18',
                                                  'a. Please attach Balance Sheet / Cash Flow Statement / Profit & Loss Statement if available':'balance_sheet_attachment',
                                                  'b. Are you Bank Approved?':'bankApproved',
                                                  'c. If Yes, Please provide name of the Bank(s) and Registration No.':'bankNameRegNo',
                                                  'd. Provide the limit of the bank guarantee you can provide to your customers (INR lakhs):':'bankGuarantee',
                                                  'f. Are you registered for Goods & Services Tax (GST)?':'gstRegistered',
                                                  'g. GST Registration Number (if registered)':'gstIN',
                                                  '4. Manpower Details >> Management Staff >> No. of employees':'management_cnt',
                                                  '4. Manpower Details >> Drivers >> No. of employees':'driver_cnt',
                                                  '4. Manpower Details >> Maintenance Staff >> No. of employees':'maintenance_cnt',
                                                  '5. Vehicle Information >> 16 MT >> No. of Self Owned':'16_MT_cnt_selfOwned',
                                                  '5. Vehicle Information >> 16 MT >> No. with GPS Units Installed':'16_MT_cnt_withGPS',
                                                  '5. Vehicle Information >> 16 MT >> Planned Increase In Self Owned Vehicles (Next 12 months)':'16_MT_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> 16 MT >> No. of Attached':'16_MT_cnt_numAttached',
                                                  '5. Vehicle Information >> 16 MT >> Name of Key Vendors providing Attached Vehicles':'16_MT_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 16 MT >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_16_MT_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> 21 / 24 / 27 MT >> No. of Self Owned':'21_24_27MT_cnt_selfOwned',
                                                  '5. Vehicle Information >> 21 / 24 / 27 MT >> No. with GPS Units Installed':'21_24_27_MT_cnt_withGPS',
                                                  '5. Vehicle Information >> 21 / 24 / 27 MT >> Planned Increase In Self Owned Vehicles (Next 12 months)':'21_24_27_MT_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> 21 / 24 / 27 MT >> No. of Attached':'21_24_27_MT_cnt_numAttached',
                                                  '5. Vehicle Information >> 21 / 24 / 27 MT >> Name of Key Vendors providing Attached Vehicles':'21_24_27_MT_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 21 / 24 / 27 MT >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_21_24_27_MT_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> Trailers (specify type of trailer) >> No. of Self Owned':'Trailers_specify_type_of_trailer_cnt_selfOwned',
                                                  '5. Vehicle Information >> Trailers (specify type of trailer) >> No. with GPS Units Installed':'Trailers_specify_type_of_trailer_cnt_withGPS',
                                                  '5. Vehicle Information >> Trailers (specify type of trailer) >> Planned Increase In Self Owned Vehicles (Next 12 months)':'Trailers_specify_type_of_trailer_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> Trailers (specify type of trailer) >> No. of Attached':'Trailers_specify_type_of_trailer_cnt_numAttached',
                                                  '5. Vehicle Information >> Trailers (specify type of trailer) >> Name of Key Vendors providing Attached Vehicles':'Trailers_specify_type_of_trailer_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> Trailers (specify type of trailer) >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_Trailer_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> 9 MT >> No. of Self Owned':'9_MT_cnt_selfOwned',
                                                  '5. Vehicle Information >> 9 MT >> No. with GPS Units Installed':'9_MT_cnt_withGPS',
                                                  '5. Vehicle Information >> 9 MT >> Planned Increase In Self Owned Vehicles (Next 12 months)':'9_MT_incSelfOwn',
                                                  '5. Vehicle Information >> 9 MT >> No. of Attached':'9_MT_cnt_numAttached',
                                                  '5. Vehicle Information >> 9 MT >> Name of Key Vendors providing Attached Vehicles':'9_MT_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 9 MT >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_9_MT_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> 32ft single axle (closed body container) >> No. of Self Owned':'32ft_single_axle_closed_body_container_cnt_selfOwned',
                                                  '5. Vehicle Information >> 32ft single axle (closed body container) >> No. with GPS Units Installed':'32ft_single_axle_closed_body_container_cnt_withGPS',
                                                  '5. Vehicle Information >> 32ft single axle (closed body container) >> Planned Increase In Self Owned Vehicles (Next 12 months)':'32ft_single_axle_closed_body_container_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> 32ft single axle (closed body container) >> No. of Attached':'32ft_single_axle_closed_body_container_cnt_numAttached',
                                                  '5. Vehicle Information >> 32ft single axle (closed body container) >> Name of Key Vendors providing Attached Vehicles':'32ft_single_axle_closed_body_container_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 32ft single axle (closed body container) >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_32FT_singleAxle_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> 32ft multi axle (closed body container) >> No. of Self Owned':'32ft_multi_axle_closed_bodycontainer_cnt_selfOwned',
                                                  '5. Vehicle Information >> 32ft multi axle (closed body container) >> No. with GPS Units Installed':'32ft_multi_axle_closed_bodycontainer_cnt_withGPS',
                                                  '5. Vehicle Information >> 32ft multi axle (closed body container) >> Planned Increase In Self Owned Vehicles (Next 12 months)':'32ft_multi_axle_closed_bodycontainer_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> 32ft multi axle (closed body container) >> No. of Attached':'32ft_multi_axle_closed_bodycontainer_cnt_numAttached',
                                                  '5. Vehicle Information >> 32ft multi axle (closed body container) >> Name of Key Vendors providing Attached Vehicles':'32ft_multi_axle_closed_bodycontainer_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 32ft multi axle (closed body container) >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_32FT_multiAxle_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> 7.5 MT >> No. of Self Owned':'7.5_MT_cnt_selfOwned',
                                                  '5. Vehicle Information >> 7.5 MT >> No. with GPS Units Installed':'7.5_MT_cnt_withGPS',
                                                  '5. Vehicle Information >> 7.5 MT >> Planned Increase In Self Owned Vehicles (Next 12 months)':'7.5_MT_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> 7.5 MT >> No. of Attached':'7.5_MT_cnt_numAttached',
                                                  '5. Vehicle Information >> 7.5 MT >> Name of Key Vendors providing Attached Vehicles':'7.5_MT_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 7.5 MT >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_7.5_MT_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> 6 MT >> No. of Self Owned':'6_MT_cnt_selfOwned',
                                                  '5. Vehicle Information >> 6 MT >> No. with GPS Units Installed':'6_MT_cnt_withGPS',
                                                  '5. Vehicle Information >> 6 MT >> Planned Increase In Self Owned Vehicles (Next 12 months)':'6_MT_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> 6 MT >> No. of Attached':'6_MT_cnt_numAttached',
                                                  '5. Vehicle Information >> 6 MT >> Name of Key Vendors providing Attached Vehicles':'6_MT_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> 6 MT >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_6_MT_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> Smaller types of trucks (< 6 MT) >> No. of Self Owned':'Smaller_types_of_trucks_<_6_MT_cnt_selfOwned',
                                                  '5. Vehicle Information >> Smaller types of trucks (< 6 MT) >> No. with GPS Units Installed':'Smaller_types_of_trucks_<_6_MT_cnt_withGPS',
                                                  '5. Vehicle Information >> Smaller types of trucks (< 6 MT) >> Planned Increase In Self Owned Vehicles (Next 12 months)':'Smaller_types_of_trucks_<_6_MT_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> Smaller types of trucks (< 6 MT) >> No. of Attached':'Smaller_types_of_trucks_<_6_MT_cnt_numAttached',
                                                  '5. Vehicle Information >> Smaller types of trucks (< 6 MT) >> Name of Key Vendors providing Attached Vehicles':'Smaller_types_of_trucks_<_6_MT_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> Smaller types of trucks (< 6 MT) >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_smallerThan_6_MT_fleet_with_RC_updated',
                                                  '5. Vehicle Information >> Other Truck Types >> No. of Self Owned':'Other_Truck_Types_cnt_selfOwned',
                                                  '5. Vehicle Information >> Other Truck Types >> No. with GPS Units Installed':'Other_Truck_Types_cnt_withGPS',
                                                  '5. Vehicle Information >> Other Truck Types >> Planned Increase In Self Owned Vehicles (Next 12 months)':'Other_Truck_Types_cnt_incSelfOwn',
                                                  '5. Vehicle Information >> Other Truck Types >> No. of Attached':'Other_Truck_Types_cnt_numAttached',
                                                  '5. Vehicle Information >> Other Truck Types >> Name of Key Vendors providing Attached Vehicles':'Other_Truck_Types_cnt_keyVendorProvider',
                                                  '5. Vehicle Information >> Other Truck Types >> % of Fleet with RC Book updated (as per new Axle Load norms)':'%_otherTruck_fleet_with_RC_updated',
                                                  'a. Please provide list of owned vehicles along with registration numbers if available':'list_of_owned_vehicles',
                                                  '6. Shipment Tracking Methods >> 1 >> Methods Used':'method_1',
                                                  '6. Shipment Tracking Methods >> 1 >> Details of methods used to track shipments':'details1',
                                                  '6. Shipment Tracking Methods >> 1 >> Name your Technology platform/GPS Service Provider(s) used t...':'techUsed1',
                                                  '6. Shipment Tracking Methods >> 2 >> Methods Used':'method_2',
                                                  '6. Shipment Tracking Methods >> 2 >> Details of methods used to track shipments':'details2',
                                                  '6. Shipment Tracking Methods >> 2 >> Name your Technology platform/GPS Service Provider(s) used t...':'techUsed2',
                                                  '6. Shipment Tracking Methods >> 3 >> Methods Used':'method_3',
                                                  '6. Shipment Tracking Methods >> 3 >> Details of methods used to track shipments':'details3',
                                                  '6. Shipment Tracking Methods >> 3 >> Name your Technology platform/GPS Service Provider(s) used t...':'techUsed3',
                                                  "7. Do you provide customers with management reports like 'on time delivery'?":'mgmtReportTypes',
                                                  '8.a Top Clientele information >> 1 >> Name of the client':'clientName1',
                                                  '8.a Top Clientele information >> 1 >> Industry of the client':'industry1',
                                                  '8.a Top Clientele information >> 1 >> Value of freight (INR Cr. per annum)':'freightValue1',
                                                  '8.a Top Clientele information >> 1 >> % of your total business':'percentOfBusiness1',
                                                  '8.a Top Clientele information >> 1 >> No. of Trucks per month':'trucksPerMonth1',
                                                  '8.a Top Clientele information >> 1 >> Product type':'productType1',
                                                  '8.a Top Clientele information >> 1 >> Multi-modal (Specify Mode)':'otherModes1',
                                                  '8.a Top Clientele information >> 2 >> Name of the client':'clientName2',
                                                  '8.a Top Clientele information >> 2 >> Industry of the client':'industry2',
                                                  '8.a Top Clientele information >> 2 >> Value of freight (INR Cr. per annum)':'freightValue2',
                                                  '8.a Top Clientele information >> 2 >> % of your total business':'percentOfBusiness2',
                                                  '8.a Top Clientele information >> 2 >> No. of Trucks per month':'trucksPerMonth2',
                                                  '8.a Top Clientele information >> 2 >> Product type':'productType2',
                                                  '8.a Top Clientele information >> 2 >> Multi-modal (Specify Mode)':'otherModes2',
                                                  '8.a Top Clientele information >> 3 >> Name of the client':'clientName3',
                                                  '8.a Top Clientele information >> 3 >> Industry of the client':'industry3',
                                                  '8.a Top Clientele information >> 3 >> Value of freight (INR Cr. per annum)':'freightValue3',
                                                  '8.a Top Clientele information >> 3 >> % of your total business':'percentOfBusiness3',
                                                  '8.a Top Clientele information >> 3 >> No. of Trucks per month':'trucksPerMonth3',
                                                  '8.a Top Clientele information >> 3 >> Product type':'productType3',
                                                  '8.a Top Clientele information >> 3 >> Multi-modal (Specify Mode)':'otherModes3',
                                                  '8.a Top Clientele information >> 4 >> Name of the client':'clientName4',
                                                  '8.a Top Clientele information >> 4 >> Industry of the client':'industry4',
                                                  '8.a Top Clientele information >> 4 >> Value of freight (INR Cr. per annum)':'freightValue4',
                                                  '8.a Top Clientele information >> 4 >> % of your total business':'percentOfBusiness4',
                                                  '8.a Top Clientele information >> 4 >> No. of Trucks per month':'trucksPerMonth4',
                                                  '8.a Top Clientele information >> 4 >> Product type':'productType4',
                                                  '8.a Top Clientele information >> 4 >> Multi-modal (Specify Mode)':'otherModes4',
                                                  '8.a Top Clientele information >> 5 >> Name of the client':'clientName5',
                                                  '8.a Top Clientele information >> 5 >> Industry of the client':'industry5',
                                                  '8.a Top Clientele information >> 5 >> Value of freight (INR Cr. per annum)':'freightValue5',
                                                  '8.a Top Clientele information >> 5 >> % of your total business':'percentOfBusiness5',
                                                  '8.a Top Clientele information >> 5 >> No. of Trucks per month':'trucksPerMonth5',
                                                  '8.a Top Clientele information >> 5 >> Product type':'productType5',
                                                  '8.a Top Clientele information >> 5 >> Multi-modal (Specify Mode)':'otherModes5',
                                                  '8.a Top Clientele information >> 6 >> Name of the client':'clientName6',
                                                  '8.a Top Clientele information >> 6 >> Industry of the client':'industry6',
                                                  '8.a Top Clientele information >> 6 >> Value of freight (INR Cr. per annum)':'freightValue6',
                                                  '8.a Top Clientele information >> 6 >> % of your total business':'percentOfBusiness6',
                                                  '8.a Top Clientele information >> 6 >> No. of Trucks per month':'trucksPerMonth6',
                                                  '8.a Top Clientele information >> 6 >> Product type':'productType6',
                                                  '8.a Top Clientele information >> 6 >> Multi-modal (Specify Mode)':'otherModes6',
                                                  '8.a Top Clientele information >> 7 >> Name of the client':'clientName7',
                                                  '8.a Top Clientele information >> 7 >> Industry of the client':'industry7',
                                                  '8.a Top Clientele information >> 7 >> Value of freight (INR Cr. per annum)':'freightValue7',
                                                  '8.a Top Clientele information >> 7 >> % of your total business':'percentOfBusiness7',
                                                  '8.a Top Clientele information >> 7 >> No. of Trucks per month':'trucksPerMonth7',
                                                  '8.a Top Clientele information >> 7 >> Product type':'productType7',
                                                  '8.a Top Clientele information >> 7 >> Multi-modal (Specify Mode)':'otherModes7',
                                                  '8.a Top Clientele information >> 8 >> Name of the client':'clientName8',
                                                  '8.a Top Clientele information >> 8 >> Industry of the client':'industry8',
                                                  '8.a Top Clientele information >> 8 >> Value of freight (INR Cr. per annum)':'freightValue8',
                                                  '8.a Top Clientele information >> 8 >> % of your total business':'percentOfBusiness8',
                                                  '8.a Top Clientele information >> 8 >> No. of Trucks per month':'trucksPerMonth8',
                                                  '8.a Top Clientele information >> 8 >> Product type':'productType8',
                                                  '8.a Top Clientele information >> 8 >> Multi-modal (Specify Mode)':'otherModes8',
                                                  '8.a Top Clientele information >> 9 >> Name of the client':'clientName9',
                                                  '8.a Top Clientele information >> 9 >> Industry of the client':'industry9',
                                                  '8.a Top Clientele information >> 9 >> Value of freight (INR Cr. per annum)':'freightValue9',
                                                  '8.a Top Clientele information >> 9 >> % of your total business':'percentOfBusiness9',
                                                  '8.a Top Clientele information >> 9 >> No. of Trucks per month':'trucksPerMonth9',
                                                  '8.a Top Clientele information >> 9 >> Product type':'productType9',
                                                  '8.a Top Clientele information >> 9 >> Multi-modal (Specify Mode)':'otherModes9',
                                                  '8.a Top Clientele information >> 10 >> Name of the client':'clientName10',
                                                  '8.a Top Clientele information >> 10 >> Industry of the client':'industry10',
                                                  '8.a Top Clientele information >> 10 >> Value of freight (INR Cr. per annum)':'freightValue10',
                                                  '8.a Top Clientele information >> 10 >> % of your total business':'percentOfBusiness10',
                                                  '8.a Top Clientele information >> 10 >> No. of Trucks per month':'trucksPerMonth10',
                                                  '8.a Top Clientele information >> 10 >> Product type':'productType10',
                                                  '8.a Top Clientele information >> 10 >> Multi-modal (Specify Mode)':'otherModes10',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 1 >> Client Name':'clientRef1',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 1 >> Name & Designation of point of contact':'contactName1',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 1 >> Phone No.':'contactPhone1',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 1 >> Email Id.':'contactEmail1',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 2 >> Client Name':'clientRef2',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 2 >> Name & Designation of point of contact':'contactName2',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 2 >> Phone No.':'contactPhone2',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 2 >> Email Id.':'contactEmail2',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 3 >> Client Name':'clientRef3',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 3 >> Name & Designation of point of contact':'contactName3',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 3 >> Phone No.':'contactPhone3',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 3 >> Email Id.':'contactEmail3',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 4 >> Client Name':'clientRef4',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 4 >> Name & Designation of point of contact':'contactName4',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 4 >> Phone No.':'contactPhone4',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 4 >> Email Id.':'contactEmail4',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 5 >> Client Name':'clientRef5',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 5 >> Name & Designation of point of contact':'contactName5',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 5 >> Phone No.':'contactPhone5',
                                                  '8.b References (Please Note: 5 references are mandatory) >> 5 >> Email Id.':'contactEmail5',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 1 >> Name of the Company':'companyName1',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 1 >> Plants/ Dispatch Locations':'location1',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 2 >> Name of the Company':'companyName2',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 2 >> Plants/ Dispatch Locations':'location2',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 3 >> Name of the Company':'companyName3',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 3 >> Plants/ Dispatch Locations':'location3',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 4 >> Name of the Company':'companyName4',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 4 >> Plants/ Dispatch Locations':'location4',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 5 >> Name of the Company':'companyName5',
                                                  '8.c. Please list top 5 companies you wish to get business fr... >> 5 >> Plants/ Dispatch Locations':'location5',
                                                  '8.d If there are any other companies you would like to work with please list them here ( press the + sign to add companies)':'other_companies_interested',
                                                  '9. Please attach the list of all the lanes that you are currently operating on ( use template attached in the email)':'lane_attachment',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 1 >> Origin':'origin1',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 1 >> Destination':'destination1',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 1 >> Truck type':'truckType1',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 1 >> Your current rate':'currentRate1',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 2 >> Origin':'origin2',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 2 >> Destination':'destination2',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 2 >> Truck type':'truckType2',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 2 >> Your current rate':'currentRate2',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 3 >> Origin':'origin3',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 3 >> Destination':'destination3',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 3 >> Truck type':'truckType3',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 3 >> Your current rate':'currentRate3',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 4 >> Origin':'origin4',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 4 >> Destination':'destination4',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 4 >> Truck type':'truckType4',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 4 >> Your current rate':'currentRate4',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 5 >> Origin':'origin5',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 5 >> Destination':'destination5',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 5 >> Truck type':'truckType5',
                                                  '9.a Please list top 5 routes you require return loads/ backh... >> 5 >> Your current rate':'currentRate5',
                                                  '9.b Please list any additional routes for which you require return loads/ Backhaul ( press the + sign to add the lanes ).  Please mention the Origin, Destination ,Truck type and your current rate':'additional_backhaul',
                                                  '10. Please attach company presentation / brochure if available':'attachmentLink',
                                                  '11. Please let us know if the below listed services provided by our partners is of interes... >> (a) Trial Loads with companies you wish to get business from':'Trial_load_from_company',
                                                  '11. Please let us know if the below listed services provided by our partners is of interes... >> (b) Participate in transporter award/incentives programme':'Award_incentive_programme',
                                                  '11. Please let us know if the below listed services provided by our partners is of interes... >> (c) Participate in transporter rating programme to increase future business prospects':'Future_business_prospects',
                                                  '12. Please select your key focus areas in logistics':'keyFocusAreas',
                                                  '13. Would you like us to contact you for further details regarding the services you are interested in?':'contactedFurther',
                                                  })
        
#--Adding Year,stripping lsp name and converting submission date to dataframe--# 
        new_metadata['Submission_Date'] = pd.to_datetime(new_metadata['Submission_Date'])           
        new_metadata['year'] = new_metadata['Submission_Date'].dt.year
        new_metadata['lspName'] = new_metadata['lspName'].str.strip()
        new_metadata['Submission_Date'] = new_metadata['Submission_Date'].dt.date
#        all_option = {k: g["lspName"].tolist() for k,g in new_metadata.groupby("year")}
        new_metadata = new_metadata.fillna(0)
        new_metadata = new_metadata.replace('str',0)
        #----------------------------------Data Restructuring-------------------------#
            
        #new_metadata['netRevenue_2014-15'] = new_metadata['netRevenue_2014-15'].str.extract('(\d+)').astype(int)
            
        #changing strings to integer
        
        new_metadata['16_MT_cnt_selfOwned'] = new_metadata['16_MT_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['16_MT_cnt_selfOwned'] = new_metadata['16_MT_cnt_selfOwned'].fillna(0)
        
        new_metadata['16_MT_cnt_numAttached'] = new_metadata['16_MT_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['16_MT_cnt_numAttached'] = new_metadata['16_MT_cnt_numAttached'].fillna(0)
        
        new_metadata['21_24_27MT_cnt_selfOwned'] = new_metadata['21_24_27MT_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['21_24_27MT_cnt_selfOwned'] = new_metadata['21_24_27MT_cnt_selfOwned'].fillna(0)
        
        new_metadata['21_24_27_MT_cnt_numAttached'] = new_metadata['21_24_27_MT_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['21_24_27_MT_cnt_numAttached'] = new_metadata['21_24_27_MT_cnt_numAttached'].fillna(0)
        
        new_metadata['Trailers_specify_type_of_trailer_cnt_selfOwned'] = new_metadata['Trailers_specify_type_of_trailer_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['Trailers_specify_type_of_trailer_cnt_selfOwned'] = new_metadata['Trailers_specify_type_of_trailer_cnt_selfOwned'].fillna(0)
        
        new_metadata['Trailers_specify_type_of_trailer_cnt_numAttached'] = new_metadata['Trailers_specify_type_of_trailer_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['Trailers_specify_type_of_trailer_cnt_numAttached'] = new_metadata['Trailers_specify_type_of_trailer_cnt_numAttached'].fillna(0)
        
        new_metadata['9_MT_cnt_selfOwned'] = new_metadata['9_MT_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['9_MT_cnt_selfOwned'] = new_metadata['9_MT_cnt_selfOwned'].fillna(0)
        
        new_metadata['9_MT_cnt_numAttached'] = new_metadata['9_MT_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['9_MT_cnt_numAttached'] = new_metadata['9_MT_cnt_numAttached'].fillna(0)
        
        new_metadata['32ft_single_axle_closed_body_container_cnt_selfOwned'] = new_metadata['32ft_single_axle_closed_body_container_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['32ft_single_axle_closed_body_container_cnt_selfOwned'] = new_metadata['32ft_single_axle_closed_body_container_cnt_selfOwned'].fillna(0)
        
        new_metadata['32ft_single_axle_closed_body_container_cnt_numAttached'] = new_metadata['32ft_single_axle_closed_body_container_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['32ft_single_axle_closed_body_container_cnt_numAttached'] = new_metadata['32ft_single_axle_closed_body_container_cnt_numAttached'].fillna(0)
        
        new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_selfOwned'] = new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_selfOwned'] = new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_selfOwned'].fillna(0)
        
        new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_numAttached'] = new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_numAttached'] = new_metadata['32ft_multi_axle_closed_bodycontainer_cnt_numAttached'].fillna(0)
        
        new_metadata['7.5_MT_cnt_selfOwned'] = new_metadata['7.5_MT_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['7.5_MT_cnt_selfOwned'] = new_metadata['7.5_MT_cnt_selfOwned'].fillna(0)
        
        new_metadata['7.5_MT_cnt_numAttached'] = new_metadata['7.5_MT_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['7.5_MT_cnt_numAttached'] = new_metadata['7.5_MT_cnt_numAttached'].fillna(0)
        
        new_metadata['6_MT_cnt_selfOwned'] = new_metadata['6_MT_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['6_MT_cnt_selfOwned'] = new_metadata['6_MT_cnt_selfOwned'].fillna(0)
        
        new_metadata['6_MT_cnt_numAttached'] = new_metadata['6_MT_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['6_MT_cnt_numAttached'] = new_metadata['6_MT_cnt_numAttached'].fillna(0)
        
        new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_selfOwned'] = new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_selfOwned'] = new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_selfOwned'].fillna(0)
        
        new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_numAttached'] = new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_numAttached'] = new_metadata['Smaller_types_of_trucks_<_6_MT_cnt_numAttached'].fillna(0)
        
        new_metadata['Other_Truck_Types_cnt_selfOwned'] = new_metadata['Other_Truck_Types_cnt_selfOwned'].convert_objects(convert_numeric = True)
        new_metadata['Other_Truck_Types_cnt_selfOwned'] = new_metadata['Other_Truck_Types_cnt_selfOwned'].fillna(0)
        
        new_metadata['Other_Truck_Types_cnt_numAttached'] = new_metadata['Other_Truck_Types_cnt_numAttached'].convert_objects(convert_numeric = True)
        new_metadata['Other_Truck_Types_cnt_numAttached'] = new_metadata['Other_Truck_Types_cnt_numAttached'].fillna(0)
        
        new_metadata['management_cnt'] = new_metadata['management_cnt'].convert_objects(convert_numeric = True)
        new_metadata['management_cnt'] = new_metadata['management_cnt'].fillna(0)
        
        new_metadata['driver_cnt'] = new_metadata['driver_cnt'].convert_objects(convert_numeric = True)
        new_metadata['driver_cnt'] = new_metadata['driver_cnt'].fillna(0)
        
        new_metadata['maintenance_cnt'] = new_metadata['maintenance_cnt'].convert_objects(convert_numeric = True)
        new_metadata['maintenance_cnt'] = new_metadata['maintenance_cnt'].fillna(0)
        
        #new_metadata['16_MT_cnt_selfOwned'] = new_metadata['16_MT_cnt_selfOwned'].str.extract('(\d+)').astype(int)
        
        #----------------------------------My SQL Dump--------------------------------#
        company_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year','website','email','companyType','keyFocusAreas']]
        contact_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year','yearEstablished','personName1','designation1','mobileNo1','phoneNo1','email1',
                                                            'personName2','designation2','mobileNo2','phoneNo2','email2',
                                                            'personName3','designation3','mobileNo3','phoneNo3','email3',
                                                            'personName4','designation4','mobileNo4','phoneNo4','email4']]
        
        finance_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year','bankApproved','bankNameRegNo','bankGuarantee','gstRegistered','gstIN','netRevenue_2014-15','netRevenue_2015-16','netRevenue_2016-17','netRevenue_2017-18',
                                                            'operatingCost_2014-15','operatingCost_2015-16','operatingCost_2016-17','operatingCost_2017-18',
                                                            'interestPayment_2014-15','interestPayment_2015-16','interestPayment_2016-17','interestPayment_2017-18',
                                                            'netProfit_2014-15','netProfit_2015-16','netProfit_2016-17','netProfit_2017-18',
                                                            'currentAssets_2014-15','currentAssets_2015-16','currentAssets_2016-17','currentAssets_2017-18',
                                                            'turnover_2014-15','turnover_2015-16','turnover_2016-17','turnover_2017-18']]
        
        financial_details = new_metadata[['Transporter_ID','Submission_Date','lspName','year','bankApproved','bankNameRegNo','bankGuarantee','gstRegistered','gstIN']]
        
        manpower_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year','management_cnt','driver_cnt','maintenance_cnt']]
        
        vehicle_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year','16_MT_cnt_selfOwned','16_MT_cnt_withGPS','16_MT_cnt_incSelfOwn','16_MT_cnt_numAttached','16_MT_cnt_keyVendorProvider','%_16_MT_fleet_with_RC_updated',
                                                            '21_24_27MT_cnt_selfOwned','21_24_27_MT_cnt_withGPS','21_24_27_MT_cnt_incSelfOwn','21_24_27_MT_cnt_numAttached','21_24_27_MT_cnt_keyVendorProvider','%_21_24_27_MT_fleet_with_RC_updated',
                                                            'Trailers_specify_type_of_trailer_cnt_selfOwned','Trailers_specify_type_of_trailer_cnt_withGPS','Trailers_specify_type_of_trailer_cnt_incSelfOwn','Trailers_specify_type_of_trailer_cnt_numAttached','Trailers_specify_type_of_trailer_cnt_keyVendorProvider','%_Trailer_fleet_with_RC_updated',
                                                            '9_MT_cnt_selfOwned','9_MT_cnt_withGPS','9_MT_incSelfOwn','9_MT_cnt_numAttached','9_MT_cnt_keyVendorProvider','%_9_MT_fleet_with_RC_updated',
                                                            '32ft_single_axle_closed_body_container_cnt_selfOwned','32ft_single_axle_closed_body_container_cnt_withGPS','32ft_single_axle_closed_body_container_cnt_incSelfOwn','32ft_single_axle_closed_body_container_cnt_numAttached','32ft_single_axle_closed_body_container_cnt_keyVendorProvider','%_32FT_singleAxle_fleet_with_RC_updated',
                                                            '32ft_multi_axle_closed_bodycontainer_cnt_selfOwned','32ft_multi_axle_closed_bodycontainer_cnt_withGPS','32ft_multi_axle_closed_bodycontainer_cnt_incSelfOwn','32ft_multi_axle_closed_bodycontainer_cnt_numAttached','32ft_multi_axle_closed_bodycontainer_cnt_keyVendorProvider','%_32FT_multiAxle_fleet_with_RC_updated',
                                                            '7.5_MT_cnt_selfOwned','7.5_MT_cnt_withGPS','7.5_MT_cnt_incSelfOwn','7.5_MT_cnt_numAttached','7.5_MT_cnt_keyVendorProvider','%_7.5_MT_fleet_with_RC_updated',
                                                            '6_MT_cnt_selfOwned','6_MT_cnt_withGPS','6_MT_cnt_incSelfOwn','6_MT_cnt_numAttached','6_MT_cnt_keyVendorProvider','%_6_MT_fleet_with_RC_updated',
                                                            'Smaller_types_of_trucks_<_6_MT_cnt_selfOwned','Smaller_types_of_trucks_<_6_MT_cnt_withGPS','Smaller_types_of_trucks_<_6_MT_cnt_incSelfOwn','Smaller_types_of_trucks_<_6_MT_cnt_numAttached','Smaller_types_of_trucks_<_6_MT_cnt_keyVendorProvider','%_smallerThan_6_MT_fleet_with_RC_updated',
                                                            'Other_Truck_Types_cnt_selfOwned','Other_Truck_Types_cnt_withGPS','Other_Truck_Types_cnt_incSelfOwn','Other_Truck_Types_cnt_numAttached','Other_Truck_Types_cnt_keyVendorProvider','%_otherTruck_fleet_with_RC_updated','list_of_owned_vehicles']]
         
#        a = new_metadata[['16_MT_cnt_selfOwned']]
#        a.to_sql(name='a',con=engine,if_exists='append',index=False)
         
        ship_track_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'method_1','details1','techUsed1',
                                                               'method_2','details2','techUsed2',
                                                               'method_3','details3','techUsed3','mgmtReportTypes','list_of_owned_vehicles']]
        
        top_clientelle_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'clientName1','industry1','freightValue1','percentOfBusiness1','trucksPerMonth1','productType1','otherModes1',
                                                                   'clientName2','industry2','freightValue2','percentOfBusiness2','trucksPerMonth2','productType2','otherModes2',
                                                                   'clientName3','industry3','freightValue3','percentOfBusiness3','trucksPerMonth3','productType3','otherModes3',
                                                                   'clientName4','industry4','freightValue4','percentOfBusiness4','trucksPerMonth4','productType4','otherModes4',
                                                                   'clientName5','industry5','freightValue5','percentOfBusiness5','trucksPerMonth5','productType5','otherModes5',
                                                                   'clientName6','industry6','freightValue6','percentOfBusiness6','trucksPerMonth6','productType6','otherModes6',
                                                                   'clientName7','industry7','freightValue7','percentOfBusiness7','trucksPerMonth7','productType7','otherModes7',
                                                                   'clientName8','industry8','freightValue8','percentOfBusiness8','trucksPerMonth8','productType8','otherModes8',
                                                                   'clientName9','industry9','freightValue9','percentOfBusiness9','trucksPerMonth9','productType9','otherModes9',
                                                                   'clientName10','industry10','freightValue10','percentOfBusiness10','trucksPerMonth10','productType10','otherModes10']]
        
        references_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'clientRef1','contactName1','contactPhone1','contactEmail1',
                                                               'clientRef2','contactName2','contactPhone2','contactEmail2',
                                                               'clientRef3','contactName3','contactPhone3','contactEmail3',
                                                               'clientRef4','contactName4','contactPhone4','contactEmail4',
                                                               'clientRef5','contactName5','contactPhone5','contactEmail5']]
        
        top_5_cmp_business_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'companyName1','location1',
                                                                       'companyName2','location2',
                                                                       'companyName3','location3',
                                                                       'companyName4','location4',
                                                                       'companyName5','location5','other_companies_interested','lane_attachment']]
        
        backhaul_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'origin1','destination1','truckType1','currentRate1',
                                                             'origin2','destination2','truckType2','currentRate2',
                                                             'origin3','destination3','truckType3','currentRate3',
                                                             'origin4','destination4','truckType4','currentRate4',
                                                             'origin5','destination5','truckType5','currentRate5','additional_backhaul','attachmentLink']]
        
        interests_info = new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'Trial_load_from_company','Award_incentive_programme','Future_business_prospects','keyFocusAreas','contactedFurther']]
        
        address_info =  new_metadata[['Transporter_ID','Submission_Date','lspName','year', 'hqAddress','City','State','Pincode']]
        
        #filled NAs with 0
        from sqlalchemy import create_engine
        import mysql.connector as sql
        
        engine = create_engine('mysql+mysqlconnector://root:root@localhost/lsp_master_test',echo = False)
        
        company_info.to_sql(name='company_info',con=engine,if_exists='append',index=False)
        financial_details.to_sql(name='financial_details',con=engine,if_exists='append',index=False)
        contact_info.to_sql(name='contact_info',con=engine,if_exists='append',index=False)
        finance_info.to_sql(name='finance_info',con=engine,if_exists='append',index=False)
        manpower_info.to_sql(name='manpower_info',con=engine,if_exists='append',index=False)
        vehicle_info.to_sql(name='vehicle_info',con=engine,if_exists='append',index=False)
        ship_track_info.to_sql(name='ship_track_info',con=engine,if_exists='append',index=False)
        top_clientelle_info.to_sql(name= 'top_clientelle_info',con=engine,if_exists='append',index=False)
        references_info.to_sql(name='references_info',con=engine,if_exists='append',index=False)
        top_5_cmp_business_info.to_sql(name='top_5_cmp_business_info',con=engine,if_exists='append',index=False)
        backhaul_info.to_sql(name='backhaul_info',con=engine,if_exists='append',index=False)
        interests_info.to_sql(name='interests_info',con=engine,if_exists='append',index=False)
        address_info.to_sql(name='address_info',con=engine,if_exists='append',index=False)
#        cord1 = pd.read_excel(r'Branch_list_LSP_v0.4.xlsx')
#        cord1.to_sql(name = 'branch_list',con = engine, if_exists = 'append', index = False)
        conn = sql.connect(host ='localhost' ,database ='lsp_master_test' ,user = 'root' ,password = 'root')
        cursor = conn.cursor()
        
        #de-duplicate company info
        cursor.execute('CREATE TABLE temp12 LIKE company_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp12 SELECT DISTINCT * FROM company_info;')
        conn.commit()
        cursor.execute('DROP TABLE company_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp12 TO company_info;')
        conn.commit()
        cursor.execute('DELETE FROM company_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM company_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #de-duplicate financial_details
        cursor.execute('CREATE TABLE temp13 LIKE financial_details;')
        conn.commit()
        cursor.execute('INSERT INTO temp13 SELECT DISTINCT * FROM financial_details;')
        conn.commit()
        cursor.execute('DROP TABLE financial_details;')
        conn.commit()
        cursor.execute('RENAME TABLE temp13 TO financial_details;')
        conn.commit()
        cursor.execute('DELETE FROM financial_details WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM financial_details GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of contact table.
        cursor.execute('CREATE TABLE temp2 LIKE contact_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp2 SELECT DISTINCT * FROM contact_info;')
        conn.commit()
        cursor.execute('DROP TABLE contact_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp2 TO contact_info;')
        conn.commit()
        cursor.execute('DELETE FROM contact_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM contact_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of address table.
        cursor.execute('CREATE TABLE temp1 LIKE address_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp1 SELECT DISTINCT * FROM address_info;')
        conn.commit()
        cursor.execute('DROP TABLE address_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp1 TO address_info;')
        conn.commit()
        cursor.execute('DELETE FROM address_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM address_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of manpower table.
        cursor.execute('CREATE TABLE temp3 LIKE manpower_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp3 SELECT DISTINCT * FROM manpower_info;')
        conn.commit()
        cursor.execute('DROP TABLE manpower_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp3 TO manpower_info;')
        conn.commit()
        cursor.execute('DELETE FROM manpower_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM manpower_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of finance table.
        cursor.execute('CREATE TABLE temp14 LIKE finance_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp14 SELECT DISTINCT * FROM finance_info;')
        conn.commit()
        cursor.execute('DROP TABLE finance_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp14 TO finance_info;')
        conn.commit()
        cursor.execute('DELETE FROM finance_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM finance_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of vehicle table.
        cursor.execute('CREATE TABLE temp4 LIKE vehicle_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp4 SELECT DISTINCT * FROM vehicle_info;')
        conn.commit()
        cursor.execute('DROP TABLE vehicle_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp4 TO vehicle_info;')
        conn.commit()
        cursor.execute('DELETE FROM vehicle_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM vehicle_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of ship_track table.
        cursor.execute('CREATE TABLE temp5 LIKE ship_track_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp5 SELECT DISTINCT * FROM ship_track_info;')
        conn.commit()
        cursor.execute('DROP TABLE ship_track_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp5 TO ship_track_info;')
        conn.commit()
        cursor.execute('DELETE FROM ship_track_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM ship_track_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of clientelle table.
        cursor.execute('CREATE TABLE temp6 LIKE top_clientelle_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp6 SELECT DISTINCT * FROM top_clientelle_info;')
        conn.commit()
        cursor.execute('DROP TABLE top_clientelle_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp6 TO top_clientelle_info;')
        conn.commit()
        cursor.execute('DELETE FROM top_clientelle_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM top_clientelle_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of reference table.
        cursor.execute('CREATE TABLE temp7 LIKE references_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp7 SELECT DISTINCT * FROM references_info;')
        conn.commit()
        cursor.execute('DROP TABLE references_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp7 TO references_info;')
        conn.commit()
        cursor.execute('DELETE FROM references_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM references_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of top 5 business table.
        cursor.execute('CREATE TABLE temp8 LIKE top_5_cmp_business_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp8 SELECT DISTINCT * FROM top_5_cmp_business_info;')
        conn.commit()
        cursor.execute('DROP TABLE top_5_cmp_business_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp8 TO top_5_cmp_business_info;')
        conn.commit()
        cursor.execute('DELETE FROM top_5_cmp_business_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM top_5_cmp_business_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of backhaul table.
        cursor.execute('CREATE TABLE temp9 LIKE backhaul_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp9 SELECT DISTINCT * FROM backhaul_info;')
        conn.commit()
        cursor.execute('DROP TABLE backhaul_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp9 TO backhaul_info;')
        conn.commit()
        cursor.execute('DELETE FROM backhaul_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM backhaul_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of interest table.
        cursor.execute('CREATE TABLE temp10 LIKE interests_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp10 SELECT DISTINCT * FROM interests_info;')
        conn.commit()
        cursor.execute('DROP TABLE interests_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp10 TO interests_info;')
        conn.commit()
        cursor.execute('DELETE FROM interests_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM interests_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        #Mysql de-duplication of reference table.
        cursor.execute('CREATE TABLE temp11 LIKE address_info;')
        conn.commit()
        cursor.execute('INSERT INTO temp11 SELECT DISTINCT * FROM address_info;')
        conn.commit()
        cursor.execute('DROP TABLE address_info;')
        conn.commit()
        cursor.execute('RENAME TABLE temp11 TO address_info;')
        conn.commit()
        cursor.execute('DELETE FROM address_info WHERE (lspName, `Submission_Date`) NOT IN (SELECT lspName, dte FROM (SELECT lspName, MAX(`Submission_Date`) dte FROM address_info GROUP BY lspName, year(`Submission_Date`)) AS A );')
        conn.commit()
        
        conn.close()
        result ='''
        <html>
        <head>
        <title>Result</title>
        </head>
        <link rel="stylesheet" type="text/css" href="static/table.css">
        <body>
        <div class="tab">
        <h1><b>This is your Dataset</b></h1></br>
        <b><a href="/data">Back</a></b>
        </div> 
        <div class="set">
        {table}
        </div>
        </body>  
        </html>      
        '''
        with open(r'E:\Projects\Python\RFIapp\templates\file.html','w') as f:
            f.write(result.format(table=new_metadata.to_html(classes='mystyle')))
        return render_template('upload1.html')
    return render_template('upload.html')

                  
conn = sql.connect(host ='localhost' ,database ='lsp_master_test' ,user = 'root' ,password = 'root')
cursor = conn.cursor()
query1 = ('SELECT * FROM contact_info')
cursor.execute(query1) 
contact = cursor.fetchall()
contact = pd.DataFrame(contact)
contact.columns = ['Transporter_ID','Submission_Date','lspName','year','yearEstablished','personName1','designation1','mobileNo1','phoneNo1','email1',
                                                    'personName2','designation2','mobileNo2','phoneNo2','email2',
                                                    'personName3','designation3','mobileNo3','phoneNo3','email3',
                                                    'personName4','designation4','mobileNo4','phoneNo4','email4']
query2 = ('SELECT * FROM finance_info')
cursor.execute(query2) 
finance = cursor.fetchall()
finance = pd.DataFrame(finance)
finance.columns = ['Transporter_ID','Submission_Date','lspName','year','bankApproved','bankNameRegNo','bankGuarantee','gstRegistered','gstIN', 'netRevenue_2014-15','netRevenue_2015-16','netRevenue_2016-17','netRevenue_2017-18',
                                                    'operatingCost_2014-15','operatingCost_2015-16','operatingCost_2016-17','operatingCost_2017-18',
                                                    'interestPayment_2014-15','interestPayment_2015-16','interestPayment_2016-17','interestPayment_2017-18',
                                                    'netProfit_2014-15','netProfit_2015-16','netProfit_2016-17','netProfit_2017-18',
                                                    'currentAssets_2014-15','currentAssets_2015-16','currentAssets_2016-17','currentAssets_2017-18',
                                                    'turnover_2014-15','turnover_2015-16','turnover_2016-17','turnover_2017-18']

query3 = ('SELECT * FROM manpower_info')
cursor.execute(query3) 
manpower = cursor.fetchall()
manpower = pd.DataFrame(manpower)
manpower.columns = ['Transporter_ID','Submission_Date','lspName','year','management_cnt','driver_cnt','maintenance_cnt']
manpower['management_cnt'] = manpower['management_cnt'].round()
manpower['driver_cnt'] = manpower['driver_cnt'].round()
manpower['maintenance_cnt'] = manpower['maintenance_cnt'].round()

query4 = ('SELECT * FROM vehicle_info')
cursor.execute(query4) 
vehicle = cursor.fetchall()
vehicle = pd.DataFrame(vehicle)
vehicle.columns = ['Transporter_ID','Submission_Date','lspName','year','16_MT_cnt_selfOwned','16_MT_cnt_withGPS','16_MT_cnt_incSelfOwn','16_MT_cnt_numAttached','16_MT_cnt_keyVendorProvider','%_16_MT_fleet_with_RC_updated',
                                                    '21_24_27MT_cnt_selfOwned','21_24_27_MT_cnt_withGPS','21_24_27_MT_cnt_incSelfOwn','21_24_27_MT_cnt_numAttached','21_24_27_MT_cnt_keyVendorProvider','%_21_24_27_MT_fleet_with_RC_updated',
                                                    'Trailers_specify_type_of_trailer_cnt_selfOwned','Trailers_specify_type_of_trailer_cnt_withGPS','Trailers_specify_type_of_trailer_cnt_incSelfOwn','Trailers_specify_type_of_trailer_cnt_numAttached','Trailers_specify_type_of_trailer_cnt_keyVendorProvider','%_Trailer_fleet_with_RC_updated',
                                                    '9_MT_cnt_selfOwned','9_MT_cnt_withGPS','9_MT_incSelfOwn','9_MT_cnt_numAttached','9_MT_cnt_keyVendorProvider','%_9_MT_fleet_with_RC_updated',
                                                    '32ft_single_axle_closed_body_container_cnt_selfOwned','32ft_single_axle_closed_body_container_cnt_withGPS','32ft_single_axle_closed_body_container_cnt_incSelfOwn','32ft_single_axle_closed_body_container_cnt_numAttached','32ft_single_axle_closed_body_container_cnt_keyVendorProvider','%_32FT_singleAxle_fleet_with_RC_updated',
                                                    '32ft_multi_axle_closed_bodycontainer_cnt_selfOwned','32ft_multi_axle_closed_bodycontainer_cnt_withGPS','32ft_multi_axle_closed_bodycontainer_cnt_incSelfOwn','32ft_multi_axle_closed_bodycontainer_cnt_numAttached','32ft_multi_axle_closed_bodycontainer_cnt_keyVendorProvider','%_32FT_multiAxle_fleet_with_RC_updated',
                                                    '7.5_MT_cnt_selfOwned','7.5_MT_cnt_withGPS','7.5_MT_cnt_incSelfOwn','7.5_MT_cnt_numAttached','7.5_MT_cnt_keyVendorProvider','%_7.5_MT_fleet_with_RC_updated',
                                                    '6_MT_cnt_selfOwned','6_MT_cnt_withGPS','6_MT_cnt_incSelfOwn','6_MT_cnt_numAttached','6_MT_cnt_keyVendorProvider','%_6_MT_fleet_with_RC_updated',
                                                    'Smaller_types_of_trucks_<_6_MT_cnt_selfOwned','Smaller_types_of_trucks_<_6_MT_cnt_withGPS','Smaller_types_of_trucks_<_6_MT_cnt_incSelfOwn','Smaller_types_of_trucks_<_6_MT_cnt_numAttached','Smaller_types_of_trucks_<_6_MT_cnt_keyVendorProvider','%_smallerThan_6_MT_fleet_with_RC_updated',
                                                    'Other_Truck_Types_cnt_selfOwned','Other_Truck_Types_cnt_withGPS','Other_Truck_Types_cnt_incSelfOwn','Other_Truck_Types_cnt_numAttached','Other_Truck_Types_cnt_keyVendorProvider','%_otherTruck_fleet_with_RC_updated','list_of_owned_vehicles']

query5 = ('SELECT * FROM ship_track_info')
cursor.execute(query5) 
ship_track = cursor.fetchall()
ship_track = pd.DataFrame(ship_track)
ship_track.columns = ['Transporter_ID','Submission_Date','lspName','year', 'method_1','details1','techUsed1',
                                                       'method_2','details2','techUsed2',
                                                       'method_3','details3','techUsed3','mgmtReportTypes','list_of_owned_vehicles']

query6 = ('SELECT * FROM references_info')
cursor.execute(query6) 
references = cursor.fetchall()
references = pd.DataFrame(references)
references.columns = ['Transporter_ID','Submission_Date','lspName','year', 'clientRef1','contactName1','contactPhone1','contactEmail1',
                                                       'clientRef2','contactName2','contactPhone2','contactEmail2',
                                                       'clientRef3','contactName3','contactPhone3','contactEmail3',
                                                       'clientRef4','contactName4','contactPhone4','contactEmail4',
                                                       'clientRef5','contactName5','contactPhone5','contactEmail5']

query7 = ('SELECT * FROM top_5_cmp_business_info')
cursor.execute(query7) 
top_5_cmp_business = cursor.fetchall()
top_5_cmp_business = pd.DataFrame(top_5_cmp_business)
top_5_cmp_business.columns = ['Transporter_ID','Submission_Date','lspName','year', 'companyName1','location1',
                                                               'companyName2','location2',
                                                               'companyName3','location3',
                                                               'companyName4','location4',
                                                               'companyName5','location5','other_companies_interested','lane_attachment']

query8 = ('SELECT * FROM backhaul_info')
cursor.execute(query8) 
backhaul = cursor.fetchall()
backhaul = pd.DataFrame(backhaul)
backhaul.columns = ['Transporter_ID','Submission_Date','lspName','year', 'origin1','destination1','truckType1','currentRate1',
                                                     'origin2','destination2','truckType2','currentRate2',
                                                     'origin3','destination3','truckType3','currentRate3',
                                                     'origin4','destination4','truckType4','currentRate4',
                                                     'origin5','destination5','truckType5','currentRate5','additional_backhaul','attachmentLink']

query9 = ('SELECT * FROM interests_info')
cursor.execute(query9) 
interests = cursor.fetchall()
interests = pd.DataFrame(interests)
interests.columns = ['Transporter_ID','Submission_Date','lspName','year', 'Trial_load_from_company','Award_incentive_programme','Future_business_prospects','keyFocusAreas','contactedFurther']

query10 = ('SELECT * FROM address_info')
cursor.execute(query10) 
address = cursor.fetchall()
address = pd.DataFrame(address)
address.columns = ['Submission_Date','Transporter_ID','lspName','year', 'hqAddress','City','State','Pincode']

query11 = ('SELECT * FROM top_clientelle_info')
cursor.execute(query11) 
top_clientelle = cursor.fetchall()
top_clientelle = pd.DataFrame(top_clientelle)
top_clientelle.columns = ['Transporter_ID','Submission_Date','lspName','year', 'clientName1','industry1','freightValue1','percentOfBusiness1','trucksPerMonth1','productType1','otherModes1',
                                                           'clientName2','industry2','freightValue2','percentOfBusiness2','trucksPerMonth2','productType2','otherModes2',
                                                           'clientName3','industry3','freightValue3','percentOfBusiness3','trucksPerMonth3','productType3','otherModes3',
                                                           'clientName4','industry4','freightValue4','percentOfBusiness4','trucksPerMonth4','productType4','otherModes4',
                                                           'clientName5','industry5','freightValue5','percentOfBusiness5','trucksPerMonth5','productType5','otherModes5',
                                                           'clientName6','industry6','freightValue6','percentOfBusiness6','trucksPerMonth6','productType6','otherModes6',
                                                           'clientName7','industry7','freightValue7','percentOfBusiness7','trucksPerMonth7','productType7','otherModes7',
                                                           'clientName8','industry8','freightValue8','percentOfBusiness8','trucksPerMonth8','productType8','otherModes8',
                                                           'clientName9','industry9','freightValue9','percentOfBusiness9','trucksPerMonth9','productType9','otherModes9',
                                                           'clientName10','industry10','freightValue10','percentOfBusiness10','trucksPerMonth10','productType10','otherModes10']

query12 = ('SELECT * FROM branch_list')
cursor.execute(query12)
m = cursor.fetchall()
m = pd.DataFrame(m)
m.columns = ['Sr No','key', 'lspName', 'Type', 'Address','City','State','Latitude','Longitude','Pin Code']
#m = pd.read_excel('E:\Rajkumar\VIA_v0.1\drv_server_08-12-2018\Branch_list_final_v2.xlsx')
query13 = ('SELECT * FROM company_info')
cursor.execute(query13)
company_info = cursor.fetchall()
company_info = pd.DataFrame(company_info)
company_info.columns = ['Transporter_ID','Submission_Date','lspName','year','website','email','companyType','keyFocusAreas']

query14 = ('SELECT * FROM financial_details')
cursor.execute(query14)
financial_details = cursor.fetchall()
financial_details = pd.DataFrame(financial_details)
financial_details.columns = ['Transporter_ID','Submission_Date','lspName','year','bankApproved','bankNameRegNo','bankGuarantee','gstRegistered','gstIN']

conn.close()
#---------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------------------------#    

#---------------------------RFI Completion %----------------------# 

contact = contact.replace('0',0)
address = address.replace('0',0)
finance = finance.replace('0',0)
manpower = manpower.replace('0',0)
ship_track = ship_track.replace('0',0)
references = references.replace('0',0)
top_5_cmp_business = top_5_cmp_business.replace('0',0)
backhaul = backhaul.replace('0',0)
top_clientelle = top_clientelle.replace('0',0)

            

#filled NAs with 0
#            new_metadata = new_metadata.fillna(0)
#            new_metadata = new_metadata.replace('str',0)

#column_names = list(new_metadata.columns) 

def completion_value(x):
    c = str(x)
    a = x.eq(0).sum(axis = 1)
    b = len(x.columns)-4 #because columns also contain two other columns namely Transporter ID and lspName
    calc = pd.DataFrame(round(((b - a)/b)*100,2))
    return calc


'''DATAFRAME COMPLETION CODE'''

#---------------------------'''Owner details'''-------------------------------#
#contact = new_metadata[['Transporter_ID','lspName','year','personName1','designation1','mobileNo1','phoneNo1','email1',
#                                                    'personName2','designation2','mobileNo2','phoneNo2','email2',
#                                                    'personName3','designation3','mobileNo3','phoneNo3','email3',
#                                                    'personName4','designation4','mobileNo4','phoneNo4','email4']]

#number of unique LSPs
num_unique_lsps = round(len(contact['lspName'].unique()),0)
#            address =  new_metadata[['Submission_Date','Transporter_ID','lspName','year', 'hqAddress','City','State','Pincode']]

#overall missing
calc_contact = completion_value(contact)
calc_contact.columns = ['% contact completion']
df_contact = pd.concat([contact['Submission_Date'],contact['Transporter_ID'],contact['lspName'],calc_contact],axis=1)
contact_info = pd.concat([address['City'],address['State'],address['Submission_Date'],address['lspName'],address['hqAddress'],
                          contact['personName1'],contact['designation1'],contact['mobileNo1']],axis=1)
#            writer = pd.ExcelWriter("contact_info.xlsx", engine = 'xlsxwriter')
#            contact_info.to_excel(writer,sheet_name = 'contact_info')
#            writer.save()   

contact_dataframe = pd.DataFrame()
for i in range(0,len(contact)):
    ctc = pd.DataFrame([[contact['lspName'][i],contact['year'][i], contact['personName1'][i],contact['designation1'][i],contact['mobileNo1'][i],contact['phoneNo1'][i],contact['email1'][i]],
                      [contact['lspName'][i], contact['year'][i], contact['personName2'][i],contact['designation2'][i],contact['mobileNo2'][i],contact['phoneNo2'][i],contact['email2'][i]],
                      [contact['lspName'][i],contact['year'][i], contact['personName3'][i],contact['designation3'][i],contact['mobileNo3'][i],contact['phoneNo3'][i],contact['email3'][i]],
                      [contact['lspName'][i], contact['year'][i], contact['personName4'][i],contact['designation4'][i],contact['mobileNo4'][i],contact['phoneNo4'][i],contact['email4'][i]]],
                      columns = ['lspName','year','Person Name','Designation','Mobile Num','Phone Num','Email ID'])  
    contact_dataframe = contact_dataframe.append(ctc, sort = False)

contact_dataframe = contact_dataframe[contact_dataframe['Person Name'] != 0]


#-----------------------------------------------------------------------------#
#-----------------------------'''Financial Details'''-------------------------#
'''Finance table'''
#finance = new_metadata[['Transporter_ID','lspName','year', 'netRevenue_2014-15','netRevenue_2015-16','netRevenue_2016-17','netRevenue_2017-18',
#                                                    'operatingCost_2014-15','operatingCost_2015-16','operatingCost_2016-17','operatingCost_2017-18',
#                                                    'interestPayment_2014-15','interestPayment_2015-16','interestPayment_2016-17','interestPayment_2017-18',
#                                                    'netProfit_2014-15','netProfit_2015-16','netProfit_2016-17','netProfit_2017-18',
#                                                    'currentAssets_2014-15','currentAssets_2015-16','currentAssets_2016-17','currentAssets_2017-18',
#                                                    'turnover_2014-15','turnover_2015-16','turnover_2016-17','turnover_2017-18']]

net_revenue = finance[['netRevenue_2014-15','netRevenue_2015-16','netRevenue_2016-17','netRevenue_2017-18']] 
#net_completion = completion_value(net_revenue)
#net_completion.columns = ['% net_revenue completion']

operating_cost = finance[['operatingCost_2014-15','operatingCost_2015-16','operatingCost_2016-17','operatingCost_2017-18']]
#operating_completion = completion_value(operating_cost)
#operating_completion.columns = ['% operating_cost completion']

interest_payment = finance[['interestPayment_2014-15','interestPayment_2015-16','interestPayment_2016-17','interestPayment_2017-18']]
#interest_completion = completion_value(interest_payment)
#interest_completion.columns = ['% interest_payment completion']

netProfit = finance[['netProfit_2014-15','netProfit_2015-16','netProfit_2016-17','netProfit_2017-18']]
#profit_completion = completion_value(netProfit)
#profit_completion.columns = ['% net_profit completion']

currentAssets = finance[['currentAssets_2014-15','currentAssets_2015-16','currentAssets_2016-17','currentAssets_2017-18']]
#current_assets_completion = completion_value(currentAssets)
#current_assets_completion.columns = ['% current_assets completion']

turnover = finance[['turnover_2014-15','turnover_2015-16','turnover_2016-17','turnover_2017-18']]
#turnover_completion = completion_value(turnover)
#turnover_completion.columns = ['% turnover completion']

#drill_down_finance = pd.concat([finance['lspName'],finance['year'],round(net_completion,2),round(operating_completion,2),round(interest_completion,2),round(profit_completion,2),round(current_assets_completion,2),round(turnover_completion,2)],axis=1)

def completion_finance(x):
    c1 = str(x)
    a1 = x.eq(0).sum(axis=1)
    b1 = len(x.columns)
    calc1 = pd.DataFrame(round(((b1-a1)/b1)*100,2))
    return calc1

finance_calc = finance[['netRevenue_2014-15','netRevenue_2015-16','netRevenue_2016-17','netRevenue_2017-18',
                        'operatingCost_2014-15','operatingCost_2015-16','operatingCost_2016-17','operatingCost_2017-18',
                        'interestPayment_2014-15','interestPayment_2015-16','interestPayment_2016-17','interestPayment_2017-18',
                        'netProfit_2014-15','netProfit_2015-16','netProfit_2016-17','netProfit_2017-18',
                        'currentAssets_2014-15','currentAssets_2015-16','currentAssets_2016-17','currentAssets_2017-18',
                        'turnover_2014-15','turnover_2015-16','turnover_2016-17','turnover_2017-18']]
calc_finance = completion_finance(finance_calc)
calc_finance.columns = ['% finance completion']
df_finance = pd.concat([finance['Submission_Date'],finance['Transporter_ID'],finance['lspName'],calc_finance],axis=1)



finance_dataframe = pd.DataFrame()
for i in range(0,len(finance)):
    inc = pd.DataFrame([[finance['lspName'][i], finance['year'][i],'Net Revenue', finance['netRevenue_2014-15'][i],finance['netRevenue_2015-16'][i],finance['netRevenue_2016-17'][i],finance['netRevenue_2017-18'][i]],
                      [finance['lspName'][i], finance['year'][i],'Operating Cost', finance['operatingCost_2014-15'][i],finance['operatingCost_2015-16'][i],finance['operatingCost_2016-17'][i],finance['operatingCost_2017-18'][i]],
                      [finance['lspName'][i], finance['year'][i],'Interest Payment', finance['interestPayment_2014-15'][i],finance['interestPayment_2015-16'][i],finance['interestPayment_2016-17'][i],finance['interestPayment_2017-18'][i]],
                      [finance['lspName'][i], finance['year'][i],'Net Profit', finance['netProfit_2014-15'][i],finance['netProfit_2015-16'][i],finance['netProfit_2016-17'][i],finance['netProfit_2017-18'][i]],
                      [finance['lspName'][i], finance['year'][i],'Current Assets', finance['currentAssets_2014-15'][i],finance['currentAssets_2015-16'][i],finance['currentAssets_2016-17'][i],finance['currentAssets_2017-18'][i]],
                      [finance['lspName'][i], finance['year'][i],'Turnover', finance['turnover_2014-15'][i],finance['turnover_2015-16'][i],finance['turnover_2016-17'][i],finance['turnover_2017-18'][i]]],
                      columns = ['lspName','year','Finance','2014-15','2015-16','2016-17','2017-18'])  
    finance_dataframe = finance_dataframe.append(inc, sort = False)
#-----------------------------------------------------------------------------#

#--------------------------------'''Manpower'''-------------------------------#
#manpower = new_metadata[['Transporter_ID','lspName','year','management_cnt','driver_cnt','maintenance_cnt']]

calc_manpower = completion_value(manpower)
calc_manpower.columns = ['% manpower completion']
df_manpower = pd.concat([manpower['year'],manpower['Transporter_ID'],manpower['lspName'],calc_manpower],axis=1)

#-----------------------------------------------------------------------------#


#----------------------------'''Vehicle information'''------------------------#
#vehicle = new_metadata[['Transporter_ID','lspName','year','16_MT_cnt_selfOwned','16_MT_cnt_withGPS','16_MT_cnt_incSelfOwn','16_MT_cnt_numAttached','16_MT_cnt_keyVendorProvider','%_16_MT_fleet_with_RC_updated',
#                                                    '21_24_27MT_cnt_selfOwned','21_24_27_MT_cnt_withGPS','21_24_27_MT_cnt_incSelfOwn','21_24_27_MT_cnt_numAttached','21_24_27_MT_cnt_keyVendorProvider','%_21_24_27_MT_fleet_with_RC_updated',
#                                                    'Trailers_specify_type_of_trailer_cnt_selfOwned','Trailers_specify_type_of_trailer_cnt_withGPS','Trailers_specify_type_of_trailer_cnt_incSelfOwn','Trailers_specify_type_of_trailer_cnt_numAttached','Trailers_specify_type_of_trailer_cnt_keyVendorProvider','%_Trailer_fleet_with_RC_updated',
#                                                    '9_MT_cnt_selfOwned','9_MT_cnt_withGPS','9_MT_incSelfOwn','9_MT_cnt_numAttached','9_MT_cnt_keyVendorProvider','%_9_MT_fleet_with_RC_updated',
#                                                    '32ft_single_axle_closed_body_container_cnt_selfOwned','32ft_single_axle_closed_body_container_cnt_withGPS','32ft_single_axle_closed_body_container_cnt_incSelfOwn','32ft_single_axle_closed_body_container_cnt_numAttached','32ft_single_axle_closed_body_container_cnt_keyVendorProvider','%_32FT_singleAxle_fleet_with_RC_updated',
#                                                    '32ft_multi_axle_closed_bodycontainer_cnt_selfOwned','32ft_multi_axle_closed_bodycontainer_cnt_withGPS','32ft_multi_axle_closed_bodycontainer_cnt_incSelfOwn','32ft_multi_axle_closed_bodycontainer_cnt_numAttached','32ft_multi_axle_closed_bodycontainer_cnt_keyVendorProvider','%_32FT_multiAxle_fleet_with_RC_updated',
#                                                    '7.5_MT_cnt_selfOwned','7.5_MT_cnt_withGPS','7.5_MT_cnt_incSelfOwn','7.5_MT_cnt_numAttached','7.5_MT_cnt_keyVendorProvider','%_7.5_MT_fleet_with_RC_updated',
#                                                    '6_MT_cnt_selfOwned','6_MT_cnt_withGPS','6_MT_cnt_incSelfOwn','6_MT_cnt_numAttached','6_MT_cnt_keyVendorProvider','%_6_MT_fleet_with_RC_updated',
#                                                    'Smaller_types_of_trucks_<_6_MT_cnt_selfOwned','Smaller_types_of_trucks_<_6_MT_cnt_withGPS','Smaller_types_of_trucks_<_6_MT_cnt_incSelfOwn','Smaller_types_of_trucks_<_6_MT_cnt_numAttached','Smaller_types_of_trucks_<_6_MT_cnt_keyVendorProvider','%_smallerThan_6_MT_fleet_with_RC_updated',
#                                                    'Other_Truck_Types_cnt_selfOwned','Other_Truck_Types_cnt_withGPS','Other_Truck_Types_cnt_incSelfOwn','Other_Truck_Types_cnt_numAttached','Other_Truck_Types_cnt_keyVendorProvider','%_otherTruck_fleet_with_RC_updated','list_of_owned_vehicles']]


real_vehicle_count = vehicle[['lspName','year','16_MT_cnt_selfOwned','21_24_27MT_cnt_selfOwned','Trailers_specify_type_of_trailer_cnt_selfOwned',
                                   '9_MT_cnt_selfOwned','32ft_single_axle_closed_body_container_cnt_selfOwned','32ft_multi_axle_closed_bodycontainer_cnt_selfOwned',
                                   '7.5_MT_cnt_selfOwned','6_MT_cnt_selfOwned','Smaller_types_of_trucks_<_6_MT_cnt_selfOwned','Other_Truck_Types_cnt_selfOwned',
                                   '16_MT_cnt_numAttached','21_24_27_MT_cnt_numAttached','Trailers_specify_type_of_trailer_cnt_numAttached','9_MT_cnt_numAttached',
                                   '32ft_single_axle_closed_body_container_cnt_numAttached','7.5_MT_cnt_numAttached','6_MT_cnt_numAttached','Smaller_types_of_trucks_<_6_MT_cnt_numAttached',
                                   'Other_Truck_Types_cnt_numAttached']]
real_vehicle_count['% vehicle completion'] = 100 - round((real_vehicle_count.eq(0).sum(axis=1)/(len(real_vehicle_count.columns)-1))*100,0)

df_vehicle = pd.concat([vehicle['year'],vehicle['Transporter_ID'],vehicle['lspName'],real_vehicle_count],axis=1)

vehicle_count_self_owned = pd.DataFrame(vehicle['16_MT_cnt_selfOwned']
                                       +vehicle['21_24_27MT_cnt_selfOwned']
                                       +vehicle['Trailers_specify_type_of_trailer_cnt_selfOwned']
                                       +vehicle['9_MT_cnt_selfOwned']
                                       +vehicle['32ft_single_axle_closed_body_container_cnt_selfOwned']
                                       +vehicle['32ft_multi_axle_closed_bodycontainer_cnt_selfOwned']
                                       +vehicle['7.5_MT_cnt_selfOwned']
                                       +vehicle['6_MT_cnt_selfOwned']
                                       +vehicle['Smaller_types_of_trucks_<_6_MT_cnt_selfOwned']
                                       +vehicle['Other_Truck_Types_cnt_selfOwned'])
vehicle_count_self_owned.columns = ['Self Owned']
vehicle_count_self_owned['Self Owned'] = vehicle_count_self_owned['Self Owned'].astype(int)

vehicle_count_attached = pd.DataFrame(vehicle['16_MT_cnt_numAttached']
                                      +vehicle['21_24_27_MT_cnt_numAttached']
                                      +vehicle['Trailers_specify_type_of_trailer_cnt_numAttached']
                                      +vehicle['9_MT_cnt_numAttached']
                                      +vehicle['32ft_single_axle_closed_body_container_cnt_numAttached']
                                      +vehicle['32ft_multi_axle_closed_bodycontainer_cnt_numAttached']
                                      +vehicle['7.5_MT_cnt_numAttached']
                                      +vehicle['6_MT_cnt_numAttached']
                                      +vehicle['Smaller_types_of_trucks_<_6_MT_cnt_numAttached']
                                      +vehicle['Other_Truck_Types_cnt_numAttached'])
vehicle_count_attached.columns = ['Attached']
vehicle_count_attached['Attached'] = vehicle_count_attached['Attached'].astype(int)


vehicle_count = pd.concat([vehicle['lspName'],vehicle_count_self_owned.round(),vehicle_count_attached.round(),vehicle['year']],axis=1)

vehicle_own_att = pd.DataFrame()
for i in range(0,len(vehicle_count)):
    trc = pd.DataFrame([[vehicle_count['lspName'][i], 'Self Owned', vehicle_count['Self Owned'][1]],
                      [vehicle_count['lspName'][i], 'Attached', vehicle_count['Attached'][i]]],
                      columns = ['lspName','Category','Count'])  
    vehicle_own_att = vehicle_own_att.append(trc, sort = False)

vehicle_lsp = pd.concat([vehicle['lspName'],
                           vehicle['Smaller_types_of_trucks_<_6_MT_cnt_numAttached'],
                           vehicle['6_MT_cnt_numAttached'],
                           vehicle['7.5_MT_cnt_numAttached'],
                           vehicle['9_MT_cnt_numAttached'],
                           vehicle['16_MT_cnt_numAttached'],
                           vehicle['21_24_27_MT_cnt_numAttached'],
                           vehicle['32ft_single_axle_closed_body_container_cnt_numAttached'],
                           vehicle['32ft_multi_axle_closed_bodycontainer_cnt_numAttached']],axis=1)
vehicle_lsp.columns = ['LSP Name','< 6MT','6 MT','7.5MT','9MT','16MT','21/24/27MT','32FT SA','32FT MA']

vehicle_dataframe = pd.DataFrame()
for i in range(0,len(vehicle)):
    veh = pd.DataFrame([[vehicle['lspName'][i],vehicle['year'][i], '< 6MT', vehicle['Smaller_types_of_trucks_<_6_MT_cnt_selfOwned'][i],vehicle['Smaller_types_of_trucks_<_6_MT_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'6MT', vehicle['6_MT_cnt_selfOwned'][i],vehicle['6_MT_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'7.5MT', vehicle['7.5_MT_cnt_selfOwned'][i],vehicle['7.5_MT_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'9MT', vehicle['9_MT_cnt_selfOwned'][i],vehicle['9_MT_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'16MT', vehicle['16_MT_cnt_selfOwned'][i],vehicle['16_MT_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'21/24/27', vehicle['21_24_27MT_cnt_selfOwned'][i],vehicle['21_24_27_MT_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'32FT Single Axle', vehicle['32ft_single_axle_closed_body_container_cnt_selfOwned'][i],vehicle['32ft_single_axle_closed_body_container_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'32FT Multi Axle', vehicle['32ft_multi_axle_closed_bodycontainer_cnt_selfOwned'][i],vehicle['32ft_multi_axle_closed_bodycontainer_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'Trailers', vehicle['Trailers_specify_type_of_trailer_cnt_selfOwned'][i],vehicle['Trailers_specify_type_of_trailer_cnt_numAttached'][i]],
                      [vehicle['lspName'][i], vehicle['year'][i],'Others', vehicle['Other_Truck_Types_cnt_selfOwned'][i],vehicle['Other_Truck_Types_cnt_numAttached'][i]]],
                      columns = ['lspName','year','Truck Type','Self Owned','Attached'])  
    vehicle_dataframe = vehicle_dataframe.append(veh, sort = False)

#-----------------------------------------------------------------------------#

#------------------------'''Shipment tracking method'''-----------------------#
#ship_track = new_metadata[['Transporter_ID','lspName','year', 'method_1','details1','techUsed1',
#                                                       'method_2','details2','techUsed2',
#                                                       'method_3','details3','techUsed3']]

calc_ship = completion_value(ship_track)
calc_ship.columns = ['% ship tracking completion']
df_ship = pd.concat([ship_track['Submission_Date'],ship_track['Transporter_ID'],ship_track['lspName'],calc_ship],axis=1)
#-----------------------------------------------------------------------------#

#-------------------------'''Top Clientelle Information'''--------------------#
#top_clientelle = new_metadata[['Transporter_ID','lspName','year', 'clientName1','industry1','freightValue1','percentOfBusiness1','trucksPerMonth1','productType1','otherModes1',
#                                                           'clientName2','industry2','freightValue2','percentOfBusiness2','trucksPerMonth2','productType2','otherModes2',
#                                                           'clientName3','industry3','freightValue3','percentOfBusiness3','trucksPerMonth3','productType3','otherModes3',
#                                                           'clientName4','industry4','freightValue4','percentOfBusiness4','trucksPerMonth4','productType4','otherModes4',
#                                                           'clientName5','industry5','freightValue5','percentOfBusiness5','trucksPerMonth5','productType5','otherModes5',
#                                                           'clientName6','industry6','freightValue6','percentOfBusiness6','trucksPerMonth6','productType6','otherModes6',
#                                                           'clientName7','industry7','freightValue7','percentOfBusiness7','trucksPerMonth7','productType7','otherModes7',
#                                                           'clientName8','industry8','freightValue8','percentOfBusiness8','trucksPerMonth8','productType8','otherModes8',
#                                                           'clientName9','industry9','freightValue9','percentOfBusiness9','trucksPerMonth9','productType9','otherModes9',
#                                                           'clientName10','industry10','freightValue10','percentOfBusiness10','trucksPerMonth10','productType10','otherModes10']]

calc_clientelle = completion_value(top_clientelle)
calc_clientelle.columns = ['% top clientelle completion']
df_clientelle = pd.concat([top_clientelle['Submission_Date'],top_clientelle['Transporter_ID'],top_clientelle['lspName'],calc_clientelle],axis=1)

top_clientelle_dataframe = pd.DataFrame()
for i in range(0,len(top_clientelle)):
    cltl = pd.DataFrame([[top_clientelle['lspName'][i],top_clientelle['year'][i],top_clientelle['clientName1'][i],top_clientelle['industry1'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName2'][i],top_clientelle['industry2'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName3'][i],top_clientelle['industry3'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName4'][i],top_clientelle['industry4'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName5'][i],top_clientelle['industry5'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName6'][i],top_clientelle['industry6'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName7'][i],top_clientelle['industry7'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName8'][i],top_clientelle['industry8'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName9'][i],top_clientelle['industry9'][i]],
                      [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName10'][i],top_clientelle['industry10'][i]]],
                      columns = ['lspName','year','Client Name','Sector'])  
    top_clientelle_dataframe = top_clientelle_dataframe.append(cltl, sort = False)


#-----------------------------------------------------------------------------#
#--------------------------------'''References'''-----------------------------#
#references = new_metadata[['Transporter_ID','lspName','year', 'clientRef1','contactName1','contactPhone1','contactEmail1',
#                                                       'clientRef2','contactName2','contactPhone2','contactEmail2',
#                                                       'clientRef3','contactName3','contactPhone3','contactEmail3',
#                                                       'clientRef4','contactName4','contactPhone4','contactEmail4',
#                                                       'clientRef5','contactName5','contactPhone5','contactEmail5']]

#references.replace('0',np.nan, inplace = True)

#test_references = references.fillna(0).astype(bool).sum(axis=1)-4
#test_references = references.isnull().sum(axis=1)#code to find nans in a row

#calc_references = (test_references/(len(references.columns)-4))*100
calc_references = completion_value(references)
calc_references.columns = ['% references completion']
df_references = pd.concat([references['Submission_Date'],references['Transporter_ID'],references['lspName'],calc_references],axis=1)
df_references.columns = ['Submission_Date','Transporter_ID','lspName','% references completion']

reference_dataframe = pd.DataFrame()
for i in range(0,len(references)):
    ref = pd.DataFrame([[references['lspName'][i], references['year'][i], references['clientRef1'][i],references['contactName1'][i],references['contactPhone1'][i],references['contactEmail1'][i]],
                      [references['lspName'][i], references['year'][i], references['clientRef2'][i],references['contactName2'][i],references['contactPhone2'][i],references['contactEmail2'][i]],
                      [references['lspName'][i], references['year'][i], references['clientRef3'][i],references['contactName3'][i],references['contactPhone3'][i],references['contactEmail3'][i]],
                      [references['lspName'][i], references['year'][i], references['clientRef4'][i],references['contactName4'][i],references['contactPhone4'][i],references['contactEmail4'][i]],
                      [references['lspName'][i], references['year'][i], references['clientRef5'][i],references['contactName5'][i],references['contactPhone5'][i],references['contactEmail5'][i]]],
                      columns = ['lspName','year','Client','Contact Name','Phone','Email-ID'])  
    reference_dataframe = reference_dataframe.append(ref, sort = False)
reference_dataframe = reference_dataframe.fillna(0)
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != '0']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != 'a']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != 'na']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != 'XYZ']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != '-']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != 'Na']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != 'x']
reference_dataframe = reference_dataframe[reference_dataframe['Client'] != '1']
#-----------------------------------------------------------------------------#
#-------------------'''Top 5 companies to get business from'''----------------#
#top_5_cmp_business = new_metadata[['Transporter_ID','lspName','year', 'companyName1','location1',
#                                                               'companyName2','location2',
#                                                               'companyName3','location3',
#                                                               'companyName4','location4',
#                                                               'companyName5','location5','other_companies_interested','lane_attachment']]

calc_business = completion_value(top_5_cmp_business)
calc_business.columns = ['% business completion']
df_business = pd.concat([top_5_cmp_business['Submission_Date'],top_5_cmp_business['Transporter_ID'],top_5_cmp_business['lspName'],calc_business],axis=1)
#-----------------------------------------------------------------------------#

#-------------------------'''Top 5 routes for backhaul'''---------------------#
#backhaul = new_metadata[['Transporter_ID','lspName','year', 'origin1','destination1','truckType1','currentRate1',
#                                                     'origin2','destination2','truckType2','currentRate2',
#                                                     'origin3','destination3','truckType3','currentRate3',
#                                                     'origin4','destination4','truckType4','currentRate4',
#                                                     'origin5','destination5','truckType5','currentRate5','additional_backhaul','attachmentLink']]

calc_backhaul = completion_value(backhaul)
calc_backhaul.columns = ['% backhaul completion']
df_backhaul = pd.concat([backhaul['Submission_Date'],backhaul['Transporter_ID'],backhaul['lspName'],calc_backhaul],axis=1)
#-----------------------------------------------------------------------------#

#----------------------------'''Interests(Yes/No)'''--------------------------#
#interests = new_metadata[['Transporter_ID','lspName','year', 'Trial_load_from_company','Award_incentive_programme','Future_business_prospects','keyFocusAreas','contactedFurther']]

calc_interests = completion_value(interests)
calc_interests.columns = ['% interests completion']
df_interests = pd.concat([interests['Submission_Date'],interests['Transporter_ID'],interests['lspName'],calc_interests],axis=1)

#-----------------------------------------------------------------------------#
'''ANALYTICS'''
#-------------------------------'''Address'''---------------------------------#
#-----------------------------------------------------------------------------#

#-----------------------------Overall dataframe-------------------------------#
overall = pd.concat([contact['lspName'],df_manpower['% manpower completion'],
                     df_references['% references completion'],df_finance['% finance completion'],contact['year']],axis=1)

overall1 = pd.concat([contact['year'],df_contact,df_finance['% finance completion'],df_manpower['% manpower completion'],
                     df_references['% references completion'],
                     df_backhaul['% backhaul completion'],df_business['% business completion'],
                     df_clientelle['% top clientelle completion'],df_interests['% interests completion'],
                     df_ship['% ship tracking completion']],axis=1)
overall1['Overall RFI Completion(%)'] = ((overall1['% contact completion']+overall1['% finance completion']+overall1['% manpower completion']+overall1['% references completion']+overall1['% backhaul completion']+overall1['% business completion']+overall1['% top clientelle completion']+overall1['% interests completion']+overall1['% ship tracking completion'])/900)*100
overall1['Overall RFI Completion(%)'] = round(overall1['Overall RFI Completion(%)'],0)

#            writer = pd.ExcelWriter("RFI_completion.xlsx", engine = 'xlsxwriter')
#            overall1.to_excel(writer,sheet_name = 'overall_info_6-10-18')
#            writer.save()            

finance_asc = overall.sort_values('% finance completion')
finance_asc = finance_asc[['lspName','% finance completion']]
finance_asc = finance_asc.iloc[0:20,:]
finance_asc.columns = ['Vendor1','Completion perc1']

reference_asc = overall.sort_values('% references completion')
reference_asc = reference_asc[['lspName','% references completion']]
reference_asc = reference_asc.iloc[0:20,:]
reference_asc.columns = ['Vendor2','Completion perc2']

#            vehicle_asc = overall.sort_values('% vehicle completion')
#            vehicle_asc = vehicle_asc[['lspName','% vehicle completion']]
#            vehicle_asc = vehicle_asc.iloc[0:20,:]
#            vehicle_asc.columns = ['Vendor3','Completion perc3']

#top_20_dataframe = pd.concat([finance_asc,reference_asc,vehicle_asc],axis = 1)
#-----------------------------------------------------------------------------#

#----------------------------Lane Data Analysis-------------------------------#

#lane_data = pd.read_excel('Lane_data_working2.xlsx')
#lane_data['count'] = 1
#
#lane_work = lane_data[['LSP Name','Sector','OriginName','OriginState','OriginDirection','DestinationName','DestinationState','DestinationDirection','TruckType','Rate','AnnualVolume']]
#lane_work_cnt = lane_data[['LSP Name','Sector','OriginName','OriginState','OriginDirection','DestinationName','DestinationState','DestinationDirection','count']]
#
#lsp_unique_lanes = lane_work.drop_duplicates()
#lsp_unique_lanes_cnt = lane_work_cnt.drop_duplicates()
#
#unique_lsp_count = len(lane_data['LSP Name'].unique())
#unique_origins = len(lane_data['OriginName'].unique())
#unique_destination = len(lane_data['DestinationName'].unique())
#
#'''count unique lsp lanes'''
#
#lsp_lane_cnt = lsp_unique_lanes_cnt.groupby('LSP Name').count()
#lsp_lane_cnt = lsp_lane_cnt.reset_index()
#
#num1 = lsp_lane_cnt[['LSP Name','count']]
#
#'''sum of volume'''
#
#lsp_vol_spend = lane_data.groupby('LSP Name').sum()
#lsp_vol_spend = lsp_vol_spend.reset_index()
#lsp_vol_spend = lsp_vol_spend[['AnnualVolume','Spend(Lakh)']]
#
#conso = pd.concat([num1,lsp_vol_spend],axis=1)

#-----------------------------------------------------------------------------#

#---------------------------Year Estd and Sector------------------------------#
df_year_sector = pd.concat([contact['lspName'],contact['yearEstablished'],contact['year']],axis=1)
df_year_sector.columns= ['lspName','Year of Establishment','year']

#-----------------------------------------------------------------------------#

#--------------------------------Man Power------------------------------------#
#df_manpower = new_metadata[['lspName','year','management_cnt','driver_cnt','maintenance_cnt']]

manpower_transpose = pd.DataFrame()
for i in range(0,len(manpower)):
    man = pd.DataFrame([[manpower['lspName'][i], manpower['year'][i], 'Management', manpower['management_cnt'][i]],
                      [manpower['lspName'][i], manpower['year'][i],'Driver', manpower['driver_cnt'][i]],
                      [manpower['lspName'][i], manpower['year'][i],'Maintenance', manpower['maintenance_cnt'][i]]],
                      columns = ['lspName','year','Employees','Count'])  
    manpower_transpose = manpower_transpose.append(man, sort = False)

sector_dataframe = pd.DataFrame()
for i in range(0,len(top_clientelle)):
    sec = pd.DataFrame([[top_clientelle['lspName'][i], top_clientelle['year'][i], top_clientelle['clientName1'][i], top_clientelle['industry1'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName2'][i], top_clientelle['industry2'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName3'][i], top_clientelle['industry3'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName4'][i], top_clientelle['industry4'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName5'][i], top_clientelle['industry5'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName6'][i], top_clientelle['industry6'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName7'][i], top_clientelle['industry7'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName8'][i], top_clientelle['industry8'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName9'][i], top_clientelle['industry9'][i]],
                         [top_clientelle['lspName'][i], top_clientelle['year'][i],top_clientelle['clientName10'][i], top_clientelle['industry10'][i]
                      ]],
                      columns = ['lspName','year','Client_Name','Sector'])
    sector_dataframe = sector_dataframe.append(sec, sort = False)
    
sector_dataframe = sector_dataframe[sector_dataframe['Client_Name'] != 0]

#-----------------------------------------------------------------------------#
all_options = {k :g["year"].tolist() for k,g in contact.groupby('lspName')}
mode = {k :g['OriginName'].tolist() for k,g in lane.groupby('Type')}
state = {k :g["City"].tolist() for k,g in m.groupby('State')}
state1={'All' : m['City'].values.tolist()}
state.update(state1)
lsp = {k :g["lspName"].tolist() for k,g in m.groupby('City')}
lsp1={'All' : m['lspName'].values.tolist()}
lsp.update(lsp1)
total=m['lspName'].values.tolist()
total1=lane['LSP Name'].values.tolist()
total1=list(pd.unique(total1))
truck = {k :g["TruckType"].tolist() for k,g in lane.groupby(['OriginCluster','DestinationCluster'])}
truck1={('All','All') : lane["TruckType"].values.tolist()}
truck.update(truck1)
for i in truck.keys():
    truck[i].append("All")
truck2 = {k :g["TruckType"].tolist() for k,g in lane.groupby('OriginCluster')}
for i in truck2.keys():
    truck2[i].append("All")
truck3 = {k :g["TruckType"].tolist() for k,g in lane.groupby('DestinationCluster')}
for i in truck3.keys():
    truck3[i].append("All")
#---------------------------------GPS SCATTER PLOT----------------------------#
#all_options = {
#    2018 : ['ABC INDIA LTD', 'ADHUNIK TRANSPORT ORGANISATION LIMITED', 'AJAY TRANSPORT'],
#    2017 : ['ABHINAV TRANSPORT INDIA PVT LTD', 'BHARAT ROADWAYS', 'GLOBE ECOLOGISTICS PRIVATE LIMITED']}
#-----------------------------------------------------------------------------#
#            return render_template('upload2.html')
#        return render_template('upload.html')
#---------------------------------UI------------------------------------------#
dest = {k :g["DestinationName"].tolist() for k,g in lane.groupby('OriginName')}
dest1={'All' : lane["DestinationName"].values.tolist()}
dest.update(dest1)

vendor = {k :g['LSP Name'].tolist() for k,g in lane.groupby('OriginName')}
vendor1={'All' : lane['LSP Name'].values.tolist()}
vendor.update(vendor1)

destcluster = {k :g["DestinationName"].tolist() for k,g in lane.groupby("OriginCluster")}
for i in destcluster.keys():
    destcluster[i].append("All")
dest1={'All' : lane["DestinationName"].values.tolist()}
destcluster.update(dest1)
origincluster = {k :g['LSP Name'].tolist() for k,g in lane.groupby("OriginCluster")}
for i in origincluster.keys():
    origincluster[i].append("All")

lane_list=lane['LSP Name'].values.tolist()
color=['turquoise','#a52a2a','#006400','#ff00ff','#000080','#a020f0','#ffa500','#adff2f','#b03060','#0000ff','#ff0000','#556b2f','#32cd32']
#lspsector= {k :g['lspName'].tolist() for k,g in lspoverview.groupby('Sector')}
#lspclient= {k :g['lspName'].tolist() for k,g in lspoverview.groupby('Client')}      
originState = list(pd.unique(lane['OriginState']))
originState.append('All')

external_stylesheets = ['static/tab1.css']
external_scripts = ['E:/Rajkumar/tina_v0.1/static/java.js']
dash_app1 = Dash(__name__, server = server, url_base_pathname='/pathname/',external_scripts=external_scripts)
dash_app1.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
#dash_app1.scripts.append_script({"external_url":['E:/Rajkumar/tina_v0.1/static/java.js']})
dash_app1.config.supress_callback_exceptions = True
dash_app1.scripts.config.serve_locally = True
@dash_app1.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(),'static')
    return send_from_directory(static_folder,path)  
#dash_app1.layout +=gdc._js_dist(src="E:/Rajkumar/tina_v0.1/static/java.js")
   

@server.route('/dash',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('notify.html')       
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.' 
            return render_template('login.html',error=error)
        else:
            return dash_app1.index()
    
@server.route('/')
def log():
    return render_template('login.html')


@server.route('/main')
def main():
    return render_template('homepage.html')

tabs_styles = {
    'position':'absolute',
    'height': '100%',
    'width':'12%',
    'left':'0%',
    'top':'0%',
#    'backgroundImage':"url('sidebar.jpeg')",
#    'opacity':'0.5',
  'backgroundColor': '#7386d5',
  'color':'#2699fb'}
tabs_styles7 = {
    'position':'absolute',
    'height': '5%',
    'width':'15%',
    'right':'2%',
    'bottom':'0%',
  'backgroundColor': '#2699fb',
  'color':'#2699fb'}
tab_style7 = {
    'borderBottom': '1px solid #d6d6d6','padding': '2px','fontWeight': 'bold','fontSize': '16px','backgroundColor': 'white',
    'position':'absolute','height': '99%','width':'49%','left':'1%','top': '1%'}
tab_style8 = {
    'borderBottom': '1px solid #d6d6d6','padding': '2px','fontWeight': 'bold','fontSize': '16px','backgroundColor': 'white',
    'position':'absolute','height': '99%','width':'49%','right':'1%','top': '1%'}
tab_selected_style7 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '16px','padding': '2px','height': '99%','width':'49%','position':'absolute',
    'left':'1%','top': '1%'}
tab_selected_style8 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '16px','padding': '2px','position':'absolute','height': '99%','width':'49%',
    'right':'1%','top': '1%'}
tab_style5 = {
    'borderBottom': '1px solid #d6d6d6','padding': '5px','fontWeight': 'bold','fontSize': '12px','backgroundColor': 'white',
    'position':'absolute','height': '5%','width':'80%','left':'10%','top': '15%'}
tab_style1 = {
    'borderBottom': '1px solid #d6d6d6','padding': '5px','fontWeight': 'bold','fontSize': '12px','backgroundColor': 'white',
    'position':'absolute','height': '5%','width':'80%','left':'10%','top': '22%'}
tab_style2 = {
    'borderBottom': '1px solid #d6d6d6','padding': '5px','fontWeight': 'bold','fontSize': '12px','backgroundColor': 'white',
    'position':'absolute','height': '5%','width':'80%','left':'10%','top': '29%'}
tab_style3 = {
    'borderBottom': '1px solid #d6d6d6','padding': '5px','fontWeight': 'bold','fontSize': '12px','backgroundColor': 'white',
    'position':'absolute','height': '5%','width':'80%','left':'10%','top': '36%'}
tab_style0 = {
    'borderBottom': '1px solid #d6d6d6','padding': '5px','fontWeight': 'bold','fontSize': '12px','backgroundColor': 'white',
    'position':'absolute','height': '5%','width':'80%','left':'10%','top': '43%'}
tab_style4 = {
    'borderBottom': '1px solid #d6d6d6','padding': '5px','fontWeight': 'bold','fontSize': '12px','backgroundColor': 'white',
    'position':'absolute','height': '5%','width':'80%','left':'10%','top': '50%'}


tab_selected_style5 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '12px','padding': '5px','height': '5%','width':'80%','position':'absolute',
    'left':'10%','top': '15%'}
tab_selected_style1 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '12px','padding': '5px','height': '5%','width':'80%','position':'absolute',
    'left':'10%','top': '22%'}

tab_selected_style2 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '12px','padding': '5px','height': '5%','width':'80%','position':'absolute',
    'left':'10%','top': '29%'}
tab_selected_style3 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '12px','padding': '5px','height': '5%','width':'80%','position':'absolute',
    'left':'10%','top': '36%'}
tab_selected_style0 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '12px','padding': '5px','height': '5%','width':'80%','position':'absolute',
    'left':'10%','top': '43%'}
tab_selected_style4 = {
    'borderTop': '1px solid #d6d6d6','borderBottom': '1px solid #d6d6d6','backgroundColor': '#abe481',
    'fontWeight': 'bold','fontSize': '12px','padding': '5px','height': '5%','width':'80%','position':'absolute',
    'left':'10%','top': '50%'}

tabs_styles1 = {'height': '30px'}
tab_style = {
    'borderBottom': '1px solid #d6d6d6', 'padding': '4px', 'fontWeight': 'bold','fontSize': '10px'}

tab_selected_style = {'borderTop': '1px solid #d6d6d6', 'borderBottom': '1px solid #d6d6d6', 'backgroundColor': '#119DFF',
                      'color': 'white','padding': '4px','fontSize': '10px'}
#summary1 = [html.Div([
#        html.Link(href='/static/tab1.css',rel='stylesheet'),
#        html.Div([html.P('Number of LSPs'),html.H1(id = 'id1')], className="indi1"),
#        html.Div([html.P('Number of Lanes'),html.H1(id = 'id2')], className="indi2"),
#        html.Div([html.P('Number of Vehicles'),html.H1(id = 'id3')], className="indi3"),
#        html.Div([html.P('Volume (MT)'),html.H1(id = 'id4')], className="indi4"),
#        html.Div([html.P('Spend (INR)'),html.H1(id = 'id5')], className="indi5"),
##        html.Div([dcc.Graph(id='top1',config={'displayModeBar':False})], className="topvolume"),
##        html.Div([dcc.Graph(id='top2',config={'displayModeBar':False}),], className="topspend"),
#        html.Div([dcc.Graph(id='top3',config={'displayModeBar':False}),], className="topveh"),
#        ], className="row")]

summary=[html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
    html.Div([html.P('Number of Lanes'),html.H1(id = 'id2')], className="button2"),
                  html.Div([html.P('Total LSPs'),html.H1(id = 'id1')], className="check1"),
           html.Div([ html.Div([ html.H1('From')], className="d1"),    html.Div([                                 
                        dcc.Checklist(id="radio2",
                        options=[{'label': 'East', 'value': 'E'},
                            {'label': 'North', 'value': 'N'},
                            {'label': 'South', 'value': 'S'},
                            {'label': 'West', 'value': 'W'},], values=['',''],
                                     labelStyle={'display': 'inline-block','padding':'3.5%'})], className="origindir"),                          
    html.Div([ html.H1('To')], className="d2"),            
    html.Div([
                        dcc.Checklist(id="radio3",
                        options=[{'label': 'East', 'value': 'E'},
                            {'label': 'North', 'value': 'N'},
                            {'label': 'South', 'value': 'S'},
                            {'label': 'West', 'value': 'W'},], values=['',''],
                                     labelStyle={'display': 'inline-block','padding':'3.5%'})], className="destdir"),], className="check2"),
          html.Div([html.P('Selected LSPs Count'),html.H5(id = 'lspcount4')], className="summary1"),                                              
            html.Div([dcc.Graph(id='direction',style={'height':'100%'},config={'displayModeBar':False}),], className="dir"),
            ], className="row")]
        
#lane1=[html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
#                        html.Div([html.H5('LSP Name'),
#                dcc.Dropdown(
#                        id='dropdown6',multi=True,
#                        options=[{'label': i, 'value': i} for i in lane['LSP Name'].unique()],
#                        value='Core Logistic')], className="div23"),
##                html.Div([html.H5('Map'),
##                        dcc.Graph(id='lane'),
##                        ], className="div24"),
#                    html.Div([html.H5('Lanes by Volume'),
#                        dcc.Graph(id='lane1',config={'displayModeBar':False}),
#                        ], className="div30"),
#            html.Div([html.A('Export table',
#                        id='download1',
#                        download="LanesByVolume.csv",
#                        href="",target="_blank")], className="down1")], className="row6")]
#lane2=[html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
#                        html.Div([html.H5('Origin'),
#                dcc.Dropdown(
#                        id='dropdown7',
#                        options=[{'label': i, 'value': i} for i in lane['OriginName'].unique()],
#                        value='PUNE')], className="div25"),
#                        html.Div([html.H5('LSP Name'),
#                dcc.Dropdown(
#                        id='dropdown9',multi=True,
#                        value='Ujjawal Logistics')], className="div27"),
#        html.Div([html.P('LSPs Count'),html.P(id = 'lsp')], className="count"),
#                html.Div([html.H5('Map'),
#                        dcc.Graph(id='origin'),
#                        ], className="div28"),
#                    html.Div([html.H5('Lanes by Volume'),
#                        dcc.Graph(id='origin1',config={'displayModeBar':False}),
#                        ], className="div29"),
#                html.Div([html.A('Export table',
#                        id='download2',
#                        download="ExOrigin.csv",
#                        href="",target="_blank")], className="down2")], className="row7")]
#@dash_app1.callback(
#    Output('dropdown9', 'options'),
#    [Input('dropdown7', 'value')])
#def set_cities_options(value):
#    code=lane[lane['OriginName']==value]['OriginCluster'].iloc[0]
#    return [{'label': i, 'value': i} for i in np.unique(origincluster[code])]
#
#tab3 = [html.Div([
#                        html.Link(href='/static/tab1.css',rel='stylesheet'),
#    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
#        dcc.Tab(label='LSP NETWORK', children=lane1, style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='Ex. Origin', children=lane2, style=tab_style, selected_style=tab_selected_style),
#    ], style=tabs_styles1)
#        ], className="row3") ]
    
dashboard=[html.Div([
        html.Link(href='/static/tab1.css',rel='stylesheet'),
        html.Link(href='/static/button.css',rel='stylesheet'),
        html.Link(href='/static/java.js',rel='script'),
        html.Div([html.P('LSP Name:'),html.P(id = 'vendorname')], className="lspname"),
                        html.Div([html.H5('Year'),
                dcc.Dropdown(
                        id='dropdown2',value=2018
                        )], className="div6"),                          
                    html.Div([                                                                    
                        dcc.Graph(id='table1',style={'height':'100%','backgroundColor': '#f1f1f1'},config={'displayModeBar':False}),
                      ], className="div2"),
#                        html.Div([                                                                    
#                        dcc.Graph(id='table5',config={'displayModeBar':False}),
#                      ], className="div9"),
                            html.Div([                                                                    
                        dcc.Graph(id='table8',style={'height':'100%'},config={'displayModeBar':False}),
                      ], className="div13"),
                html.Div([
            html.Div([dcc.RadioItems(id='radio5',options=[{'label': i, 'value': i} for i in ['Branch','Details','Lanes']], 
                value= 'Branch',labelStyle={'display': 'inline-block','padding':'3%'})], className="button3"), 
                 html.Div([dcc.Graph(id='lane',style={'height':'100%'},config={'displayModeBar':False}), ],className="net")
                                                                         ], className="network"),
                html.Div([html.H5('Finance Summary'),
                dcc.Graph(id='map',style={'height':'100%'},config={'displayModeBar':False})
                ], className="div8"),
                    html.Div([html.H5('Manpower'),                                                                    
                        dcc.Graph(id='table4',style={'height':'100%'},config={'displayModeBar':False}),
                      ], className="div7"),
            html.Div([html.H5('Clients'),
                                dcc.Graph(id='client',style={'height':'100%'},config={'displayModeBar':False}),
                                ], className="div15"),
                    html.Div([html.H5('Contact Details'),                                                                    
                        dcc.Graph(id='table7',style={'height':'100%'},config={'displayModeBar':False}),
                      ], className="div10"),
                    html.Div([html.H5('Fleet Details'),                                                                    
                        dcc.Graph(id='table6',style={'height':'100%'},config={'displayModeBar':False}),
                      ], className="div11"),
    html.Div([html.Button(id='submit-button3', type='submit', children='Shortlist',className="btn btn1")], className="short")
            ], className="row1")]
    
tab4 = [html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
        html.Div([html.H5('Origin State'),                                 
                dcc.Dropdown(
                        id='state1',multi=True,
                        options=[{'label': i, 'value': i} for i in np.unique(sorted(originState))],
                        value="Maharashtra", className="state")], className="state1"), 
                        html.Div([html.H5('Origin Location'),                                 
                dcc.Dropdown(
                        id='dropdown10',multi=True,value="All")], className="div33"), 
            html.Div([html.H5('Destination State'),                                 
                dcc.Dropdown(
                        id='state2',multi=True,value="Tamil Nadu")], className="state2"), 
                        html.Div([html.H5('Destination Location'),                                 
                dcc.Dropdown(
                        id='dropdown11',multi=True,value="All")], className="div34"),  
                        html.Div([html.H5('Industry'),                                 
                dcc.Dropdown(
                        id='sector1',multi=True,value="All")], className="sector1"),                           
                    html.Div([                                                                    
                        dcc.Graph(id='view',style={'height':'100%'},config={'displayModeBar':False}),], className="div36"),
                html.Div([dcc.RadioItems(id='radio4',value= ''),], className="div37"),
        html.Div([html.P('LSPs Count'),html.H5(id = 'lspcount')], className="summary2"),
        dcc.Tabs(id="initiate", value='tab-2', children=[
        dcc.Tab(label='View RFI', children=dashboard, style=tab_style7, selected_style=tab_selected_style7),
        dcc.Tab(label='Back', value='tab-2', style=tab_style8, selected_style=tab_selected_style8),
    ], style=tabs_styles7),], className="row5") ]
   
#rfi = [html.Div([
#            html.Link(href='/static/tab1.css',rel='stylesheet'),
#    dcc.Tabs(id="RFI", value='tab-1', children=[
#        dcc.Tab(label='DASHBOARD', children='tab-1', style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='COMPANY DETAILS', value='tab-2', style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='FINANCIAL DETAILS', value='tab-3', style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='VEHICLE DETAILS', value='tab-4', style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='CLIENTELLE', value='tab-5', style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='LANE DETAILS', value='tab-6', style=tab_style, selected_style=tab_selected_style),
#    ], style=tabs_styles1)
#        ], className="row4")] 
shortlisted=[html.Link(href='/static/tab1.css',rel='stylesheet'),
                     html.Link(href='/static/button.css',rel='stylesheet'),
        html.Link(href='/static/java.js',rel='script'),
            html.Div([ html.Div([html.H5(id='dummy1')]),
            html.Div([html.H5('Shortlisted LSPs'),
                                dcc.Graph(id='shortlist',style={'height':'100%'},config={'displayModeBar':False})], className="shorted"),
html.Div([dcc.ConfirmDialogProvider(children=html.Button(id='submit-button4', type='submit', children='Request Meeting',className="btn btn1"),
        id='alert1',
        message='Meeting scheduled! Please check your email for further details.'),html.Div(id='output1')], className="book"),
html.Div([dcc.ConfirmDialogProvider(children=html.Button(id='submit-button5', type='submit', children='Request Reference Check',className="btn btn1"),
               id='alert2',
        message='Your request has been acknowledged, Our team will get back to you.'),html.Div(id='output2')], className="refcheck"),
html.Div([dcc.ConfirmDialogProvider(children=html.Button(id='submit-button6', type='submit', children='Request LSP Details',className="btn btn1"),
               id='alert3',
        message='Your request has been acknowledged, Our team will get back to you.'),html.Div(id='output3')], className="details")
                                                                                            ,], className="ct")]
    
#overview = [html.Div([
#    dcc.Tabs(id="overview", value='tab-1', children=[
#        dcc.Tab(label='Sector Wise LSP', children=sector, style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='Client Wise LSP', children=client, style=tab_style, selected_style=tab_selected_style),
#    ], style=tabs_styles1)
#        ], className="row3") ]
click5=0   
@dash_app1.callback(Output('output1', 'children'),
              [Input('alert1', 'submit_n_clicks'),Input('submit-button3', 'n_clicks')])
def update_output(clicks,value):
    global click5
    if value==0:
        return 'Please shortlist LSPs'
    elif clicks>click5:
        click5=clicks
        return ''
click4=0   
@dash_app1.callback(Output('output2', 'children'),
              [Input('alert2', 'submit_n_clicks')])
def update_output(clicks):
    global click4
    if clicks>click4:
        click4=clicks
        return ''
click3=0   
@dash_app1.callback(Output('output3', 'children'),
              [Input('alert3', 'submit_n_clicks')])
def update_output(clicks):
    global click3
    if clicks>click3:
        click3=clicks
        return ''
    
clientteam =[html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
                               html.Link(href='/static/button.css',rel='stylesheet'),
        html.Link(href='/static/java.js',rel='script'),
             html.Div(id='target1'),
             html.Div(
                     [html.H4('Name:'),
              dcc.Input(id='name1', value='', type='text'),
   html.H5('Designation:'),
              dcc.Input(id='designation1', value='', type='text'),
   html.H4('LSP Name:'),
   dcc.Dropdown(
                id='lspname1',
                options=[{'label': i, 'value': i} for i in contact['lspName'].unique()],
                value=None,className="lspname1"),
   html.H4('Rating:'),
   dcc.Dropdown(
                id='rating1',
                options=[{'label': i, 'value': i} for i in [1,2,3,4,5]],
                value=None,className="rating1"),
    html.H5('Feedback:'),
        dcc.Textarea(id='comment1',placeholder='Enter a feedback...',value='',style={'width': '100%'}),
    html.Button(id='submit-button2', type='submit', children='Submit',className="btn btn1"),
    html.Div(id='confirm1',className="msg1"),html.Div(id='confirm2',className="msg2"),html.Div(id='confirm3',className="msg3"),], className="form2"),
        ], className="clientteam")]


#comment = [html.Div([
#    dcc.Tabs(id="comment2", value='tab-1', children=[
#        dcc.Tab(label='Client', children=clientteam, style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='LSP Team', children=lspteam, style=tab_style, selected_style=tab_selected_style),
#    ], style=tabs_styles1)
#        ], className="feed") ]
address= [html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
             html.Div([html.H1('LOGISTICSNOW PVT. LTD.'),html.P('409, Neptune Flying Colors, LBS Cross Road, Mulund West, Mumbai 400080, Contact: 9930526189')],className="add")],className="address")]
lsplist=list(reviewfile['LSP Names'])
lsplist.append('All')
review = [html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
             html.Link(href='/static/button.css',rel='stylesheet'),
        html.Link(href='/static/java.js',rel='script'),
             html.Div([  html.H5('LSP Name'),
   dcc.Dropdown(id='lsprev',options=[{'label': i, 'value': i} for i in pd.unique(sorted(lsplist))],multi=True,value='All'),],className="lsprev"),
             html.Div([  html.H5('Sort By Rating:'),
   dcc.Dropdown(id='shortby',options=[{'label': i, 'value': i} for i in ['Largest to Smallest','Smallest to Largest']],value='Largest to Smallest'),],className='shortby'),
   html.Div([html.H5('Rating:'),dcc.Dropdown(id='rating2',options=[{'label': str(i)+' & above', 'value': i} for i in [1,2,3,4]],value=3),],className="rating2"),
    html.Div([dcc.Graph(id='reviewtab',style={'height':'100%'},config={'displayModeBar':False})],className="reviewtab"),],className="review")]
    ############ Dashboard layout #########################################

dash_app1.layout= html.Div([html.Link(href='/static/tab1.css',rel='stylesheet'),
#        html.Div([
#                html.Div([html.Img(src=dash_app1.get_asset_url('lsp.jpg'))],className="icon1")
#                ],className="main"),
                html.Div([html.H1('Transport Intelligence & Network Application (TINA)')], className="bar"),
        html.Div(
        children =[dcc.Tabs(id="tabs", value='tab-2',vertical=True, children=[
        dcc.Tab(label='Shortlisted LSPs', children=shortlisted,style=tab_style2 , selected_style=tab_selected_style2),
        dcc.Tab(label='Master Summary', children=summary,style=tab_style5 , selected_style=tab_selected_style5),
        dcc.Tab(label='LSPs By Lane', children=tab4,style=tab_style1, selected_style=tab_selected_style1),
        dcc.Tab(label='Feedback', children=clientteam,style=tab_style0, selected_style=tab_selected_style0),
        dcc.Tab(label='LSPs Review', children=review,style=tab_style3, selected_style=tab_selected_style3),
#        dcc.Tab(label='CONTACT US', children=address,style=tab_style4, selected_style=tab_selected_style4),
        ],style=tabs_styles),
         html.Div([html.A('Logout',href="/")],className="div32")
    ],className="body")])

#@dash_app1.callback(Output('target', 'children'),
#                  [Input('submit-button1', 'n_clicks'),Input('lspname', 'value')],
#                  [State('name', 'value'),State('designation', 'value'),State('contact', 'value')
#                  ,State('phone', 'value'),State('email', 'value'),State('comment', 'value')])
#def update_output(clicks,lsp,name,designation,point,contactNum,email,comment):
#    date_time = dt.datetime.now()
#    date = date_time.date()
#    time = date_time.time()
#    engine = create_engine('mysql+mysqlconnector://root:root@localhost/lsp_master_test',echo = False)
#    feedback = pd.DataFrame({'LSP_Name':[lsp],'Date':[date],'Time':[time],'Name_of_Person':[name],'Designation':[designation],'Point_of_contact':[point],'email-id':[email],'Phone_number':[contactNum],'Feedback':[comment]})    
#    return feedback.to_sql(name='feedback_lsp_team',con=engine,if_exists='append',index=False)
click1=0

@dash_app1.callback(Output('confirm1', 'children'),
              [Input('submit-button2', 'n_clicks')],
              [State('name1', 'value')])
def display_confirm(value1,value2):
    global click1
    if value2 =='' and value1>=click1:
        click1 = value1
        return 'Please enter your name.'
    else:
        return ''
val2=''
click=0
@dash_app1.callback(Output('confirm2', 'children'),
              [Input('submit-button2', 'n_clicks'),Input('lspname1', 'value')])
def display_confirm(value1,value2):
    global click
    global val2
    if value2==None and value1>=click:
        msg= 'Please choose LSP Name.'
    else:
        msg= ''
    click = value1
    val2=value2
    return msg
val3=''
click3=0
@dash_app1.callback(Output('confirm3', 'children'),
              [Input('submit-button2', 'n_clicks'),Input('rating1', 'value')])
def display_confirm(value1,value2):
    global click3
    global val3
    if value2 ==None and value1>=click3:
        msg= 'Please give rating to LSP.'
    else:
        msg= ''
    click3 = value1
    val3 = value2
    return msg
@dash_app1.callback(Output('target1', 'children'),
                  [Input('submit-button2', 'n_clicks'),Input('lspname1', 'value'),Input('rating1', 'value')],
                  [State('name1', 'value'),State('designation1', 'value'),State('comment1', 'value')])
def update_output(clicks,lsp,rating,name,designation,comment):
    if name is '' or lsp is '':
        return True
    else:
        date_time = dt.datetime.now()
        date = date_time.date()
        time = date_time.time()
        engine = create_engine('mysql+mysqlconnector://root:root@localhost/lsp_master_test',echo = False)
        feedback1 = pd.DataFrame({'LSP_Name':[lsp],'Date':[date],'Time':[time],'Name_of_Person':[name],'Designation':[designation],'Feedback':[comment],'Rating':[rating]})    
        return feedback1.to_sql(name='feedback_client',con=engine,if_exists='append',index=False)    

vendor=pd.DataFrame(columns=['lspName','Person Name','Designation','Email ID','# vehicle'])                              
click = 0
@dash_app1.callback(Output('shortlist', 'figure'),
                  [Input('submit-button3', 'n_clicks'),Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_output(clicks,lsp,year):
    global vendor
    global click
    over = contact_dataframe[contact_dataframe['year'] == year].iloc[:,np.r_[0,2:4,6]]
    contact = over[over['lspName']==lsp]
    over1 = vehicle_dataframe[vehicle_dataframe['year'] == year].iloc[:,np.r_[0,2:5]]
    veh = over1[over1['lspName']==lsp]
    number=sum(veh['Self Owned'])+sum(veh['Attached'])
    contact['# vehicle'] = number
    vendor=vendor.append(contact,sort=False)
    vendor = vendor.drop_duplicates()
    if click == 0:
#        elif len(vendor) == 0:           
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgb(50, 50, 50)'),
        align = 'left',
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['NO LSP SELECTED']],
                font=dict(size=30,color='#000000'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'center',
                height = 50,
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        click = 1
#        figure = {'data': [table], 'layout': layout} 
#        return figure
    elif clicks == click:
        table = go.Table(
        columnwidth=[0.3,0.15,0.15,0.3,0.1],
        header=dict(
        values=['LSP Name','Contact Name','Designation','Email ID','Total Number of Vehicle'],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgb(50, 50, 50)'),
        align = 'left',
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[vendor[k].tolist() for k in vendor.columns[0:]],
                font=dict(size=9,color='#000000'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        click = clicks+1
    figure = {'data': [table], 'layout': layout}    
    return figure

click1=0
@dash_app1.callback(Output('dummy1', 'children'),
                  [Input('submit-button4', 'n_clicks')])
def update_output(clicks):
    global click1
    if clicks > click1:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("keyccnts@gmail.com", "sricity1")    
#        client_name = "Rajkumar"
#        LSP_name = "MD Movers"
        text = "Hello, admin wants to book a meeting with LSP"   
        fromaddr = "keyccnts@gmail.com"
        toaddr = "projects@logisticsnow.in"    
        server.sendmail(fromaddr, toaddr, text)
        click1 = clicks
    return None

def change_var(variable):
    if type(variable)==str:
        variable = [variable]
    else:
        pass
    return variable

def dirt(val2,val3):
    val2 = change_var(val2)
    val3 = change_var(val3)
#    if val2[0]=='All':
#        option1=lane
#    else:       
    option1=lane[lane['OriginDirection'].isin(val2)] 
#    if val3[0]=='All':
#        option=option1
#    else:
    option=option1[option1['DestinationDirection'].isin(val3)] 
    return option

@dash_app1.callback(      
     Output('lspcount4','children'),
    [Input('radio2', 'values'),Input('radio3', 'values')])
def update_graph(val2,val3):
    option=dirt(val2,val3)
    count=len(pd.unique(option['LSP Name']))
    x="{:,}".format(count)
#    lsp=str(count)
#    '{}/{}'.format(lsp, count_lsps)
    return x

@dash_app1.callback(      
     Output('vendorname','children'),
    [Input('radio4', 'value')])
def update_graph(value):
    return value

@dash_app1.callback(
     Output('direction','figure'),
    [Input('radio2', 'values'),Input('radio3', 'values')])
def update_graph(val2,val3):
    mapbox_access_token = 'pk.eyJ1IjoicmFqaWl0YjY5IiwiYSI6ImNqbmozZDd4aDB2ZTYzcG9zNWNzbnB5dTEifQ.dfwwo4R4cZFklzRIID6snA'
    layout = go.Layout(autosize=True, hovermode='closest',showlegend=False,
                   legend = dict(x= 0, y= 1,font = dict(size = 8)),margin={'l': 0, 'b': 0, 't': 0,'r': 0},
               mapbox=dict(accesstoken=mapbox_access_token,bearing=0,
                           center=dict(lat=21.153, lon=79.083),
                           pitch=0, zoom=4,style='mapbox://styles/rajiitb69/cjpp4ernb02n52sjjcckrmfwg')) 

    if len(val2)>1 or len(val3)>1: 
        direction=dirt(val2,val3)
        direction1=direction.drop_duplicates(['OriginCluster','DestinationCluster'])    
        data=[]
        for i in range(0,len(direction1)): 
            data.append(
                        go.Scattermapbox(lon = [direction1['OriginLongitude'].iloc[i], direction1['DestinationLongitude'].iloc[i]],
            lat = [direction1['OriginLatitude'].iloc[i], direction1['DestinationLatitude'].iloc[i]],
            mode = 'lines',showlegend=False,
            line = dict(width =1,color = 'turquoise'),)) 
    
        lon1=pd.DataFrame(direction1['OriginLongitude'])
        lon2=pd.DataFrame(direction1['DestinationLongitude'])

        lat1=pd.DataFrame(direction1['OriginLatitude'])
        lat2=pd.DataFrame(direction1['DestinationLatitude'])

        name1=pd.DataFrame(direction1['OriginName'])
        name2=pd.DataFrame(direction1['DestinationName'])

#        points=[go.Scattermapbox(lat = lat['OriginLatitude'], lon=lon['OriginLongitude'], mode='markers+text', marker=dict(size=3,color='#2699fb'),
#                                 text=name['OriginName'],showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]             
        point1=[go.Scattermapbox(lat = lat1['OriginLatitude'], lon=lon1['OriginLongitude'], mode='markers+text', marker=dict(size=8,color='#f9a602'),
                                 text=name1['OriginName'],textposition='top center',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]         
        point2=[go.Scattermapbox(lat = lat2['DestinationLatitude'], lon=lon2['DestinationLongitude'], mode='markers+text', marker=dict(size=8,color='blue'),
                                 text=name2['DestinationName'],textposition='top center',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]         
        figure = {'data': data+point1+point2, 'layout': layout}    
        return figure
    else:
        points=[go.Scattermapbox(lat = ['21.153'], lon=['79.083'], mode='markers', marker=dict(size=0.5,color='#ffffff'),
                             showlegend=False)]             
        figure = {'data': points, 'layout': layout} 
        return figure

z=0
@dash_app1.callback(      
     Output('reviewtab','figure'),
    [Input('lsprev', 'value'),Input('shortby', 'value'),Input('rating2', 'value')])
def update_graph(val1,val2,val3):
    global z
    val1 = change_var(val1)
    if val1[0]=='All':
        lsptable=reviewfile
    else:
        lsptable=reviewfile[reviewfile['LSP Names'].isin(val1)]
    if val2=='Largest to Smallest':
        lsptable=lsptable.sort_values(['Ratings'], ascending=[False])
    elif val2=='Smallest to Largest':
        lsptable=lsptable.sort_values(['Ratings'], ascending=[True])
    lsptable=lsptable[lsptable['Ratings']>=val3]
    lsptable.sort_values('LSP Names')
    table = go.Table(
    columnwidth=[0.3, 0.2,0.1,0.4],
    header=dict(
        values=['LSP Name','Headquarter','Rating','Reviews'],
        font=dict(size=15,color='#FFFFFF'),
        line = dict(color='rgb(50, 50, 50)'),
        align = 'center',
        fill = dict(color='#2699fb'),
    ),
    cells=dict(
        values=[lsptable[k].tolist() for k in lsptable.columns[1:]],
        font=dict(size=10,color='#000000'),
        line = dict(color='rgb(50, 50, 50)'),
        align = 'left',
        fill = dict(color='#f5f5fa')))
    layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 10})
    figure = {'data': [table], 'layout': layout}
    return figure
    

#@dash_app1.callback(
#     Output('top3','figure'),
#    [Input('radio4', 'value')])
#def update_graph(value):
#    trace = [
#    {
#      "values": pd.Series(major_trucks.head(5)['Count']),
#      "labels": pd.Series(major_trucks.head(5)['TruckType']),
#      "domain": {"x": [0, 0.8]},
#      "name": value,
#      "hoverinfo":"value+label",
#      "textinfo":"percent",
#      "textposition":"inside",
#      "textfont":{"size":12},
#      "hole": .4,
#      "type": "pie"
#    }]
#    layout= {'showlegend': True,'height':250,'margin':{'l': 10, 'b': 5, 't': 40,'r': 100},
#             "title":"MAJOR TRUCK TYPES",
#             'legend':{'x': 1.3, 'y': 0.8, 'font':{'size':10}},
#        "annotations": [
#            {
#                "font": {
#                    "size": 12
#                },
#                "showarrow": False,
#                "text": "",
#                "x": 0.5,
#                "y": 0.5}]}
#    figure = {'data': trace, 'layout': layout}
#    return figure
 
@dash_app1.callback(
    Output('id1', 'children'),
    [Input('radio4', 'value')])
def set_cities_options(value):
    return count_lsps
@dash_app1.callback(
    Output('id2', 'children'),
    [Input('radio4', 'value')])
def set_cities_options(value):
    x="{:,}".format(count_of_unique_lanes)
    return x
@dash_app1.callback(
    Output('id3', 'children'),
    [Input('radio4', 'value')])
def set_cities_options(value):
    x="{:,}".format(count_of_trucks)
    return x
@dash_app1.callback(
    Output('id4', 'children'),
    [Input('radio4', 'value')])
def set_cities_options(value):
    x="{:,}".format(volume_sum_lsp)
    return x
@dash_app1.callback(
    Output('id5', 'children'),
    [Input('radio4', 'value')])
def set_cities_options(value):
    x="{:,}".format(spend_sum_lsp)
    return x


def fun(state1,origin):
    origin = change_var(origin)
    state1 = change_var(state1)
    if state1[0]=='All':
        state2=lane
    else:
        state2=lane[lane['OriginState'].isin(state1)]
    if origin[0]=='All':
        city2 = state2
    else:
        code1=state2[state2['OriginName'].isin(origin)]['OriginCluster']
        code1 = list(pd.unique(code1))
        city2=state2[state2['OriginCluster'].isin(code1)]
    return city2
@dash_app1.callback(
    Output('dropdown2', 'options'),
    [Input('radio4', 'value')])
def set_cities_options(selected_lsp):
    return [{'label': i, 'value': i} for i in all_options[selected_lsp]]
    
@dash_app1.callback(
    Output('dropdown10', 'options'),
    [Input('state1', 'value')])
def set_cities_options(state1):
    state1 = change_var(state1)
    if state1[0]=='All':
        state2=lane
    else:
        state2=lane[lane['OriginState'].isin(state1)]
    city1 = list(pd.unique(state2['OriginName']))
    city1.append('All')
    return [{'label': i, 'value': i} for i in sorted(city1)]
@dash_app1.callback(
    Output('state2', 'options'),
    [Input('state1', 'value'),Input('dropdown10', 'value')])
def set_cities_options(state1,origin):
    city2=fun(state1,origin)
    city = list(pd.unique(city2['DestinationState']))
    city.append('All')
    return [{'label': i, 'value': i} for i in sorted(city)]
@dash_app1.callback(
    Output('dropdown11', 'options'),
    [Input('state1', 'value'),Input('dropdown10', 'value'),Input('state2', 'value')])
def set_cities_options(state1,origin,state2):
    city2=fun(state1,origin)
    state2 = change_var(state2)
    if state2[0]=='All':
        city2=city2
    else:
        city2=city2[city2['DestinationState'].isin(state2)]
    city = list(pd.unique(city2['DestinationName']))
    city.append('All')
    return [{'label': i, 'value': i} for i in sorted(city)]
@dash_app1.callback(
    Output('sector1', 'options'),
    [Input('state1', 'value'),Input('dropdown10', 'value'),Input('state2', 'value'),Input('dropdown11', 'value')])
def set_cities_options(state1,origin,state2,dest):
    city2=fun(state1,origin)
    state2 = change_var(state2)
    dest = change_var(dest)
    if state2[0]=='All':
        city2=city2
    else:
        city2=city2[city2['DestinationState'].isin(state2)]
    if dest[0]=='All':
        sector=city2
    else:
        code2=city2[city2['DestinationName'].isin(dest)]['DestinationCluster']
        code2 = list(pd.unique(code2))
        code2 = change_var(code2)
        sector=city2[city2['DestinationCluster'].isin(code2)]
    city = list(pd.unique(sector['Sector']))
    city.append('All')
    return [{'label': i, 'value': i} for i in sorted(city)]
           
@dash_app1.callback(
     Output('my-graph','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    dff = overall[overall['year'] == year_value]
    x= pd.Series((dff[dff['lspName']==value].set_index('lspName').transpose()).iloc[0:3,:][value])
    trace = go.Bar(y= pd.Series((dff[dff['lspName']==value].set_index('lspName').transpose()).iloc[0:3,:][value]),
                       x= ['ManPower','References','Finance'],text=x,textfont=dict(family='sans serif',size=10,color='rgb(0,0,0)'),width = .35, textposition = 'outside',
                               marker=dict(color='rgb(50, 171, 96)', line=dict(color='rgba(50, 171, 96, 1.0)',width=2,)))
    layout=go.Layout(
                   xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        domain=[0.15, 1]
    ),
    yaxis=dict(
        showgrid=True,
        showline=True,
        showticklabels=True,
        range=[0,105]

    ),height=300,
                margin={'l': 5, 'b': 20, 't': 20, 'r': 5},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
    figure = {'data': [trace], 'layout': layout}
    return figure 
 
@dash_app1.callback(
     Output('comp','figure'),
    [Input('radio4', 'value'),Input('year', 'value')])
def update_graph(value,year_value):
    dff = overall[overall['year'] == year_value]
    x= pd.Series((dff[dff['lspName']==value].set_index('lspName').transpose()).iloc[0:3,:][value])
    trace = go.Bar(y= pd.Series((dff[dff['lspName']==value].set_index('lspName').transpose()).iloc[0:3,:][value]),
                       x= ['ManPower','References','Finance'],text=x,textfont=dict(family='sans serif',size=10,color='rgb(0,0,0)'),width = .35, textposition = 'outside',
                               marker=dict(color='rgb(50, 171, 96)', line=dict(color='rgba(50, 171, 96, 1.0)',width=2,)))
    layout=go.Layout(
                   xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        domain=[0.15, 1]
    ),
    yaxis=dict(
        showgrid=True,
        showline=True,
        showticklabels=True,
        range=[0,105]

    ),height=300,
                margin={'l': 5, 'b': 20, 't': 20, 'r': 5},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
    figure = {'data': [trace], 'layout': layout}
    return figure 
@dash_app1.callback(
     Output('map','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    dfg = finance_dataframe[finance_dataframe['year'] == year_value]
    if len(dfg) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        height=20,
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=10,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                height=40,
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        r= pd.Series((dfg[dfg['lspName']==value].set_index('lspName').transpose()).iloc[2:6,:1:2][value])
        s= pd.Series((dfg[dfg['lspName']==value].set_index('lspName').transpose()).iloc[2:6,3:4][value])
        trace1 = go.Bar(y= pd.Series((dfg[dfg['lspName']==value].set_index('lspName').transpose()).iloc[2:6,:1:2][value]),
                           x= ['2014-15','2015-16','2016-17','2017-18'],text=r,textfont=dict(family='sans serif',size=10,color='rgb(0,0,0)'),width = .35, textposition = 'outside',
                                   marker=dict(color='rgb(55, 83, 109)'),name='Net Revenue (in Cr)')
        trace2 = go.Bar(y= pd.Series((dfg[dfg['lspName']==value].set_index('lspName').transpose()).iloc[2:6,3:4][value]),
                           x= ['2014-15','2015-16','2016-17','2017-18'],text=s,textfont=dict(family='sans serif',size=10,color='rgb(0,0,0)'), textposition = 'outside',
                                   marker=dict(color='rgb(26, 118, 255)'),name='Net Profit (in Cr)')
        data = [trace1, trace2]
        layout=go.Layout(
                       xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=True,
            showline=True,
            showticklabels=True,
            range=[0,max(r)*(1.1)]
        ),
                    margin={'l': 5, 'b': 20, 't': 60,'r': 5},
                    legend={'x': 0, 'y': 1.3, 'font':dict(
                family='sans-serif',
                size=10
            )},
                    hovermode='closest'
                )
        figure = {'data': data, 'layout': layout}
        return figure 


def xyz(o_name, d_name, o_state, d_state, sector):
    def change_var(variable):
        if type(variable)==str:
            variable = [variable]
        else:
            pass
        return variable
    o_state = change_var(o_state)
    o_name = change_var(o_name)
    d_state = change_var(d_state)
    d_name = change_var(d_name)
    sector = change_var(sector)
    if o_state[0] == 'All':
        dfg = lane
    else:
        dfg = lane[lane['OriginState'].isin(o_state)]
    if o_name[0] =='All':
        dfg = dfg
    else:
        code1=dfg[dfg['OriginName'].isin(o_name)]['OriginCluster']
        code1 = list(pd.unique(code1))
        dfg=dfg[dfg['OriginCluster'].isin(code1)]
    if d_state[0] =='All':
        dfg = dfg
    else:
        dfg = dfg[dfg['DestinationState'].isin(d_state)]
    if d_name[0] =='All':
        dfg = dfg
    else:
        code2=dfg[dfg['DestinationName'].isin(d_name)]['DestinationCluster']
        code2 = list(pd.unique(code2))
        dfg=dfg[dfg['DestinationCluster'].isin(code2)]
    if sector[0] == 'All':
        unique = list(pd.unique(dfg['Sector']))
        dfg = dfg[dfg['Sector'].isin(unique)]
    else:
        dfg= dfg[dfg['Sector'].isin(sector)]
    return dfg

@dash_app1.callback(
    Output('lspcount', 'children'),
    [Input('dropdown10', 'value'),Input('dropdown11', 'value'),Input('state1', 'value'),Input('state2', 'value'),Input('sector1', 'value')])
def graph(origin,dest,state1,state2,sector):
    dfh=xyz(origin,dest,state1,state2,sector)
    count=len(pd.unique(dfh['LSP Name']))
    x="{:,}".format(count)
    return x
@dash_app1.callback(
    Output('view', 'figure'),
    [Input('dropdown10', 'value'),Input('dropdown11', 'value'),Input('state1', 'value'),Input('state2', 'value'),Input('sector1', 'value')])
def graph(origin,dest,state1,state2,sector):
    mapbox_access_token = 'pk.eyJ1IjoicmFqaWl0YjY5IiwiYSI6ImNqbmozZDd4aDB2ZTYzcG9zNWNzbnB5dTEifQ.dfwwo4R4cZFklzRIID6snA'
    layout = go.Layout(autosize=True, hovermode='closest',showlegend=False,
                       legend = dict(x= 0, y= 1,font = dict(size = 8)),margin={'l': 1, 'b': 1, 't': 1,'r': 1},
                   mapbox=dict(accesstoken=mapbox_access_token,bearing=0,
                               center=dict(lat=21.153, lon=79.083),
                               pitch=0, zoom=4, style= 'mapbox://styles/rajiitb69/cjpp4ernb02n52sjjcckrmfwg'))
    if origin==None and dest==None and state1==None and state2==None and sector==None:
        points=[go.Scattermapbox(lat = ['21.153'], lon=['79.083'], mode='markers', marker=dict(size=0.5,color='#ffffff'),
                             showlegend=False)]             
        figure = {'data': points, 'layout': layout} 
        return figure
    else:   
        dfh=xyz(origin,dest,state1,state2,sector)
        dfh = dfh.drop_duplicates(['OriginCluster', 'DestinationCluster'])
        data=[]
        for i in range(0,len(dfh)): 
            data.append(
                        go.Scattermapbox(lon = [dfh['OriginLongitude'].iloc[i], dfh['DestinationLongitude'].iloc[i]],
            lat = [dfh['OriginLatitude'].iloc[i], dfh['DestinationLatitude'].iloc[i]],
            mode = 'lines',showlegend=False,
            line = dict(width =1,color = 'turquoise'),))
    
        lon1=pd.DataFrame(dfh['OriginLongitude'])
        lon2=pd.DataFrame(dfh['DestinationLongitude'])

        lat1=pd.DataFrame(dfh['OriginLatitude'])
        lat2=pd.DataFrame(dfh['DestinationLatitude'])

        name1=pd.DataFrame(dfh['OriginName'])
        name2=pd.DataFrame(dfh['DestinationName'])

#        points=[go.Scattermapbox(lat = lat['OriginLatitude'], lon=lon['OriginLongitude'], mode='markers+text', marker=dict(size=3,color='#2699fb'),
#                                 text=name['OriginName'],showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]             
        point1=[go.Scattermapbox(lat = lat1['OriginLatitude'], lon=lon1['OriginLongitude'], mode='markers+text', marker=dict(size=8,color='#f9a602'),
                                 text=name1['OriginName'],textposition='top center',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]         
        point2=[go.Scattermapbox(lat = lat2['DestinationLatitude'], lon=lon2['DestinationLongitude'], mode='markers+text', marker=dict(size=8,color='blue'),
                                 text=name2['DestinationName'],textposition='top center',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]     
        figure = {'data': data+point1+point2, 'layout': layout}
        return figure
@dash_app1.callback(
    Output('radio4', 'options'),
    [Input('dropdown10', 'value'),Input('dropdown11', 'value'),Input('state1', 'value'),Input('state2', 'value'),Input('sector1', 'value')])
def graph(origin,dest,state1,state2,sector):
    dfh=xyz(origin,dest,state1,state2,sector)
    lspunique= pd.Series(pd.unique(dfh['LSP Name']))
    lspunique = lspunique.dropna()
    lspunique = list(lspunique)
    lspunique= sorted(lspunique)
    return [{'label': i, 'value': i} for i in lspunique]


def colors(n):
  ret = []
  r = int(random.random() * 256)
  g = int(random.random() * 256)
  b = int(random.random() * 256)
  step = 256 / n
  for i in range(n):
    r += step
    g += step
    b += step
    r = int(r) % 256
    g = int(g) % 256
    b = int(b) % 256
    ret.append('rgb'+str((r,g,b)))
  return ret


@dash_app1.callback(
     Output('lane','figure'),
    [Input('radio4', 'value'),Input('radio5', 'value')])
def update_graph(value,value1):
    mapbox_access_token = 'pk.eyJ1IjoicmFqaWl0YjY5IiwiYSI6ImNqbmozZDd4aDB2ZTYzcG9zNWNzbnB5dTEifQ.dfwwo4R4cZFklzRIID6snA'

    layout = go.Layout(autosize=True, hovermode='closest',
                   legend = dict(x= 0, y= 1,font = dict(size = 8)),margin={'l': 1, 'b': 1, 't': 1,'r': 1},
               mapbox=dict(accesstoken=mapbox_access_token,bearing=0,
                           center=dict(lat=21.153, lon=79.083),
                           pitch=0, zoom=4, style= 'mapbox://styles/rajiitb69/cjpp4ernb02n52sjjcckrmfwg')) 
    if value1=='Lanes':
        dfg = lane[lane['LSP Name'] == value]
        dfg = dfg.drop_duplicates(subset=['OriginName', 'DestinationName'])
        lanes = []
        for i in range(0,len(dfg)):        
            lanes.append(
                go.Scattermapbox(lon = [dfg['OriginLongitude'].iloc[i], dfg['DestinationLongitude'].iloc[i]],
                    lat = [dfg['OriginLatitude'].iloc[i], dfg['DestinationLatitude'].iloc[i]],
                    mode = 'lines',name=value,showlegend=False,
                    line = dict(width = 0.6,color = 'turquoise'),))
        lon1=pd.DataFrame(dfg['OriginLongitude'])
        lon2=pd.DataFrame(dfg['DestinationLongitude'])
#        lon2.columns=['OriginLongitude']
#        lon=lon1.append(lon2)
        lat1=pd.DataFrame(dfg['OriginLatitude'])
        lat2=pd.DataFrame(dfg['DestinationLatitude'])
#        lat2.columns=['OriginLatitude']
#        lat=lat1.append(lat2)
        name1=pd.DataFrame(dfg['OriginName'])
        name2=pd.DataFrame(dfg['DestinationName'])
#        name2.columns=['OriginName']
#        name=name1.append(name2)
#        points=[go.Scattermapbox(lat = lat['OriginLatitude'], lon=lon['OriginLongitude'], mode='markers+text', marker=dict(size=3,color='#2699fb'),
#                                 text=name['OriginName'],showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]             
        point1=[go.Scattermapbox(lat = lat1['OriginLatitude'], lon=lon1['OriginLongitude'], mode='markers+text', marker=dict(size=8,color='#f9a602'),
                                 text=name1['OriginName'],textposition='top center',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]         
        point2=[go.Scattermapbox(lat = lat2['DestinationLatitude'], lon=lon2['DestinationLongitude'], mode='markers+text', marker=dict(size=8,color='blue'),
                                 text=name2['DestinationName'],textposition='top center',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))]         
        figure = {'data': lanes+point1+point2, 'layout': layout}   
    elif value1=='Branch':
        branch = m[m['lspName']==value]
        if len(branch) == 0:          
            table = go.Table(
            header=dict(
            values=[''],
            font=dict(size=10,color='#FFFFFF'),
            line = dict(color='rgba(255, 255, 255, .4)'),
            align = 'left',
            height=20,
            fill = dict(color='#2699fb'),
            ),
            cells=dict(
                    values=[['Branches are not available']],
                    font=dict(size=15,color='#000000'),
                    line = dict(color='rgba(255, 255, 255, .4)'),
                    align = 'center',
                    height=40,
                    fill = dict(color='#f5f5fa')))
            layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
            figure = {'data': [table], 'layout': layout} 
            return figure
        else:
            data1 = go.Scattermapbox(lat = m[m['lspName']==value]['Latitude'], lon=m[m['lspName']==value]['Longitude'], mode='markers+text', marker=dict(size=10),
                                 text=m[m['lspName']==value]['City'],textposition='top center',name='Branch',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))
            data2 = go.Scattermapbox(lat = [str(m[m['lspName']==value].set_index('lspName')['Latitude'].values.tolist()[0])],lon=[str(m[m['lspName']==value].set_index('lspName')['Longitude'].values.tolist()[0])], mode='markers', marker=dict(size=10, color='red'),
                                 text=[m[(m['lspName']==value) & (m['Type']=='HQ')]['City'].iloc[0]],textposition='top center',name='HQ',showlegend=False,textfont=dict(family='sans serif',size=10,color='rgb(255,255,255)'))
            data = [data1, data2]
            figure = {'data': data, 'layout': layout}
    elif value1=='Details':
        dfg = lane[lane['LSP Name'] == value]
        dff=pd.concat([dfg['OriginName'],dfg['DestinationName'],dfg['TruckType']],axis=1)
        dff=dff.drop_duplicates(subset=['OriginName','DestinationName','TruckType'])
        table = go.Table(
            columnwidth=[0.3, 0.3,0.2],
            header=dict(
                #values=list(df.columns[1:]),
                values=['Origin Location','Destination Location','Truck Type'],
                font=dict(size=11,color='#FFFFFF'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#2699fb'),
            ),
            cells=dict(
                values=[dff[k].tolist() for k in dff.columns[0:]],
                font=dict(size=9,color='#000000'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 10})
        figure = {'data': [table], 'layout': layout}
    return figure 
@dash_app1.callback(
     Output('head','children'),
    [Input('radio5', 'value')])
def update_graph(value):
    return value

@dash_app1.callback(
     Output('table1','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    est = df_year_sector[df_year_sector['year'] == year_value].iloc[:,0:2]
    summary = est[est['lspName']==value].set_index('lspName')
    if len(summary) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=10,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        table = go.Table(
        columnwidth=[1],
        header=dict(
            values=['Year of Establishment'],
            font=dict(size=10,color='#FFFFFF'),
            line = dict(color='rgba(255, 255, 255, .4)'),
            align = 'center',
            fill = dict(color='#2699fb'),
        ),
        cells=dict(
            values=[summary[k].tolist() for k in summary.columns[0:]],
            font=dict(size=12,color='#000000'),
            line = dict(color='rgba(255, 255, 255, .4)'),
            align = 'center',
            fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 0, 'b': 0, 't': 0,'r': 0})
        figure = {'data': [table], 'layout': layout}
        return figure

@dash_app1.callback(
     Output('table8','figure'),
    [Input('radio4', 'value')])
def update_graph(value):
    summary = rating[rating['lspName']==value].set_index('lspName')
    if len(summary) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=10,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        table = go.Table(
            columnwidth=[1],
            header=dict(
                values=['LSP Rating'],
                font=dict(size=10,color='#FFFFFF'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                fill = dict(color='#2699fb'),
            ),
            cells=dict(
                values=[summary[k].tolist() for k in summary.columns[0:]],
                font=dict(size=12,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 0, 'b': 0, 't': 0,'r': 0})
        figure = {'data': [table], 'layout': layout}
        return figure
#@dash_app1.callback(
#     Output('table5','figure'),
#    [Input('radio4', 'value'),Input('dropdown2', 'value')])
#def update_graph(value,year_value):
#    over = overall1[overall1['year'] == year_value].iloc[:,np.r_[3,13]]
#    summary = np.around(over[over['lspName']==value].set_index('lspName'), decimals=0)
#    final = ff.create_table(summary,height_constant=10)
#    for i in range(len(final.layout.annotations)):
#        final.layout.annotations[i].font.size = 10
#    return final
 
@dash_app1.callback(
     Output('table4','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    over = manpower_transpose[manpower_transpose['year'] == year_value].iloc[:,np.r_[0,2,3]]
    summary = over[over['lspName']==value].set_index('lspName')
    if len(summary) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        height=20,
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=15,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                height=40,
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        table = go.Table(
            columnwidth=[0.6, 0.4],
            header=dict(
                values=['ManPower','Count'],
                font=dict(size=10,color='#FFFFFF'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'center',
                fill = dict(color='#2699fb'),
            ),
            cells=dict(
                values=[summary[k].tolist() for k in summary.columns[0:]],
                font=dict(size=8,color='#000000'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#f5f5fa')))
        layout = dict(height=150,margin={'l': 0, 'b': 0, 't': 0,'r': 1})
        figure = {'data': [table], 'layout': layout}
        return figure
@dash_app1.callback(
     Output('client','figure'),
    [Input('radio4', 'value')])
def update_graph(value):
    ref = sector_dataframe[sector_dataframe['lspName']==value]
    over = ref[['Client_Name','Sector']]
    if len(over) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        height=20,
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=15,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                height=40,
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        table = go.Table(
            columnwidth=[0.6, 0.4],
            header=dict(
                values=['Client Name','Sector'],
                font=dict(size=10,color='#FFFFFF'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'center',
                fill = dict(color='#2699fb'),
            ),
            cells=dict(
                values=[over[k].tolist() for k in over.columns[0:]],
                font=dict(size=8,color='#000000'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#f5f5fa')))
        layout = dict(height=150,margin={'l': 0.5, 'b': 0, 't': 0,'r': 1})
        figure = {'data': [table], 'layout': layout}
        return figure  
@dash_app1.callback(
     Output('table7','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    over = contact_dataframe[contact_dataframe['year'] == year_value].iloc[:,np.r_[0,2:4,6]]
    cont = over[over['lspName']==value].set_index('lspName')
    if len(cont) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        height=20,
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=15,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                height=40,
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        table = go.Table(
            columnwidth=[0.2, 0.2,0.4],
            header=dict(
                #values=list(df.columns[1:]),
                values=['Person Name','Designation','Email Id'],
                font=dict(size=11,color='#FFFFFF'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#2699fb'),
            ),
            cells=dict(
                values=[cont[k].tolist() for k in cont.columns[0:]],
                font=dict(size=9,color='#000000'),
                line = dict(color='rgb(50, 50, 50)'),
                align = 'left',
                fill = dict(color='#f5f5fa')))
        layout = dict(height=150,margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout}
        return figure
@dash_app1.callback(
     Output('table9','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    over = top_clientelle_dataframe[top_clientelle_dataframe['year'] == year_value].T
    cont = over[over['lspName']==value].set_index('lspName')
    final = ff.create_table(cont,height_constant=25)
    for i in range(len(final.layout.annotations)):
        final.layout.annotations[i].font.size = 9
    return final
@dash_app1.callback(
     Output('table6','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    over = vehicle_dataframe[vehicle_dataframe['year'] == year_value].iloc[:,np.r_[0,2:5]]
    veh1 = over[over['lspName']==value].set_index('lspName')
    veh1=veh1.round(0)
    if len(veh1) == 0:          
        table = go.Table(
        header=dict(
        values=[''],
        font=dict(size=10,color='#FFFFFF'),
        line = dict(color='rgba(255, 255, 255, .4)'),
        align = 'left',
        height=20,
        fill = dict(color='#2699fb'),
        ),
        cells=dict(
                values=[['On Request']],
                font=dict(size=15,color='#000000'),
                line = dict(color='rgba(255, 255, 255, .4)'),
                align = 'center',
                height=40,
                fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout} 
        return figure
    else:
        table = go.Table(
        columnwidth=[0.5, 0.25,0.25],
        header=dict(
            #values=list(df.columns[1:]),
            values=['Truck Type','Self Owned','Attached'],
            font=dict(size=11,color='#FFFFFF'),
            line = dict(color='rgb(50, 50, 50)'),
            align = 'left',
            fill = dict(color='#2699fb'),
        ),
        cells=dict(
            values=[veh1[k].tolist() for k in veh1.columns[0:]],
            font=dict(size=9,color='#000000'),
            line = dict(color='rgb(50, 50, 50)'),
            align = 'left',
            fill = dict(color='#f5f5fa')))
        layout = dict(margin={'l': 1, 'b': 1, 't': 1,'r': 1})
        figure = {'data': [table], 'layout': layout}
        return figure
@dash_app1.callback(
     Output('truck','figure'),
    [Input('radio4', 'value'),Input('dropdown2', 'value')])
def update_graph(value,year_value):
    dfg = vehicle_count[vehicle_count['year'] == year_value].iloc[:,0:3]
    a=str((dfg[dfg['lspName']==value].set_index('lspName')['Self Owned'][value]))
    b=str((dfg[dfg['lspName']==value].set_index('lspName')['Attached'][value]))
    trace = [
    {
      "values": pd.Series((dfg[dfg['lspName']==value].set_index('lspName').transpose()).iloc[0:2,:][value]),
      "labels": ['Self-Owned'+': '+a,'Attached'+': '+b],
      "domain": {"x": [0, 1]},
      "name": value,
      "hoverinfo":"name+label",
      "textinfo":"label+percent",
      "textposition":"outside",
      "textfont":{"size":12},
      "hole": .4,
      "type": "pie"
    }]
    layout= {'showlegend': False,'height':300,'margin':{'l': 100, 'b': 40, 't': 40,'r': 90},
        "annotations": [
            {
                "font": {
                    "size": 12
                },
                "showarrow": False,
                "text": "",
                "x": 0.5,
                "y": 0.5}]}
    figure = {'data': trace, 'layout': layout}
    return figure 

#@server.route('/dash/')
#def render_dashboard():
#    return flask.redirect('/dash1')

app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server}
                            )

if __name__ == '__main__':
    port=5000+ random.randint(0,999)
    url="http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25,lambda:webbrowser.open(url)).start()
    run_simple('127.0.0.1',port, app,use_debugger=True, use_evalex=True)
#    app.run_server(debug=True)
    
