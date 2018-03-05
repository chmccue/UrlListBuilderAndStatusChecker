import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
# -*- coding: utf-8 -*-

#from pprint import pprint
#############################################
# the google feed for the API.
#scope = ['https://spreadsheets.google.com/feeds']
#############################################
#credentials from json file for API.
#creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#client = gspread.authorize(creds)
#############################################


#def set_credentials(email_acct_json_file):
#    '''Pass the json file from the Google API that has the meail account for connecting to the google sheets'''
    # the google feed for the API.
#    scope = ['https://spreadsheets.google.com/feeds']
#    creds = ServiceAccountCredentials.from_json_keyfile_name(email_acct_json_file, scope)
#    client = gspread.authorize(creds)
#    return client

class GSpreadListBuilder(object):

    def __init__(self, scope=['https://spreadsheets.google.com/feeds'], json_cred_file='client_secret.json'):
        '''init function sets the credentials and authorization via json file. File must be named client_secret.json,
        and must use email designated in that json file to add to the gspreadsheets the user is looking to access via
        gspread title.'''
        self.scope = scope
        #############################################
        #credentials from json file for API.
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_cred_file, self.scope)
        self.client = gspread.authorize(self.creds)

    def set_gspread_title(self, gspread_title):
        return gspread_title
    
    def connect_to_gspread_tab(self, credentials, gspread_title, gspread_tab):
        '''
        will connect to the appropriate google sheet based on its title, and worksheet tab based on name.
        '''
        return credentials.open(gspread_title).worksheet(gspread_tab)

    def get_data_from_a_specific_gspread_tab(self, gspread_title, gspread_tab, search_list=["http"], col_num=None, use_regex=False):
        '''
        After connecting to the appropriate tab, this will scrape all URLs in a specific column.
        If the google sheet is more structured and maintained, this can be targeted based on 
        column.
        
        :param:gspread_title:
            Type: String.
            Name of the Google Sheet title to use.
        :param:gspread_tab:
            Type: String.
            Name of the Google Sheet tab to search.
        :param:search_list:
            Type: List
            Default set at "http" in order to locate any URLs that start with http. If more than one string is
            desired to be searched for, enter it in list format, such as search_list=["http", "https"]
        :param:col_num:
            Type: Integer
            Set to None by default. If set to none, the entire tab will be scraped for the search_list content.
            If you set this value to a number, such as col_num=3, it will only search for data in column 3.s
        :param:use_regex:
            Type: Boolean.
            You can use a regular expression if desired for searching the search_list. If set to False, 
        '''

        new_list = []
        gspread_tab = self.connect_to_gspread_tab(gspread_title=gspread_title, gspread_tab=gspread_tab)
        if col_num != None:
            for url in gspread_tab.col_values(col_num):
            #if "http" in url:
                for item in search_list:
                    if use_regex:
                        if re.search(item, item.lower().strip()):
                            new_list.append(url)
                    else:
                        if url.strip().startswith(item):
                            new_list.append(url)
                    
        else:
            for url in gspread_tab.get_all_values():
                for item in search_list:
                    if url.strip().startswith(item):
                        new_list.append(url)
        if len(new_list) == 1:
            print str(len(new_list)) + " url added for validation."  #checks the length of the dynamically built list.
        else:
            print str(len(new_list)) + " urls added for validation."  #checks the length of the dynamically built list.

        return new_list

    def get_all_urls_from_all_tabs(self, gspread_title, search_list=["http"], use_regex=True):
        '''
        This will go to the google spreadsheet provided, count the tabs, then go through all tabs and scrape all 
        content and provide a list of the content that starts with a word, partial word, or letter of your 
        choice. Since this is for scraping URLs, it defaults to searching for http, and nothing needs to be 
        entered into the method if this is being used for getting urls.
        
        :param:spread_title:
            Type: String
            The title of the google spreadsheet. Used to locate the spreadsheet, once the api google email 
            has been successfully added to it as a viewer or editor. Assumes the google email has been 
            authorized with credentials.
        
        :param:search_list:
            Type: List with nested strings
            Default set at "http" in order to locate any URLs that start with http. If more than one string is
            desired to be searched for, enter it in list format, such as search_list=["http", "https"]
        '''
        new_list = []
        # connect to the google sheet with the correct credentials.
        gspread_title = self.set_gspread_title(gspread_title=gspread_title)
        #print "gspread title:"
        #print gspread_title
        #client = self.client
        tab_list = self.client.open(gspread_title).worksheets()
        #print "\nnumber of tabs found in sheet: " + str(len(tab_list))
        for tab in range(0, len(tab_list)):
            #new_list = []
            current_tab = self.client.open(gspread_title).get_worksheet(tab)
            #print current_tab

            get_all = current_tab.get_all_values()
            # Below displays output of all the records on the google sheet tab. Uncomment if needed for debugging purposes.
            #print(get_all)
            #print "tab " + str(tab)
            #print "new list " + str(len(new_list))
            '''
            The data in "get_all" is a list/array, which has nested dictionaries within it that represent each row of the google sheet. 
            This will count all the items in get_all list, then loop through each row. For each row, it will then loop through each cell
            in the row with a dictionary loop, and search for data that matches the "search_list" argument. If it finds data that matches 
            the search_list argument, it will add that to new_list, which will be returned at the end of the method.
            
            # Section documentation:
            # For loop that takes the range of all the tabs found in the Google Sheet.
            for num in range(0, len(get_all)):
                
                # Since the data returned is in the form of nested lists (each list representing a row from the Google Sheet), we
                # must then loop through each nested list using the [num] value that is being looped through in the main list.
                for value in get_all[num]:
                
                    # We are looking for URL values, which will always be strings. Anything else that may be returned, such as ID's or 
                    # non string items, we can ignore.
                    if type(value) is str:
                    
                        # This is the real power of the method; what we had to loop through in order to find. This takes the value of any string,
                        # (.strip()) removes any white space before it, then (.startswith()) will check to see if the string starts with the 
                        # entered value. If the startswith value is found at the start of the string, it will add the string into the "new_list" 
                        # via the (.append()) method.
                        if value.strip().startswith(startswith):
                            new_list.append(value)
            '''
            
            for num in range(0, len(get_all)):
                #print num
                for value in get_all[num]:
                    if type(value) is str:
                        for item in search_list:
                            if use_regex:
                                if re.search(item, value.lower().strip()):
                                    new_list.append(value)
                            else:
                                if value.lower().strip().startswith(item):
                                    new_list.append(value)
                            #print "new value added from tab " + str(tab) + ": " +  str(value)

            #print new_list
            #print len(new_list)
        print "total number of urls added for validation: " + str(len(new_list))
        return new_list
