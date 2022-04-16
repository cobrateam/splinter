#!/usr/bin/env python

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest
from splinter import Browser
from splinter.data_collector import DataCollector

    


class TestTwitterDataAfterLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = DataCollector(startUrl="https://twitter.com/i/flow/login", browser=Browser('chrome', incognito=True)) #1
        cls.obj.waitUntilURL("https://twitter.com/home") 
        cls.obj.addUrlTemplate("https://twitter.com/{PAGE}") 
        cls.obj.iterateOverPages(varName="PAGE",
                         varValues=["tldrnewsletter", "cnni", "realpython", "elonmusk"],
                         callbacks=[("_getInnermostTagTextContainingStrings", {"tag":'span', "strings":["Joined"]}),
                                    ("_getInnermostTagTextContainingStrings", {"tag":'a', "strings":["following","Following"]}),
                                    ("_getInnermostTagTextContainingStrings", {"tag":'a', "strings":["Followers"]}),
                                    ("waitRandomTime", {"minTime": 5, "maxTime": 15})
                                    ])


    def test_data_collection_len(self):
        self.assertTrue(len(self.obj.dataCollection) == 4)

    def test_data_collection_joined(self):
        self.assertTrue("Joined" in self.obj.dataCollection["{PAGE}=tldrnewsletter"][0])
        self.assertTrue("Joined" in self.obj.dataCollection["{PAGE}=cnni"][0])
        self.assertTrue("Joined" in self.obj.dataCollection["{PAGE}=realpython"][0])
        self.assertTrue("Joined" in self.obj.dataCollection["{PAGE}=elonmusk"][0])
        
    def test_data_collection_following(self):
        self.assertTrue("Following" in self.obj.dataCollection["{PAGE}=tldrnewsletter"][1])
        self.assertTrue("Following" in self.obj.dataCollection["{PAGE}=cnni"][1])
        self.assertTrue("Following" in self.obj.dataCollection["{PAGE}=realpython"][1])
        self.assertTrue("Following" in self.obj.dataCollection["{PAGE}=elonmusk"][1])
        
    def test_data_collection_followers(self):
        self.assertTrue("Followers" in self.obj.dataCollection["{PAGE}=tldrnewsletter"][2])
        self.assertTrue("Followers" in self.obj.dataCollection["{PAGE}=cnni"][2])
        self.assertTrue("Followers" in self.obj.dataCollection["{PAGE}=realpython"][2])
        self.assertTrue("Followers" in self.obj.dataCollection["{PAGE}=elonmusk"][2])

unittest.main()