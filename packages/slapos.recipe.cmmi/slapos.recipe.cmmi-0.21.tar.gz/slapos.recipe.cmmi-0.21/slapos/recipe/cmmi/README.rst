Supported options
=================

``url``

    URL to the package that will be downloaded and extracted. The
    supported package formats are .tar.gz, .tar.bz2, and .zip. The
    value must be a full URL,
    e.g. http://python.org/ftp/python/2.4.4/Python-2.4.4.tgz. The
    ``path`` option can not be used at the same time with ``url``.

``path``

    Path to a local directory containing the source code to be built
    and installed. The directory must contain the ``configure``
    script. The ``url`` option can not be used at the same time with
    ``path``.

``strip-top-level-dir``

    Omit the topmost directory of the package when unpacking.
    true or false. Defaults to false.

``prefix``

    Custom installation prefix passed to the ``--prefix`` option of the
    ``configure`` script. Defaults to the location of the part. Note that this
    is a convenience shortcut which assumes that the default ``configure``
    command is used to configure the package. If the ``configure-command``
    option is used to define a custom configure command no automatic
    ``--prefix`` injection takes place. You can also set the ``--prefix``
    parameter explicitly in ``configure-options``.

``shared``

    See documentation of slapos.recipe.build's default recipe.

``md5sum``

    MD5 checksum for the package file. If available the MD5
    checksum of the downloaded package will be compared to this value
    and if the values do not match the execution of the recipe will
    fail.

``make-binary``

    Path to the ``make`` program. Defaults to 'make' which
    should work on any system that has the ``make`` program available
    in the system ``PATH``.

``make-options``

    Extra ``KEY=VALUE`` options included in the invocation of the ``make``
    program. Multiple options can be given on separate lines to increase
    readability.

``make-targets``

    Targets for the ``make`` command. Defaults to 'install'
    which will be enough to install most software packages. You only
    need to use this if you want to build alternate targets. Each
    target must be given on a separate line.

``configure-command``

    Name of the configure command that will be run to generate the Makefile.
    This defaults to ``./configure`` which is fine for packages that come with
    a configure script. You may wish to change this when compiling packages
    with a different set up. See the ``Compiling a Perl package`` section for
    an example.

``configure-options``

    Extra options to be given to the ``configure`` script. By default
    only the ``--prefix`` option is passed which is set to the part
    directory. Each option must be given on a separate line.

``patch-binary``

    Path to the ``patch`` program. Defaults to 'patch' which should
    work on any system that has the ``patch`` program available in the
    system ``PATH``.

``patch-options``

    Options passed to the ``patch`` program. Defaults to ``-p0``.

``patches``

    List of patch files to the applied to the extracted source. Each
    file should be given on a separate line.

.. _Python hook scripts:

``pre-configure-hook``

    Custom python script that will be executed before running the
    ``configure`` script. The format of the options is::

        /path/to/the/module.py:name_of_callable
        url:name_of_callable
        url#md5sum:name_of_callable

    where the first part is a filesystem path or url to the python
    module and the second part is the name of the callable in the
    module that will be called.  The callable will be passed three
    parameters in the following order:

        1. The ``options`` dictionary from the recipe.

        2. The global ``buildout`` dictionary.

        3. A dictionary containing the current ``os.environ`` augmented with
           the part specific overrides.

    The callable is not expected to return anything.

    .. note:: The ``os.environ`` is not modified so if the hook script is
              interested in the environment variable overrides defined for the
              part it needs to read them from the dictionary that is passed in
              as the third parameter instead of accessing ``os.environ``
              directly.

``pre-make-hook``

    Custom python script that will be executed before running
    ``make``. The format and semantics are the same as with the
    ``pre-configure-hook`` option.

``post-make-hook``

    Custom python script that will be executed after running
    ``make``. The format and semantics are the same as with the
    ``pre-configure-hook`` option.

.. hook shell command:

``pre-configure``

    Shell command that will be executed before running ``configure``
    script. It takes the same effect as ``pre-configure-hook`` option
    except it's shell command.

