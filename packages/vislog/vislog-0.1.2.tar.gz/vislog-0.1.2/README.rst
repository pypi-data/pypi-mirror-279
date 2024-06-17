
.. image:: https://readthedocs.org/projects/vislog/badge/?version=latest
    :target: https://vislog.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/vislog-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/vislog-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/vislog-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/vislog-project

.. image:: https://img.shields.io/pypi/v/vislog.svg
    :target: https://pypi.python.org/pypi/vislog

.. image:: https://img.shields.io/pypi/l/vislog.svg
    :target: https://pypi.python.org/pypi/vislog

.. image:: https://img.shields.io/pypi/pyversions/vislog.svg
    :target: https://pypi.python.org/pypi/vislog

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/vislog-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/vislog-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://vislog.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://vislog.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/vislog-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/vislog-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/vislog-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/vislog#files


Welcome to ``vislog`` Documentation
==============================================================================
.. image:: https://vislog.readthedocs.io/en/latest/_static/vislog-logo.png
    :target: https://vislog.readthedocs.io/en/latest/

``vislog`` is a ZERO-dependency logging library that brings visual effect to your logging message. It allows you to use any logging library you like, and just add visual effect.

.. code-block:: python

    @logger.emoji_block(msg="build", emoji="🏭")
    def run_build():
        time.sleep(1)
        logger.info("run build")

    @logger.emoji_block(msg="test", emoji="🧪")
    def run_test():
        time.sleep(1)
        logger.info("run test")
        with logger.nested():
            run_build()

    @logger.emoji_block(msg="deploy", emoji="🚀")
    def run_deploy():
        time.sleep(1)
        logger.info("run deploy")
        with logger.nested():
            run_test()

    run_deploy()

Will show:

.. code-block::

    [User 2024-06-16 15:06:44] +----- 🕑 🚀 Start 'deploy' -----------------------------------------------------+
    [User 2024-06-16 15:06:44] 🚀
    [User 2024-06-16 15:06:45] 🚀 run deploy
    [User 2024-06-16 15:06:45] 🚀 +----- 🕑 🧪 Start 'test' -----------------------------------------------------+
    [User 2024-06-16 15:06:45] 🚀 🧪
    [User 2024-06-16 15:06:46] 🚀 🧪 run test
    [User 2024-06-16 15:06:46] 🚀 🧪 +----- 🕑 🏭 Start 'build' --------------------------------------------------+
    [User 2024-06-16 15:06:46] 🚀 🧪 🏭
    [User 2024-06-16 15:06:47] 🚀 🧪 🏭 run build
    [User 2024-06-16 15:06:47] 🚀 🧪 🏭
    [User 2024-06-16 15:06:47] 🚀 🧪 +----- ⏰ ✅ 🏭 End 'build', elapsed = 1.01 sec ------------------------------+
    [User 2024-06-16 15:06:47] 🚀 🧪
    [User 2024-06-16 15:06:47] 🚀 +----- ⏰ ✅ 🧪 End 'test', elapsed = 2.02 sec ---------------------------------+
    [User 2024-06-16 15:06:47] 🚀
    [User 2024-06-16 15:06:47] +----- ⏰ ✅ 🚀 End 'deploy', elapsed = 3.03 sec ---------------------------------+


.. _install:

Install
------------------------------------------------------------------------------

``vislog`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install vislog

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade vislog
