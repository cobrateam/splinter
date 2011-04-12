"""
Overview
========

The multiprocess plugin enables you to distribute your test run among a set of
worker processes that run tests in parallel. This can speed up CPU-bound test
runs (as long as the number of work processeses is around the number of
processors or cores available), but is mainly useful for IO-bound tests that
spend most of their time waiting for data to arrive from someplace else.

.. note ::

   See :doc:`../doc_tests/test_multiprocess/multiprocess` for
   additional documentation and examples. Use of this plugin on python
   2.5 or earlier requires the multiprocessing_ module, also available
   from PyPI.

.. _multiprocessing : http://code.google.com/p/python-multiprocessing/

How tests are distributed
=========================

The ideal case would be to dispatch each test to a worker process
separately. This ideal is not attainable in all cases, however, because many
test suites depend on context (class, module or package) fixtures.

The plugin can't know (unless you tell it -- see below!) if a context fixture
can be called many times concurrently (is re-entrant), or if it can be shared
among tests running in different processes. Therefore, if a context has
fixtures, the default behavior is to dispatch the entire suite to a worker as
a unit.

Controlling distribution
^^^^^^^^^^^^^^^^^^^^^^^^

There are two context-level variables that you can use to control this default
behavior.

If a context's fixtures are re-entrant, set ``_multiprocess_can_split_ = True``
in the context, and the plugin will dispatch tests in suites bound to that
context as if the context had no fixtures. This means that the fixtures will
execute concurrently and multiple times, typically once per test.

If a context's fixtures can be shared by tests running in different processes
-- such as a package-level fixture that starts an external http server or
initializes a shared database -- then set ``_multiprocess_shared_ = True`` in
the context. These fixtures will then execute in the primary nose process, and
tests in those contexts will be individually dispatched to run in parallel.

How results are collected and reported
======================================

As each test or suite executes in a worker process, results (failures, errors,
and specially handled exceptions like SkipTest) are collected in that
process. When the worker process finishes, it returns results to the main
nose process. There, any progress output is printed (dots!), and the
results from the test run are combined into a consolidated result
set. When results have been received for all dispatched tests, or all
workers have died, the result summary is output as normal.

Beware!
=======

Not all test suites will benefit from, or even operate correctly using, this
plugin. For example, CPU-bound tests will run more slowly if you don't have
multiple processors. There are also some differences in plugin
interactions and behaviors due to the way in which tests are dispatched and
loaded. In general, test loading under this plugin operates as if it were
always in directed mode instead of discovered mode. For instance, doctests
in test modules will always be found when using this plugin with the doctest
plugin.

But the biggest issue you will face is probably concurrency. Unless you
have kept your tests as religiously pure unit tests, with no side-effects, no
ordering issues, and no external dependencies, chances are you will experience
odd, intermittent and unexplainable failures and errors when using this
plugin. This doesn't necessarily mean the plugin is broken; it may mean that
your test suite is not safe for concurrency.

"""
import logging
import os
import sys
import time
import traceback
import unittest
import pickle
import nose.case
from nose.core import TextTestRunner
from nose import failure
from nose import loader
from nose.plugins.base import Plugin
from nose.result import TextTestResult
from nose.suite import ContextSuite
from nose.util import test_address
try:
    # 2.7+
    from unittest.runner import _WritelnDecorator
except ImportError:
    from unittest import _WritelnDecorator
from Queue import Empty
from warnings import warn
try:
    from cStringIO import StringIO
except ImportError:
    import StringIO

log = logging.getLogger(__name__)

Process = Queue = Pool = Event = None

def _import_mp():
    global Process, Queue, Pool, Event
    try:
        from multiprocessing import Process as Process_, \
            Queue as Queue_, Pool as Pool_, Event as Event_
        Process, Queue, Pool, Event = Process_, Queue_, Pool_, Event_
    except ImportError:
        warn("multiprocessing module is not available, multiprocess plugin "
             "cannot be used", RuntimeWarning)


