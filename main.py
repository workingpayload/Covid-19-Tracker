import kivy.uix.label
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.button import ButtonBehavior,Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen,NoTransition,CardTransition
from kivy.config import Config
from bar import Bar
from datetime import date
from covid import Covid
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

Config.set('graphics','width','1200')
Config.set('graphics','height',900)
Config.set('graphics','borderless','1')
Config.write()
Config.set('kivy', 'exit_on_escape', '0')

import kivy.utils

class LocationBarItem(BoxLayout):
    def __init__(self,**kwargs):
        self.orientation = "horizontal"
        self.size_hint = (0.74,1)
        super().__init__()

        bar_item = BoxButton(orientation="vertical",size_hint=(0.01,0.9))
        _bar = Bar(size_hint=(1,0.9),value = kwargs['cases'])
        _loc = Label(size_hint=(1,0.1),text = kwargs['loc'], font_size="10sp", color=kivy.utils.get_color_from_hex("#4746e"))
        bar_item.add_widget(_bar)
        bar_item.add_widget(_loc)
        self.add_widget(bar_item)




class BoxButton(ButtonBehavior,BoxLayout):
    pass



class Spacer(Label):
    pass
class ImageButton(ButtonBehavior,Image):
    pass

class LabelButton(ButtonBehavior,Label):
    pass

class DashboardScreen(Screen):
    pass

GUI = Builder.load_file("main.kv")


class MainApp(App):

    def build(self):
        self.today = date.today()
        self.date = self.today.strftime("%B %d, %Y")

        return GUI

    def on_start(self):
        LabelBase.register(name="myraid_pro_reg", fn_regular='Fonts/MYRIADPRO-CONDIT.OTF')
        LabelBase.register(name="d_din_reg", fn_regular='Fonts/D-DIN.otf')
        LabelBase.register(name="roboto_medium", fn_regular='Fonts/Roboto-Medium.ttf')
        LabelBase.register(name="roboto_thin", fn_regular='Fonts/Roboto-Thin.ttf')
        LabelBase.register(name="bistecca", fn_regular='Fonts/Bistecca.ttf')
        LabelBase.register(name="teko-reg", fn_regular='Fonts/Teko-Regular.ttf')
        LabelBase.register(name="barlow-reg", fn_regular='Fonts/BarlowSemiCondensed-Regular.ttf')
        LabelBase.register(name="barlow-bold", fn_regular='Fonts/BarlowSemiCondensed-SemiBold.ttf')
        LabelBase.register(name="SourceSansPro-Regular", fn_regular='Fonts/SourceSansPro-Regular.ttf')

        self.root.ids['dashboard_screen'].ids['date_label_id'].text = self.date
        cases_plot = self.root.ids['dashboard_screen'].ids['cases_plot_id']
        self.codvid = Covid(source="worldometers")

        chart_countries = {
            "AR": "Argentina",
            "AT": "Austria",
            "AZ": "Azerbaijan",
            "BD": "Bangladesh",
            "BE": "Belgium",
            "BR": "Brazil",
            "CA": "Canada",
            "FR": "France",
            "DE": "Germany",
            "GR": "Greece",
            "IN": "India",
            "ID": "Indonesia",
            "IR": "Iran",
            "IQ": "Iraq",
            "IT": "Italy",
            "JM": "Jamaica",
            "JP": "Japan",
            "MX": "Mexico",
            "NP": "Nepal",
            "NL": "Netherlands",
            "NZ": "New Zealand",
            "PK": "Pakistan",
            "PW": "Palau",
            "PH": "Philippines",
            "SA": "Saudi Arabia",
            "SG": "Singapore",
            "ZA": "South Africa",
            "EA": "Spain",
            "LK": "Sri Lanka",
            "SE": "Sweden",
            "CH": "Switzerland",
            "TW": "Taiwan",
            "TJ": "Tajikistan",
            "TH": "Thailand",
            "TR": "Turkey",
            "UG": "Uganda",
            "UA": "Ukraine",
            "AE": "UAE",
            "GB": "UK",
            "US": "USA"}

        temp_json = self.codvid.get_status_by_country_name("USA")
        US_cases = temp_json['confirmed']

        for key, value in chart_countries.items():
            location_case = self.codvid.get_status_by_country_name(value)
            normalized_value = int((location_case['confirmed']/US_cases)*100)
            location_bar_item = LocationBarItem(loc=str(key),cases=normalized_value)
            cases_plot.add_widget(location_bar_item)

    def close(self):
        quit()

    def minimize(self):
        Window.minimize()

    def process_datasearch(self):
        _location = (self.root.ids['dashboard_screen'].ids['search_location_id'].text).strip()
        error_message = "This location doesn't exist."
        try:
            _data = self.codvid.get_status_by_country_name(_location)
            self.root.ids['dashboard_screen'].ids['confirmed_cases_id'].text=(f"{(_data['confirmed']):,d}")
            self.root.ids['dashboard_screen'].ids['confirmed_cases_delta_id'].text = (f"{(_data['new_cases']):,d}")
            self.root.ids['dashboard_screen'].ids['confirmed_deaths_id'].text = (f"{(_data['deaths']):,d}")
            self.root.ids['dashboard_screen'].ids['confirmed_deaths_delta_id'].text = (f"{(_data['new_deaths']):,d}")
            self.root.ids['dashboard_screen'].ids['recovered_cases_id'].text = (f"{(_data['recovered']):,d}")
            self.root.ids['dashboard_screen'].ids['active_cases_id'].text = (f"{(_data['active']):,d}")

            #Recovery rate: % of Confirmed cases recovered
            recovery_rate = (_data['recovered']/_data['confirmed'])*100

            self.root.ids['dashboard_screen'].ids['recovery_rate_id'].text = str(int(recovery_rate)) + "% of cases\n recovered"

            self.root.ids['dashboard_screen'].ids['critical_cases_id'].text = str((f"{(_data['critical']):,d}"))+" cases in\n critical state"





        except:
            self.root.ids['dashboard_screen'].ids['error_message_id'].text=error_message





MainApp().run()





