Contributing to nose
====================

You'd like to contribute to nose? Great! Now that nose is hosted under
`Mercurial <http://selenic.com/mercurial/>`__, contributing is even easier.

Get the code!
-------------

Start by getting a local working copy of nose, either stable, from google code::

  hg clone http://python-nose.googlecode.com/hg/ nose-stable

or unstable, from bitbucket::

  hg clone http://bitbucket.org/jpellerin/nose/ nose-unstable

If you plan to submit changes back to the core repository, you should set up a
public repository of your own somewhere. `Bitbucket <http://bitbucket.org>`__
is a good place to do that. Once you've set up your bitbucket nose repository,
if working from **stable**, pull from your working copy of nose-stable, and push
to bitbucket. That (with occasional merging) will be your normal practice for
keeping your repository up to date. If you're on bitbucket and working from
**unstable**, just **fork** http://bitbucket.org/jpellerin/nose/.

Running nose's tests
--------------------

nose runs its own test suite with `tox
<http://codespeak.net/tox/>`. You don't have to install tox to run
nose's test suite, but you should, because tox makes it easy to run
all tests on all supported python versions. You'll also need python
2.4, 2.5, 2.6, 2.7, 3.1 and jython installed somewhere in your $PATH.

Discuss
-------

Join the `nose developer list
<http://groups.google.com/group/nose-dev>`__ at google groups. It's
low-traffic and mostly signal.

What to work on?
----------------

You can find a list of open issues at nose's `google code repository
<http://code.google.com/p/python-nose/issues>`__. If you'd like to
work on an issue, leave a comment on the issue detailing how you plan
to fix it, and where to find the Mercurial repository where you will
publish your changes.

I have a great idea for a plugin...
-----------------------------------

Great! :doc:`Write it <plugins/writing>`. Release it on `pypi
<http://pypi.python.org>`__. If it gains a large following, and
becomes stable enough to work with nose's 6+ month release cycles, it
may be a good candidate for inclusion in nose's builtin plugins.

