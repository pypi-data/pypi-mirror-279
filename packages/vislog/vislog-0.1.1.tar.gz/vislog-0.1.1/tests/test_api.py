# -*- coding: utf-8 -*-

import vislog


def test():
    _ = vislog.VisLog


if __name__ == "__main__":
    from vislog.tests import run_cov_test

    run_cov_test(__file__, "vislog.api", preview=False)
