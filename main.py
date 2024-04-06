import dearpygui.dearpygui as dpg
from PyP100 import PyL530
from colorsys import rgb_to_hsv
import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b'rtxo0hhTT', salt)
    return hashed_password.decode()


def save(sender,app_data): #Login data save
    ip = dpg.get_value("ip")
    email = dpg.get_value("email")
    password = dpg.get_value("password")
    h_pass = hash_password(password)
    with open('config.txt', 'w+') as c:
        if ip and email and password is not None:
            c.write(f'{ip} {email} {h_pass}')
            c.seek(0)
            data = c.read().split(' ')
            if bcrypt.checkpw(password, h_pass):
                password = dpg.get_value("password")
                print('HASHED REALLY')
            global l530
            l530 = PyL530.L530(str(data[0]), str(data[1]), str(data[2]))
        else:
            show_notification('Please fill all fields!')


def load(): #Login data load
    with open('config.txt','r') as c:
        data = c.read().split(' ')
        global l530
        l530 = PyL530.L530(str(data[0]), str(data[1]), str(data[2]))
        return connect()
        

def color_picker(sender, app_data): # Color picker?
    if connect() == True:
        color = dpg.get_value(sender)
        rgb = (color[0], color[1], color[2])
        hsv_color = list(rgb_to_hsv(*rgb))
        l530.setColor(round(hsv_color[0] * 360), round(hsv_color[1] * 100))
    else: 
        if load() == False: 
            show_notification('     Failed to Connect!\n Please check data, you \n provided')
#И сейчас всё тоже заебись


def brightness(sender, app_data): #Brightness slider
    l530.setBrightness(int(dpg.get_value(sender)))


def switch_power(sender, appdata): #On/Off bulb switch
    if dpg.get_value(sender) == True:
        l530.turnOn()
    else: 
        l530.turnOff()


def connect(): #Connection status indicator
    try:
        return l530.get_status()
    except: 
        return False


def show_notification(message): #Error notification
    with dpg.window(label="Notification", width=200, height=100, no_resize=True) as popup_id:
        dpg.add_text(message)
    dpg.configure_item(popup_id, show=True)
    dpg.set_item_pos(popup_id, (100, 100))


dpg.create_context()
dpg.create_viewport(title='Tapo Control panel', width=400, height=500)


with dpg.window(tag="Tapo Control Panel") as window:
    tapo_ip = dpg.add_input_text(label="IP", id='ip', hint="192.168.*.*", default_value='192.168.', width=200)
    tapo_email = dpg.add_input_text(label="Email", id='email', hint="Your email here:", width=200)
    tapo_pass = dpg.add_input_text(label="Tapo password", id='password', password=True, hint="Your Tapo Password here:", width=200)
    #Connect to the bulb 

    tapo_data_save = dpg.add_button(label="Save data", tag='save', callback=save)
    tapo_data_load = dpg.add_button(label="Load data", tag='load', callback=load)
    #Connect data Save/Load buttons

    color_picker = dpg.add_color_picker(default_value=(255, 0, 0), tag='ColorPicker', callback=color_picker)
    brightness = dpg.add_slider_double(label='Brightness' , min_value=1, default_value=100, width=200, format="%.0f", callback=brightness)
    switch = dpg.add_checkbox(label='Power', default_value=True , callback=switch_power)
    #Bulb settings change

    dpg.set_item_width(color_picker, 200)
    dpg.set_item_height(color_picker, 300)
    dpg.set_item_pos(tapo_data_load, [85, 77])
    #Item size and position settings

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_imgui_demo
dpg.set_primary_window("Tapo Control Panel", True)
dpg.start_dearpygui()
dpg.destroy_context()