# -*- coding: utf-8 -*-

from acore_conf import api


def test():
    _ = api
    _ = api.read_config_file
    _ = api.read_config_content
    _ = api.update_config_file
    _ = api.update_config_content
    _ = api.write_config_content
    _ = api.write_config_file
    _ = api.apply_changes


if __name__ == "__main__":
    from acore_conf.tests import run_cov_test

    run_cov_test(__file__, "acore_conf.api", preview=False)
