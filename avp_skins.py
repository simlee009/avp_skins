"""Edit skins in AvP (2010) save file"""
from tkinter import *
from tkinter import ttk
from os import path, listdir


class AvPSkinSelect:

    # Offsets inside the binary save file for each skin.
    xeno_offset = 0x0A29
    usmc_offset = 0x0A2D
    pred_offset = 0x0A25

    # Dictionaries of skin values in bytes.
    xeno_skins = {b'\x00': 'Warrior', b'\x01': 'Warrior Dome', b'\x02': 'Number 6',
                  b'\x03': 'Warrior Ridged', b'\x04': 'Praetorian',
                  b'\x05': 'Nethead'}
    usmc_skins = {b'\x00': 'Franco', b'\x01': 'Rookie', b'\x02': 'Van Zandt',
                  b'\x03': 'Moss', b'\x04': 'Kaneko',
                  b'\x05': 'Connor', b'\x06': 'Gibson', b'\x07': 'Johnson'}
    pred_skins = {b'\x00': 'Dark', b'\x01': 'Claw', b'\x02': 'Stalker',
                  b'\x03': 'Hunter', b'\x04': 'Spartan',
                  b'\x05': 'Wolf', b'\x06': 'Lord', b'\x07': 'Alien'}

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
        self.xeno_skin = StringVar()
        self.usmc_skin = StringVar()
        self.pred_skin = StringVar()

        path_entry = ttk.Entry(frame, width=100, textvariable=self.path)
        path_entry.grid(column=2, row=1, sticky=(N, E, W))
        ttk.Label(frame, text='Save File').grid(column=1, row=1, sticky=(N, W))
        ttk.Button(frame, text='Load', command=self.load_data).grid(
            column=3, row=1, sticky=(N, E))
        ttk.Separator(frame, orient=HORIZONTAL).grid(
            column=1, row=2, columnspan=3, sticky=(N, E, W))

        AvPSkinSelect.create_combobox(
            frame, 'Alien', self.xeno_skin, self.xeno_skins.values(), 3)
        AvPSkinSelect.create_combobox(
            frame, 'Marine', self.usmc_skin, self.usmc_skins.values(), 4)
        AvPSkinSelect.create_combobox(
            frame, 'Predator', self.pred_skin, self.pred_skins.values(), 5)

        ttk.Button(frame, text='Save', command=self.save_data).grid(
            column=3, row=6, sticky=(N, E))

        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def load_data(self):
        path = self.path.get()
        self.data = None
        with open(path, mode='rb') as save_file:
            self.data = bytearray(save_file.read())

        # Set the selected skins with the values from the save file.
        self.xeno_skin.set(self.get_skin(self.xeno_offset, self.xeno_skins))
        self.usmc_skin.set(self.get_skin(self.usmc_offset, self.usmc_skins))
        self.pred_skin.set(self.get_skin(self.pred_offset, self.pred_skins))

    def save_data(self):
        path = self.path.get()
        if path and self.data:
            # Set the skins to the selected values, and then save the file.
            self.set_skin(self.xeno_offset, self.xeno_skins,
                          self.xeno_skin.get())
            self.set_skin(self.usmc_offset, self.usmc_skins,
                          self.usmc_skin.get())
            self.set_skin(self.pred_offset, self.pred_skins,
                          self.pred_skin.get())
            with open(path, mode='wb') as save_file:
                save_file.write(self.data)

    def get_skin(self, offset, skins):
        skin_name = ''
        skin = bytes(self.data[offset:offset + 1])
        if skin in skins:
            skin_name = skins[skin]
        return skin_name

    def set_skin(self, offset, skins, skin_name):
        codes = list(skins.keys())
        names = list(skins.values())
        i = names.index(skin_name)
        value = codes[i]
        self.data[offset:offset + 1] = value

    @staticmethod
    def create_combobox(frame, label, textvar, values, row):
        entry = ttk.Combobox(frame, textvariable=textvar)
        entry.grid(column=2, row=row, columnspan=2, sticky=(N, E, W))
        entry['values'] = list(values)
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
