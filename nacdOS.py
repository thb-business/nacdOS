import pjsua as pj
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import bluetooth  # For Bluetooth audio support

# SIP Configuration (use your Callcentric details)
SIP_USER = "17778691633102"  # Your Callcentric SIP Username
SIP_PASS = "HorizonUser2"    # Your Callcentric SIP Password
SIP_DOMAIN = "sip.callcentric.net"

class PhoneApp(App):
    def build(self):
        self.sip_client = SIPClient()
        self.layout = BoxLayout(orientation="vertical")
        
        self.label = Label(text="nacdOS - VoIP Phone")
        self.layout.add_widget(self.label)
        
        # Number Input
        self.number_input = TextInput(hint_text="Enter Number", font_size=30)
        self.layout.add_widget(self.number_input)
        
        # Call Button
        self.call_button = Button(text="Call", font_size=25, on_press=self.make_call)
        self.layout.add_widget(self.call_button)
        
        # End Call Button
        self.end_call_button = Button(text="End Call", font_size=25, on_press=self.end_call)
        self.layout.add_widget(self.end_call_button)

        return self.layout
    
    def make_call(self, instance):
        number = self.number_input.text
        if number:
            self.sip_client.make_call(number)
    
    def end_call(self, instance):
        self.sip_client.end_call()

class SIPClient:
    def __init__(self):
        self.lib = pj.Lib()
        self.lib.init(log_cfg=pj.LogConfig(level=3, console_level=3))
        
        # Create transport (UDP)
        transport = self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))
        self.lib.start()
        
        # Create SIP account with the updated Callcentric details
        acc_cfg = pj.AccountConfig()
        acc_cfg.id_uri = f"sip:{SIP_USER}@{SIP_DOMAIN}"
        acc_cfg.reg_config.registrar_uri = f"sip:{SIP_DOMAIN}"
        acc_cfg.sip_config.auth_creds.append(pj.AuthCredInfo("digest", SIP_DOMAIN, SIP_USER, 0, SIP_PASS))
        
        # Enable registration (register SIP account)
        acc_cfg.reg_config.registrar_uri = f"sip:{SIP_DOMAIN}"
        acc_cfg.reg_config.timeout = 1800  # Re-register every 30 minutes
        
        self.acc = self.lib.create_account(acc_cfg)
        self.call = None
    
    def make_call(self, number):
        if self.call is None:
            call_prm = pj.CallOpParam(True)
            self.call = self.acc.make_call(f"sip:{number}@{SIP_DOMAIN}", call_prm)
        else:
            self._show_popup("Already on call!", "You are already in a call.")

    def end_call(self):
        if self.call:
            self.call.hangup()
            self.call = None
        else:
            self._show_popup("No active call!", "You are not in an active call.")
    
    def _show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def init_bluetooth_audio(self):
        # Placeholder for Bluetooth Audio initialization
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("Nearby Bluetooth devices:")
        for addr, name in nearby_devices:
            print(f"{addr} - {name}")
        
        # Add more Bluetooth audio setup here based on your requirements

if __name__ == "__main__":
    PhoneApp().run()
