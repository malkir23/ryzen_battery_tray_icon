from time import sleep
import os
from PIL import Image, ImageDraw
import pystray
from openrazer.client import DeviceManager

dir_path = os.path.dirname(os.path.realpath(__file__))
FULL_BATTERY_IMG = Image.open(f"{dir_path}/image/full.png")
LOW_BATTERY_IMG = Image.open(f"{dir_path}/image/low.png")
MIDDLE_BATTERY_IMG = Image.open(f"{dir_path}/image/middle.png")
CHARGED_BATTERY_IMG = Image.open(f"{dir_path}/image/charged.png")
DEVICE_MANAGER = DeviceManager()

# FULL_PERCENT = 80
MIDDLE_PERCENT = 40
LOW_PERCENT = 20
SIZE_TRAY_ICON = (20, 22)

def get_battery_img():
    """Gets the battery image."""
    viper = None
    for device in DEVICE_MANAGER.devices:
        if "Razer Viper Ultimate (Wireless)" == device.name:
            viper = device

    if viper is None:
        print("n/a")
        os._exit(0)

    battery_count = viper.battery_level
    if viper.is_charging:
        battery_img = CHARGED_BATTERY_IMG
    elif battery_count >= MIDDLE_PERCENT:
        battery_img = FULL_BATTERY_IMG
    elif battery_count >= LOW_PERCENT:
        battery_img = MIDDLE_BATTERY_IMG
    else:
        battery_img = LOW_BATTERY_IMG

    img = battery_img.copy()
    resized_image = img.resize(SIZE_TRAY_ICON)
    draw = ImageDraw.Draw(resized_image)
    draw.text((4, 5), str(battery_count), fill='black')
    return resized_image


def change_img(ico):
    """Changes the icon of the tray."""
    ico.visible = False
    ico.icon = get_battery_img()
    ico.visible = True
    sleep(10)
    ico.run(setup=change_img)


def on_clicked():
    """exits the application."""
    os._exit(0)


exit_menu = pystray.MenuItem("Exit razer battery status", on_clicked)

razer_icon = pystray.Icon(
    "Razer battery status", icon=LOW_BATTERY_IMG, menu=pystray.Menu(exit_menu)
)

razer_icon.run(setup=change_img)
