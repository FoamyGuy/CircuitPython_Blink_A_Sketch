import board
import terminalio
import time
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_seesaw import seesaw, rotaryio, digitalio
from adafruit_turtle import Color, turtle
import displayio

board.DISPLAY.rotation = 180

NORTH = 0
EAST = 90
SOUTH = 180
WEST = 270

STEP_SIZE = 1
PEN_SIZE = 1

STATE_DRAWING = 0
STATE_MENU = 1

CUR_STATE = STATE_DRAWING

MENU_PRESS_THRESHOLD = 1
MENU_ITEMS = (
    "Pen Size",
    "Step Size",
    "Clear",
    "Exit Menu"
)

colors = (
    Color.WHITE,
    Color.RED,
    Color.YELLOW,
    Color.GREEN,
    Color.ORANGE,
    Color.BLUE,
    Color.PURPLE,
    Color.PINK,
    Color.GRAY,
    Color.LIGHT_GRAY,
    Color.BROWN,
    Color.DARK_GREEN,
    Color.TURQUOISE,
    Color.DARK_BLUE,
    Color.DARK_RED,
)

cur_pen_color_index = 0

menu_group = displayio.Group()

menu_title = label.Label(
    terminalio.FONT,
    anchor_point=(0.5, 0),
    anchored_position=(board.DISPLAY.width // 2, -4),
    text="Menu",
    scale=2
)
menu_group.append(menu_title)

menu_detail = label.Label(
    terminalio.FONT,
    anchor_point=(0.5, 0),
    anchored_position=(3 * board.DISPLAY.width // 4, 30),
    text="",
    scale=2
)
menu_group.append(menu_detail)

menu_list = GridLayout(
    x=10,
    y=30,
    width=200,
    height=100,
    grid_size=(1, len(MENU_ITEMS)),
    divider_lines=False
)
for index, item in enumerate(MENU_ITEMS):
    menu_list.add_content(
        label.Label(terminalio.FONT, scale=2, text=" {}".format(item)), grid_position=(0, index), cell_size=(1, 1)
    )

menu_group.append(menu_list)

MENU_SELECTED_INDEX = 0

turtle = turtle(board.DISPLAY)
turtle.pendown()

seesaw_up_down = seesaw.Seesaw(board.I2C(), addr=0x37)
seesaw_right_left = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw_up_down.get_version() >> 16) & 0xFFFF
print("seesaw1 Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw_product = (seesaw_right_left.get_version() >> 16) & 0xFFFF
print("seesaw2 Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw_up_down.pin_mode(24, seesaw_up_down.INPUT_PULLUP)
button_up_down = digitalio.DigitalIO(seesaw_up_down, 24)
button_up_down_held = False
encoder_up_down = rotaryio.IncrementalEncoder(seesaw_up_down)
last_position_up_down = encoder_up_down.position

seesaw_right_left.pin_mode(24, seesaw_right_left.INPUT_PULLUP)
button_right_left = digitalio.DigitalIO(seesaw_right_left, 24)
button_right_left_held = False
encoder_right_left = rotaryio.IncrementalEncoder(seesaw_right_left)
last_position_right_left = encoder_right_left.position

button_right_left_press_time = 0
button_right_left_ignore_release = False


def show_menu_selection(selected_index):
    for _index, _item in enumerate(MENU_ITEMS):
        item_label = menu_list.get_cell((0, _index)).text
        if _index != selected_index:
            item_label = item_label.lstrip(">")
            item_label = item_label.lstrip(" ")
            menu_list.get_cell((0, _index)).text = " {}".format(item_label)
        else:
            item_label = item_label.lstrip(" ")
            item_label = item_label.lstrip(">")
            menu_list.get_cell((0, _index)).text = ">{}".format(item_label)
            if _item == "Pen Size":
                menu_detail.text = "Current\n{}".format(PEN_SIZE)
            if _item == "Step Size":
                menu_detail.text = "Current\n{}".format(STEP_SIZE)


while True:
    #  read the encoder values
    # negate the position to make clockwise rotation positive
    position_up_down = -encoder_up_down.position
    position_right_left = -encoder_right_left.position

    if CUR_STATE == STATE_DRAWING:

        # if up/down encoder value changed
        if position_up_down != last_position_up_down:
            # if it went up
            if position_up_down > last_position_up_down:
                # point the turtle north
                turtle.setheading(NORTH)
                # move the turtle 1 unit
                turtle.forward(STEP_SIZE)

            else:  # position went down
                # point the turtle south
                turtle.setheading(SOUTH)
                # move the turtle 1 unit
                turtle.forward(STEP_SIZE)

        # if right/left encoder value changed
        if position_right_left != last_position_right_left:
            # if it went up
            if position_right_left > last_position_right_left:
                # point the turtle east
                turtle.setheading(EAST)
                # move the turtle 1 unit
                turtle.forward(STEP_SIZE)

            else:  # position went down
                # point the turtle west
                turtle.setheading(WEST)
                # move the turtle 1 unit
                turtle.forward(STEP_SIZE)

        if not button_up_down.value and not button_up_down_held:
            button_up_down_held = True
            print("Button up/down pressed")

        if button_up_down.value and button_up_down_held:
            button_up_down_held = False
            print("Button up/down released")
            cur_pen_color_index += 1
            if cur_pen_color_index >= len(colors):
                cur_pen_color_index = 0
            turtle.pencolor(colors[cur_pen_color_index])
            print("new color index: {}".format(cur_pen_color_index))

        if not button_right_left.value and not button_right_left_held:
            button_right_left_held = True
            print("Button right/left pressed")
            button_right_left_press_time = time.monotonic()

        if button_right_left.value and button_right_left_held:
            button_right_left_held = False
            print("Button right/left released")
            if not turtle.isdown():
                turtle.pendown()
            else:
                turtle.penup()

        if button_right_left_held:
            if time.monotonic() - button_right_left_press_time > MENU_PRESS_THRESHOLD:
                CUR_STATE = STATE_MENU
                MENU_SELECTED_INDEX = 0
                show_menu_selection(0)
                button_right_left_ignore_release = True
                board.DISPLAY.show(menu_group)

    if CUR_STATE == STATE_MENU:

        # if up/down encoder value changed
        if position_up_down != last_position_up_down:
            # if it went up
            if position_up_down > last_position_up_down:
                if MENU_SELECTED_INDEX == MENU_ITEMS.index("Step Size"):
                    STEP_SIZE += 1
            else:  # position went down
                if MENU_SELECTED_INDEX == MENU_ITEMS.index("Step Size"):
                    STEP_SIZE -= 1

            show_menu_selection(MENU_SELECTED_INDEX)

        # if right/left encoder value changed
        if position_right_left != last_position_right_left:
            # if it went up
            if position_right_left > last_position_right_left:
                MENU_SELECTED_INDEX -= 1
                if MENU_SELECTED_INDEX < 0:
                    MENU_SELECTED_INDEX = len(MENU_ITEMS) - 1

            else:  # position went down
                MENU_SELECTED_INDEX += 1
                if MENU_SELECTED_INDEX >= len(MENU_ITEMS):
                    MENU_SELECTED_INDEX = 0
            show_menu_selection(MENU_SELECTED_INDEX)

        if not button_right_left.value and not button_right_left_held:
            button_right_left_held = True
            print("Button right/left pressed")

        if button_right_left.value and button_right_left_held:
            print("Button right/left released")
            print("ignore: {}".format(button_right_left_ignore_release))
            button_right_left_held = False
            if not button_right_left_ignore_release:
                pass
            else:
                button_right_left_ignore_release = False

        if not button_up_down.value and not button_up_down_held:
            button_up_down_held = True
            print("Button up/down pressed")

        if button_up_down.value and button_up_down_held:
            button_up_down_held = False
            print("Button up/down released")
            if MENU_SELECTED_INDEX == MENU_ITEMS.index("Exit Menu"):
                print("back to drawing")
                CUR_STATE = STATE_DRAWING
                board.DISPLAY.show(turtle._splash)
            if MENU_SELECTED_INDEX == MENU_ITEMS.index("Step Size"):
                pass

        """
        STEP_SIZE += 1
        if STEP_SIZE >= 4:
            STEP_SIZE = 1
        print("new stepsize: {}".format(STEP_SIZE))
        """

    # update the last position variables
    last_position_right_left = position_right_left
    last_position_up_down = position_up_down
