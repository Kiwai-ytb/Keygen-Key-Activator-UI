import customtkinter as ctk, subprocess
from tkinter import messagebox
from api_call import activate_key

def get_uuid():
    try:
        lines = [l.strip() for l in subprocess.check_output("wmic csproduct get uuid", shell=True).decode().splitlines() if l.strip()]
        if len(lines) >= 2: 
            return lines[1]
        return "Not Found"
    except Exception:
        return "Not Found"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Basic parameters
        self.geometry("600x350")
        self.title("Kiwai's Key Activator")
        self.iconbitmap("Alya.ico")

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        # Main frame
        frame = ctk.CTkFrame(self)
        frame.pack(pady=30, padx=50, fill="both", expand=True)

        title_font = ctk.CTkFont(family="Segoe UI Bold", size=30)
        main_font = ctk.CTkFont(family="Segoe UI", size=15)

        # Widgets
        title = ctk.CTkLabel(frame, text="Welcome to Kiwai's Key Activator", font=title_font)
        ty_msg = ctk.CTkLabel(frame, text="Made by Kiwai with <3", font=main_font)
        activate_button = ctk.CTkButton(frame, text="Activate it!", command=self.on_activate, font=main_font, width=525)

        # Frame for the label + entry line
        key_frame = ctk.CTkFrame(frame)
        key_title = ctk.CTkLabel(key_frame, text="Please enter your Key to Activate it:", font=main_font)
        self.key_input = ctk.CTkEntry(key_frame, placeholder_text="Put your Key here", font=main_font, width=250)

        # Success/fail msg
        self.success_msg = ctk.CTkLabel(frame, text_color="green", font=main_font)
        self.fail_msg = ctk.CTkLabel(frame, text_color="red", font=main_font)
        self.no_key_msg = ctk.CTkLabel(frame, text="Please enter a Key", text_color="red", font=main_font)

        # Pack vertical dans le frame principal
        title.pack(pady=20)

        # Label + entry line
        key_frame.pack(pady=5, padx=20,)
        key_title.pack(side="left", padx=10, pady=10)
        self.key_input.pack(side="right", padx=10, pady=10)

        activate_button.pack(padx=20, pady=5)

        # Created by Kiwai msg
        ty_msg.pack(side="bottom", pady=10)

    def on_activate(self):
        license_key = self.key_input.get().strip()
        if not license_key:
            self.no_key_msg.pack(padx=10, pady=10)
            return
        
        len_k = len(license_key)
        print(f"license_key fetched: {license_key}")

        machine_udid = get_uuid()
        print(f"machine_udid fetched: {machine_udid}")

        result = activate_key(license_key, machine_udid)

        if result.get("success"):
            self.success_msg.configure(text=f"Key `{license_key}` activated successfuly!")
            self.success_msg.pack(padx=10, pady=10)
            self.key_input.delete(first_index=0, last_index=len_k)
            print("Successfuly activated the key!")
        elif result.get("status") == 422:
            self.fail_msg.configure(text=f"Key `{license_key}` couln't be activated!\nError: Key already activated!")
            self.fail_msg.pack(padx=10, pady=10)
            print(f"Couln't activate the key! (already activated)")
        elif result.get("error") == "'NoneType' object is not subscriptable":
            self.fail_msg.configure(text=f"Key `{license_key}` couln't be activated!\nError: Unvalid Key!")
            self.fail_msg.pack(padx=10, pady=10)
            print(f"Couln't activate the key! (unvalid key)")
        else:
            self.fail_msg.configure(text=f"Key `{license_key}` couln't be activated!\nError: {result.get("error")}")
            self.fail_msg.pack(padx=10, pady=10)
            print(f"Couln't activate the key!")

app = App()
app.mainloop()