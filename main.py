from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import date
from connection_db import ConnectDb
import re


class MainScreenManager(ScreenManager):
    pass

class LoginScreen(Screen):
    #Variable for alert box
    dialog = None

    #Method for authenticate login in app
    def login(self):
        username = self.ids.username_input.text.lower()
        password = self.ids.password_input.text

        db = LoginApp.consult_db()

        if db.find_user("SELECT username, password FROM users WHERE \
                         username = %s AND password = %s", (username, password)):

            self.ids.msg_login.text = "Log in"
            self.alert_login_successful()            
            MDApp.get_running_app().root.current = "main_screen"

        else:
            self.ids.msg_login.text = "Username or password invalid.\nCheck and try again."
            self.ids.username_input.text = ""
            self.ids.password_input.text = ""
    
    #Method for open sign up screen
    def sign_up(self):
        MDApp.get_running_app().root.current = "sign_up_screen"
    
    #Method for open recover password screen
    def recover_password(self):
        MDApp.get_running_app().root.current = "recover_screen"
    
    #Method that open login alert box if login is successful
    def alert_login_successful(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Login successful!",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_login_successful
                    ),                    
                ],
            )
        self.dialog.open()

    #Method that close login alert box
    def close_alert_login_successful(self, *args):
        self.dialog.dismiss(force=True)

