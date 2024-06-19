# LCD_tools 
##### lcd-tools expands upon the RPLCD library to provide short-cut commands for various LCD Display control options.  

****  

### Commands:

* write_to_lcd( ) - A multi-function command that writes string variables to the LCD display. The exact behavior will depend on arguments.
    * **Write single string variable to LCD**:
    ```python
        # lcd = CharLCD object as defined by rplcd
        write_to_lcd(lcd, "Example String")
    ```
    * **Write a single string variable to a specific row on the LCD screen**:
    ```python
        # lcd = CharLCD object as defined by rplcd
        write_to_lcd(lcd, "Example String", row=1)
    ```
    * **Write a frame_buffer to the LCD screen**:
    ```python
        # lcd = CharLCD object as defined by rplcd
        
        # frame_buffer = ["Line 0", "Line 1", "Line2"]
        #   List of strings representing each line of the LCD screen
        
        # num_cols = int **Number of columns on LCD screen
    
        write_to_lcd(lcd, frame_buffer, num_cols)
    ```
    
* scroll_line( ) - Command used to scroll a single string across the specified line on LCD 
    * **Arguments**: scroll_line(lcd, string, row, num_cols, direction, speed)
        * lcd (list): ** REQUIRED ** - LCD object as defined by RPLCD library:
        * string (string): ** REQUIRED ** - String variable that will be scrolled across screen
        * row (int): ** optional ** - Integer var for the LCD screen row the text will be scrolled on.—defaults to row 0 if undefined. 
        * num_cols (int): ** REQUIRED ** - Integer var for number of columns on LCD screen
        * direction (string): ** optional ** - String var with direction ("left" or "right") text should scroll—defaults to left scrolling if undefined. 
        * speed (int): ** optional ** - Integer var (1-10) representing the speed of scrolling.—defaults to 8 if undefined.

    ```python
        scroll_line(lcd, "Hello World", 1, 12, "right", 9)
    ```

* scroll_frame_buffer( ) - Command used to scroll all lines in an input frame_buffer across the LCD screen
     * **Arguments**: scroll_frame_buffer(lcd, frame_buffer, num_cols, direction, speed)
        * lcd (list): ** REQUIRED ** - LCD object as defined by RPLCD library:
        * frame_buffer (string list): ** REQUIRED ** - List of strings that represent each line on LCD screen
        * num_cols (int): ** REQUIRED ** - Integer var for number of columns on LCD screen
        * direction (string): ** optional ** - String var with direction ("left" or "right") text should scroll—defaults to left scrolling if undefined. 
        * speed (int): ** optional ** - Integer var (1-10) representing speed of scrolling.—defaults to 8 if undefined.

    ```python
        frame_buffer = ["Line 0", "Line 1"]
        scroll_frame_buffer(lcd, frame_buffer, 12, "left", 8)
    ```