``pre-build``

    Shell command that will be executed before running ``make``. It
    takes the same effect as ``pre-make-hook`` option except it's
    shell command.

``pre-install``

    Shell command that will be executed before running ``make``
    install.

``post-install``

    Shell command that will be executed after running ``make``. It
    takes the same effect as ``post-make-hook`` option except it's
    shell command.

``keep-compile-dir``

    Switch to optionally keep the temporary directory where the
    package was compiled. This is mostly useful for other recipes that
    use this recipe to compile a software but wish to do some
    additional steps not handled by this recipe. The location of the
    compile directory is stored in ``options['compile-directory']``.
    Accepted values are ``true`` or ``false``, defaults to ``false``.

``promises``

   List the pathes and files should be existed after install part. The
   file or path must be absolute path. One line one item

   If any item doesn't exist, the recipe shows a warning message. The
   default value is empty.

``environment``

  See documentation of slapos.recipe.build's default recipe.

Additionally, the recipe honors the ``download-cache`` option set
in the ``[buildout]`` section and stores the downloaded files under
it. If the value is not set a directory called ``downloads`` will be
created in the root of the buildout and the ``download-cache``
option set accordingly.

The recipe will first check if there is a local copy of the package
before downloading it from the net. Files can be shared among
different buildouts by setting the ``download-cache`` to the same
location.

The recipe honors the ``prefix`` option set in the ``[buildout]``
section either. It implicts all the parts which recipe is
slapos.recipe.cmmi in this buildout process will be installed in the
same ``prefix`` option in the ``[buildout]``. Besides, once it takes
effects, recipe will return all the installed files in the prefix
directory. The own ``prefix`` of part will disable this behaviour.

If the ``buildout`` section has a valid ``prefix`` option, the recipe
will add it to environmet variables as the following::

  PATH=${buildout:prefix}/bin:$PATH
  CPPFLAGS=-I${buildout:prefix} $CPPFLAGS
  CFLAGS=-I${buildout:prefix} $CFFLAGS
  CXXFLAGS=-I${buildout:prefix} $CXXFLAGS
  LDFLAGS=-L${buildout:prefix}/lib


Example usage
=============

We'll use a few tarballs to demonstrate the recipe.
We'll modify one of them in-place but we don't want to alter the source tree.

    >>> import os
    >>> src = join(os.path.dirname(__file__), 'testdata')
    >>> ls(src)
    - Foo-Bar-0.0.0.tar.gz
    - haproxy-1.4.8-dummy.tar.gz
    - package-0.0.0.tar.gz
    >>> package_path = join(tmpdir('testdata'), 'package-0.0.0.tar.gz')
    >>> os.symlink(join(src, 'package-0.0.0.tar.gz'), package_path)

The package contains a dummy ``configure`` script that will simply
echo the options it was called with and create a ``Makefile`` that
will do the same.

Let's create a buildout to build and install the package.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = true
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... """ % package_path)

This will download, extract and build our demo package with the
default build options.

    >>> print(system(buildout)) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Installing package.
    configure --prefix=/sample_buildout/parts/package
    building package
    installing package
    <BLANKLINE>

Check option "promises"

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = packagex
    ...
    ... [packagex]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... promises = /usr/bin/myfoo
    ... """ % package_path)

This will download, extract and build our demo package with the
default build options.

    >>> print(system(buildout))
    Uninstalling package.
    Installing packagex.
    configure --prefix=/sample_buildout/parts/packagex
    building package
    installing package
    packagex: could not find promise '/usr/bin/myfoo'
    <BLANKLINE>

As we can see the configure script was called with the ``--prefix``
option by default followed by calls to ``make`` and ``make install``.

Installing a Perl package
=========================

The recipe can be used to install packages that use a slightly different build
process. Perl packages often come with a ``Makefile.PL`` script that performs
the same task as a ``configure`` script and generates a ``Makefile``.

