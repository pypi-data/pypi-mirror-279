"""
The following module provides multiple functions that provide various control options for LCD screen via RaspberryPi.

Extension of RPLCD library.

Utilizing RPi.GPIO
"""

import time

import RPi.GPIO as GPIO
from RPLCD import CharLCD


# def write_to_lcd(lcd, frame_buffer: list, num_cols: int, string: string) -> None :
def write_to_lcd(*args, **kwargs) -> None:
    """
    write_to_lcd is a multi-use function that can be called by other functions and directly through the library.

    Function can be overridden via argument inputs

    Args (Two arg override):
        lcd (list): **REQUIRED** - LCD object as defined by RPLCD library:
            lcd = CharLCD(
                numbering_mode = <string>,
                cols = <int>,
                rows = <int>,
                pin_rs = <int>,
                pin_e = <int>,
                pins_data = <list>
            )
        string (string): **optional** - String variable that usually will be written directly to lcd if given
            string  = <string>
    Return:
        (None)

    Args (Three arg override - buffer render):
        lcd (list): **REQUIRED** - LCD object as defined by RPLCD library:
            lcd = CharLCD(
                numbering_mode = <string>,
                cols = <int>,
                rows = <int>,
                pin_rs = <int>,
                pin_e = <int>,
                pins_data = <list>
            )


        frame_buffer (list): **optional** - Array of strings - Each string in array represents line on LCD screen. Can be used to write multiple lines at once.
            frame_buffer = [<string>, ... <string>]

        num_cols (int): **optional** - Integer representing number of columns on LCD screen
            num_cols = <int>
    Return:
        (None)

    Args (Three arg override - 'row' kwarg inclusion):
        lcd (list): **REQUIRED** - LCD object as defined by RPLCD library:
            lcd = CharLCD(
                numbering_mode = <string>,
                cols = <int>,
                rows = <int>,
                pin_rs = <int>,
                pin_e = <int>,
                pins_data = <list>
            )

        string (string): **REQUIRED** - String variable that usually will be written directly to lcd if given
            string  = <string>

        row (int): **REQUIRED** - Integer var for the row the text will be presented
            row =  <int>
    Return:
        (None)
    """

    # 2 Arg Override
    if len(args) == 2:

        lcd = args[0]
        frame_buffer = args[1]

        row = 0

        # Implementation of "Three arg override - 'row' kwarg inclusion" 
        if 'row' in kwargs:
            # Use row keyword argument to set cursor position
            row = kwargs['row']

            ## FUTURE DEVELOPMENT: 

        lcd.cursor_pos = (row, 0)

        try:
            lcd.write_string(args[1])
        except Exception as exc:
            arg0 = str(type(lcd))
            arg1 = str(type(frame_buffer))
            print(
                f"\nERROR: Expected LCD and string objects \n Received: \n arg[0] - {arg0} \n arg[1] - {arg1}"
                )
            raise SystemExit from exc
        
    # Implementation of "Args (Three arg override - buffer render)"
    elif len(args) == 3:
        # Three argument override: lcd object, frame_buffer list, and optionally num_cols
        lcd = args[0]
        frame_buffer = args[1]
        num_cols = args[2]


            # Write multiple lines from frame_buffer with optional num_cols for truncation
        lcd.home()
        for row in frame_buffer:
            lcd.write_string(row.ljust(num_cols)[:num_cols])
            lcd.write_string("\r\n")
    else:
        # Handle incorrect number of arguments
        print(f"\nERROR: Expected 2 or 3 arguments. \nReceived - {len(args)}")
        raise SystemExit


