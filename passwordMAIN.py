import customtkinter as ctk
import string
import random

# ------------------------
# PASSWORD LOGIC
# ------------------------

def evaluate_password_strength(pw: str):
    if not pw:
        return "Enter a password", "babyblue"

    score = 0
    length = len(pw)

    has_lower = any(c.islower() for c in pw)
    has_upper = any(c.isupper() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_symbol = any(c in string.punctuation or c == "-" for c in pw)

    # length scoring
    if length >= 8:
        score += 2
    if length >= 12:
        score += 2
    if length >= 16:
        score += 2

    # variety scoring
    score += sum([has_lower, has_upper, has_digit, has_symbol])

    # 0–4: weak, 5–8: okay, 9+: strong
    if score <= 4:
        return "Weak", "#ff4c4c"      # red
    elif score <= 8:
        return "Okay", "#ffcc00"      # yellow
    else:
        return "Strong", "#00ff99"    # green


# ------------------------
# APP
# ------------------------

class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # global appearance
        ctk.set_appearance_mode("light")
        self.title("Password Tool")
        self.geometry("1000x600")
        self.configure(fg_color="#5a189a")  # main purple

        self.main_purple = "#5a189a"
        self.light_purple = "#7b2cbf"
        self.accent_purple = "#9d4edd"
        self.text_baby_blue = "#9ef0ff"
        self.white = "#ffffff"

        # TABVIEW
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=self.light_purple,
            corner_radius=20,
            segmented_button_fg_color=self.light_purple,
            segmented_button_selected_color=self.accent_purple,
            segmented_button_unselected_color=self.light_purple,
            segmented_button_selected_hover_color=self.accent_purple,
            segmented_button_unselected_hover_color="#8c42d9",
            text_color=self.text_baby_blue,
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # tabs
        self.tab_checker = self.tabview.add("Password Checker")
        self.tab_generator = self.tabview.add("Password Generator")

        # make selected tab visually "bigger" by padding + bold font
        self.tabview._segmented_button.configure(
            corner_radius=20,
            font=("Segoe UI", 14, "bold"),
            border_width=0,
        )

        self.build_checker_tab()
        self.build_generator_tab()

    # ------------------------
    # CHECKER TAB
    # ------------------------

    def build_checker_tab(self):
        frame = self.tab_checker

        title = ctk.CTkLabel(
            frame,
            text="Password Checker",
            font=("Segoe UI", 24, "bold"),
            text_color=self.text_baby_blue,
        )
        title.pack(pady=(20, 10))

        self.checker_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter password...",
            show="*",
            width=400,
            height=45,
            corner_radius=20,
            fg_color=self.white,
            border_color=self.accent_purple,
            border_width=2,
            text_color="black",
        )
        self.checker_entry.pack(pady=10)

        self.show_pw_var = ctk.BooleanVar(value=False)
        show_pw_toggle = ctk.CTkSwitch(
            frame,
            text="Show password",
            variable=self.show_pw_var,
            command=self.toggle_password_visibility,
            fg_color=self.accent_purple,
            progress_color=self.white,
            text_color=self.text_baby_blue,
            button_color=self.white,
            button_hover_color="#dedcff",
        )
        show_pw_toggle.pack(pady=5)

        check_button = ctk.CTkButton(
            frame,
            text="Check Strength",
            command=self.check_strength,
            fg_color=self.accent_purple,
            hover_color="#c77dff",
            text_color=self.white,
            corner_radius=20,
            width=200,
            height=40,
        )
        check_button.pack(pady=15)

        self.result_label = ctk.CTkLabel(
            frame,
            text="",
            font=("Segoe UI", 20, "bold"),
            text_color=self.text_baby_blue,
        )
        self.result_label.pack(pady=10)

    def toggle_password_visibility(self):
        self.checker_entry.configure(show="" if self.show_pw_var.get() else "*")

    def check_strength(self):
        pw = self.checker_entry.get()
        strength, color = evaluate_password_strength(pw)
        self.result_label.configure(text=strength, text_color=color)

    # ------------------------
    # GENERATOR TAB
    # ------------------------

    def build_generator_tab(self):
        frame = self.tab_generator

        title = ctk.CTkLabel(
            frame,
            text="Password Generator",
            font=("Segoe UI", 24, "bold"),
            text_color=self.text_baby_blue,
        )
        title.pack(pady=(20, 10))

        # length slider
        length_frame = ctk.CTkFrame(
            frame,
            fg_color=self.main_purple,
            corner_radius=20,
        )
        length_frame.pack(pady=10, padx=40, fill="x")

        length_label = ctk.CTkLabel(
            length_frame,
            text="Password length",
            font=("Segoe UI", 14),
            text_color=self.text_baby_blue,
        )
        length_label.pack(pady=(10, 0))

        self.length_var = ctk.IntVar(value=16)
        self.length_slider = ctk.CTkSlider(
            length_frame,
            from_=5,
            to=50,
            number_of_steps=45,
            variable=self.length_var,
            fg_color=self.white,
            progress_color=self.accent_purple,
            button_color=self.accent_purple,
            button_hover_color="#c77dff",
            corner_radius=100,
            height=14,
            command=self.update_length_label,
        )
        self.length_slider.pack(pady=10, padx=20, fill="x")

        self.length_value_label = ctk.CTkLabel(
            length_frame,
            text="16 characters",
            text_color=self.text_baby_blue,
            font=("Segoe UI", 12),
        )
        self.length_value_label.pack(pady=(0, 10))

        # include symbols toggle
        self.include_symbols_var = ctk.BooleanVar(value=True)
        symbols_switch = ctk.CTkSwitch(
            frame,
            text="Include symbols (!@#$...)",
            variable=self.include_symbols_var,
            fg_color=self.accent_purple,
            progress_color=self.white,
            button_color=self.white,
            button_hover_color="#dedcff",
            text_color=self.text_baby_blue,
        )
        symbols_switch.pack(pady=10)

        # generate button
        generate_button = ctk.CTkButton(
            frame,
            text="Generate Password",
            command=self.generate_password,
            fg_color=self.accent_purple,
            hover_color="#c77dff",
            text_color=self.white,
            corner_radius=20,
            width=220,
            height=40,
        )
        generate_button.pack(pady=15)

        # output field
        self.generated_entry = ctk.CTkEntry(
            frame,
            width=500,
            height=45,
            corner_radius=20,
            fg_color=self.white,
            border_color=self.accent_purple,
            border_width=2,
            text_color="black",
        )
        self.generated_entry.pack(pady=10)

        # strength of generated password
        self.gen_strength_label = ctk.CTkLabel(
            frame,
            text="",
            font=("Segoe UI", 14, "bold"),
            text_color=self.text_baby_blue,
        )
        self.gen_strength_label.pack(pady=5)

        # copy button
        copy_button = ctk.CTkButton(
            frame,
            text="Copy to Clipboard",
            command=self.copy_password,
            fg_color=self.light_purple,
            hover_color="#c77dff",
            text_color=self.white,
            corner_radius=20,
            width=200,
            height=36,
        )
        copy_button.pack(pady=10)

    def update_length_label(self, value):
        self.length_value_label.configure(text=f"{int(float(value))} characters")

    def generate_password(self):
        length = int(self.length_var.get())

        # always allow letters, digits, and dashes
        chars = string.ascii_letters + string.digits + "-"
        if self.include_symbols_var.get():
            chars += string.punctuation

        # ensure we don't accidentally break if length < 1
        if length < 1:
            length = 1

        password = "".join(random.choice(chars) for _ in range(length))

        self.generated_entry.delete(0, "end")
        self.generated_entry.insert(0, password)

        strength, color = evaluate_password_strength(password)
        self.gen_strength_label.configure(text=f"Strength: {strength}", text_color=color)

    def copy_password(self):
        pw = self.generated_entry.get()
        if not pw:
            return
        self.clipboard_clear()
        self.clipboard_append(pw)


if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
