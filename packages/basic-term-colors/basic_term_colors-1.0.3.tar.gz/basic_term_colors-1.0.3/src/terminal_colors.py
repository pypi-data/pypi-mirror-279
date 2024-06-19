import os


class TerminalColors:
    """ TerminalColor,
    Modify Terminal Text and Background Color 
     and Formatting

     Returns a string with the ANSI Character Sequence
    """
    os.system("")

    END = '\33[0m'
    RESET = '\33[0m'
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    SELECTED = '\33[7m'

    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    TEAL = '\33[36m'
    WHITE = '\33[37m'

    BLACK_BACKGROUND = '\33[40m'
    RED_BACKGROUND = '\33[41m'
    GREEN_BACKGROUND = '\33[42m'
    YELLOW_BACKGROUND = '\33[43m'
    BLUE_BACKGROUND = '\33[44m'
    VIOLET_BACKGROUND = '\33[45m'
    TEAL_BACKGROUND = '\33[46m'
    WHITE_BACKGROUND = '\33[47m'

    GRAY = '\33[90m'
    LIGHT_RED = '\33[91m'
    LIGHT_GREEN = '\33[92m'
    LIGHT_YELLOW = '\33[93m'
    LIGHT_BLUE = '\33[94m'
    LIGHT_VIOLET = '\33[95m'
    LIGHT_TEAL = '\33[96m'
    LIGHT_GRAY = '\33[97m'

    GRAY_BACKGROUND = '\33[100m'
    LIGHT_RED_BACKGROUND = '\33[101m'
    LIGHT_GREEN_BACKGROUND = '\33[102m'
    LIGHT_YELLOW_BACKGROUND = '\33[103m'
    LIGHT_BLUE_BACKGROUND = '\33[104m'
    LIGHT_VIOLET_BACKGROUND = '\33[105m'
    LIGHT_TEAL_BACKGROUND = '\33[106m'
    LIGHT_GRAY_BACKGROUND = '\33[107m'

    @staticmethod
    def error(error_message: str, formatting=(RED + BOLD), should_print=True):
        """
        Easily Generate Error Log Message
        :param should_print: bool
        :param error_message: str
        :param formatting: str
        :return formatted string: str
        """
        if should_print:
            print(formatting + f"ERROR: {error_message}" + TerminalColors.RESET)
        return formatting + f"ERROR: {error_message}" + TerminalColors.RESET

    @staticmethod
    def warning(error_message: str, formatting=(YELLOW + BOLD), should_print=True):
        """
        Easily Generate Warning Log Message
        :param should_print: bool
        :param error_message: str
        :param formatting: str
        :return: str
        """
        if should_print:
            print(formatting + f"WARNING: {error_message}" + TerminalColors.RESET)
        return formatting + f"WARNING: {error_message}" + TerminalColors.RESET

    @staticmethod
    def success(error_message: str, formatting=(LIGHT_GREEN + BOLD), should_print=True):
        """
        Easily Generate Success Log Message
        :param should_print: bool
        :param error_message: str
        :param formatting: str
        :return: str
        """
        if should_print:
            print(formatting + f"SUCCESS: {error_message}" + TerminalColors.RESET)
        return formatting + f"SUCCESS: {error_message}" + TerminalColors.RESET

    @staticmethod
    def info(error_message: str, formatting=(LIGHT_GRAY + BOLD), should_print=True):
        """
        Easily Generate Success Info Message
        :param should_print: bool
        :param error_message: str
        :param formatting: str
        :return: str
        """
        if should_print:
            print(formatting + f"INFO: {error_message}" + TerminalColors.RESET)
        return formatting + f"INFO: {error_message}" + TerminalColors.RESET


