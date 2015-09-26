# Compiled and Written by Donovan Bartish aka DRockstar
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement

transport_menu = ["TRANSPORT",
    "STOP", "PLAY", "RECORD", "SHIFT",
    "REWIND", "FFWD", "LOOP", "VIEW"
]

volume_menu = ["VOLUME",
    "MUTE", "SOLO", "ARM", "SHIFT",
    "BANK LEFT", "BANK RIGHT", "TRACK LEFT", "TRACK RIGHT"
]

pan_menu = ["PAN",
    "MUTE", "SOLO", "ARM", "SHIFT",
    "BANK LEFT", "BANK RIGHT", "TRACK LEFT", "TRACK RIGHT"
]

send_menu = ["SEND",
    "MUTE", "SOLO", "ARM", "SHIFT",
    "BANK LEFT", "BANK RIGHT", "SEND DOWN", "SEND UP"
]

device_menu = ["DEVICE",
    "DEVICE ON/OFF", "DEVICE LOCK", "ARM", "SHIFT",
    "DEVICE LEFT", "DEVICE RIGHT", "BANK DOWN", "BANK UP"
]

clip_menu = ["CLIPS",
    "CLIP STOP", "CLIP PLAY", "SCENE PLAY", "SHIFT",
    "CLIP UP", "CLIP DOWN", "CLIP LEFT", "CLIP RIGHT" 
]

