Documenting plugins
===================

A parable. If a plugin is released on pypi without any documentation, does
anyone care?

To make it easy to document your plugins, nose includes a `Sphinx`_ extension
that will automatically generate plugin docs like those for nose's builtin
plugins. Simply add 'nose.sphinx.pluginopts' to the list of extensions in your
conf.py::

  extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
                'nose.sphinx.pluginopts']

Then in your plugin documents, include a title and the ``.. autoplugin``
directive::

  My Cool Plugin
  ==============

  .. autoplugin :: package.module.with.plugin
     :plugin: PluginClass

The ``:plugin:`` option is optional. In most cases, the directive will
automatically detect which class in the named module is the plugin to be
documented.

The output of the directive includes the docstring of the plugin module, the
options defined by the plugin, `autodoc`_ generated for the plugin class, and
the plugin module source. This is roughly equivalent to::

  My Cool Plugin
  ==============

  .. automodule :: package.module.with.plugin

  Options
  -------
  
  .. cmdoption :: --with-coolness

     Help text of the coolness option.

  .. cmdoption :: 

  Plugin
  -------
 
  .. autoclass :: package.module.with.plugin.PluginClass
     :members:

  Source
  ------

  .. include :: path/to/package/module/with/plugin.py
     :literal:

Document your plugins! Your users might not thank you -- but at least you'll
*have* some users.

.. _`Sphinx` : http://sphinx.pocoo.org/
.. _`autodoc`: http://sphinx.pocoo.org/ext/autodoc.html