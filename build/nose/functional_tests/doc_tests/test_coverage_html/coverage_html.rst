Generating HTML Coverage with nose
----------------------------------

.. Note ::

    HTML coverage requires Ned Batchelder's coverage.py module.
..

Console coverage output is useful but terse. For a more browseable view of
code coverage, the coverage plugin supports basic HTML coverage output.

.. Note ::

   The run() function in :mod:`nose.plugins.plugintest` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

The console coverage output is printed, as normal.

    >>> import os
    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> cover_html_dir = os.path.join(support, 'cover')
    >>> from nose.plugins.cover import Coverage
    >>> run(argv=[__file__, '-v', '--with-coverage', '--cover-package=blah', 
    ...           '--cover-html', '--cover-html-dir=' + cover_html_dir,
    ...           support, ], 
    ...     plugins=[Coverage()]) # doctest: +REPORT_NDIFF
    test_covered.test_blah ... hi
    ok
    <BLANKLINE>
    Name    Stmts   Miss  Cover   Missing
    -------------------------------------
    blah        4      1    75%   6
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

The html coverage reports are saved to disk in the directory specified by the
``--cover-html-dir`` option. The index page includes links to a detailed
coverage report page for each module in the report.
    
    >>> print open(os.path.join(cover_html_dir, 'index.html')).read() # doctest: +REPORT_NDIFF
    <html><head><title>Coverage Index</title></head><body><p>Covered: 3 lines<br/>
    Missed: 1 lines<br/>
    Skipped 3 lines<br/>
    Percent: 75 %<br/>
    <table><tr><td>File</td><td>Covered</td><td>Missed</td><td>Skipped</td><td>Percent</td></tr><tr><td><a href="blah.html">blah</a></td><td>3</td><td>1</td><td>3</td><td>75 %</td></tr></table></p></html

Detail pages show the module source, colorized to indicated which lines are
covered and which are not.
    
    >>> print open(os.path.join(cover_html_dir, 'blah.html')).read() # doctest: +REPORT_NDIFF
    <html>
    <head>
    <title>blah</title>
    </head>
    <body>
    blah
    <style>
    .coverage pre {float: left; margin: 0px 1em; border: none;
                   padding: 0px; }
    .num pre { margin: 0px }
    .nocov, .nocov pre {background-color: #faa}
    .cov, .cov pre {background-color: #cfc}
    div.coverage div { clear: both; height: 1.1em}
    </style>
    <div class="stats">
    Covered: 3 lines<br/>
    Missed: 1 lines<br/>
    Skipped 3 lines<br/>
    Percent: 75 %<br/>
    <BLANKLINE>
    </div>
    <div class="coverage">
    <div class="cov"><span class="num"><pre>1</pre></span><pre>def dostuff():</pre></div>
    <div class="cov"><span class="num"><pre>2</pre></span><pre>    print 'hi'</pre></div>
    <div class="skip"><span class="num"><pre>3</pre></span><pre></pre></div>
    <div class="skip"><span class="num"><pre>4</pre></span><pre></pre></div>
    <div class="cov"><span class="num"><pre>5</pre></span><pre>def notcov():</pre></div>
    <div class="nocov"><span class="num"><pre>6</pre></span><pre>    print 'not covered'</pre></div>
    <div class="skip"><span class="num"><pre>7</pre></span><pre></pre></div>
    </div>
    </body>
    </html>
    <BLANKLINE>

The html coverage output for a module looks like this:

.. raw :: html
   :file: support/cover/blah.html
