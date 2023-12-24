import tkinter as tk
import math
from tkinter import ttk
import customtkinter as ctk
from PIL import Image,ImageTk


# Constants
WIDTH, HEIGHT = 700, 600
GRAVITY = 9.8  # m/s^2
GRID_SCALE = 50  # Scale of the grid lines


class ProjectileMotion:
    def __init__(self, root):
        self.root = root
        
        self.frame_left = ctk.CTkFrame(self.root, width=200, height=HEIGHT)
        self.frame_left.pack(side=tk.LEFT, padx=30, pady=20)

        self.image = ImageTk.PhotoImage(Image.open('bg.jpg'))
        
        self.canvas = ctk.CTkCanvas(self.root, width=WIDTH + 300, height=HEIGHT -50, bg='lightgray')
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)
        self.image = ImageTk.PhotoImage(Image.open('bg.jpg'))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        self.angle_label = ctk.CTkLabel(self.root,text="Launch Angle:", font=("Press Start 2P", 11))
        self.angle_label.place(x=60, y= 100)
        self.angle_value = tk.DoubleVar()   
        self.angle_scale = tk.Scale(self.root, from_=0, to=90, variable=self.angle_value, orient=tk.HORIZONTAL, showvalue=True)
        self.angle_scale.set(45)
        self.angle_scale.place(x=110, y=160)

        self.speed_label = ctk.CTkLabel(self.root, text="Initial Speed:", font=("Press Start 2P", 11))
        self.speed_label.place(x= 55, y= 200)
        self.speed_entry = ctk.CTkEntry(self.root)
        self.speed_entry.place(x=65, y=230)

        self.mass_label = ctk.CTkLabel(self.root, text="Mass:", font=("Press Start 2P", 11))
        self.mass_label.place(x=105, y=300)
        self.mass_entry = ctk.CTkEntry(self.root)
        self.mass_entry.place(x=65, y=330)

        self.height_label = ctk.CTkLabel(self.root, text="Initial Height:",font=("Press Start 2P", 11))
        self.height_label.place(x=50, y=400)
        self.height_entry = ctk.CTkEntry(self.root)
        self.height_entry.place(x=65, y=430)

        self.launch_button = ctk.CTkButton(self.root, text="Launch", command=self.launch_projectile)
        self.launch_button.place(x=60, y= 500)

        self.launch_button_pressed = False 

        self.help_button = ctk.CTkButton(self.root, text="Instructions", command=self.show_instructions)
        self.help_button.place(x= 800, y= 30)

        self.init_values()
        self.create_grid()
   
        self.create_axis()

        self.label_text = ctk.CTkLabel(self.root, text="Projectile Motion", font=("Press Start 2P", 20, 'bold'))
        self.label_text.place(x=400 , y=20)
        

        self.path = []

        self.projectile_image = Image.open('ball.png')
        self.projectile_image = ImageTk.PhotoImage(self.projectile_image)

        self.time_display = tk.Label(self.root, text="", font=("Verdana", 11), foreground="blue")
        self.time_display.place(x=WIDTH + 250 , y=130)
        
    def place_background_image(self):
    
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def create_axis(self):
        # X-axis
        self.canvas.create_line(0, HEIGHT - 75, WIDTH + 250, HEIGHT - 75, fill='black', width=2)

        # Y-axis
        self.canvas.create_line(50, 0, 50, HEIGHT, fill='black', width=2)

    def create_grid(self):
        # Draw horizontal lines
        for y in range(0, HEIGHT, GRID_SCALE):
            if y % (GRID_SCALE * 2) == 0:  
                color = 'gray'
            else:
                color = 'lightgray'

            self.canvas.create_line(0, y, WIDTH + 250, y, fill=color, tags='grid_line', dash=(2, 2))  # Dashed lines

        # Draw vertical lines
        for x in range(0, WIDTH + 250, GRID_SCALE):
            if x % (GRID_SCALE * 2) == 0:  
                color = 'gray'
            else:
                color = 'lightgray'

            self.canvas.create_line(x, 0, x, HEIGHT, fill=color, tags='grid_line', dash=(2, 2))  # Dashed lines

    def show_instructions(self):
        self.instruction_popup = ctk.CTk()
        self.instruction_popup.title("Instructions")
        self.instruction_popup.geometry("600x300")
        self.instruction_popup.resizable(False, False)

        instructions_text = """
        Welcome to Projectile Motion Simulation!

        This is our Final Project in Calculus Based Physics:)
        
        Instructions to use this simulation:
        - Adjust the Launch Angle using the slider.
        - Enter the Initial Speed, Mass, and Initial Height.
        - Click the 'Launch' button to start the simulation.
        - After launching the projectile it calculate the 
          MaxHeight, Range and Time of an object
        - Explore and enjoy simulating projectile motion!

        note: Depending on the entered value of the user vary the 
              simulation so make sure to balance the mass and speed 
              for smoother simulation. 
        """
        
        instructions_label = ctk.CTkLabel(self.instruction_popup, text=instructions_text, font=("Arial", 14), justify=tk.LEFT)
        instructions_label.pack(padx=20, pady=20)
        self.instruction_popup.mainloop()

    def init_values(self):
        self.x0, self.y0 = 50, HEIGHT - 75  # Initial position
        self.angle = 45  # Initial angle
        self.velocity = 30  # Initial velocity 
        self.time = 0.1
        self.drawn_object = None
        self.mass = 1
        self.range_value = tk.StringVar()  
        self.max_height_value = tk.StringVar()  

        self.grid_interval = 20  
        self.grid_color = 'gray'

    def range_height(self):
        self.range_display = tk.Label(self.root, textvariable=self.range_value, font=("Verdana", 11))
        self.range_display.place(x=WIDTH + 250 , y=150) 

        self.max_height_display = tk.Label(self.root, textvariable=self.max_height_value, font=("Verdana", 11))
        self.max_height_display.place(x=WIDTH + 250, y=170)

    def update_angle(self, value):
        self.angle = float(value)
        
        
        
    def calculate_motion(self):
        user_speed = self.speed_entry.get()
        user_mass = self.mass_entry.get()
        user_height = self.height_entry.get()

        angle_value = self.angle_scale.get()
        
        try:
            self.velocity = float(user_speed)
        except ValueError:
            self.velocity = 30
        
        try:
            self.mass = float(user_mass)
        except ValueError:
            self.mass = 1

        try:
            initial_height = float(user_height)
            if initial_height < 0:
                raise ValueError("Height should be a positive value.")
        except ValueError:
            initial_height = 0

        initial_height = initial_height if initial_height <= HEIGHT else initial_height / 100

        self.y0 = HEIGHT - 75 - initial_height

        self.vx = self.velocity * math.cos(math.radians(angle_value))
        self.vy = self.velocity * math.sin(math.radians(angle_value))

        # Calculate time to reach ground 
        self.time_to_ground = (2 * (self.vy + math.sqrt(self.vy**2 + 2 * GRAVITY * initial_height))) / GRAVITY/2
        self.time_display.config(text=f"Time to Ground: {self.time_to_ground:.2f} seconds")


        acceleration = GRAVITY * (self.mass / 10)

        self.x = self.x0 + self.vx * self.time
        self.y = self.y0 - (self.vy * self.time - 0.5 * acceleration * self.time ** 2)
        

        self.time += 0.1

        # Calculate the range
        self.range = self.vx * ((2 * (self.vy + math.sqrt(self.vy**2 + 2 * GRAVITY * initial_height))) / GRAVITY)/2
        self.range_value.set(f"Range: {self.range:.2f} meters")

        #Calculate the maximum height
        self.max_height = initial_height + (self.vy ** 2) / (2 * GRAVITY)
        self.max_height_value.set(f"Max Height: {self.max_height:.2f} meters")

    def draw(self):
        self.calculate_motion()
        
        if self.drawn_object:
            self.canvas.delete(self.drawn_object)
      
        self.drawn_object = self.canvas.create_image(self.x, self.y, anchor=tk.CENTER, image=self.projectile_image)
        self.path.append((self.x, self.y))

        if len(self.path) > 1:
            self.canvas.create_line(self.path, fill='blue', smooth=True, width=2)

        if self.y < HEIGHT - 73:
            self.root.after(40, self.draw)
        else:
            self.init_values()
            self.path = []
        self.time += 1

    def enable_launch_button(self):
        self.launch_button_pressed = False

    def launch_projectile(self):
        if self.launch_button_pressed:
            return 
         
        self.launch_button_pressed = True  
        self.canvas.delete(tk.ALL)
        self.root.after(2000, self.enable_launch_button)
        if self.drawn_object:
            self.canvas.delete(self.drawn_object)
        if self.path:
            self.canvas.delete(*self.path)

        self.init_values()

        self.place_background_image()

        self.create_grid()
        self.create_axis()
        self.range_height()
        
        try:
            initial_height = float(self.height_entry.get())
            if initial_height < 0:
                raise ValueError("Height should be a positive value.")
        except ValueError:
            initial_height = 0  

        self.y0 = HEIGHT - 50 - initial_height
    
        self.draw() 



def main():
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    
    root.title("Projectile Motion Simulation")
    root.geometry("1000x600+100+100")
    root.resizable(False, False)
    app = ProjectileMotion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