class TestLet:
    def __init__(self, case):
        try:
            self._id = case.id()
        except AttributeError:
            pass
        self._short_description = case.shortDescription()
        self._str = str(case)

    def id(self):
        return self._id

    def shortDescription(self):
        return self._short_description

    def __str__(self):
        return self._str


class MultiProcess(Plugin):
    """
    Run tests in multiple processes. Requires processing module.
    """
    score = 1000
    status = {}

    def options(self, parser, env):
        """
        Register command-line options.
        """
        parser.add_option("--processes", action="store",
                          default=env.get('NOSE_PROCESSES', 0),
                          dest="multiprocess_workers",
                          metavar="NUM",
                          help="Spread test run among this many processes. "
                          "Set a number equal to the number of processors "
                          "or cores in your machine for best results. "
                          "[NOSE_PROCESSES]")
        parser.add_option("--process-timeout", action="store",
                          default=env.get('NOSE_PROCESS_TIMEOUT', 10),
                          dest="multiprocess_timeout",
                          metavar="SECONDS",
                          help="Set timeout for return of results from each "
                          "test runner process. [NOSE_PROCESS_TIMEOUT]")

    def configure(self, options, config):
        """
        Configure plugin.
        """
        try:
            self.status.pop('active')
        except KeyError:
            pass
        if not hasattr(options, 'multiprocess_workers'):
            self.enabled = False
            return
        # don't start inside of a worker process
        if config.worker:
            return
        self.config = config
        try:
            workers = int(options.multiprocess_workers)
        except (TypeError, ValueError):
            workers = 0
        if workers:
            _import_mp()
            if Process is None:
                self.enabled = False
                return
            self.enabled = True
            self.config.multiprocess_workers = workers
            self.config.multiprocess_timeout = int(options.multiprocess_timeout)
            self.status['active'] = True

    def prepareTestLoader(self, loader):
        """Remember loader class so MultiProcessTestRunner can instantiate
        the right loader.
        """
        self.loaderClass = loader.__class__

    def prepareTestRunner(self, runner):
        """Replace test runner with MultiProcessTestRunner.
        """
        # replace with our runner class
        return MultiProcessTestRunner(stream=runner.stream,
                                      verbosity=self.config.verbosity,
                                      config=self.config,
                                      loaderClass=self.loaderClass)


