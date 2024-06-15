# -*- coding: utf-8 -*-

from pathlib import Path
from acore_conf.impl import (
    read_config_file,
    apply_changes,
)

dir_here = Path(__file__).absolute().parent
p_auth = dir_here / "authserver.conf"
p_world = dir_here / "worldserver.conf"
p_auth_out = dir_here / "authserver.conf.out"
p_world_out = dir_here / "worldserver.conf.out"


def test_apply_changes():
    apply_changes(
        p_world,
        p_world_out,
        data={"worldserver": {"DataDir": "/home/azeroth-server/data"}},
    )
    config = read_config_file(p_world_out)
    assert config["worldserver"]["DataDir"] == "/home/azeroth-server/data"


if __name__ == "__main__":
    from acore_conf.tests import run_cov_test

    run_cov_test(__file__, "acore_conf.impl", preview=False)
