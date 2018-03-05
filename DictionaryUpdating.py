



class DictionaryUpdating():
    



    def merge_dictionaries(self, dictionary_to_add_to, dictionaries_to_combine=[]):
        '''
        This takes any number of dictionaries and merges them into 1 dictionary. If the same data of a dictionary
        is entered, this currently won't remove any duplicates, so adding a validation that duplicates have been removed
        is a consideration in the future, if this becomes an issue.
        :param:dictionary_to_add_to
            Takes a dictionary (preferably an empty dictionary so the other dictionaries can be easily combined).
            Required argument.
        :param:dictionaries_to_combine
            Takes a list of dictionaries. Must be provided in this format: 
                dictionary_to_make = {}  #empty dictionary; this is the dictionary that will have all the dictionaries in it after combining them.
                dictionary1 = {"this is: "dictionary1"}  #first dictionary defined
                dictionary2 = {"this is: "dictionary2"}  #second dictionary defined
                merge_dictionaries(dictionary_to_make, dictionaries_to_combine=[dictionary1, dictionary 2]
        
        '''
        final_dictionary = dictionary_to_add_to.copy()   # start with dict_to_add_to's keys and values
        for dictionary in dictionaries_to_combine:
            final_dictionary.update(dictionary)          # modifies final_dictionary with dicts_to_combine's keys and values & returns None
        return final_dictionary                    #fully combined dictionary returned for use.