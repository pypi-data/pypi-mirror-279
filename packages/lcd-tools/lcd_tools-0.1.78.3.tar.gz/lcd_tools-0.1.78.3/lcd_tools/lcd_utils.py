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

    Args (Three arg override):
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
    """

    # 2 Arg Override
    if len(args) == 2:
        try:
            args[0].home()
            args[0].write_string(args[1])
        except:
            arg0 = str(type(args[0]))
            arg1 = str(type(args[1]))
            print(
                "\nERROR: Expected LCD and string objects \n Received: \n arg[0] - {} \n arg[1] - {}".format(
                    arg0, arg1
                )
            )
            raise SystemExit
    # 3 Arg Override
    elif len(args) == 3:
        args[0].home()
        for row in args[1]:
            args[0].write_string(row.ljust(args[2])[: args[2]])
            args[0].write_string("\r\n")
    else:
        print("\nERROR: Expected 2 or 3 arguments. \nReceived - {}".format(len(args)))
        raise SystemExit


def loop_string_single_line(
    lcd, string, row, num_cols=16, direction="right", speed=8
):

    # Validate direction argument
    valid_directions = ["right", "left"]
    if direction not in valid_directions:
        raise ValueError(
            f"Invalid direction: '{direction}'. Please specify 'right' or 'left'."
        )
    
    frame_buffer = [""] * (row+1)

    # Pad either side of the string for the full scrolling effect
    padding = " " * num_cols
    string = padding + string + padding

    if direction == "left":
        for i in range(len(string) - num_cols + 1):
            frame_buffer[row] = string[i : i + num_cols]
            write_to_lcd(lcd, frame_buffer, num_cols)
            time.sleep(1.99 - (speed*0.1))
    elif direction == "right":
        for i in range(len(string), num_cols - 1, -1):
            frame_buffer[row] = string[i - num_cols : i]
            write_to_lcd(lcd, frame_buffer, num_cols)
            time.sleep(1.99 - (speed*0.1))


def loop_string_double_line(
    string1, string2, lcd, frame_buffer, num_cols, direction="right", speed=8
):
    # Validate direction argument
    valid_directions = ["right", "left"]
    if direction not in valid_directions:
        raise ValueError(
            f"Invalid direction: '{direction}'. Please specify 'right' or 'left'."
        )

    # Pad either side of the string for the full scrolling effect
    padding = " " * num_cols
    string1 = padding + string1 + padding
    string2 = padding + string2 + padding

    scrollLength = len(string1) if (len(string1) > len(string2)) else len(string2)

    if direction == "left":
        for i in range(scrollLength - num_cols + 1):
            frame_buffer[0] = string1[i : i + num_cols]
            frame_buffer[1] = string2[i : i + num_cols]
            write_to_lcd(lcd, frame_buffer, num_cols)
            time.sleep(1.99 - (speed*0.1))
    elif direction == "right":
        for i in range(scrollLength, num_cols - 1, -1):
            frame_buffer[0] = string1[i - num_cols : i]
            frame_buffer[1] = string2[i - num_cols : i]
            write_to_lcd(lcd, frame_buffer, num_cols)
            time.sleep(1.99 - (speed*0.1))


if __name__ == "__main__":
    # Initialize LCD object
    lcd = CharLCD(
        numbering_mode=GPIO.BCM,
        cols=16,
        rows=2,
        pin_rs=25,
        pin_e=24,
        pins_data=[23, 17, 18, 22],
    )

    # 2-D list for each line in the LCD display
    frame_buffer = ["Line 0", "Line 1"]

    try:
        while True:
            # loop_string_single_line("Hello World", lcd, frame_buffer, 0, 16, "left")
            # loop_string_single_line(
            #    "Hello World", lcd, frame_buffer, 0, 16, "invalid_direction"
            # )
            loop_string_double_line(
                "Line0", "Line1", lcd, frame_buffer, 12, "left", 0.2
            )
    except ValueError as ve:
        print(f"Error: {ve}")
    finally:
        GPIO.cleanup()
