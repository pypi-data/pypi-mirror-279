
.. .. image:: https://readthedocs.org/projects/acore-conf/badge/?version=latest
    :target: https://acore-conf.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_conf-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/acore_conf-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_conf-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_conf-project

.. image:: https://img.shields.io/pypi/v/acore-conf.svg
    :target: https://pypi.python.org/pypi/acore-conf

.. image:: https://img.shields.io/pypi/l/acore-conf.svg
    :target: https://pypi.python.org/pypi/acore-conf

.. image:: https://img.shields.io/pypi/pyversions/acore-conf.svg
    :target: https://pypi.python.org/pypi/acore-conf

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_conf-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_conf-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-conf.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-conf.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_conf-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_conf-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_conf-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-conf#files


Welcome to ``acore_conf`` Documentation
==============================================================================
.. image:: https://acore-conf.readthedocs.io/en/latest/_static/acore_conf-logo.png
    :target: https://acore-conf.readthedocs.io/en/latest/

**背景**

`AzerothCore <https://www.azerothcore.org/>`_ (acore) 是一个开源的魔兽世界模拟器, 其代码质量以及文档是目前 (2023 年) 我看来所有的开源魔兽世界模拟器中最好的. 它有一个 ``.conf`` 配置文件格式用于定义服务器的各种配置. 这个格式不是 acore 独有的, 而是所有的魔兽世界模拟器, 包括各个不同的资料片几乎都用的这个格式.

**Links**

- `How configuration files are composed <https://www.azerothcore.org/wiki/how-to-work-with-conf-files>`_: AzerothCore 官方对 config file 格式的解释.
- `authserver.conf <https://github.com/azerothcore/azerothcore-wotlk/blob/master/src/server/apps/authserver/authserver.conf.dist>`_: AzerothCore 官方 GitHub 源码中的初始 ``authserver.conf`` 文件.
- `worldserver.conf <https://github.com/azerothcore/azerothcore-wotlk/blob/master/src/server/apps/worldserver/worldserver.conf.dist>`_: AzerothCore 官方 GitHub 源码中的初始 ``worldserver.conf`` 文件.

**关于本项目**

本项目是一个简单的 Python 工具, 用于管理, 修改 ``.conf`` 文件. 使得开发者可以用业内比较通用的 JSON 格式对 ``.conf`` 进行修改.

**用法**

.. code-block:: python

    from acore_conf.api import apply_changes

    apply_changes(
        "/path/to/authserver.conf.dist",
        "/path/to/authserver.conf",
        data={"worldserver": {"DataDir": "/home/azeroth-server/data"}},
    )

**更多 API 详细文档请参考下面的链接**

- `acore_conf.api.update_config_content <https://acore-conf.readthedocs.io/en/latest/acore_conf/impl.html#acore_conf.impl.update_config_content>`_
- `acore_conf.api.apply_changes <https://acore-conf.readthedocs.io/en/latest/acore_conf/impl.html#acore_conf.impl.apply_changes>`_


.. _install:

Install
------------------------------------------------------------------------------

``acore_conf`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-conf

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-conf