import dearpygui.dearpygui as dpg
import numpy as np


sp_width = 300          # Side panel width
w_width  = 1000         # Window width
w_height = 750          # Window height

n_scale = 1;
t_scale = 1;
speed = 1;

clr_funcs = {
    'Position': 1,
    'Age': 2,
    'Angle': 3,
}
clr_func = clr_funcs['Angle']

min_age = 1
max_age = 50

min_rgb = [91,109,255,255]
max_rgb = [154,0,190,255]
# COLOR CONFIG
bg_color = [1,5,58,255] # Background Color
d_alpha = 10            # Dimmer alpha
p_alpha = 50            # Particle alpha

def setup_biped_sim():

    # Callbacks
    def set_n_scale(sender, data):
        global n_scale
        n_scale = data

    def set_t_scale(sender, data):
        global t_scale
        t_scale = data

    def set_particle_speed(sender, data):
        global speed
        speed = data

    def set_color_function(sender, data):
        global clr_func
        clr_func = clr_funcs[data]

    def set_min_max_age(sender, data):
        global min_age, max_age
        if sender == 'min-age':
            min_age = data
        elif sender == 'max-age':
            max_age = data

    def set_min_max_rgb(sender, data):
        global min_rgb, max_rgb
        if sender == 'min_rgb':
            min_rgb = [int(c*255) for c in data]
        elif sender == 'max_rgb':
            max_rgb = [int(c*255) for c in data]

    def set_particle_opacity(sender, data):
        global p_alpha
        p_alpha = data
    
    def handle_dropdown(sender, data, group):
        if dpg.is_item_shown(group):
            dpg.configure_item(sender, direction=dpg.mvDir_Right)
            dpg.configure_item(group, show=False)
        else:
            dpg.configure_item(sender, direction=dpg.mvDir_Down)
            dpg.configure_item(group, show=True)

    with dpg.window(tag='biped', pos=(0,0)):
        # Theme setting
        dpg.set_primary_window('biped', True)
        with dpg.theme() as biped_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, bg_color, category=dpg.mvThemeCat_Core)
        dpg.bind_item_theme('biped', biped_theme)

        # Flux GUI
        with dpg.child_window(tag='parameters', pos=(w_width, 0), width=sp_width, height=-1):
            with dpg.theme() as side_panel_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8)
            dpg.bind_item_theme('parameters', side_panel_theme)
            
            # biped Settings
            dpg.add_spacer(height=3)
            with dpg.group(horizontal=True):
                dpg.add_button(tag='ff-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='biped-settings')
                dpg.add_text(default_value='Biped Properties')
            with dpg.group(tag='biped-settings'):
                dpg.add_slider_float(width=sp_width/2, label='noisescale', min_value=0.05, default_value=n_scale, max_value=3, callback=set_n_scale)
                dpg.add_slider_float(width=sp_width/2, label='timescale', min_value=0, default_value=t_scale, max_value=0.1, callback=set_t_scale)
            
            dpg.add_separator()
            
            # Particle Settings
            with dpg.group(horizontal=True):
                dpg.add_button(tag='pp-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='particle-settings')
                dpg.add_text(default_value='Particle Properties')
            with dpg.group(tag='particle-settings'):
                dpg.add_slider_float(width=sp_width/2, label='speed', min_value=0.5, default_value=speed, max_value=4, callback=set_particle_speed)
                dpg.add_slider_int(width=sp_width/2, label='min age', tag='min-age', min_value=min_age, default_value=min_age, max_value=100, callback=set_min_max_age)
                dpg.add_slider_int(width=sp_width/2, label='max age', tag='max-age', min_value=101, default_value=max_age, max_value=max_age, callback=set_min_max_age)
      
            dpg.add_separator()

            # Color Settings
            with dpg.group(horizontal=True):
                dpg.add_button(tag='cl-dropdown', arrow=True, direction=dpg.mvDir_Down, callback=handle_dropdown, user_data='color-settings')
                dpg.add_text(default_value='Color Settings')
            with dpg.group(tag='color-settings'):
                dpg.add_combo(width=sp_width/2, label='Color Function', tag='color-functions', items=list(clr_funcs.keys()), default_value='Age', callback=set_color_function)
                dpg.add_slider_int(width=sp_width/2, label='particle alpha', default_value=p_alpha, max_value=255, callback=set_particle_opacity)
                dpg.add_color_picker(width=sp_width/2, label='min_rgb', tag='min_rgb', default_value=min_rgb, no_tooltip=True, no_alpha=True, callback=set_min_max_rgb)
                dpg.add_color_picker(width=sp_width/2, label='max_rgb', tag='max_rgb', default_value=max_rgb, no_tooltip=True, no_alpha=True, callback=set_min_max_rgb)
            
            # Bottom Padding
            dpg.add_spacer(height=3)

    
    

def start_biped_sim():
    dpg.create_context()
    dpg.create_viewport(title='Biped', width=w_width+sp_width, height=w_height, resizable=False)
    dpg.setup_dearpygui()
    setup_biped_sim()
    dpg.show_viewport()
    # dpg.set_frame_callback(20, callback=lambda: dpg.output_frame_buffer(callback=init_frame_buffer))
    # dpg.set_viewport_vsync(False)
    # dpg.show_metrics()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    start_biped_sim()