class MultiProcessTestRunner(TextTestRunner):

    def __init__(self, **kw):
        self.loaderClass = kw.pop('loaderClass', loader.defaultTestLoader)
        super(MultiProcessTestRunner, self).__init__(**kw)

    def run(self, test):
        """
        Execute the test (which may be a test suite). If the test is a suite,
        distribute it out among as many processes as have been configured, at
        as fine a level as is possible given the context fixtures defined in the
        suite or any sub-suites.

        """
        log.debug("%s.run(%s) (%s)", self, test, os.getpid())
        wrapper = self.config.plugins.prepareTest(test)
        if wrapper is not None:
            test = wrapper

        # plugins can decorate or capture the output stream
        wrapped = self.config.plugins.setOutputStream(self.stream)
        if wrapped is not None:
            self.stream = wrapped

        testQueue = Queue()
        resultQueue = Queue()
        tasks = {}
        completed = {}
        workers = []
        to_teardown = []
        shouldStop = Event()

        result = self._makeResult()
        start = time.time()

        # dispatch and collect results
        # put indexes only on queue because tests aren't picklable
        for case in self.nextBatch(test):
            log.debug("Next batch %s (%s)", case, type(case))
            if (isinstance(case, nose.case.Test) and
                isinstance(case.test, failure.Failure)):
                log.debug("Case is a Failure")
                case(result) # run here to capture the failure
                continue
            # handle shared fixtures
            if isinstance(case, ContextSuite) and self.sharedFixtures(case):
                log.debug("%s has shared fixtures", case)
                try:
                    case.setUp()
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    log.debug("%s setup failed", sys.exc_info())
                    result.addError(case, sys.exc_info())
                else:
                    to_teardown.append(case)
                    for _t in case:
                        test_addr = self.address(_t)
                        testQueue.put(test_addr, block=False)
                        tasks[test_addr] = None
                        log.debug("Queued shared-fixture test %s (%s) to %s",
                                  len(tasks), test_addr, testQueue)

            else:
                test_addr = self.address(case)
                testQueue.put(test_addr, block=False)
                tasks[test_addr] = None
                log.debug("Queued test %s (%s) to %s",
                          len(tasks), test_addr, testQueue)

        log.debug("Starting %s workers", self.config.multiprocess_workers)
        for i in range(self.config.multiprocess_workers):
            p = Process(target=runner, args=(i,
                                             testQueue,
                                             resultQueue,
                                             shouldStop,
                                             self.loaderClass,
                                             result.__class__,
                                             pickle.dumps(self.config)))
            # p.setDaemon(True)
            p.start()
            workers.append(p)
            log.debug("Started worker process %s", i+1)

        num_tasks = len(tasks)
        while tasks:
            log.debug("Waiting for results (%s/%s tasks)",
                      len(completed), num_tasks)
            try:
                addr, batch_result = resultQueue.get(
                    timeout=self.config.multiprocess_timeout)
                log.debug('Results received for %s', addr)
                try:
                    tasks.pop(addr)
                except KeyError:
                    log.debug("Got result for unknown task? %s", addr)
                else:
                    completed[addr] = batch_result
                self.consolidate(result, batch_result)
                if (self.config.stopOnError
                    and not result.wasSuccessful()):
                    # set the stop condition
                    shouldStop.set()
                    break
            except Empty:
                log.debug("Timed out with %s tasks pending", len(tasks))
                any_alive = False
                for w in workers:
                    if w.is_alive():
                        any_alive = True
                        break
                if not any_alive:
                    log.debug("All workers dead")
                    break
        log.debug("Completed %s/%s tasks (%s remain)",
                  len(completed), num_tasks, len(tasks))

        for case in to_teardown:
            log.debug("Tearing down shared fixtures for %s", case)
            try:
                case.tearDown()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                result.addError(case, sys.exc_info())

        stop = time.time()

        result.printErrors()
        result.printSummary(start, stop)
        self.config.plugins.finalize(result)

        # Tell all workers to stop
        for w in workers:
            if w.is_alive():
                testQueue.put('STOP', block=False)

        return result

    def address(self, case):
        if hasattr(case, 'address'):
            file, mod, call = case.address()
        elif hasattr(case, 'context'):
            file, mod, call = test_address(case.context)
        else:
            raise Exception("Unable to convert %s to address" % case)
        parts = []
        if file is None:
            if mod is None:
                raise Exception("Unaddressable case %s" % case)
            else:
                parts.append(mod)
        else:
            # strip __init__.py(c) from end of file part
            # if present, having it there confuses loader
            dirname, basename = os.path.split(file)
            if basename.startswith('__init__'):
                file = dirname
            parts.append(file)
        if call is not None:
            parts.append(call)
        return ':'.join(map(str, parts))

    def nextBatch(self, test):
        # allows tests or suites to mark themselves as not safe
        # for multiprocess execution
        if hasattr(test, 'context'):
            if not getattr(test.context, '_multiprocess_', True):
                return

        if ((isinstance(test, ContextSuite)
             and test.hasFixtures(self.checkCanSplit))
            or not getattr(test, 'can_split', True)
            or not isinstance(test, unittest.TestSuite)):
            # regular test case, or a suite with context fixtures

            # special case: when run like nosetests path/to/module.py
            # the top-level suite has only one item, and it shares
            # the same context as that item. In that case, we want the
            # item, not the top-level suite
            if isinstance(test, ContextSuite):
                contained = list(test)
                if (len(contained) == 1
                    and getattr(contained[0], 'context', None) == test.context):
                    test = contained[0]
            yield test
        else:
            # Suite is without fixtures at this level; but it may have
            # fixtures at any deeper level, so we need to examine it all
            # the way down to the case level
            for case in test:
                for batch in self.nextBatch(case):
                    yield batch

    def checkCanSplit(self, context, fixt):
        """
        Callback that we use to check whether the fixtures found in a
        context or ancestor are ones we care about.

        Contexts can tell us that their fixtures are reentrant by setting
        _multiprocess_can_split_. So if we see that, we return False to
        disregard those fixtures.
        """
        if not fixt:
            return False
        if getattr(context, '_multiprocess_can_split_', False):
            return False
        return True

    def sharedFixtures(self, case):
        context = getattr(case, 'context', None)
        if not context:
            return False
        return getattr(context, '_multiprocess_shared_', False)

    def consolidate(self, result, batch_result):
        log.debug("batch result is %s" , batch_result)
        try:
            output, testsRun, failures, errors, errorClasses = batch_result
        except ValueError:
            log.debug("result in unexpected format %s", batch_result)
            failure.Failure(*sys.exc_info())(result)
            return
        self.stream.write(output)
        result.testsRun += testsRun
        result.failures.extend(failures)
        result.errors.extend(errors)
        for key, (storage, label, isfail) in errorClasses.items():
            if key not in result.errorClasses:
                # Ordinarily storage is result attribute
                # but it's only processed through the errorClasses
                # dict, so it's ok to fake it here
                result.errorClasses[key] = ([], label, isfail)
            mystorage, _junk, _junk = result.errorClasses[key]
            mystorage.extend(storage)
        log.debug("Ran %s tests (%s)", testsRun, result.testsRun)


