import os
import sys
import json
import subprocess
import flet as ft
from time import sleep

#-Custom imports-#
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utils

#-Main class for PythonOTA-#
class PythonOTA:

    #-Init function-#
    def __init__(self, page: ft.Page) -> None:

        #-Page properties-#
        self.page = page
        self.page.title = "Python OTA"
        self.page.window.maximized = True
        self.page.window.full_screen = True
        self.connected_text = "Device connected: 🟢" + (" " * 100)
        self.disconnected_text = "Device not connected: 🔴" + (" " * 100)
        self.page.on_keyboard_event = self.on_keyboard_event_handler
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        #-Loading the JSON config-#
        with open("config.json", "r", encoding = "utf-8") as file:
            self.config = json.load(file)

        #-Running initialization functions-#
        self.components_init()


    #-Function to create base components-#
    def components_init(self):

        #-Creating component objects-#
        self.label_connect_status = ft.Text(value = self.disconnected_text)
        self.tf_ip_address = ft.TextField(label = "Enter Device IP.", width = 300, value = self.config["device_ip"])
        self.button_connect = ft.ElevatedButton(text = "Connect device", on_click = self.button_connect_event_handler)
        self.header_title = ft.Text("Python OTA", size = 60, weight = ft.FontWeight.BOLD, text_align = ft.TextAlign.CENTER, height = 100)

        #-Card containing input and button-#
        components = [self.label_connect_status, self.tf_ip_address, self.button_connect]
        column_card = ft.Column(components, alignment = ft.MainAxisAlignment.CENTER, horizontal_alignment = ft.CrossAxisAlignment.CENTER, spacing = 20)
        self.card_main = ft.Container(content = column_card, padding = 30, bgcolor = ft.colors.GREY_900, border_radius = 10, width = 350)

        #-Adding these components objects to the page-#
        self.page.add(self.header_title)
        self.page.add(self.card_main)
        self.page.add(ft.Container(height = 250))


    #-Function to create connection with your android-#
    def button_connect_event_handler(self, _: ft.ControlEvent):

        #-Disabling the button during runtime-#
        self.button_connect.disabled = True
        self.page.update(self.button_connect)

        #-Running the adb commands to connect to your device-#
        connected_devices = subprocess.run(["adb", "devices"], capture_output = True, text = True).stdout.strip()
        device_ip = self.tf_ip_address.value + ":5555"

        #-Give the device connected signal if connected-#
        if device_ip in connected_devices:
            sleep(1)
            self.label_connect_status.value = self.connected_text
            self.page.open(ft.AlertDialog(title = ft.Text(f"Connected successfully to {device_ip}.", text_align = ft.TextAlign.CENTER), title_padding = ft.padding.only(top = 20, left = 20, right = 20)))

        #-Else run the connect function to establish the connection-#
        else:
            status = utils.connect(device_ip)

            #-Give the device connected signal if connected-#
            if status:
                self.page.open(ft.AlertDialog(title = ft.Text(f"Connected successfully to {device_ip}.", text_align = ft.TextAlign.CENTER), title_padding = ft.padding.only(top = 20, left = 20, right = 20)))
                self.label_connect_status.value = self.connected_text

            #-Else give the error message-#
            else:
                self.page.open(ft.AlertDialog(title = ft.Text(utils.error_message, text_align = ft.TextAlign.LEFT), title_padding = ft.padding.only(top = 20, left = 20, right = 20)))
                self.label_connect_status.value = self.disconnected_text

        #-Enabling the button again and updating the page-#
        self.button_connect.disabled = False
        self.page.update()


    #-Function to handle keyboard bindings-#
    def on_keyboard_event_handler(self, event: ft.KeyboardEvent):

        #-Supported events-#
        events = {"F11": self.fullscreen_toggle_handler}

        #-Executing the events if key match else execute an empty lambda function-#
        events.get(event.key, lambda: None)()


    def fullscreen_toggle_handler(self):

        #-Toggling full screen on and off and updating the page-#
        self.page.window.full_screen = not self.page.window.full_screen
        self.page.update()


#-Running the app-#
ft.app(PythonOTA)
