# Install necessary libraries
# pip install kivy
# pip install plyer (for notifications)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime, timedelta


class CountdownApp(App):
    def build(self):
        self.title = 'Event Countdown App'
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.event_name_input = TextInput(hint_text='Event Name', multiline=False)
        self.event_date_input = TextInput(hint_text='Event Date (YYYY-MM-DD)', multiline=False)

        self.create_button = Button(text='Create Countdown')
        self.create_button.bind(on_press=self.create_countdown)

        self.layout.add_widget(self.event_name_input)
        self.layout.add_widget(self.event_date_input)
        self.layout.add_widget(self.create_button)

        return self.layout

    def create_countdown(self, instance):
        event_name = self.event_name_input.text
        event_date_str = self.event_date_input.text

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
        except ValueError:
            self.show_popup("Invalid date format. Please use YYYY-MM-DD.")
            return

        now = datetime.now()
        time_remaining = event_date - now

        if time_remaining.total_seconds() <= 0:
            self.show_popup("Invalid event date. Please choose a future date.")
            return

        self.show_popup(f"Countdown for {event_name} created!\n{time_remaining.days} days remaining.")

        # Schedule update every second
        Clock.schedule_interval(lambda dt: self.update_countdown(event_date), 1)

    def update_countdown(self, event_date):
        now = datetime.now()
        time_remaining = event_date - now

        if time_remaining.total_seconds() <= 0:
            self.show_notification(f"{self.event_name_input.text} has arrived!")
            Clock.unschedule(self.update_countdown)
            return

        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=f"Time remaining: {time_remaining}"))

    def show_popup(self, message):
        popup = Popup(title='Notification', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_notification(self, message):
        notification.notify(
            title='Event Countdown',
            message=message,
            timeout=10
        )

if __name__ == '__main__':
    CountdownApp().run()
