# -*- coding: utf-8 -*-:

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import time
import random
import re

class DataCollector:
    def __init__(self, startUrl, browser):
        self.startUrl = startUrl
        self.browser = browser
        self.browser.visit(self.startUrl)
        self.dataCollection = dict()
        self.urlTemplates = []
        
    def waitUntilURL(self, url):
        while self.browser.url != url:
            time.sleep(5)
    
    def addToDataCollection(self, dataLabel, values):
        if dataLabel not in self.dataCollection:
            self.dataCollection[dataLabel] = []
        self.dataCollection[dataLabel].append(values)
    
    def removeHTML(self, html):
        return re.sub(re.compile("<.*?>"),'', html)
        
    def _getInnermostTagTextContainingStrings(self, tag, strings=[]):
        '''
        This method searches for the given tag in a non greedy way, containing
        all the strings in the same order they occur in the input list.
        

        Parameters
        ----------
        tag : STRING
            The tag name (with no angle parenthesis). Case sensitive.
        strings : LIST, optional
            List of strings which must be included after "<tag.." in the same
            order they occur.
            The default is [].

        Returns
        -------
        STRING
            Text inside the matched string after deleting all contained HTML tags.         

        '''

        match = None    
        while match is None:
            match = re.search("<"+tag+"(?:(?!<"+tag+").)*"+".*?".join(strings)+".*?</"+tag+">", self.browser.html)
        return self.removeHTML(match.group(0))
        
        
    
    def iterateOverPages(self, varName, varValues, callbacks):
        for urlTemplate in self.urlTemplates:
            placeholder = "{"+varName+"}"
            if placeholder in urlTemplate:
                for varValue in varValues:
                    self.browser.visit(urlTemplate.replace(placeholder, varValue))
                    for callback, params in callbacks:
                        data = getattr(self, callback)(**params)
                        if data is not None:
                            self.addToDataCollection(placeholder+"="+varValue, data)
                
                    
    def waitRandomTime(self, minTime, maxTime):
        time.sleep(random.randint(minTime,maxTime))
        
        
    def addUrlTemplate(self, url):
        self.urlTemplates.append(url)
        
        
        
        
            