class ControlModeSelector(ModeSelectorComponent):

    def __init__(self, parent, mixer, session, device, device_nav):
        ModeSelectorComponent.__init__(self)
        self._parent = parent
        self._mixer = mixer
        self._session = session
        self._device = device
        self._device_nav = device_nav
        self._controls = None
        self._pads = None
        self._transport_buttons = None
        self.sends_index = 0
        self.send_button_up = None
        self.send_button_down = None
        self.send_controls = []
        self._modes_buttons = []
        self._pads_len = None
        self._transport_len = None
        self._clip_launch_button = None
        self._clip_stop_button = None
        self._mode_index = 0

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._parent = None
        self._mixer = None
        self._session = None
        self._device = None
        self._device_nav = None
        self._controls = None
        self._pads = None
        self._transport_buttons = None
        self.sends_index = 0
        self.send_button_up = None
        self.send_button_down = None
        self.send_controls = []
        self._modes_buttons = []
        self._pads_len = None
        self._transport_len = None
        self._clip_launch_button = None
        self._clip_stop_button = None

    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button)
        self.set_mode(0)
        
    def set_lengths(self, pads, transport_buttons):
        self._pads_len = len(pads)
        self._transport_len = len(transport_buttons)

    def set_mode_buttons(self, buttons):
        assert isinstance(buttons, (tuple, type(None))) or AssertionError
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                assert isinstance(button, ButtonElement) or AssertionError
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

    def set_controls(self, controls, pads, transport_buttons):
        self._controls = controls
        self._pads = pads
        self._transport_buttons = transport_buttons
        self.update()

    def number_of_modes(self):
        # Max number of modes? 16 pads + 8 transport buttons, should be enough!?!
        return 24

    def update(self):
        if (self.is_enabled() and self._controls != None and self._pads != None 
        and self._mode_index in range(self.number_of_modes())):
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()
            mode = self._mode_index

            if mode == 0 or (mode - self._pads_len) == 0:
                menu = list(volume_menu)
                del menu[0]
                del menu[3]
                self._mixer.selected_strip().set_mute_button(self._pads[menu.index("MUTE")])
                self._mixer.selected_strip().set_solo_button(self._pads[menu.index("SOLO")])
                self._mixer.selected_strip().set_arm_button(self._pads[menu.index("ARM")])
                self._session.set_track_bank_buttons(self._pads[menu.index("BANK RIGHT")], self._pads[menu.index("BANK LEFT")])
                self._mixer.set_select_buttons(self._pads[menu.index("TRACK RIGHT")], self._pads[menu.index("TRACK LEFT")])
                self._set_volume_controls()
                self._parent.menu_message(volume_menu)

            elif mode == 1 or (mode - self._pads_len) == 1:
                menu = list(pan_menu)
                del menu[0]
                del menu[3]
                self._mixer.selected_strip().set_mute_button(self._pads[menu.index("MUTE")])
                self._mixer.selected_strip().set_solo_button(self._pads[menu.index("SOLO")])
                self._mixer.selected_strip().set_arm_button(self._pads[menu.index("ARM")])
                self._session.set_track_bank_buttons(self._pads[menu.index("BANK RIGHT")], self._pads[menu.index("BANK LEFT")])
                self._mixer.set_select_buttons(self._pads[menu.index("TRACK RIGHT")], self._pads[menu.index("TRACK LEFT")])
                self._set_pan_controls()
                self._parent.menu_message(pan_menu)

            elif mode == 2 or (mode - self._pads_len) == 2:
                menu = list(send_menu)
                del menu[0]
                del menu[3]
                self._mixer.selected_strip().set_mute_button(self._pads[menu.index("MUTE")])
                self._mixer.selected_strip().set_solo_button(self._pads[menu.index("SOLO")])
                self._mixer.selected_strip().set_arm_button(self._pads[menu.index("ARM")])
                self._session.set_track_bank_buttons(self._pads[menu.index("BANK RIGHT")], self._pads[menu.index("BANK LEFT")])
                self._set_send_nav(self._pads[menu.index("SEND UP")], self._pads[menu.index("SEND DOWN")])
                self._update_send_index(self.sends_index)

            elif mode == 3 or (mode - self._pads_len) == 3:
                menu = list(device_menu)
                del menu[0]
                del menu[3]
                self._device.set_on_off_button(self._pads[menu.index("DEVICE ON/OFF")])
                self._device.set_lock_button(self._pads[menu.index("DEVICE LOCK")])
                self._mixer.selected_strip().set_arm_button(self._pads[menu.index("ARM")])
                self._device_nav.set_device_nav_buttons(self._pads[menu.index("DEVICE LEFT")], self._pads[menu.index("DEVICE RIGHT")])
                self._device.set_bank_nav_buttons(self._pads[menu.index("BANK DOWN")], self._pads[menu.index("BANK UP")])
                self._device.set_parameter_controls(self._controls)
                self._parent.menu_message(device_menu)

            elif mode == 4 or (mode - self._pads_len) == 4:
                menu = list(clip_menu)
                del menu[0]
                del menu[3]
                self.application().view.show_view('Session')
                self._session._num_tracks = 1
                self._session._do_show_highlight()
                scene = self._session.scene(0)
                self._session.set_track_bank_buttons(self._pads[menu.index("CLIP RIGHT")], self._pads[menu.index("CLIP LEFT")])
                self._session.set_scene_bank_buttons(self._pads[menu.index("CLIP DOWN")], self._pads[menu.index("CLIP UP")])
                scene.set_launch_button(self._pads[menu.index("SCENE PLAY")])
                self._set_clip_launch_button(self._pads[menu.index("CLIP PLAY")])
                self._set_clip_stop_button(self._pads[menu.index("CLIP STOP")])
                strip = self._mixer.channel_strip(0)
                strip.set_volume_control(self._controls[0])
                strip.set_pan_control(self._controls[1])
                self.send_controls = []
                for index in range(len(self._controls) - 2):
                    self.send_controls.append(self._controls[index + 2])
                strip.set_send_controls(tuple(self.send_controls))
                self._parent.menu_message(clip_menu)

            else:
                self._mode_index = 0
                self.update()

    def _set_volume_controls(self):
        for index in range(len(self._controls)):
            strip = self._mixer.channel_strip(index)
            strip.set_volume_control(self._controls[index])

    def _set_pan_controls(self):
        for index in range(len(self._controls)):
            strip = self._mixer.channel_strip(index)
            strip.set_pan_control(self._controls[index])

    def _set_send_nav(self, send_up, send_down):
        if (send_up is not self.send_button_up):
            if (self.send_button_up != None):
                self.send_button_up.remove_value_listener(self._send_up_value)
            self.send_button_up = send_up
            if (self.send_button_up != None):
                self.send_button_up.add_value_listener(self._send_up_value)
        if (send_down is not self.send_button_down):
            if (self.send_button_down != None):
                self.send_button_down.remove_value_listener(self._send_down_value)
            self.send_button_down = send_down
            if (self.send_button_down != None):
                self.send_button_down.add_value_listener(self._send_down_value)

    def _send_up_value(self, value):
        assert isinstance(value, int)
        assert isinstance(self.send_button_up, ButtonElement)
        if value > 0 or not self.send_button_up.is_momentary():
            if self.sends_index == (len(self.song().return_tracks) - 1):
                self.sends_index = 0
            else:
                new_sends_index = self.sends_index + 1
                self.sends_index = new_sends_index
        self._update_send_index(self.sends_index)

    def _send_down_value(self, value):
        assert isinstance(value, int)
        assert isinstance(self.send_button_down, ButtonElement)
        if value > 0 or not self.send_button_down.is_momentary():
            if self.sends_index == 0:
                self.sends_index = (len(self.song().return_tracks) - 1)
            else:
                new_sends_index = self.sends_index - 1
                self.sends_index = new_sends_index
        self._update_send_index(self.sends_index)

    def _update_send_index(self, sends_index):
        send_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        for index in range(len(self._controls)):
            self.send_controls = []
            strip = self._mixer.channel_strip(index)
            for i in range(12):
                self.send_controls.append(None)
            self.send_controls[sends_index] = self._controls[index]
            strip.set_send_controls(tuple(self.send_controls))
        menu = list(send_menu)
        menu[0] = menu[0].replace("SEND", "SEND " + send_letters[sends_index])
        self._parent.menu_message(menu)

    def _set_clip_launch_button(self, button):
        if (button is not self._clip_launch_button):
            if (self._clip_launch_button != None):
                self._clip_launch_button.remove_value_listener(self._fire_clip_slot)
            self._clip_launch_button = button
            if (self._clip_launch_button != None):
                self._clip_launch_button.add_value_listener(self._fire_clip_slot)

    def _fire_clip_slot(self, value):
        self.song().view.highlighted_clip_slot.fire()
        
    def _set_clip_stop_button(self, button):
        if (button is not self._clip_stop_button):
            if (self._clip_stop_button != None):
                self._clip_stop_button.remove_value_listener(self._stop_clip_slot)
            self._clip_stop_button = button
            if (self._clip_stop_button != None):
                self._clip_stop_button.add_value_listener(self._stop_clip_slot)

    def _stop_clip_slot(self, value):
        self.song().view.highlighted_clip_slot.stop()
