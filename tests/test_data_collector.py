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
        cls.obj = DataCollector(start_url="https://twitter.com/i/flow/login", browser=Browser('chrome', incognito=True))
        cls.obj.wait_until_url("https://twitter.com/home") 
        cls.obj.add_url_template("https://twitter.com/{PAGE}") 
        cls.obj.iterate_over_pages(var_name="PAGE",
                         var_values=["tldrnewsletter", "cnni", "realpython", "elonmusk"],
                         callbacks=[("_get_innermost_tag_text_containing_strings", {"tag":'span', "strings":["Joined"]}),
                                    ("_get_innermost_tag_text_containing_strings", {"tag":'a', "strings":["following","Following"]}),
                                    ("_get_innermost_tag_text_containing_strings", {"tag":'a', "strings":["Followers"]}),
                                    ("wait_random_time", {"min_time": 5, "max_time": 15})
                                    ])

    def test_data_collection_len(self):
        self.assertTrue(len(self.obj.data_collection) == 4)

    def test_data_collection_joined(self):
        self.assertTrue("Joined" in self.obj.data_collection["{PAGE}=tldrnewsletter"][0])
        self.assertTrue("Joined" in self.obj.data_collection["{PAGE}=cnni"][0])
        self.assertTrue("Joined" in self.obj.data_collection["{PAGE}=realpython"][0])
        self.assertTrue("Joined" in self.obj.data_collection["{PAGE}=elonmusk"][0])

    def test_data_collection_following(self):
        self.assertTrue("Following" in self.obj.data_collection["{PAGE}=tldrnewsletter"][1])
        self.assertTrue("Following" in self.obj.data_collection["{PAGE}=cnni"][1])
        self.assertTrue("Following" in self.obj.data_collection["{PAGE}=realpython"][1])
        self.assertTrue("Following" in self.obj.data_collection["{PAGE}=elonmusk"][1])

    def test_data_collection_followers(self):
        self.assertTrue("Followers" in self.obj.data_collection["{PAGE}=tldrnewsletter"][2])
        self.assertTrue("Followers" in self.obj.data_collection["{PAGE}=cnni"][2])
        self.assertTrue("Followers" in self.obj.data_collection["{PAGE}=realpython"][2])
        self.assertTrue("Followers" in self.obj.data_collection["{PAGE}=elonmusk"][2])

unittest.main()
