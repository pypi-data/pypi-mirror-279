import pytest
from src.terminal_colors import *

display_colors = DisplayColors()


def test_show_light_colors():
    display_colors.show_light_colors_and_backgrounds()


def test_show_dark_colors():
    display_colors.show_dark_colors_and_backgrounds()


def test_show_all_colors():
    display_colors.show_all_colors_and_backgrounds()


def test_error_default():
    TerminalColors.error("This Is An Error")


def test_error_print_false():
    print(TerminalColors.error("This Is An Error Message", should_print=False))


def test_error_different_color():
    TerminalColors.error("This Is An Error Message", formatting=TerminalColors.LIGHT_RED + TerminalColors.ITALIC)


def test_warning_default():
    TerminalColors.warning("This Is A Warning Message")


def test_warning_print_false():
    print(TerminalColors.warning("This Is A Warning Message", should_print=False))


def test_warning_different_color():
    TerminalColors.warning("This Is A Warning Message", formatting=TerminalColors.LIGHT_YELLOW + TerminalColors.ITALIC)


def test_success_default():
    TerminalColors.success("This Is An Success Message")


def test_success_print_false():
    print(TerminalColors.success("This Is A Success Message", should_print=False))


def test_success_different_color():
    TerminalColors.success("This Is A Success Message", formatting=TerminalColors.LIGHT_GREEN + TerminalColors.ITALIC)


def test_info_default():
    TerminalColors.info("This Is An Info Message")


def test_info_print_false():
    print(TerminalColors.info("This Is An Info Message", should_print=False))


def test_info_different_color():
    TerminalColors.info("This Is An Info Message", formatting=TerminalColors.BLUE + TerminalColors.ITALIC)