We can build and install such a package by overriding the ``configure-command``
option. The following example builds a Foo::Bar perl module and installs it in
a custom location within the buildout::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = foobar
    ... perl_lib = ${buildout:directory}/perl_lib
    ...
    ... [foobar]
    ... recipe = slapos.recipe.cmmi
    ... configure-command = perl -I${buildout:perl_lib}/lib/perl5 Makefile.PL INSTALL_BASE=${buildout:perl_lib}
    ... url = file://%s/Foo-Bar-0.0.0.tar.gz
    ... """ % src)

    >>> print(system(buildout))
    Uninstalling packagex.
    Installing foobar.
    building package
    installing package

.. _Installing a package without an autoconf like system:

Installing a package without an ``autoconf`` like system
========================================================

Some packages do not use a configuration mechanism and simply provide a
``Makefile`` for building. It is common in these cases that the build process
is controlled entirely by direct options to ``make``. We can build such a
package by faking a configure command that does nothing and passing the
appropriate options to ``make``. The ``true`` utility found in most shell
environments is a good candidate for this although anything that returns a
zero exit code would do.

We are using a dummy "HAProxy" package as an example of a package with only a
Makefile and using explicit ``make`` options to control the build process.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = haproxy
    ...
    ... [haproxy]
    ... recipe = slapos.recipe.cmmi
    ... configure-command = true
    ... make-options =
    ...     TARGET=linux26
    ...     CPU=i686
    ...     USE_PCRE=1
    ... url = file://%s/haproxy-1.4.8-dummy.tar.gz
    ... """ % src)

    >>> print(system(buildout))
    Uninstalling foobar.
    Installing haproxy.
    Building HAProxy 1.4.8 (dummy package)
    TARGET: linux26
    CPU: i686
    USE_PCRE: 1
    Installing haproxy

Installing checkouts
====================

Sometimes instead of downloading and building an existing tarball we need to
work with code that is already available on the filesystem, for example an SVN
checkout.

Instead of providing the ``url`` option we will provide a ``path`` option to
the directory containing the source code.

Let's demonstrate this by first unpacking our test package to the filesystem
and building that.

    >>> checkout_dir = tmpdir('checkout')
    >>> import setuptools.archive_util
    >>> setuptools.archive_util.unpack_archive(package_path, checkout_dir)
    >>> ls(checkout_dir)
    d package-0.0.0

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... path = %s/package-0.0.0
    ... """ % checkout_dir)

    >>> print(system(buildout))
    Uninstalling haproxy.
    Installing package.
    package: Using local source directory: /checkout/package-0.0.0
    configure --prefix=/sample_buildout/parts/package
    building package
    installing package

Since using the ``path`` implies that the source code has been acquired
outside of the control of the recipe also the responsibility of managing it is
outside of the recipe.

Depending on the software you may need to manually run ``make clean`` etc.
between buildout runs if you make changes to the code. Also, the
``keep-compile-dir`` has no effect when ``path`` is used.


Advanced configuration
======================

The above options are enough to build most packages. However, in some cases it
is not enough and we need to control the build process more. Let's try again
with a new buildout and provide more options.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... md5sum = 6b94295c042a91ea3203857326bc9209
    ... prefix = /somewhere/else
    ... environment =
    ...     CFLAGS=-I/sw/include
    ...     LDFLAGS=-L/sw/lib -L/some/extra/lib
    ... configure-options =
    ...     --with-threads
    ...     --without-foobar
    ... make-targets =
    ...     install
    ...     install-lib
    ... patches =
    ...     patches/configure.patch
    ...     patches/Makefile.dist.patch
    ... """ % package_path)

This configuration uses custom configure options, environment variables,
custom prefix, multiple make targets and also patches the source code
before the scripts are run.

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    package: Applying patches
    package: [ENV] CFLAGS = -I/sw/include
    package: [ENV] LDFLAGS = -L/sw/lib -L/some/extra/lib
    patching file configure
    patching file Makefile.dist
    patched-configure --prefix=/somewhere/else --with-threads --without-foobar
    building patched package
    installing patched package
    installing patched package-lib
    <BLANKLINE>

Customizing the build process
=============================

Sometimes even the above is not enough and you need to be able to control the
process in even more detail. One such use case would be to perform dynamic
substitutions on the source code (possible based on information from the
buildout) which cannot be done with static patches or to simply run arbitrary
commands.