def runner(ix, testQueue, resultQueue, shouldStop,
           loaderClass, resultClass, config):
    config = pickle.loads(config)
    config.plugins.begin()
    log.debug("Worker %s executing", ix)
    log.debug("Active plugins worker %s: %s", ix, config.plugins._plugins)
    loader = loaderClass(config=config)
    loader.suiteClass.suiteClass = NoSharedFixtureContextSuite

    def get():
        case = testQueue.get(timeout=config.multiprocess_timeout)
        return case

    def makeResult():
        stream = _WritelnDecorator(StringIO())
        result = resultClass(stream, descriptions=1,
                             verbosity=config.verbosity,
                             config=config)
        plug_result = config.plugins.prepareTestResult(result)
        if plug_result:
            return plug_result
        return result

    def batch(result):
        failures = [(TestLet(c), err) for c, err in result.failures]
        errors = [(TestLet(c), err) for c, err in result.errors]
        errorClasses = {}
        for key, (storage, label, isfail) in result.errorClasses.items():
            errorClasses[key] = ([(TestLet(c), err) for c, err in storage],
                                 label, isfail)
        return (
            result.stream.getvalue(),
            result.testsRun,
            failures,
            errors,
            errorClasses)
    try:
        try:
            for test_addr in iter(get, 'STOP'):
                if shouldStop.is_set():
                    break
                result = makeResult()
                test = loader.loadTestsFromNames([test_addr])
                log.debug("Worker %s Test is %s (%s)", ix, test_addr, test)

                try:
                    test(result)
                    resultQueue.put((test_addr, batch(result)))
                except KeyboardInterrupt, SystemExit:
                    raise
                except:
                    log.exception("Error running test or returning results")
                    failure.Failure(*sys.exc_info())(result)
                    resultQueue.put((test_addr, batch(result)))
        except Empty:
            log.debug("Worker %s timed out waiting for tasks", ix)
    finally:
        testQueue.close()
        resultQueue.close()
    log.debug("Worker %s ending", ix)


class NoSharedFixtureContextSuite(ContextSuite):
    """
    Context suite that never fires shared fixtures.

    When a context sets _multiprocess_shared_, fixtures in that context
    are executed by the main process. Using this suite class prevents them
    from executing in the runner process as well.

    """

    def setupContext(self, context):
        if getattr(context, '_multiprocess_shared_', False):
            return
        super(NoSharedFixtureContextSuite, self).setupContext(context)

    def teardownContext(self, context):
        if getattr(context, '_multiprocess_shared_', False):
            return
        super(NoSharedFixtureContextSuite, self).teardownContext(context)
