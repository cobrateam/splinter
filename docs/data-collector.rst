.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Splinter data collection automation tool
    :keywords: splinter, python, data collection

+++++++++++++++++
Data Collector
+++++++++++++++++

Splinter can be used to simplify data collection automation.

The following example shows how to use the DataCollector class.

Gathering Twitter profiles data after login
=========================

This script will first visit Twitter login page (using Chrom in incognito mode (#1) 
and waits until the user manually enter his credentials i.e. for the twitter home
url to be automatically visited on successful loin (#2)

Afterwards, an url template is created (#3), e.g. ``https://twitter.com/{PAGE}`` 
where ``{PAGE}`` is a placeholder which will be replaced sequencially by
values provided in a list as input parameters of ``iterate_over_pages`` method.
The resulting urls will be visited one by one and for each of them, all
callbacks are executed. (#4)

**Note:** A callback is a ``DataCollector`` method which can return or not a value.
If no value is returned, the callback is simply executed.
If a callback return data, such data will be automatically collected inside
the ``data_collection`` attribute.

``_get_innermost_tag_text_containing_strings(self, tag, strings)`` searches
for the (innermost) input tag containing all the strings in the same order
they occur in the input list. 

.. highlight:: python

::
    
    from splinter import Browser, DataCollector
    
    obj = DataCollector(startUrl="https://twitter.com/i/flow/login", browser=Browser('chrome', incognito=True)) #1
    obj.wait_until_url("https://twitter.com/home") #2
    obj.add_url_template("https://twitter.com/{PAGE}") #3
    obj.iterate_over_pages(var_name="PAGE",
                           var_values=["tldrnewsletter", "cnni", "realpython", "elonmusk"],
                           callbacks=[("_get_innermost_tag_text_containing_strings", {"tag":'span', "strings":["Joined"]}),
                                      ("_get_innermost_tag_text_containing_strings", {"tag":'a', "strings":["following","Following"]}),
                                    ("_get_innermost_tag_text_containing_strings", {"tag":'a', "strings":["Followers"]}),
                                    ("wait_random_time", {"min_time": 5, "max_time": 15})
                                    ]) #4
    print(obj.data_collection) #5

The print command outputs all data collected as a dictionary, like the following

.. highlight:: python

::
    
    {'{PAGE}=tldrnewsletter': ['Joined July 2018', '134 Following', '16.5K Followers'],
     '{PAGE}=cnni': ['Joined March 2007', '369 Following', '13.6M Followers'],
     '{PAGE}=realpython': ['Joined August 2012', '165 Following', '136.6K Followers'],
     '{PAGE}=elonmusk': ['Joined June 2009', '114 Following', '82.1M Followers']}