The recipe allows you to write custom python scripts that hook into the build
process. You can define a script to be run:

 - before the configure script is executed (pre-configure-hook)
 - before the make process is executed (pre-make-hook)
 - after the make process is finished (post-make-hook)

Each option needs to contain the following information

  /full/path/to/the/python/module.py:name_of_callable

where the callable object (here name_of_callable) is expected to take three
parameters:

    1. The ``options`` dictionary from the recipe.

    2. The global ``buildout`` dictionary.

    3. A dictionary containing the current ``os.environ`` augmented with
       the part specific overrides.

These parameters should provide the callable all the necessary information to
perform any part specific customization to the build process.

Let's create a simple python script to demonstrate the functionality. You can
naturally have separate modules for each hook or simply use just one or two
hooks. Here we use just a single module.

    >>> hooks = tmpdir('hooks')
    >>> write(hooks, 'customhandlers.py',
    ... """
    ... import logging
    ... log = logging.getLogger('hook')
    ...
    ... def preconfigure(options, buildout, environment):
    ...     log.info('This is pre-configure-hook!')
    ...
    ... def premake(options, buildout, environment):
    ...     log.info('This is pre-make-hook!')
    ...
    ... def postmake(options, buildout, environment):
    ...     log.info('This is post-make-hook!')
    ...
    ... """)

and a new buildout to try it out

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%(package_path)s
    ... pre-configure-hook = %(module)s:preconfigure
    ... pre-make-hook = %(module)s:premake
    ... post-make-hook = %(module)s:postmake
    ... """ % dict(package_path=package_path,
    ...            module=join(hooks, 'customhandlers.py')))

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    package: Executing pre-configure-hook
    hook: This is pre-configure-hook!
    configure --prefix=/sample_buildout/parts/package
    package: Executing pre-make-hook
    hook: This is pre-make-hook!
    building package
    installing package
    package: Executing post-make-hook
    hook: This is post-make-hook!

If you prefer to use shell script, then try these options:
  pre-configure
  pre-build
  pre-install
  post-install

Let's create a buildout to use these options.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... pre-configure = echo "Configure part: ${:_buildout_section_name_}"
    ... pre-build = echo "OH OH OH" > a.txt
    ... pre-install = cat a.txt
    ... post-install = rm -f a.txt && echo "Finished."
    ... """ % package_path)

This will run pre-configure, pre-build, pre-install, post-install as
shell command in the corresponding stage.

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    package: Executing pre-configure
    Configure part: package
    configure --prefix=/sample_buildout/parts/package
    package: Executing pre-build
    building package
    package: Executing pre-install
    OH OH OH
    installing package
    package: Executing post-install
    Finished.

Union prefix
============

If the recipe finds ``prefix`` option in the section buildout, it will

  * First, use this ``prefix`` as configure prefix, if
    ``configure-command`` isn't set in the part, or ``make-binary``
    equals 'make' and ``make-target`` includes pattern '\s+install.*'

  * Second, return all the new installed files in the prefix when the
    recipe returns after intall.

  * Finally, change some environment variables(See first section).

Let's see what happens when set prefix in the buildout section:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ... prefix = ${buildout:directory}/mylocal
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... pre-configure = mkdir -p "${buildout:prefix}"
    ... """ % package_path)

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    package: Executing pre-configure
    configure --prefix=/sample_buildout/mylocal
    building package
    installing package
    <BLANKLINE>

Look these environment variables and prefix's value, you know what's
the differences.

If part has its own ``prefix``, it will disable above behavious. For
example,

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ... prefix = ${buildout:directory}/mylocal
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... prefix = ${buildout:parts-directory}/package
    ... url = file://%s
    ... pre-configure = rm -rf "${buildout:prefix}"
    ... post-install = test -d "${buildout:prefix}" || echo "None"
    ... """ % package_path)

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    package: Executing pre-configure
    configure --prefix=/sample_buildout/parts/package
    building package
    installing package
    package: Executing post-install
    None

