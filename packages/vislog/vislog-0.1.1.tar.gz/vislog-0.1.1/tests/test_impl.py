# -*- coding: utf-8 -*-

import pytest
import time
from vislog.impl import (
    format_line,
    format_ruler,
    AlignEnum,
    VisLog,
)

logger = VisLog(
    name="vis_logger_unit_test",
    # log_format="%(message)s",
    # tab="    ",
)


def setup_module(module):
    print("")


def _test_format_line():
    assert format_line("hello") == "| hello"
    assert format_line("hello", nest=1) == "| | hello"
    assert format_line("hello", nest=1, _pipes=["| ", "# "]) == "| # hello"

    assert format_line("hello", indent=1) == "|   hello"
    assert format_line("hello", indent=1, nest=1) == "| |   hello"
    assert format_line("hello", indent=1, nest=1, _pipes=["| ", "# "]) == "| #   hello"

    with pytest.raises(ValueError):
        format_line("hello", indent=1, nest=1, _pipes=["| "])


def _test_format_ruler():
    assert format_ruler(
        "Hello",
        length=40,
    ) == ("---------------- Hello -----------------")
    assert format_ruler(
        "Hello",
        length=20,
    ) == ("------ Hello -------")
    assert format_ruler(
        "Hello",
        char="=",
        length=40,
    ) == ("================ Hello =================")
    assert format_ruler(
        "Hello",
        corner="+",
        length=40,
    ) == ("+--------------- Hello ----------------+")
    assert format_ruler(
        "Hello",
        align=AlignEnum.left,
        length=40,
    ) == ("----- Hello ----------------------------")
    assert format_ruler(
        "Hello",
        align=AlignEnum.right,
        length=40,
    ) == ("---------------------------- Hello -----")
    assert format_ruler(
        "Hello",
        left_padding=3,
        align=AlignEnum.left,
        length=40,
    ) == ("--- Hello ------------------------------")
    assert format_ruler(
        "Hello",
        right_padding=3,
        align=AlignEnum.right,
        length=40,
    ) == ("------------------------------ Hello ---")
    assert format_ruler(
        "Hello",
        right_padding=3,
        align=AlignEnum.right,
        length=40,
        nest=1,
    ) == ("| ---------------------------- Hello ---")
    assert format_ruler(
        "Hello",
        right_padding=3,
        align=AlignEnum.right,
        length=40,
        nest=2,
    ) == ("| | -------------------------- Hello ---")
    with pytest.raises(ValueError):
        format_ruler(
            "Hello",
            _pipes=["|"],
        )


def _test_nested_context_manager():
    print("")
    logger.ruler("section 1")
    logger.info("hello 1")
    with logger.nested():
        logger.ruler("section 1.1")
        logger.info("hello 1.1")
        with logger.nested():
            logger.ruler("section 1.1.1")
            logger.info("hello 1.1.1")
            logger.ruler("section 1.1.1")
        logger.ruler("section 1.1")
    logger.ruler("section 1")


def _test_disabled_context_manager():
    print("")

    logger.info("a")
    with logger.disabled(
        disable=True,
        # disable=False,
    ):
        logger.info("b")
    logger.info("c")


def _test_pretty_log_decorator():
    print("")

    @logger.pretty_log(pipe="🏭")
    def run_build():
        time.sleep(1)
        logger.info("run build")

    @logger.pretty_log(pipe="🧪")
    def run_test():
        time.sleep(1)
        logger.info("run test")
        with logger.nested():
            run_build()

    @logger.pretty_log(pipe="🚀")
    def run_deploy():
        time.sleep(1)
        logger.info("run deploy")
        with logger.nested():
            run_test()

    # run_deploy()

    @logger.pretty_log()
    def this_wont_work():
        logger.info("run this_wont_work")
        raise Exception("something wrong")

    @logger.pretty_log()
    def outter_may_work():
        logger.info("run outter_may_work")
        with logger.nested():
            this_wont_work()

    with pytest.raises(Exception):
        outter_may_work()


def _test_start_and_end():
    print("")

    @logger.start_and_end(
        msg="My Function 1",
        pipe="📦",
    )
    def my_func1(name: str):
        time.sleep(1)
        logger.info(f"{name} do something in my func 1")

    my_func1(name="alice")

    @logger.start_and_end(
        msg="My Function 2",
        pipe="📦",
    )
    def my_func2(name: str):
        time.sleep(1)
        logger.info(f"{name} do something in my func 1")
        raise ValueError("something wrong")

    with pytest.raises(Exception):
        my_func2(name="alice")


def _test_emoji_block():
    print("")

    @logger.emoji_block(
        msg="Deploy app {app_name}",
        emoji="🚀",
    )
    def deploy_app(app_name: str):
        logger.info("working ...")
        logger.info("done")

    deploy_app(app_name="my_app")


def _test_indent():
    logger.ruler("start test indent")

    logger.info("a")
    with logger.indent():
        logger.info("b")
        with logger.indent():
            logger.info("c")
        logger.info("d")
    logger.info("e")

    logger.info("x")
    with logger.indent(2):
        logger.info("y")
        logger.info("z", 2)

    logger.ruler("end test indent")


def test():
    with logger.disabled(
        disable=True,
        # disable=False,
    ):
        _test_format_line()
        _test_format_ruler()
        _test_nested_context_manager()
        _test_disabled_context_manager()
        _test_pretty_log_decorator()
        _test_start_and_end()
        _test_emoji_block()
        _test_indent()


if __name__ == "__main__":
    from vislog.tests import run_cov_test

    run_cov_test(__file__, "vislog.impl", preview=False)