class SignUpScreen(Screen):
    #Variables for alert boxes
    dialog_confirm_sign_up = None
    dialog_check_password = None
    dialog_check_empty_field = None
    dialog_already_exists = None
    dialog_check_connection = None
    dialog_email_invalid = None

    #Method that insert a new account into database
    def insert_into_db(self):
        #Variables for save new user data
        today_date = date.today()
        new_name = self.ids.new_name_input.text.lower()
        new_email = self.ids.new_email_input.text.lower()
        new_username = self.ids.new_username_input.text.lower()
        new_password = self.ids.new_password_input.text

        db = LoginApp.consult_db()
        verify = db.find_user("SELECT * FROM users WHERE \
                               username = %s OR email = %s", (new_username, new_email))

        if verify:
            self.alert_already_exists()
        else:
            db.add_user("INSERT INTO users (name, email, signed_up_date, \
                        username, password) VALUES (%s, %s, %s, %s, %s)",
                        (new_name, new_email, today_date, new_username, new_password))
            self.alert_confirm_sign_up()
            self.back_sign_up_screen()

    #Method that warns if the email or username already exists in the database
    def alert_already_exists(self):
        if not self.dialog_already_exists:
            self.dialog_already_exists = MDDialog(
                text="Email or username already exists, \
                     \nplease verify and choose another.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_already_exists
                    ),                    
                ],
            )
        self.dialog_already_exists.open()
    
    #Method that close already exists alert box
    def close_alert_already_exists(self, *args):
        self.dialog_already_exists.dismiss(force=True)

    #Method that back to login screen
    def back_sign_up_screen(self):
        MDApp.get_running_app().root.current = "login_screen"
        self.ids.new_name_input.text = ""
        self.ids.new_username_input.text = ""
        self.ids.new_email_input.text = ""
        self.ids.new_password_input.text = ""
        self.ids.new_password_confirm_input.text = ""
    
    #Method that open confirm sign up alert box if sign up is successful
    def alert_confirm_sign_up(self):
        if not self.dialog_confirm_sign_up:
            self.dialog_confirm_sign_up = MDDialog(
                text="Sign up successful.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_confirm_sign_up
                    ),                    
                ],
            )
        self.dialog_confirm_sign_up.open()
    
    #Method that close confirm sign up alert box
    def close_alert_confirm_sign_up(self, *args):
        self.dialog_confirm_sign_up.dismiss(force=True)

    #Method that open alert for check password
    #If a password text field don't match with a password confirm text field
    def alert_check_password(self):
        if not self.dialog_check_password:
            self.dialog_check_password = MDDialog(
                text="Passwords don't match, check and try again!",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_check_password
                    ),                    
                ],
            )
        self.dialog_check_password.open()
    
    #Method that close check password alert box
    def close_alert_check_password(self, *args):
        self.dialog_check_password.dismiss(force=True)
    
    #Method that open alert box if have a text field in blank
    def alert_check_empty_field(self):
        if not self.dialog_check_empty_field:
            self.dialog_check_empty_field = MDDialog(
                text="Please,\nfill in the fields correctly.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_check_empty_field
                    ),                    
                ],
            )
        self.dialog_check_empty_field.open()
    
    #Method that close check empty text field alert box
    def close_alert_check_empty_field(self, *args):
        self.dialog_check_empty_field.dismiss(force=True)

    #Method that open alert box if email is invalid
    def alert_email_invalid(self):
        if not self.dialog_email_invalid:
            self.dialog_email_invalid = MDDialog(
                text="Invalid Email.\nPlease check and try again.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_email_invalid
                    ),                    
                ],
            )
        self.dialog_email_invalid.open()
    
    #Method that close email invalid alert box
    def close_alert_email_invalid(self, *args):
        self.dialog_email_invalid.dismiss(force=True)

    #Method that validate data in text fields 
    def validate_field(self):
        name = len(self.ids.new_name_input.text)
        user = len(self.ids.new_username_input.text)  
        email = self.ids.new_email_input.text.lower()
        password = len(self.ids.new_password_input.text)

        pattern = "[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"

        if name < 3 or name > 50:
            self.ids.new_name_input.error = True
            self.ids.new_name_input.helper_text_mode = "on_error"
            self.ids.new_name_input.helper_text = "Invalid Name."
        else:
            self.ids.new_name_input.error = False
        
        if user < 3 or user > 15:
            self.ids.new_username_input.error = True
            self.ids.new_username_input.helper_text_mode = "on_error"
            self.ids.new_username_input.helper_text = "Invalid Username."
        else:
            self.ids.new_username_input.error = False

        if password < 3 or password > 15:
            self.ids.new_password_input.error = True
            self.ids.new_password_input.helper_text_mode = "on_error"
            self.ids.new_password_input.helper_text = "Invalid Password."
        else:
            self.ids.new_password_input.error = False

        if name >= 3 and name <= 50 and user >= 3 \
            and user <= 15 and password >= 3 and password <= 15:

            if len(email) <= 50:
                if re.search(pattern, email):
                    self.validate_password()
                else:
                    self.ids.new_email_input.error = True
                    self.ids.new_email_input.helper_text_mode = "on_error"
                    self.ids.new_email_input.helper_text = "Invalid Email."
                    self.alert_email_invalid()
            else:
                self.ids.new_email_input.error = True
                self.ids.new_email_input.helper_text_mode = "on_error"
                self.ids.new_email_input.helper_text = "Invalid Email."
                self.alert_email_invalid()
        else:
            self.alert_check_empty_field()

    #Method that validates the password if the data is validated by the validate_field method
    def validate_password(self):
        if self.ids.new_password_input.text == self.ids.new_password_confirm_input.text:
            self.insert_into_db()
        else:
            self.alert_check_password()

class RecoverPasswordScreen(Screen):    
    #Variable for alert box
    dialog_alert_email_not_find = None
    
    #Method for back to login screen
    def back_recover_password_screen(self):
        self.ids.email_recover_input.text = ""
        self.ids.email_recover_input.error = False
        MDApp.get_running_app().root.current = "login_screen"
    
    #Method that verify email is registered for recover password
    def verify_email(self):
        email_recover = self.ids.email_recover_input.text        

        db = LoginApp.consult_db()
        verify = db.find_user("SELECT * FROM users WHERE \
                               email = %s", (email_recover,))
        
        if verify:
            MDApp.get_running_app().root.current = "new_password_screen"
            self.ids.email_recover_input.text = ""
            NewPasswordScreen.user_id = verify[0]            
        else:
            self.alert_email_not_find()
            self.ids.email_recover_input.text = ""
            self.ids.email_recover_input.error = True
            self.ids.email_recover_input.helper_mode = "on_error"
            self.ids.email_recover_input.helper_text = "Invalid Email."

    #Method that open alert if email informed not find in database
    def alert_email_not_find(self):
        if not self.dialog_alert_email_not_find:
            self.dialog_alert_email_not_find = MDDialog(
                text="Email not find.\nCheck and try again.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_email_not_find
                    ),                    
                ],
            )
        self.dialog_alert_email_not_find.open()
    
    #Method that close email not find alert
    def close_alert_email_not_find(self, *args):
        self.dialog_alert_email_not_find.dismiss(force=True)    