Then no extra environment variables such as CFLAGS etc., and no
${buildout:prefix} directory is created.

The following example shows how to install package, package-2 in one
prefix:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package package-2
    ... prefix = ${buildout:directory}/mylocal
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... pre-install = sleep 2; mkdir -p "${buildout:prefix}" ; echo x >"${buildout:prefix}/a.txt"
    ... [package-2]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... pre-install = sleep 2; mkdir -p "${buildout:prefix}" ; echo x >"${buildout:prefix}/b.txt"; echo
    ... """ % (package_path, package_path))

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    configure --prefix=/sample_buildout/mylocal
    building package
    package: Executing pre-install
    installing package
    Installing package-2.
    configure --prefix=/sample_buildout/mylocal
    building package
    package-2: Executing pre-install
    <BLANKLINE>
    installing package
    <BLANKLINE>

    >>> ls('mylocal')
    - a.txt
    - b.txt

Next we unintall package-2, it should only remove file b.txt (which seems broken currently
as nothing it is removing):

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ... prefix = ${buildout:directory}/mylocal
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... pre-install = sleep 2; mkdir -p "${buildout:prefix}" ; echo x >"${buildout:prefix}/a.txt"
    ... """ % package_path)

    >>> print(system(buildout))
    Uninstalling package-2.
    Updating package.

    >>> ls('mylocal')
    - a.txt
    - b.txt

Magic prefix
============

If configure-command is set, the recipe wouldn't insert "--prefix"
into configure-options. Then it checks whether both of make-binary and
make-targets aren't set, if so, string "prefix=xxx" will be appended
in the make-targets. xxx is the final prefix of this recipe. We call
it Magic Prefix.

In these options magic prefix can be represented by ``%(prefix)s``:

    ``configure-command``, ``configure-options``,
    ``make-binary``, ``make-options``, ``make-targets``,
    ``pre-configure``, ``pre-build``, ``pre-install``, ``post-install``

For example::

  [bzip2]
  post-install = rm %(prefix)s/*.h

The other part can refer to magic prefix of this part by
${part:prefix}, it will return the magic prefix, other than literal
value in the part section. For example::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package package-2
    ... prefix = /mytemp
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... configure-command = true
    ... make-binary = true
    ...
    ... [package-2]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... configure-command = true
    ... make-binary = true
    ... post-install = echo package magic prefix is ${package:prefix}
    ... """ % (package_path, package_path))

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    Installing package-2.
    package-2: Executing post-install
    package magic prefix is /mytemp
    <BLANKLINE>

Here it's another sample, we change Makefile before installing so it
can display "prefix" value in the stdout.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... configure-command = ./configure
    ... pre-install = sed -i -e "s/installing package/installing package at \\$\\$prefix /g" Makefile
    ... """ % package_path)

    >>> print(system(buildout))
    Uninstalling package-2.
    Uninstalling package.
    Installing package.
    configure
    building package
    package: Executing pre-install
    installing package at /sample_buildout/parts/package

You even can include pattern %(prefix)s in this option, it will be
replaced with the recipe final prefix.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... newest = false
    ... parts = package
    ...
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... configure-command = ./configure
    ... make-targets = install-lib prefix=%%(prefix)s
    ... pre-install = sed -i -e "s/installing package/installing package at \\$\\$prefix /g" Makefile
    ... """ % package_path)

    >>> print(system(buildout))
    Uninstalling package.
    Installing package.
    configure
    building package
    package: Executing pre-install
    installing package at /sample_buildout/parts/package -lib

For even more specific needs you can write your own recipe that uses
``slapos.recipe.cmmi`` and set the ``keep-compile-dir`` option to ``true``.
You can then continue from where this recipe finished by reading the location
of the compile directory from ``options['compile-directory']`` from your own
recipe.


Contributors
============

* Kai Lautaportti (dokai), Author
* Cédric de Saint Martin (desaintmartin)
* Marc Abramowitz (msabramo)
* Nicolas Dumazet (nicdumz)
* Guy Rozendorn (grzn)
* Marco Mariani (mmariani)
* galpin
