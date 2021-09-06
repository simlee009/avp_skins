"""Edit skins in AvP (2010) save file"""
from tkinter import *
from tkinter import ttk
from os import path, listdir

XENO = 0x0A29
USMC = 0x0A2D
PRED = 0x0A25

RACES = {XENO: 'Alien', USMC: 'Marine', PRED: 'Predator'}
SKINS = {XENO: {b'\x00': 'Warrior',
                b'\x01': 'Warrior Dome',
                b'\x02': 'Number 6',
                b'\x03': 'Warrior Ridged',
                b'\x04': 'Praetorian',
                b'\x05': 'Nethead'},
         USMC: {b'\x00': 'Franco',
                b'\x01': 'Rookie',
                b'\x02': 'Van Zandt',
                b'\x03': 'Moss',
                b'\x04': 'Kaneko',
                b'\x05': 'Connor',
                b'\x06': 'Gibson',
                b'\x07': 'Johnson'},
         PRED: {b'\x00': 'Dark',
                b'\x01': 'Claw',
                b'\x02': 'Stalker',
                b'\x03': 'Hunter',
                b'\x04': 'Spartan',
                b'\x05': 'Wolf',
                b'\x06': 'Lord',
                b'\x07': 'Alien'}
         }


class AvPSkinSelect:

    def __init__(self, root):
        self.data = None
        self.create_ui(root)

    def create_ui(self, root):
        root.title('AvP Skin Select')

        frame = ttk.Frame(root, padding='5 5 5 5')
        frame.grid(column=0, row=0, sticky=(N, E, W, S))
        if path.exists('avp.ico'):
            root.iconbitmap('avp.ico')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.resizable(height=False, width=False)

        self.path = StringVar(value=AvPSkinSelect.get_save_dir())
        self.skin = {}
        row = 3
        for race in RACES:
            self.skin[race] = StringVar()
            AvPSkinSelect.create_combobox(
                frame, RACES[race], self.skin[race], SKINS[race], row)
            row += 1

        path_entry = ttk.Entry(frame, width=100, textvariable=self.path)
        path_entry.grid(column=2, row=1, sticky=(N, E, W))
        ttk.Label(frame, text='Save File').grid(column=1, row=1, sticky=(N, W))
        ttk.Button(frame, text='Load', command=self.load_data).grid(
            column=3, row=1, sticky=(N, E))
        ttk.Separator(frame, orient=HORIZONTAL).grid(
            column=1, row=2, columnspan=3, sticky=(N, E, W))
        ttk.Button(frame, text='Save', command=self.save_data).grid(
            column=3, row=6, sticky=(N, E))

        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def load_data(self):
        file_path = self.path.get()
        if path.exists(file_path):
            self.data = None
            with open(file_path, mode='rb') as save_file:
                self.data = bytearray(save_file.read())
            for race in RACES:
                self.skin[race].set(self.get_skin(race, SKINS[race]))

    def save_data(self):
        file_path = self.path.get()
        if path.exists(file_path) and self.data:
            for race in RACES:
                self.set_skin(race, SKINS[race], self.skin[race].get())
            with open(file_path, mode='wb') as save_file:
                save_file.write(self.data)

    def get_skin(self, race, skins):
        """Get the name of the race's selected skin from the saved game data."""
        skin_name = ''
        # The race is actually an offset.
        skin = bytes(self.data[race:race + 1])
        if skin in skins:
            skin_name = skins[skin]
        return skin_name

    def set_skin(self, offset, skins, skin_name):
        """Set the race's skin by name in the saved game data."""
        codes = list(skins.keys())
        names = list(skins.values())
        i = names.index(skin_name)
        value = codes[i]
        self.data[offset:offset + 1] = value

    @staticmethod
    def create_combobox(frame, label, textvar, skins, row):
        entry = ttk.Combobox(frame, textvariable=textvar)
        entry.grid(column=2, row=row, columnspan=2, sticky=(N, E, W))
        entry['values'] = list(skins.values())
        entry.state(['readonly'])
        ttk.Label(frame, text=label).grid(column=1, row=row, sticky=(N, W))
        return entry

    @staticmethod
    def get_save_dir():
        base_dir = path.expandvars(r'%LOCALAPPDATA%/AliensVsPredator')
        dir_list = listdir(base_dir)
        id = dir_list[0]
        file_path = path.join(base_dir, id, id + '.prf')
        return file_path


if __name__ == '__main__':
    root = Tk()
    AvPSkinSelect(root)
    root.mainloop()