class DisplayColors:
    """
    Helper Functions To Display All Combinations Of
    Colors, Styles and Backgrounds
    """
    os.system("")

    def __init__(self):
        self.background_colors = self.get_background_colors()
        self.text_colors = self.get_text_colors()
        self.text_styles = self.get_text_styles()

    @staticmethod
    def get_text_colors():
        colors = {
            "BLACK": TerminalColors.BLACK,
            "RED": TerminalColors.RED,
            "GREEN": TerminalColors.GREEN,
            "YELLOW": TerminalColors.YELLOW,
            "BLUE": TerminalColors.BLUE,
            "VIOLET": TerminalColors.VIOLET,
            "TEAL": TerminalColors.TEAL,
            "WHITE": TerminalColors.WHITE,
        }
        light_colors = {
            "GRAY": TerminalColors.GRAY,
            "LIGHT_RED": TerminalColors.LIGHT_RED,
            "LIGHT_GREEN": TerminalColors.LIGHT_GREEN,
            "LIGHT_YELLOW": TerminalColors.LIGHT_YELLOW,
            "LIGHT_BLUE": TerminalColors.LIGHT_BLUE,
            "LIGHT_VIOLET": TerminalColors.LIGHT_VIOLET,
            "LIGHT_TEAL": TerminalColors.LIGHT_TEAL,
            "LIGHT_GRAY": TerminalColors.LIGHT_GRAY,
        }
        return colors, light_colors

    @staticmethod
    def get_text_styles():
        styles = {
            "END": TerminalColors.END,
            "BOLD": TerminalColors.BOLD,
            "ITALIC": TerminalColors.ITALIC,
            "URL": TerminalColors.URL,
            "SELECTED": TerminalColors.SELECTED,
        }
        return styles

    @staticmethod
    def get_background_colors():
        background_colors = {
            "BLACK_BACKGROUND": TerminalColors.BLACK_BACKGROUND,
            "RED_BACKGROUND": TerminalColors.RED_BACKGROUND,
            "GREEN_BACKGROUND": TerminalColors.GREEN_BACKGROUND,
            "YELLOW_BACKGROUND": TerminalColors.YELLOW_BACKGROUND,
            "BLUE_BACKGROUND": TerminalColors.BLUE_BACKGROUND,
            "VIOLET_BACKGROUND": TerminalColors.VIOLET_BACKGROUND,
            "TEAL_BACKGROUND": TerminalColors.TEAL_BACKGROUND,
            "WHITE_BACKGROUND": TerminalColors.WHITE_BACKGROUND,
        }
        light_background_colors = {
            "GRAY_BACKGROUND": TerminalColors.GRAY_BACKGROUND,
            "LIGHT_RED_BACKGROUND": TerminalColors.LIGHT_RED_BACKGROUND,
            "LIGHT_GREEN_BACKGROUND": TerminalColors.LIGHT_GREEN_BACKGROUND,
            "LIGHT_YELLOW_BACKGROUND": TerminalColors.LIGHT_YELLOW_BACKGROUND,
            "LIGHT_BLUE_BACKGROUND": TerminalColors.LIGHT_BLUE_BACKGROUND,
            "LIGHT_VIOLET_BACKGROUND": TerminalColors.LIGHT_VIOLET_BACKGROUND,
            "LIGHT_TEAL_BACKGROUND": TerminalColors.LIGHT_TEAL_BACKGROUND,
            "LIGHT_GRAY_BACKGROUND": TerminalColors.LIGHT_GRAY_BACKGROUND, }
        return background_colors, light_background_colors

    def show_dark_colors_and_backgrounds(self):
        """
        Prints All Dark Colors, Background and Styles in Every Combination
        To The Terminal
        :return:
        """
        for style in self.text_styles.keys():
            for color in self.text_colors[0].keys():
                text = ''
                for background in self.background_colors[0].keys():
                    text_format = ';'.join([style, color, background])
                    color_format = f"{self.text_styles.get(style) + self.text_colors[0].get(color) + self.background_colors[0].get(background)}"
                    needed_white_space = 35 - len(text_format)
                    text += f'{color_format}{text_format}{" " * needed_white_space}{TerminalColors.RESET}'
                print(text)
            print('\n')

    def show_light_colors_and_backgrounds(self):
        """
        Prints All Light Colors, Background and Styles in Every Combination
        To The Terminal
        :return:
        """
        for style in self.text_styles.keys():
            for color in self.text_colors[1].keys():
                text = ''
                for background in self.background_colors[1].keys():
                    text_format = ';'.join([style, color, background])
                    color_format = f"{self.text_styles.get(style) + self.text_colors[1].get(color) + self.background_colors[1].get(background)}"
                    needed_white_space = 46 - len(text_format)
                    text += f'{color_format}{text_format}{" " * needed_white_space}{TerminalColors.RESET}'
                print(text)
            print('\n')

    def show_all_colors_and_backgrounds(self):
        """
        Prints All Colors, Background and Styles in Every Combination
        To The Terminal
        :return:
        """
        full_text = ""
        for style in self.text_styles.keys():
            for color in self.text_colors[0].keys():
                text = ''
                for background in self.background_colors[0].keys():
                    text_format = ';'.join([style, color, background])
                    color_format = f"{self.text_styles.get(style) + self.text_colors[0].get(color) + self.background_colors[0].get(background)}"
                    needed_white_space = 46 - len(text_format)
                    text += f'{color_format}{text_format}{" " * needed_white_space}{TerminalColors.RESET}'
                full_text += f"{text}\n"
            for color in self.text_colors[1].keys():
                text = ''
                for background in self.background_colors[1].keys():
                    text_format = ';'.join([style, color, background])
                    color_format = f"{self.text_styles.get(style) + self.text_colors[1].get(color) + self.background_colors[1].get(background)}"
                    needed_white_space = 46 - len(text_format)
                    text += f'{color_format}{text_format}{" " * needed_white_space}{TerminalColors.RESET}'
                full_text += f"{text}\n"
        return full_text