class NewPasswordScreen(Screen):
    #Variables for alert boxes and for save user id
    user_id = None
    dialog_password_changed = None
    dialog_check_password = None
    dialog_alert_password_invalid = None

    #Method that back to login screen
    def quit_new_password_screen(self):
        MDApp.get_running_app().root.current = "login_screen"

    #Method that back to recover password screen
    def back_new_password_screen(self):
        self.ids.password_recover_input.text = ""
        self.ids.password_recover_confirm_input.text = ""
        MDApp.get_running_app().root.current = "recover_screen"

    #Method that verifies and validates the new password entered
    def change_password(self):
        db = LoginApp.consult_db()

        if len(self.ids.password_recover_input.text) < 3 \
            or len(self.ids.password_recover_input.text) > 15:

            self.ids.password_recover_input.text = ""
            self.ids.password_recover_confirm_input.text = ""
            self.ids.password_recover_input.error = True
            self.ids.password_recover_input.helper_text_mode = "on_error"
            self.ids.password_recover_input.helper_text = "Invalid Password."
            self.alert_password_invalid()
        else:
            self.ids.password_recover_input.error = False

            if self.ids.password_recover_input.text \
                == self.ids.password_recover_confirm_input.text:

                db.add_user("UPDATE users SET password = %s WHERE \
                            id = %s", (self.ids.password_recover_input.text, self.user_id))

                self.ids.password_recover_input.text = ""
                self.ids.password_recover_confirm_input.text = ""
                self.alert_password_changed()
                self.quit_new_password_screen()
            else:
                self.alert_check_password()

    #Method that open alert if 
    #password text field don't match with password confirm text field
    def alert_check_password(self):
        if not self.dialog_check_password:
            self.dialog_check_password = MDDialog(
                text="Passwords don't match, check and try again!",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_check_password
                    ),                    
                ],
            )
        self.dialog_check_password.open()
    
    #Method that close check password alert
    def close_alert_check_password(self, *args):
        self.dialog_check_password.dismiss(force=True)

    #Method that open password invalid alert if password entered is invalid
    def alert_password_invalid(self):
        if not self.dialog_alert_password_invalid:
            self.dialog_alert_password_invalid = MDDialog(
                text="Invalid password.\nCheck and try again!",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_password_invalid
                    ),                    
                ],
            )
        self.dialog_alert_password_invalid.open()
    
    #Method that close password invalid alert
    def close_alert_password_invalid(self, *args):
        self.dialog_alert_password_invalid.dismiss(force=True)

    #Method that open password changed alert
    def alert_password_changed(self):
        if not self.dialog_password_changed:
            self.dialog_password_changed = MDDialog(
                text="Password changed successful.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_password_changed
                    ),                    
                ],
            )
        self.dialog_password_changed.open()
    
    #Method that close password changed alert
    def close_alert_password_changed(self, *args):
        self.dialog_password_changed.dismiss(force=True)  

class MainScreen(Screen):
    #Method that quit the system and back to login screen.
    def quit_main_screen(self):
        MDApp.get_running_app().root.current = "login_screen"
    
    #Method that open data screen
    def see_data(self):              
        MDApp.get_running_app().root.current = "data_screen"

