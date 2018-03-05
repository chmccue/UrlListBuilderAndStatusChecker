from __future__ import print_function
import requests, sys
from pprint import pprint

'''Global used variables'''
test_count = 0
fail_dict = {}
fail_count = 0


class UrlStatusChecker(object):
    '''
    Contains methods for getting url responses and assertions for validating the responses.
    '''

    def __init__(self):
        self.fail_msg = ''
        

    def assert_actual_url_contains_expected_url(self, expected_url, actual_url):
        '''
        This takes an expected_url argument and makes sure it is appearing in the request library get request (req) argument.
        :param:expected_url
            The string you want to assert against the actual_url argument.
        
        :param:actual_url
            URL to assert against.
        
        The expected_url doesn't have to match exactly, but has to be included in the actual_url.
        For example:
        >>>assert_actual_url_contains_expected_url("www.justfab.com/example", "www.justfab.com/example")
        >>>PASS  #URLs match exactly.
        
        >>>assert_actual_url_contains_expected_url("justfab", "www.justfab.com/example")
        >>>PASS  #expected_url argument is found to be in actual_url argument.
        
        >>>assert_actual_url_contains_expected_url("www.justfab.com/example/1", "www.justfab.com/example")
        >>>FAIL  #expected_url argument is not found in actual_url argument, due to the '/1' part not appearing in the actual_url argument.
        '''
        assert expected_url in actual_url
        #print ("URL assertion validated: " + expected_url + " in " + actual_url)
        #print ("\n")

    def assert_status_code_is_200(self, actual_status_code):
        '''
        Simple assertion that status code is returning 200 status ok.
        :param:actual_status_code
            The actual status code to assert it is matching 200.
        '''
        assert "200" in str(actual_status_code)

    def assert_status_code_not_bad(self, codes=[]):
        '''
        Documentation: function takes a list. The list should contain the status codes and/or redirect codes of whatever URL status path
        to assert 404 is not found. If 404 is found in entered status code or status code redirect history, the test will raise an 
        exception and fail.        
        '''
        if len(codes) > 0:
            for code in codes:
                assert "404" not in str(code)
                assert "403" not in str(code)
                assert "500" not in str(code)
        elif len(codes) == 0:
            raise Exception("No status codes were entered for validation.")

    def get_url_response_data(self, url):
        
        
        with requests.Session() as s:
            '''try/except catches any errors with receiving the get request to start the test.'''
            try:
                r = s.get(url)
                # ====================
                returned_url = r.url
                returned_status_code = r.status_code
                returned_status_code_history = r.history

                data_dict = {}
                data_dict.update({url: 
                                  [returned_url, 
                                   returned_status_code, 
                                   returned_status_code_history]})

                return data_dict
            except Exception, e:
                # ====================
                self.update_fail_dict([str(e), type(e)])
                #fail_dict([str(e), type(e)])
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(type(e))
                print(e)
                # ====================


    def counting_each_validation(self):
        global test_count
        test_count += 1
        #print (test_count)
        '''Below checks if a 100's number is being checked. If it is, it will print out a simple statement that the 
            automation is still running'''
        if test_count % 100 == 0:
            print("Checked " + str(test_count) + " URLs so far. Still in progress...")
        elif test_count % 20 == 0:
            print('. ', end='')
        return test_count



    def validate_all_assertions(self, entered_url, returned_url, 
                                returned_status_code, returned_status_code_history, 
                                text_in_url=None):
        '''try/except catches fails in the main asserts of the method, and adds to the fail count and dictionary upon failure.'''
        global test_count#, fail_dict, fail_count
        #try:
            #if "403" != str(returned_status_code):

        self.counting_each_validation()
        #print ("url number checked: %d" %test_count)
        #print ("\nurl entered:  %s\nurl returned: %s" %(entered_url, returned_url))
        #print ("status code: %s" %returned_status_code)
        #print ("status code history: %s" %returned_status_code_history)

        ''' try/except catches fails during the status code assertions. A fail message will be set and be able to be 
                delivered to the fail_dict upon encountering an exception.'''
        try:
            self.assert_status_code_not_bad(codes=[returned_status_code, returned_status_code_history])
            self.assert_status_code_is_200(returned_status_code)
        except:
            fail_msg = "status code or redirect issue found."
            self.update_fail_dict([entered_url, returned_url, returned_status_code, returned_status_code_history, fail_msg])
        # ====================
        '''try/except catches fails during the return url domain assertion. A fail message will be set and be able to be 
           delivered to the fail_dict upon encountering an exception.'''
        try:
            if text_in_url != None:
                self.assert_actual_url_contains_expected_url(text_in_url, str(returned_url))
        except:  #Exception, e:
            fail_msg = "entered or returned URL incorrect or not recognized."
            self.update_fail_dict([entered_url, returned_url, returned_status_code, returned_status_code_history, fail_msg])
        # ====================
        #except Exception, e:
            # UNCOMMENT OUT BELOW PRINT STATEMENTS WHEN DEBUGGING FOR FAILS INVOLVING THIS EXCEPTION.
            #print('\nError on line {}'.format(sys.exc_info()[-1].tb_lineno))
            #print (type(e))
            #print (e)
            #print ("####################FAILURE REPORTED####################")

        #adds a line break in the log for easily viewing output.
        #print ("______________________\n")


    def update_fail_dict(self, *kwargs):
        global fail_count, fail_dict
        fail_count += 1
        fail_dict.update({fail_count: kwargs})
        #print (fail_count)
        #print (fail_dict)


    def output_test_statistics(self):
        global test_count, fail_dict, fail_count
        print("Total number of URLs checked: " + str(test_count)) #str(self.count)
        #print ("\n\n")
            # ====================
        if len(fail_dict) > 0:
            print("______________________\n______________________\nFailed link information:\n______________________\n______________________\n")
            pprint(fail_dict)
            print("Total number of Failed URLs reported: " + str(fail_count) + "/" + str(test_count)) #str(self.count))
            raise Exception("Total number of Failed URLs reported: " + str(len(fail_dict)) + "/" + str(test_count) + "\n" + str(fail_dict)) #str(fail_count)            
            #return False
        elif test_count == 0:
            print ("\n NO URLS FOUND. NO TESTS HAVE RUN.\n##############################")
        else:
            print ("\nALL TESTS HAVE PASSED: " + str(test_count) + "/" + str(test_count))
            #return True
 

    def reset_test_statistics(self):
        '''Resets global statistics used between tests, such as fail_count, fail_dict and test_count.
        This way, statistics do not carry on to the next test case.'''
        global test_count, fail_count, fail_dict
        #print ("resetting test statistics for current test case.")
        if len(fail_dict) > 0:
            #print ("fail_dict should be getting cleared now.")
            fail_dict.clear()
            #print (fail_dict)
        if fail_count > 0:
            fail_count = 0
            #print ("fail count: " + str(fail_count))
        test_count = 0



    def check_data_urls_as_list(self, data_list=[], text_in_url=None):
        '''
        This is the main method that ties all the other methods together. Technically this is the only method in the class you would need
        to validate content, as it gets the url response, loops through them all, and runs the assertions in the class.
        At the end, it outputs the fail information and statistics.
        
        :param:data_list
            List/Array.
            How the urls are stored. Once the list is plugged into this method, it is looped through and validated for its responses.
        :param:text_in_url
            String
            Can be used to assert the returned URL matches what is entered for this argument. It is a container validation, so an exact match
            does not need to be entered. A partial match will return a passing status. This argument defaults to None. If None is in the 
            argument, the assertion is skipped altogether.
        '''
        self.reset_test_statistics()
        
        if len(data_list) > 0:
            for url in data_list:
                #print (url)
                get_responses = self.get_url_response_data(url)
                
                try:
                    #print (get_responses)
                    #for key, values in get_responses.iteritems():
                    for values in get_responses.itervalues():
                    #print (values[0])
                    #print (values[1])
                    #print (values[2])
                
                        self.validate_all_assertions(entered_url=url, 
                                                           returned_url=values[0], 
                                                           returned_status_code=values[1], 
                                                           returned_status_code_history=values[2], 
                                                           text_in_url=text_in_url)
                except AttributeError, e:
                    #self.update_fail_dict(url)
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    print (type(e))
                    print (e)
                    
        elif len(data_list) == 0:
            print ("Nothing entered in list. Please make sure you are entering data in a list format, otherwise this will not run.")
            #raise Exception("Nothing entered in list. Please make sure you are entering data in a list format, otherwise this will not run.")
        return self.output_test_statistics()



