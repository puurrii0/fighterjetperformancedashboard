import tkinter as tk
import webbrowser
from PIL import Image, ImageTk

class LoginDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Dashboard")

        # Get screen dimensions
        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()

        try:
            bg_image = Image.open("./bg.webp")  # Replace with your image path
            bg_image = bg_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.bg_photo = None

        # Create canvas for background
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        rect_width = 300
        rect_height = 300
        rect_x1 = (self.screen_width - rect_width) / 2
        rect_y1 = (self.screen_height - rect_height) / 2
        rect_x2 = rect_x1 + rect_width
        rect_y2 = rect_y1 + rect_height

        # Create centered semi-transparent blue login area
        self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="light blue", stipple="gray25")

        # Add login elements
        self.canvas.create_text(self.screen_width / 2, rect_y1 + 30, text="Login Dashboard", font=("undefined", 16, "bold"), fill="black")

        self.canvas.create_text(self.screen_width / 2 - 90, rect_y1 + 80, text="Username:", anchor="w", font=("undefined", 12), fill="black")
        self.username_entry = tk.Entry(self, width=20, font=("undefined", 12))
        self.canvas.create_window(self.screen_width / 2 - 90, rect_y1 + 110, window=self.username_entry, anchor="w")

        self.canvas.create_text(self.screen_width / 2 - 90, rect_y1 + 150, text="Password:", anchor="w", font=("undefined", 12), fill="black")
        self.password_entry = tk.Entry(self, show="*", width=20, font=("undefined", 12))
        self.canvas.create_window(self.screen_width / 2 - 90, rect_y1 + 180, window=self.password_entry, anchor="w")

        self.login_button = tk.Button(self, text="Login", font=("undefined", 12), command=self.login)
        self.canvas.create_window(self.screen_width / 2, rect_y2 - 50, window=self.login_button)

    def login(self):
        correct_username = "admin"
        correct_password = "password"

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == correct_username and password == correct_password:
            webbrowser.open("./dashboard/index.html")
        else:
            print("Incorrect username or password")

if __name__ == "__main__":
    app = LoginDashboard()
    app.mainloop()