class DataScreen(Screen):
    #Variable for alert boxes and for save user id
    user_id = None
    dialog_alert_confirm_data_changed = None
    dialog_alert_data = None

    #Method that back to main screen and save new data if a new data is changed
    #with calling change_data_back_btn method
    def back_data_screen(self):
        if self.ids.data_name.disabled == False:
            self.change_data_back_btn()
        else:
            MDApp.get_running_app().root.current = "main_screen"
    
    #Method that open confirm data changed alert box
    def alert_confirm_data_changed(self):
        if not self.dialog_alert_confirm_data_changed:
            self.dialog_alert_confirm_data_changed = MDDialog(
                text="Successfully changed data.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_confirm_data_changed
                    ),                    
                ],
            )
        self.dialog_alert_confirm_data_changed.open()
    
    #Method that close confirm data changed alert box
    def close_alert_confirm_data_changed(self, *args):
        self.dialog_alert_confirm_data_changed.dismiss(force=True)

    #Method that change data and validate new data
    def change_data(self):
        db = LoginApp.consult_db()      

        if self.ids.data_name.disabled == True:
            self.ids.data_name.disabled = False
        else:
            if len(self.ids.data_name.text) < 3 or len(self.ids.data_name.text) > 50:
                self.alert_data()
            else:
                db.add_user("UPDATE users SET name = %s WHERE \
                             id = %s", (self.ids.data_name.text.lower(), self.user_id))
                self.ids.data_name.disabled = True
                self.alert_confirm_data_changed()  
    
    #Method that change and save data in data screen if back button is clicked
    def change_data_back_btn(self):  
        db = LoginApp.consult_db() 

        if self.ids.data_name.disabled == True:
            self.ids.data_name.disabled = False
        else:
            if len(self.ids.data_name.text) < 3 or len(self.ids.data_name.text) > 50:
                self.alert_data()
            else:
                db.add_user("UPDATE users SET name = %s WHERE \
                             id = %s", (self.ids.data_name.text.lower(), self.user_id))
                self.ids.data_name.disabled = True                
                self.alert_confirm_data_changed()  
                MDApp.get_running_app().root.current = "main_screen"

    #Method that open invalid data alert box if a new data is invalid
    def alert_data(self):
        if not self.dialog_alert_data:
            self.dialog_alert_data = MDDialog(
                text="Invalid data.",
                size_hint_x=0.7,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        on_release=self.close_alert_data
                    ),                    
                ],
            )
        self.dialog_alert_data.open()

    #Method that close invalid data alert box
    def close_alert_data(self, *args):
        self.dialog_alert_data.dismiss(force=True)

class LoginApp(MDApp, App):
    #Set window size and window title
    Window.size = 500, 700
    Window.minimum_width = 500
    Window.minimum_height = 700
    MDApp.title=('Login System by Cesar C. Santos')

    def build(self):  
        #Set primary and accent palette and material style
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.accent_palette = "Blue"  
        self.theme_cls.accent_hue = "100"
        self.theme_cls.material_style = "M3"  

        return MainScreenManager()

    #Method to switch between dark mode and light mode
    def on_active(self, switch, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
    
    #Method that changes the data on the data screen to the current user's data
    def user_data(self):
        username = self.root.get_screen("login_screen").ids.username_input.text
        password = self.root.get_screen("login_screen").ids.password_input.text

        try:
            db = LoginApp.consult_db()
            data = db.find_user("SELECT name, username, email, signed_up_date, id FROM \
                                users WHERE username = %s AND password = %s", (username, password)) 

            self.root.get_screen("data_screen").ids.data_name.text = (data[0].title())
            self.root.get_screen("data_screen").ids.data_username.text = (data[1])
            self.root.get_screen("data_screen").ids.data_email.text = (data[2])
            self.root.get_screen("data_screen").ids.data_sign_up_date.text \
                                                        = (data[3].strftime(f"%m/%d/%Y"))            
            DataScreen.user_id = data[4]
        except:
            pass
    
    #Method to clear login screen
    def clear_login(self):
        self.root.get_screen("login_screen").ids.username_input.text = ""
        self.root.get_screen("login_screen").ids.password_input.text = ""
    
    #Function for database consults
    def consult_db():
        db = ConnectDb()
        return db
    
    #Function to check if the database is connected
    def verify_db_is_on():
        db = ConnectDb()
        dbs = db.connect()
        return dbs

#If database not connected, the app don't initialize and print a alert message on terminal
if __name__ == '__main__':
    LoginApp().run() if LoginApp.verify_db_is_on() == None \
    else print('No connection with database. Verify and try again.')