def scroll_line(lcd, string, row=0, num_cols=16, direction="left", speed=8):
    """
    scroll_line() is used to scroll a single text line across the LCD screen

    Args :
        lcd (list): **REQUIRED** - LCD object as defined by RPLCD library:
            lcd = CharLCD(
                numbering_mode = <string>,
                cols = <int>,
                rows = <int>,
                pin_rs = <int>,
                pin_e = <int>,
                pins_data = <list>
            )
        string (string): **REQUIRED** - String variable that usually will be written directly to lcd if given
            string  = <string>
        row (int): **REQUIRED** - Integer var for the row the text will be scrolled on.
            row =  <int>
        num_cols (int): **REQUIRED** - Integer var for the number of columns on lcd
            num_cols = <int>
        direction (string): **optional** - String var with direction text should scroll. Defaults to left scrolling
            direction = "left" OR "right"
        speed (int): **optional** - Integer var (1-10) representing speed of scrolling
            speed = <int>
    Return:
        (None)

    """

    # Validate direction argument
    valid_directions = ["right", "left"]
    if direction not in valid_directions:
        raise ValueError(
            f"Invalid direction: '{direction}'. Please specify 'right' or 'left'."
        )

    # Validate speed input
    if speed not in range(1, 10):
        raise ValueError(f"Invalid speed: '{speed}'. Please specify speed integer 1-10")

    frame_buffer = [""] * (row + 1)

    # Pad either side of the string for the full scrolling effect
    padding = " " * num_cols
    string = padding + string + padding

    lcd.cursor_pos = (row, 0)

    # Scroll through frame_buffer
    if direction == "left":
        for i in range(len(string) - num_cols + 1):
            frame_buffer[row] = string[i : i + num_cols]
            write_to_lcd(lcd, frame_buffer, num_cols)
            time.sleep(1.01 - (speed * 0.1))
    elif direction == "right":
        for i in range(len(string), num_cols - 1, -1):
            frame_buffer[row] = string[i - num_cols : i]
            write_to_lcd(lcd, frame_buffer, num_cols)
            time.sleep(1.01 - (speed * 0.1))


def scroll_frame_buffer(lcd, frame_buffer, num_cols, direction="left", speed=8):
    """
    scroll_frame_buffer() is used to scroll all lines of text in an input frame_buffer across the LCD screen

    Args :
        lcd (list): **REQUIRED** - LCD object as defined by RPLCD library:
            lcd = CharLCD(
                numbering_mode = <string>,
                cols = <int>,
                rows = <int>,
                pin_rs = <int>,
                pin_e = <int>,
                pins_data = <list>
            )
        string (string): **REQUIRED** - String variable that usually will be written directly to lcd if given
            string  = <string>
        row (int): **REQUIRED** - Integer var for the row the text will be scrolled on.
            row =  <int>
        num_cols (int): **REQUIRED** - Integer var for the number of columns on lcd
            num_cols = <int>
        direction (string): **optional** - String var with direction text should scroll. Defaults to left scrolling
            direction = "left" OR "right"
        speed (int): **optional** - Integer var (1-10) representing speed of scrolling
            speed = <int>
    Return:
        (None)

    """
    
    # Validate direction argument
    valid_directions = ["right", "left"]
    if direction not in valid_directions:
        raise ValueError(
            f"Invalid direction: '{direction}'. Please specify 'right' or 'left'."
        )

    # Validate speed input
    if speed not in range(1, 10):
        raise ValueError(f"Invalid speed: '{speed}'. Please specify speed integer 1-10")

    # Initilize padding, new padded buffer, and longest string to get full scroll
    padding = " " * num_cols
    padded_buffer = []
    longest_string = ""

    for row in frame_buffer:
        padded_string = padding + row + padding
        padded_buffer.append(padded_string)
        if len(longest_string) < len(padded_string):
            longest_string = padded_string

    # Determine the length of the longest padded string
    scroll_length = len(longest_string)

    # Scroll through frame_buffer
    if direction == "left":
        for i in range(scroll_length - num_cols + 1):
            temp_buffer = []
            for row in padded_buffer:
                temp_buffer.append(row[i : i + num_cols])
            write_to_lcd(lcd, temp_buffer, num_cols)
            time.sleep(1.01 - (speed * 0.1))
    elif direction == "right":
        for i in range(scroll_length - 1, num_cols - 2, -1):
            temp_buffer = []
            for row in padded_buffer:
                temp_buffer.append(row[i - num_cols + 1 : i + 1])
            write_to_lcd(lcd, temp_buffer, num_cols)
            time.sleep(1.01 - (speed * 0.1))
