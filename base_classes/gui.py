import tkinter
from datetime import timedelta

import customtkinter
from geopy.distance import geodesic
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk

from KPIs.eurocontrol import Eurocontrol
from KPIs.gianzza import Gianazza
from KPIs.metron_aviation import Metron
from KPIs.nasa_additional import NasaAdditional
from KPIs.nasa_metric_one import NasaOne
from KPIs.nasa_metric_two import NasaTwo
from KPIs.wjthc import WJTHC
from KPIs.workload_one import WorkLoadOne
from KPIs.workloadtwo import WorkloadTwo
from base_classes.sector import Sector

customtkinter.set_default_color_theme("dark-blue")


# 48.324622, 11.723162
# 48.373255, 11.751073
# 48.381391, 11.851919
# 48.337307, 11.849061
class App(customtkinter.CTk):
    APP_NAME = "Air Traffic Control"
    WIDTH = 1500
    HEIGHT = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window8 = None
        self.list_path = []
        self.list_markers = []
        self.window7 = None
        self.poly_sector = None
        self.nasa_one = None
        self.nasa_additional = None
        self.gianzza = None
        self.nasa_two = None
        self.whjthc = None
        self.workload_one = None
        self.workload_two = None
        self.metron_avaiation = None
        self.eurocontrol = None
        self.sector = None
        self.window_second = None
        self.window_initial = None
        self.entry_ceiling = None
        self.entry_floor = None
        self.entry_name = None
        self.entry15 = None
        self.entry16 = None
        self.entry14 = None
        self.entry13 = None
        self.entry12 = None
        self.entry11 = None
        self.entry10 = None
        self.entry9 = None
        self.entry6 = None
        self.entry7 = None
        self.entry8 = None
        self.entry5 = None
        self.entry3 = None
        self.entry2 = None
        self.entry1 = None
        self.entry4 = None
        self.label2 = None
        self.label1 = None
        self.list_of_entries_with_values = []
        self.list_of_entries = []
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=400, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(15, weight=1)

        self.create_sector_button = customtkinter.CTkButton(master=self.frame_left,
                                                            text="Create Sector",
                                                            command=self.create_sector)
        self.create_sector_button.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.delete_sector_button = customtkinter.CTkButton(master=self.frame_left, text="Delete Sector",
                                                            command=self.delete_sector, state="disabled")
        self.delete_sector_button.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.ac_count_label = customtkinter.CTkLabel(self.frame_left, text="Aircraft Count:", anchor="w")
        self.ac_count_label.grid(row=2, column=0, padx=(20, 20), pady=(20, 0))
        self.slider_aircraft_count = customtkinter.CTkSlider(master=self.frame_left, from_=0, to=100,
                                                             orientation="horizontal", number_of_steps=100,
                                                             state="disabled", command=self.update_aircraft_count)
        self.slider_aircraft_count.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)

        self.variance_label = customtkinter.CTkLabel(self.frame_left, text="Variance of Aircraft:", anchor="w")
        self.variance_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))
        self.slider_variance = customtkinter.CTkSlider(master=self.frame_left, from_=0, to=100,
                                                       orientation="horizontal", number_of_steps=100,
                                                       state="disabled", command=self.update_variance)
        self.slider_variance.grid(pady=(20, 0), padx=(20, 20), row=5, column=0)

        self.time_label = customtkinter.CTkLabel(self.frame_left, text="Timespan", anchor="w")
        self.time_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
        self.slider_time = customtkinter.CTkSlider(master=self.frame_left, from_=0, to=120, orientation="horizontal",
                                                   state="disabled", command=self.update_time, number_of_steps=120)
        self.slider_time.grid(pady=(20, 0), padx=(20, 20), row=7, column=0)

        self.create_traffic_data_button = customtkinter.CTkButton(master=self.frame_left, text="Create Traffic Data",
                                                                  command=self.create_traffic_data, state="disabled")
        self.create_traffic_data_button.grid(pady=(20, 0), padx=(20, 20), row=8, column=0)

        self.pit_label = customtkinter.CTkLabel(self.frame_left, text="Point in Time", anchor="w")
        self.pit_label.grid(row=9, column=0, padx=(20, 20), pady=(20, 0))
        self.slider_point_in_time = customtkinter.CTkSlider(master=self.frame_left, from_=0, to=120,
                                                            orientation="horizontal",
                                                            state="disabled", number_of_steps=120,
                                                            command=self.adjust_point_in_time)
        self.slider_point_in_time.grid(pady=(20, 0), padx=(20, 20), row=10, column=0)

        self.KPI_button = customtkinter.CTkButton(master=self.frame_left, text="Show KPIs",
                                                  command=self.kpi_button)  # , state="disabled")
        self.KPI_button.grid(pady=(20, 0), padx=(20, 20), row=11, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=12, column=0, padx=(20, 20), pady=(300, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal",
                                                                                    "Google satellite",
                                                                                    "Black / White"],
                                                           command=self.change_map)
        self.map_option_menu.grid(row=13, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=14, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=15, column=0, padx=(20, 20), pady=(10, 0))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        # Set default values
        self.map_widget.set_address("Munich")
        self.map_widget.set_zoom(10)
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")

    def create_sector(self):
        self.window_initial = customtkinter.CTkToplevel(self)
        self.window_initial.geometry("400x600")
        self.window_initial.title(
            "Create Sector, enter the corner coordinates for the sector, leave unused fields empty")
        self.window_initial.grid_rowconfigure(9, weight=1)
        self.window_initial.grid_columnconfigure(2, weight=1)

        self.label1 = customtkinter.CTkLabel(self.window_initial, text="Latitude Coordinate")
        self.label1.grid(row=0, column=0, padx=20, pady=10)
        self.label2 = customtkinter.CTkLabel(self.window_initial, text="Longitude Coordinate")
        self.label2.grid(row=0, column=1, padx=20, pady=10)

        self.entry1 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry1.grid(row=1, column=0, padx=20, pady=10)
        self.entry2 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry2.grid(row=1, column=1, padx=20, pady=10)

        self.entry3 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry3.grid(row=2, column=0, padx=20, pady=10)
        self.entry4 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry4.grid(row=2, column=1, padx=20, pady=10)

        self.entry5 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry5.grid(row=3, column=0, padx=20, pady=10)
        self.entry6 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry6.grid(row=3, column=1, padx=20, pady=10)

        self.entry7 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry7.grid(row=4, column=0, padx=20, pady=10)
        self.entry8 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry8.grid(row=4, column=1, padx=20, pady=10)

        self.entry9 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry9.grid(row=5, column=0, padx=20, pady=10)
        self.entry10 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry10.grid(row=5, column=1, padx=20, pady=10)

        self.entry11 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry11.grid(row=6, column=0, padx=20, pady=10)
        self.entry12 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry12.grid(row=6, column=1, padx=20, pady=10)

        self.entry13 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry13.grid(row=7, column=0, padx=20, pady=10)
        self.entry14 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry14.grid(row=7, column=1, padx=20, pady=10)

        self.entry15 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Latitude")
        self.entry15.grid(row=8, column=0, padx=20, pady=10)
        self.entry16 = customtkinter.CTkEntry(self.window_initial, placeholder_text="Longitude")
        self.entry16.grid(row=8, column=1, padx=20, pady=10)

        self.list_of_entries = [(self.entry1, self.entry2), (self.entry3, self.entry4), (self.entry5, self.entry6),
                                (self.entry7,
                                 self.entry8), (self.entry9, self.entry10), (self.entry11, self.entry12), (self.entry13,
                                                                                                           self.entry14),
                                (self.entry15, self.entry16)]

        button = customtkinter.CTkButton(self.window_initial, text="Create Sector", command=self.button_confirm)
        button.grid(row=9, column=1, padx=20, pady=10, sticky="SE")

    def button_confirm(self):
        self.list_of_entries_with_values = []

        for entry, entry2 in self.list_of_entries:
            if entry.get() == "" or entry2.get() == "":
                pass
            else:
                try:
                    entry = float(entry.get())
                    entry2 = float(entry2.get())
                except ValueError:
                    print("Error", "Latitude and Longitude must be floats")
                    return
                self.list_of_entries_with_values.append((entry, entry2))

        self.window_initial.destroy()

        self.window_second = customtkinter.CTkToplevel(self)
        self.window_second.geometry("400x400")
        self.window_second.title("Enter additional infos for sector")
        self.window_second.grid_rowconfigure(4, weight=1)
        self.window_second.grid_columnconfigure(2, weight=1)

        label_name = customtkinter.CTkLabel(self.window_second, text="Enter the Sector Name")
        label_name.grid(row=0, column=0, padx=20, pady=10)
        self.entry_name = customtkinter.CTkEntry(self.window_second, placeholder_text="Name")
        self.entry_name.grid(row=0, column=1, padx=20, pady=10)

        label_floor = customtkinter.CTkLabel(self.window_second, text="Enter the Sector Floor in ft")
        label_floor.grid(row=1, column=0, padx=20, pady=10)
        self.entry_floor = customtkinter.CTkEntry(self.window_second, placeholder_text="Floor")
        self.entry_floor.grid(row=1, column=1, padx=20, pady=10)

        label_ceiling = customtkinter.CTkLabel(self.window_second, text="Enter the Sector Ceiling in ft")
        label_ceiling.grid(row=2, column=0, padx=20, pady=10)
        self.entry_ceiling = customtkinter.CTkEntry(self.window_second, placeholder_text="Ceiling")
        self.entry_ceiling.grid(row=2, column=1, padx=20, pady=10)

        button = customtkinter.CTkButton(self.window_second, text="Create Sector", command=self.button_confirm2)
        button.grid(row=3, column=1, padx=20, pady=10, sticky="SE")

    def button_confirm2(self):
        sector_name = self.entry_name.get()

        try:
            sector_floor = int(self.entry_floor.get())
            sector_ceiling = int(self.entry_ceiling.get())
        except ValueError:
            print("Error", "Floor and Ceiling must be integers")
            return

        self.window_second.destroy()

        if len(self.list_of_entries_with_values) < 4:
            print("Error", "You must enter at least 4 coordinates")
            return
        self.sector = Sector(sector_name, sector_floor, sector_ceiling, self.list_of_entries_with_values)
        print(self.sector.__str__() + " created")
        # self.eurocontrol = Eurocontrol(self.sector)
        self.gianzza = Gianazza(self.sector)
        self.metron_avaiation = Metron(self.sector)
        self.nasa_additional = NasaAdditional(self.sector)
        self.nasa_one = NasaOne(self.sector)
        self.nasa_two = NasaTwo(self.sector)
        self.whjthc = WJTHC(self.sector)
        self.workload_one = WorkLoadOne(self.sector)
        self.workload_two = WorkloadTwo(self.sector)

        self.poly_sector = self.map_widget.set_polygon(self.sector.get_corner_points(), fill_color=None,
                                                       outline_color="green",
                                                       border_width=4, name=self.sector.get_name())
        self.poly_sector.add_position(self.sector.get_corner_points()[0][0], self.sector.get_corner_points()[0][1])

        self.create_sector_button.configure(state="disabled")
        self.slider_aircraft_count.configure(state="normal")
        self.slider_variance.configure(state="normal")
        self.slider_time.configure(state="normal")
        self.create_traffic_data_button.configure(state="normal")
        self.delete_sector_button.configure(state="normal")
        self.KPI_button.configure(state="normal")

    def delete_sector(self):
        """
        def yes():
            self.poly_sector.delete()
            self.create_sector_button.configure(state="normal")
            dialog.destroy()

        def no():
            dialog.destroy()

        dialog = customtkinter.CTkInputDialog(title="Delete Sector", text="Are you sure you want to delete the sector?")
        button = customtkinter.CTkButton(dialog, text="Yes", command=yes())
        button.place(relx=0.5, rely=0.5, anchor="center")
        button2 = customtkinter.CTkButton(dialog, text="No", command=no())
        button2.place(relx=0.5, rely=0.5, anchor="center")
        """
        self.poly_sector.delete()
        for marker in self.list_markers:
            marker.delete()
        self.list_markers.clear()
        for path in self.list_path:
            path.delete()
        self.list_path.clear()
        self.create_sector_button.configure(state="normal")
        self.slider_aircraft_count.configure(state="disabled")
        self.slider_variance.configure(state="disabled")
        self.slider_time.configure(state="disabled")
        self.create_traffic_data_button.configure(state="disabled")
        self.delete_sector_button.configure(state="disabled")
        # self.KPI_button.configure(state="disabled")

    def create_traffic_data(self):
        self.slider_time.configure(state="disabled")
        self.slider_variance.configure(state="disabled")
        self.slider_aircraft_count.configure(state="disabled")
        self.create_traffic_data_button.configure(state="disabled")

        time = int(self.slider_time.get())
        print("Time: " + str(time))
        print(self.slider_time.get())
        time = time * 6  # time is given in minutes, every ten seconds a new data entry is created, 6 entries per minute

        for i in range(time):
            self.sector.create_traffic_loop(self.slider_aircraft_count.get(), self.slider_variance.get())

        self.window7 = customtkinter.CTkToplevel(self)
        self.window7.geometry("200x200")
        self.window7.grid_rowconfigure(2, weight=1)
        self.window7.grid_columnconfigure(1, weight=1)
        label7 = customtkinter.CTkLabel(self.window7, text="Traffic Data created")
        label7.grid(row=0, column=0, padx=20, pady=10)
        button = customtkinter.CTkButton(master=self.window7, text="Continue", command=self.button_event_7)
        button.grid(row=1, column=0, padx=20, pady=10, sticky="SE")

        time2 = int(time / 10)
        self.slider_point_in_time.configure(state="normal", to=time, number_of_steps=time2)

        planes_to_draw = self.sector.current_planes

        def get_distance(speed_knts):
            speed_in_ms = speed_knts * 0.514444  # converts speed from knots to m/s
            distance = speed_in_ms * 10  # 10 seconds
            return distance / 500  # no longer accurate but better visualization

        plane_image = ImageTk.PhotoImage(
            Image.open("C:/Users/Kilian/PycharmProjects/pythonProject2/images/small_red_icon.png").resize((10, 10)))
        for plane in planes_to_draw:
            plane_info = plane.get_callsign() + "\n" + str(plane.get_altitude()) + "\n" + str(
                plane.get_speed()) + "\n" + str(plane.get_heading())
            marker = self.map_widget.set_marker(plane.get_position_x(), plane.get_position_y(), text=plane_info,
                                                icon=plane_image)
            current_pos = (plane.get_position_x(), plane.get_position_y())
            heading = plane.get_heading()
            speed = plane.get_speed()
            new_pos = geodesic(kilometers=get_distance(speed)).destination(current_pos, heading)
            path = self.map_widget.set_path(
                [(plane.get_position_x(), plane.get_position_y()), (new_pos[0], new_pos[1])],
                color="red", width=3)

            self.list_markers.append(marker)
            self.list_path.append(path)

    def button_event_7(self):
        self.window7.destroy()

    def adjust_point_in_time(self, value):
        pit = "Point in Time: " + str(value)
        self.pit_label.configure(text=pit)
        planes_to_draw = []

        for marker in self.list_markers:
            marker.delete()
        self.list_markers.clear()
        for path in self.list_path:
            path.delete()
        self.list_path.clear()

        # find the correct point in time in the traffic data
        for time, planes in self.sector.get_history_planes():
            if time == timedelta(seconds=value):
                planes_to_draw = planes
                break

        def get_distance(speed_knts):
            speed_in_ms = speed_knts * 0.514444  # converts speed from knots to m/s
            distance = speed_in_ms * 10  # 10 seconds
            return distance / 500  # no longer accurate but better visualization

        plane_image = ImageTk.PhotoImage(
            Image.open("C:/Users/Kilian/PycharmProjects/pythonProject2/images/small_red_icon.png").resize((10, 10)))
        for plane in planes_to_draw:
            plane_info = plane.get_callsign() + "\n" + str(plane.get_altitude()) + "\n" + str(
                plane.get_speed()) + "\n" + str(plane.get_heading())
            marker = self.map_widget.set_marker(plane.get_position_x(), plane.get_position_y(), text=plane_info,
                                                icon=plane_image)
            current_pos = (plane.get_position_x(), plane.get_position_y())
            heading = plane.get_heading()
            speed = plane.get_speed()
            new_pos = geodesic(kilometers=get_distance(speed)).destination(current_pos, heading)
            path = self.map_widget.set_path(
                [(plane.get_position_x(), plane.get_position_y()), (new_pos[0], new_pos[1])],
                color="red", width=3)

            self.list_markers.append(marker)
            self.list_path.append(path)

        planes_to_draw.clear()

    def update_variance(self, value):
        variance = "Variance: " + str(value)
        self.variance_label.configure(text=variance)

    def update_time(self, value):
        time = "Time: " + str(value)
        self.time_label.configure(text=time)

    def update_aircraft_count(self, value):
        ac_count = "Aircraft Count: " + str(value)
        self.ac_count_label.configure(text=ac_count)

    def kpi_button(self):
        self.window8 = customtkinter.CTkToplevel(self)
        self.window8.geometry("1000x1000")
        tabview = customtkinter.CTkTabview(self.window8, width=1000, height=1000)
        tabview.pack(padx=20, pady=20)
        metron = tabview.add("Metron Aviation")
        gianazza = tabview.add("Gianazza")
        nasa_one = tabview.add("Nasa One")
        nasa_two = tabview.add("Nasa Two")
        wjthc = tabview.add("WJTHC")
        additional = tabview.add("Nasa Additional")
        wl_1 = tabview.add("Workload 1")
        wl_2 = tabview.add("Workload 2")

        # Metron Aviation
        metron.grid_rowconfigure(9, weight=1)
        metron.grid_columnconfigure(2, weight=1)

        label_wact = customtkinter.CTkLabel(metron, text="WACT")
        label_wact.grid(row=0, column=0, padx=20, pady=10)
        label_wact_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wact()))
        label_wact_value.grid(row=0, column=1, padx=20, pady=10)

        label_wden = customtkinter.CTkLabel(metron, text="WDEN")
        label_wden.grid(row=1, column=0, padx=20, pady=10)
        label_wden_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wden()))
        label_wden_value.grid(row=1, column=1, padx=20, pady=10)

        label_wclap = customtkinter.CTkLabel(metron, text="WCLAP")
        label_wclap.grid(row=2, column=0, padx=20, pady=10)
        label_wclap_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wclap()))
        label_wclap_value.grid(row=2, column=1, padx=20, pady=10)

        label_wconvang = customtkinter.CTkLabel(metron, text="WCONVANG")
        label_wconvang.grid(row=3, column=0, padx=20, pady=10)
        label_wconvang_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wconvang()))
        label_wconvang_value.grid(row=3, column=1, padx=20, pady=10)

        label_wconflict_nbrs = customtkinter.CTkLabel(metron, text="WCONFLICT_NBRs")
        label_wconflict_nbrs.grid(row=4, column=0, padx=20, pady=10)
        label_wconflict_nbrs_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wconflict_nbrs()))
        label_wconflict_nbrs_value.grid(row=4, column=1, padx=20, pady=10)

        label_wconf_bound = customtkinter.CTkLabel(metron, text="WCONFLICT_BOUND")
        label_wconf_bound.grid(row=5, column=0, padx=20, pady=10)
        label_wconf_bound_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wconf_bound()))
        label_wconf_bound_value.grid(row=5, column=1, padx=20, pady=10)

        label_walc = customtkinter.CTkLabel(metron, text="WALC")
        label_walc.grid(row=6, column=0, padx=20, pady=10)
        label_walc_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.walc()))
        label_walc_value.grid(row=6, column=1, padx=20, pady=10)

        label_wheadvar = customtkinter.CTkLabel(metron, text="WHEADVAR")
        label_wheadvar.grid(row=7, column=0, padx=20, pady=10)
        label_wheadvar_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wheadvar()))
        label_wheadvar_value.grid(row=7, column=1, padx=20, pady=10)

        label_wbprox = customtkinter.CTkLabel(metron, text="WBPROX")
        label_wbprox.grid(row=8, column=0, padx=20, pady=10)
        label_wbprox_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wbprox()))
        label_wbprox_value.grid(row=8, column=1, padx=20, pady=10)

        label_wasp = customtkinter.CTkLabel(metron, text="WASP")
        label_wasp.grid(row=9, column=0, padx=20, pady=10)
        label_wasp_value = customtkinter.CTkLabel(metron, text=str(self.metron_avaiation.wasp()))
        label_wasp_value.grid(row=9, column=1, padx=20, pady=10)

        # Gianazza
        gianazza.grid_rowconfigure(5, weight=1)
        gianazza.grid_columnconfigure(2, weight=1)

        label_v = customtkinter.CTkLabel(gianazza, text="V")
        label_v.grid(row=0, column=0, padx=20, pady=10)
        label_v_value = customtkinter.CTkLabel(gianazza, text=str(self.gianzza.v()))
        label_v_value.grid(row=0, column=1, padx=20, pady=10)

        label_nb = customtkinter.CTkLabel(gianazza, text="NB")
        label_nb.grid(row=1, column=0, padx=20, pady=10)
        label_nb_value = customtkinter.CTkLabel(gianazza, text=str(self.gianzza.nb()))
        label_nb_value.grid(row=1, column=1, padx=20, pady=10)

        label_avg_vs = customtkinter.CTkLabel(gianazza, text="AVG_VS")
        label_avg_vs.grid(row=2, column=0, padx=20, pady=10)
        label_avg_vs_value = customtkinter.CTkLabel(gianazza, text=str(self.gianzza.avg_vs()))
        label_avg_vs_value.grid(row=2, column=1, padx=20, pady=10)

        label_f15 = customtkinter.CTkLabel(gianazza, text="F15")
        label_f15.grid(row=3, column=0, padx=20, pady=10)
        label_f15_value = customtkinter.CTkLabel(gianazza, text=str(self.gianzza.f15(10)))
        label_f15_value.grid(row=3, column=1, padx=20, pady=10)

        label_f60 = customtkinter.CTkLabel(gianazza, text="F60")
        label_f60.grid(row=4, column=0, padx=20, pady=10)
        label_f60_value = customtkinter.CTkLabel(gianazza, text=str(self.gianzza.f60(10)))
        label_f60_value.grid(row=4, column=1, padx=20, pady=10)

        label_inter_hori = customtkinter.CTkLabel(gianazza, text="INTER_HORI")
        label_inter_hori.grid(row=5, column=0, padx=20, pady=10)
        label_inter_hori_value = customtkinter.CTkLabel(gianazza, text=str(self.gianzza.inter_hori()))
        label_inter_hori_value.grid(row=5, column=1, padx=20, pady=10)

        # Nasa One
        nasa_one.grid_rowconfigure(15, weight=1)
        nasa_one.grid_columnconfigure(2, weight=1)

        label_c1 = customtkinter.CTkLabel(nasa_one, text="C1")
        label_c1.grid(row=0, column=0, padx=20, pady=10)
        label_c1_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_1()))
        label_c1_value.grid(row=0, column=1, padx=20, pady=10)

        label_c2 = customtkinter.CTkLabel(nasa_one, text="C2")
        label_c2.grid(row=1, column=0, padx=20, pady=10)
        label_c2_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_2()))
        label_c2_value.grid(row=1, column=1, padx=20, pady=10)

        label_c3 = customtkinter.CTkLabel(nasa_one, text="C3")
        label_c3.grid(row=2, column=0, padx=20, pady=10)
        label_c3_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_3()))
        label_c3_value.grid(row=2, column=1, padx=20, pady=10)

        label_c4 = customtkinter.CTkLabel(nasa_one, text="C4")
        label_c4.grid(row=3, column=0, padx=20, pady=10)
        label_c4_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_4()))
        label_c4_value.grid(row=3, column=1, padx=20, pady=10)

        label_c5 = customtkinter.CTkLabel(nasa_one, text="C5")
        label_c5.grid(row=4, column=0, padx=20, pady=10)
        label_c5_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_5()))
        label_c5_value.grid(row=4, column=1, padx=20, pady=10)

        label_c6 = customtkinter.CTkLabel(nasa_one, text="C6")
        label_c6.grid(row=5, column=0, padx=20, pady=10)
        label_c6_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_6()))
        label_c6_value.grid(row=5, column=1, padx=20, pady=10)

        label_c7 = customtkinter.CTkLabel(nasa_one, text="C7")
        label_c7.grid(row=6, column=0, padx=20, pady=10)
        label_c7_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_7()))
        label_c7_value.grid(row=6, column=1, padx=20, pady=10)

        label_c8 = customtkinter.CTkLabel(nasa_one, text="C8")
        label_c8.grid(row=7, column=0, padx=20, pady=10)
        label_c8_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_8()))
        label_c8_value.grid(row=7, column=1, padx=20, pady=10)

        label_c9 = customtkinter.CTkLabel(nasa_one, text="C9")
        label_c9.grid(row=8, column=0, padx=20, pady=10)
        label_c9_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_9()))
        label_c9_value.grid(row=8, column=1, padx=20, pady=10)

        label_c10 = customtkinter.CTkLabel(nasa_one, text="C10")
        label_c10.grid(row=9, column=0, padx=20, pady=10)
        label_c10_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_10()))
        label_c10_value.grid(row=9, column=1, padx=20, pady=10)

        label_c11 = customtkinter.CTkLabel(nasa_one, text="C11")
        label_c11.grid(row=10, column=0, padx=20, pady=10)
        label_c11_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_11()))
        label_c11_value.grid(row=10, column=1, padx=20, pady=10)

        label_c12 = customtkinter.CTkLabel(nasa_one, text="C12")
        label_c12.grid(row=11, column=0, padx=20, pady=10)
        label_c12_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_12()))
        label_c12_value.grid(row=11, column=1, padx=20, pady=10)

        label_c13 = customtkinter.CTkLabel(nasa_one, text="C13")
        label_c13.grid(row=12, column=0, padx=20, pady=10)
        label_c13_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_13()))
        label_c13_value.grid(row=12, column=1, padx=20, pady=10)

        label_c14 = customtkinter.CTkLabel(nasa_one, text="C14")
        label_c14.grid(row=13, column=0, padx=20, pady=10)
        label_c14_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_14()))
        label_c14_value.grid(row=13, column=1, padx=20, pady=10)

        label_c15 = customtkinter.CTkLabel(nasa_one, text="C15")
        label_c15.grid(row=14, column=0, padx=20, pady=10)
        label_c15_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_15()))
        label_c15_value.grid(row=14, column=1, padx=20, pady=10)

        label_c16 = customtkinter.CTkLabel(nasa_one, text="C16")
        label_c16.grid(row=15, column=0, padx=20, pady=10)
        label_c16_value = customtkinter.CTkLabel(nasa_one, text=str(self.nasa_one.c_16()))
        label_c16_value.grid(row=15, column=1, padx=20, pady=10)

        # Nasa Two
        nasa_two.grid_rowconfigure(8, weight=1)
        nasa_two.grid_columnconfigure(2, weight=1)

        label_traffic_density_n = customtkinter.CTkLabel(nasa_two, text="Traffic Density")
        label_traffic_density_n.grid(row=0, column=0, padx=20, pady=10)
        label_traffic_density_n_value = customtkinter.CTkLabel(nasa_two, text=str(self.nasa_two.traffic_density_n()))
        label_traffic_density_n_value.grid(row=0, column=1, padx=20, pady=10)

        label_heading_change_nh = customtkinter.CTkLabel(nasa_two, text="Heading Change")
        label_heading_change_nh.grid(row=1, column=0, padx=20, pady=10)
        label_heading_change_nh_value = customtkinter.CTkLabel(nasa_two, text=str(self.nasa_two.heading_change_nh()))
        label_heading_change_nh_value.grid(row=1, column=1, padx=20, pady=10)

        label_speed_change_ns = customtkinter.CTkLabel(nasa_two, text="Speed Change")
        label_speed_change_ns.grid(row=2, column=0, padx=20, pady=10)
        label_speed_change_ns_value = customtkinter.CTkLabel(nasa_two, text=str(self.nasa_two.speed_change_ns()))
        label_speed_change_ns_value.grid(row=2, column=1, padx=20, pady=10)

        label_altitude_change_na = customtkinter.CTkLabel(nasa_two, text="Altitude Change")
        label_altitude_change_na.grid(row=3, column=0, padx=20, pady=10)
        label_altitude_change_na_value = customtkinter.CTkLabel(nasa_two, text=str(self.nasa_two.altitude_change_na()))
        label_altitude_change_na_value.grid(row=3, column=1, padx=20, pady=10)

        label_distance_between_0_and_5_s5 = customtkinter.CTkLabel(nasa_two, text="Distance Between 0 and 5")
        label_distance_between_0_and_5_s5.grid(row=4, column=0, padx=20, pady=10)
        label_distance_between_0_and_5_s5_value = customtkinter.CTkLabel(nasa_two, text=str(
            self.nasa_two.distance_between_0_and_5_s5()))
        label_distance_between_0_and_5_s5_value.grid(row=4, column=1, padx=20, pady=10)

        label_distance_between_5_and_10_s10 = customtkinter.CTkLabel(nasa_two, text="Distance Between 5 and 10")
        label_distance_between_5_and_10_s10.grid(row=5, column=0, padx=20, pady=10)
        label_distance_between_5_and_10_s10_value = customtkinter.CTkLabel(nasa_two, text=str(
            self.nasa_two.distance_between_5_and_10_s10()))
        label_distance_between_5_and_10_s10_value.grid(row=5, column=1, padx=20, pady=10)

        label_distance_between_10_and_25_s25 = customtkinter.CTkLabel(nasa_two, text="Distance Between 10 and 25")
        label_distance_between_10_and_25_s25.grid(row=6, column=0, padx=20, pady=10)
        label_distance_between_10_and_25_s25_value = customtkinter.CTkLabel(nasa_two, text=str(
            self.nasa_two.distance_between_0_and_25_s25()))
        label_distance_between_10_and_25_s25_value.grid(row=6, column=1, padx=20, pady=10)

        label_distance_between_25_and_40_s40 = customtkinter.CTkLabel(nasa_two, text="Distance Between 25 and 40")
        label_distance_between_25_and_40_s40.grid(row=7, column=0, padx=20, pady=10)
        label_distance_between_25_and_40_s40_value = customtkinter.CTkLabel(nasa_two, text=str(
            self.nasa_two.distance_between_25_and_40_s40()))
        label_distance_between_25_and_40_s40_value.grid(row=7, column=1, padx=20, pady=10)

        label_distance_between_40_and_70_s70 = customtkinter.CTkLabel(nasa_two, text="Distance Between 40 and 70")
        label_distance_between_40_and_70_s70.grid(row=8, column=0, padx=20, pady=10)
        label_distance_between_40_and_70_s70_value = customtkinter.CTkLabel(nasa_two, text=str(
            self.nasa_two.distance_between_40_and_70_s70()))
        label_distance_between_40_and_70_s70_value.grid(row=8, column=1, padx=20, pady=10)

        # WJTHC
        wjthc.grid_rowconfigure(8, weight=1)
        wjthc.grid_columnconfigure(2, weight=1)

        label_sector_volume = customtkinter.CTkLabel(wjthc, text="Sector Volume")
        label_sector_volume.grid(row=0, column=0, padx=20, pady=10)
        label_sector_volume_value = customtkinter.CTkLabel(wjthc, text=str(self.whjthc.sector_volume()))
        label_sector_volume_value.grid(row=0, column=1, padx=20, pady=10)

        label_aircraft_count = customtkinter.CTkLabel(wjthc, text="Aircraft Count")
        label_aircraft_count.grid(row=1, column=0, padx=20, pady=10)
        label_aircraft_count_value = customtkinter.CTkLabel(wjthc, text=str(self.whjthc.aircraft_count()))
        label_aircraft_count_value.grid(row=1, column=1, padx=20, pady=10)

        label_aircraft_density_one = customtkinter.CTkLabel(wjthc, text="Aircraft Density One")
        label_aircraft_density_one.grid(row=2, column=0, padx=20, pady=10)
        label_aircraft_density_one_value = customtkinter.CTkLabel(wjthc, text=str(self.whjthc.aircraft_density_one()))
        label_aircraft_density_one_value.grid(row=2, column=1, padx=20, pady=10)

        label_aircraft_density_two = customtkinter.CTkLabel(wjthc, text="Aircraft Density Two")
        label_aircraft_density_two.grid(row=3, column=0, padx=20, pady=10)
        label_aircraft_density_two_value = customtkinter.CTkLabel(wjthc, text=str(self.whjthc.aircraft_density_two()))
        label_aircraft_density_two_value.grid(row=3, column=1, padx=20, pady=10)

        label_convergence_recognition_index = customtkinter.CTkLabel(wjthc, text="Convergence Recognition Index")
        label_convergence_recognition_index.grid(row=4, column=0, padx=20, pady=10)
        label_convergence_recognition_index_value = customtkinter.CTkLabel(wjthc, text=str(
            self.whjthc.convergence_recognition_index()))
        label_convergence_recognition_index_value.grid(row=4, column=1, padx=20, pady=10)

        label_separation_criticality_index = customtkinter.CTkLabel(wjthc, text="Separation Criticality Index")
        label_separation_criticality_index.grid(row=5, column=0, padx=20, pady=10)
        label_separation_criticality_index_value = customtkinter.CTkLabel(wjthc, text=str(
            self.whjthc.separation_criticality_index()))
        label_separation_criticality_index_value.grid(row=5, column=1, padx=20, pady=10)

        label_degrees_of_freedom_index = customtkinter.CTkLabel(wjthc, text="Degrees of Freedom Index")
        label_degrees_of_freedom_index.grid(row=6, column=0, padx=20, pady=10)
        label_degrees_of_freedom_index_value = customtkinter.CTkLabel(wjthc,
                                                                      text=str(self.whjthc.degrees_of_freedom_index()))
        label_degrees_of_freedom_index_value.grid(row=6, column=1, padx=20, pady=10)

        label_coordination_taskload_index = customtkinter.CTkLabel(wjthc, text="Coordination Taskload Index")
        label_coordination_taskload_index.grid(row=7, column=0, padx=20, pady=10)
        label_coordination_taskload_index_value = customtkinter.CTkLabel(wjthc, text=str(
            self.whjthc.coordination_taskload_index()))
        label_coordination_taskload_index_value.grid(row=7, column=1, padx=20, pady=10)

        # NASA additional
        additional.grid_rowconfigure(8, weight=1)
        additional.grid_columnconfigure(2, weight=1)

        label_numhorizon = customtkinter.CTkLabel(additional, text="Number of Horizon")
        label_numhorizon.grid(row=0, column=0, padx=20, pady=10)
        label_numhorizon_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.numhorizon()))
        label_numhorizon_value.grid(row=0, column=1, padx=20, pady=10)

        label_hdgvari = customtkinter.CTkLabel(additional, text="Heading Variation")
        label_hdgvari.grid(row=1, column=0, padx=20, pady=10)
        label_hdgvari_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.hdgvari()))
        label_hdgvari_value.grid(row=1, column=1, padx=20, pady=10)

        label_axishdg = customtkinter.CTkLabel(additional, text="Axis Heading")
        label_axishdg.grid(row=2, column=0, padx=20, pady=10)
        label_axishdg_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.axishdg()))
        label_axishdg_value.grid(row=2, column=1, padx=20, pady=10)

        label_convconf = customtkinter.CTkLabel(additional, text="ConvConf")
        label_convconf.grid(row=3, column=0, padx=20, pady=10)
        label_convconf_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.convconf()))
        label_convconf_value.grid(row=3, column=1, padx=20, pady=10)

        label_proxcount = customtkinter.CTkLabel(additional, text="ProxCount")
        label_proxcount.grid(row=4, column=0, padx=20, pady=10)
        label_proxcount_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.proxcount()))
        label_proxcount_value.grid(row=4, column=1, padx=20, pady=10)

        label_confcount = customtkinter.CTkLabel(additional, text="ConfCount")
        label_confcount.grid(row=5, column=0, padx=20, pady=10)
        label_confcount_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.confcount()))
        label_confcount_value.grid(row=5, column=1, padx=20, pady=10)

        label_altvari = customtkinter.CTkLabel(additional, text="Altitude Variation")
        label_altvari.grid(row=6, column=0, padx=20, pady=10)
        label_altvari_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.altvari()))
        label_altvari_value.grid(row=6, column=1, padx=20, pady=10)

        label_numbndy = customtkinter.CTkLabel(additional, text="Number of Boundary")
        label_numbndy.grid(row=7, column=0, padx=20, pady=10)
        label_numbndy_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.numbndy()))
        label_numbndy_value.grid(row=7, column=1, padx=20, pady=10)

        label_aspect = customtkinter.CTkLabel(additional, text="Aspect")
        label_aspect.grid(row=8, column=0, padx=20, pady=10)
        label_aspect_value = customtkinter.CTkLabel(additional, text=str(self.nasa_additional.aspect()))
        label_aspect_value.grid(row=8, column=1, padx=20, pady=10)

        # Workload One
        wl_1.grid_rowconfigure(2, weight=1)
        wl_1.grid_columnconfigure(2, weight=1)

        label_workload_one = customtkinter.CTkLabel(wl_1, text="Workload One")
        label_workload_one.grid(row=0, column=0, padx=20, pady=10)
        label_workload_one_value = customtkinter.CTkLabel(wl_1, text=str(self.workload_one.compute_workload()))
        label_workload_one_value.grid(row=0, column=1, padx=20, pady=10)

        label_workload_percentage = customtkinter.CTkLabel(wl_1, text="Workload Percentage")
        label_workload_percentage.grid(row=1, column=0, padx=20, pady=10)
        label_workload_percentage_value = customtkinter.CTkLabel(wl_1, text=str(
            self.workload_one.compute_workload_percentage()))
        label_workload_percentage_value.grid(row=1, column=1, padx=20, pady=10)

        # Workload Two
        wl_2.grid_rowconfigure(5, weight=1)
        wl_2.grid_columnconfigure(2, weight=1)

        label_wl_monitoring = customtkinter.CTkLabel(wl_2, text="Monitoring")
        label_wl_monitoring.grid(row=0, column=0, padx=20, pady=10)
        label_wl_monitoring_value = customtkinter.CTkLabel(wl_2, text=str(self.workload_two.wl_mon()))
        label_wl_monitoring_value.grid(row=0, column=1, padx=20, pady=10)

        label_wl_conflict = customtkinter.CTkLabel(wl_2, text="Conflict")
        label_wl_conflict.grid(row=1, column=0, padx=20, pady=10)
        label_wl_conflict_value = customtkinter.CTkLabel(wl_2, text=str(self.workload_two.wl_cdr()))
        label_wl_conflict_value.grid(row=1, column=1, padx=20, pady=10)

        label_wl_cord = customtkinter.CTkLabel(wl_2, text="Coordination")
        label_wl_cord.grid(row=2, column=0, padx=20, pady=10)
        label_wl_cord_value = customtkinter.CTkLabel(wl_2, text=str(self.workload_two.wl_cor()))
        label_wl_cord_value.grid(row=2, column=1, padx=20, pady=10)

        label_wl_acm = customtkinter.CTkLabel(wl_2, text="Airspace Coordination")
        label_wl_acm.grid(row=3, column=0, padx=20, pady=10)
        label_wl_acm_value = customtkinter.CTkLabel(wl_2, text=str(self.workload_two.wl_acm()))
        label_wl_acm_value.grid(row=3, column=1, padx=20, pady=10)

        label_total_wl = customtkinter.CTkLabel(wl_2, text="Total Workload")
        label_total_wl.grid(row=4, column=0, padx=20, pady=10)
        label_total_wl_value = customtkinter.CTkLabel(wl_2, text=str(self.workload_two.workload()))
        label_total_wl_value.grid(row=4, column=1, padx=20, pady=10)

        button = customtkinter.CTkButton(master=self.window8, text="Close", command=self.button_event_8)
        button.grid(row=1, column=0, padx=20, pady=10)

    def button_event_8(self):
        self.window8.destroy()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
        elif new_map == "Black / White":
            self.map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
