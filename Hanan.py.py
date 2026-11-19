# Name: Hanan Binti Muhammad Termizi
# Matrics No: BS21110095

from tkinter import Tk, Canvas, Button, Menu, filedialog, messagebox, Frame, StringVar, OptionMenu, Label 
from tkinter import PhotoImage, simpledialog, colorchooser, Toplevel, Menubutton
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

class MyImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Hanan's Image Editor")
        self.root.geometry("800x600")
        self.root.iconbitmap("Office_-58_icon-icons.com_73965.ico")
        self.root.color_fg = 'black'
        self.root.configure(bg="lightgrey")
        
        # Canvas for displaying the image
        self.canvas = Canvas(self.root, bg="white", width=1000, height=550)
        self.canvas.pack(side="bottom")

        self.create_widgets()
        self.image = None
        
        self.image_history = []  # Store image history for undo and redo
        self.current_index = -1  # Keep track of the current index in the history
        
        # To bind the mouse buttons with events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # For drawing function
        self.run = False
        self.prev_x = None
        self.prev_y = None
        
        # Bind the circle drawing function to mouse click event
        self.canvas.bind("<Button-1>", self.on_canvas_click) 
        
        self.drawing = False  # Flag to control drawing
        self.draw_button = None  # Initialize the draw button
        self.tool = "line"  # Default drawing tool
        
        self.text_tool_active = False  # Flag to check if text tool is active
        
        #self.original_image = None
        self.cropped_image = None
                
    # Function that holds the buttons, frames and menus            
    def create_widgets(self):
        
        # Menubar
        menubar = Menu(self.root)
        
        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Undo Button
        menubar.add_command(label="Undo", command= self.undo)
        
        # Redo Button
        menubar.add_command(label="Redo", command= self.redo)
        
        self.root.config(menu=menubar)
        
        # Top panel with buttons
        self.top_panel = Frame(self.root, bg="gray97", height=40)
        self.top_panel.pack(fill="x")  # Fill horizontally
        
        property_button = Button(self.top_panel, text="Image Properties", command=self.img_property)
        property_button.pack(side="left", padx=10, pady=5)
        
        # Vertical separator
        separator = ttk.Separator(self.top_panel, orient='vertical')
        separator.pack(side="left", fill="y", padx=5, pady=5)
        
        # Separate frame for colour conversion
        conversion_menu_frame = Frame(self.top_panel, bg="gray97")  # New frame for color conversion widgets
        conversion_menu_frame.pack(side="left", padx=10, pady=5)
        
        myLabel = Label(conversion_menu_frame, text = "Color Conversions", bg="gray97")
        myLabel.pack(side="top")

        self.color_conversion_choices = [
            "RGB to GRAY", "RGB to HSV", "RGB to CIE", "RGB to HLS", "RGB to YCrCb",
            "GRAY to RGB", "GRAY to HSV", "GRAY to CIE", "GRAY to HLS", "GRAY to YCrCb"
        ]
        self.selected_conversion = StringVar(self.root)
        self.selected_conversion.set(self.color_conversion_choices[0])  # Set default choice

        conversion_menu = OptionMenu(conversion_menu_frame, self.selected_conversion, *self.color_conversion_choices)
        conversion_menu.pack(side="top", padx=10, pady=5)

        color_conversion_button = Button(conversion_menu_frame, text="Convert Color", command=self.perform_color_conversion)
        color_conversion_button.pack(side="top", padx=10, pady=5)
        
        # Vertical separator
        separator = ttk.Separator(self.top_panel, orient='vertical')
        separator.pack(side="left", fill="y", padx=5, pady=5)
        
        # Separate frame for transformation buttons
        trans_menu_frame = Frame(self.top_panel, bg = "gray97")
        trans_menu_frame.pack(side="left", padx=10, pady=5)
        
        # Image Transformations label
        myLabel = Label(trans_menu_frame, text = "Image Transformations", bg="gray97")
        myLabel.pack(side="top")
        
        crop_image_path = r"C:\DIP_MyProject\crop.png"
        crop_image = Image.open(crop_image_path)
        crop_image_resized = crop_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        crop_photo = ImageTk.PhotoImage(crop_image_resized)
        crop_button = Button(trans_menu_frame, image=crop_photo, compound="top", text="Crop", command=self.crop_image)
        crop_button.image = crop_photo 
        crop_button.pack(side="left", padx=10, pady=5)
        
        rotate_image_path = r"C:\DIP_MyProject\rotate.png"
        rotate_image = Image.open(rotate_image_path)
        rotate_image_resized = rotate_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        rotate_photo = ImageTk.PhotoImage(rotate_image_resized)
        rotate_button = Button(trans_menu_frame, image=rotate_photo, compound="top", text="Rotate", command=self.rotate_image)
        rotate_button.image = rotate_photo 
        rotate_button.pack(side="left", padx=10, pady=5)
        
        scale_image_path = r"C:\DIP_MyProject\scaling.png"
        scale_image = Image.open(scale_image_path)
        scale_image_resized = scale_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        scale_photo = ImageTk.PhotoImage(scale_image_resized)
        scale_button = Button(trans_menu_frame, image=scale_photo, compound="top", text="Scale", command=self.scale_image)
        scale_button.image = scale_photo 
        scale_button.pack(side="left", padx=10, pady=5)
        
        translate_image_path = r"C:\DIP_MyProject\translation.png"
        translate_image = Image.open(translate_image_path)
        translate_image_resized = translate_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        translate_photo = ImageTk.PhotoImage(translate_image_resized)
        translate_button = Button(trans_menu_frame, image=translate_photo, compound="top", text="Translate", command=self.translate_image)
        translate_button.image = translate_photo
        translate_button.pack(side="left", padx=10, pady=5)

        flip_image_path = r"C:\DIP_MyProject\flip_hor.webp"
        flip_image = Image.open(flip_image_path)
        flip_image_resized = flip_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        flip_photo = ImageTk.PhotoImage(flip_image_resized)
        flip_button = Menubutton(self.top_panel, image=flip_photo, compound="top", text="Flip", relief="raised")
        flip_button.image = flip_photo
        flip_button.pack(side="left", padx=5)

        flip_menu = Menu(flip_button, tearoff=0)
        flip_menu.add_command(label="Flip Vertical", command=self.flip_vertical)
        flip_menu.add_command(label="Flip Horizontal", command=self.flip_horizontal)
        flip_button.config(menu=flip_menu)
        
        # Vertical separator
        separator = ttk.Separator(self.top_panel, orient='vertical')
        separator.pack(side="left", fill="y", padx=5, pady=5)
        
        # Separate frame for draw buttons
        tools_menu_frame = Frame(self.top_panel, bg = "gray97")
        tools_menu_frame.pack(side="left", padx=10, pady=5)
        
        # Draw label
        myLabel = Label(tools_menu_frame, text = "Tools", bg="gray97")
        myLabel.pack(side="top")
        
        # Draw Button
        draw_path = r"C:\DIP_MyProject\draw3.png"
        draw_image = Image.open(draw_path)
        draw_image_resized = draw_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        draw_photo = ImageTk.PhotoImage(draw_image_resized)
        self.draw_button = Button(tools_menu_frame, image= draw_photo, compound="top", text="Draw", command=self.toggle_draw_tool)
        self.draw_button.image = draw_photo
        self.draw_button.pack(side="left", padx=10, pady=5)
        
        
        # Draw circle
        circle_path = r"C:\DIP_MyProject\circle.png"
        circle_image = Image.open(circle_path)
        circle_image_resized = circle_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        circle_photo = ImageTk.PhotoImage(circle_image_resized)
        self.circle_button = Button(tools_menu_frame, image = circle_photo, compound="top", text="Circle", command=self.toggle_circle_tool)
        self.circle_button.image = circle_photo
        self.circle_button.pack(side="right", padx=10, pady=5)
        
        # Text 
        text_path = r"C:\DIP_MyProject\text.png"
        text_image = Image.open(text_path)
        text_image_resized = text_image.resize((30, 30), Image.BILINEAR)  # Adjust the size as needed
        text_photo = ImageTk.PhotoImage(text_image_resized)
        self.text_button = Button(tools_menu_frame, image = text_photo, compound="top", text="Text", command=self.create_text_on_canvas)
        self.text_button.image = text_photo
        self.text_button.pack(side="right", padx=10, pady=5)
        
        # Vertical separator
        separator = ttk.Separator(self.top_panel, orient='vertical')
        separator.pack(side="left", fill="y", padx=5, pady=5)
        
        # Separate frame for color buttons
        color_menu_frame = Frame(self.top_panel, bg = "gray97")
        color_menu_frame.pack(side="left", padx=10, pady=5)
        
        # Draw label
        myLabel = Label(color_menu_frame, text = "Colors", bg="gray97")
        myLabel.pack(side="top")
        
        self.color_pick_button = Button(color_menu_frame, text="Color", command=self.pick_color)
        self.color_pick_button.pack(side="left", padx=10, pady=5)
    
    # Function for opening and loading image onto our canvas    
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.display_image = ImageTk.PhotoImage(self.image.resize((300, 300)))
                self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
                
                # Update image history when opening a new image
                self.update_image_history() 
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

    # Function for saving image into our directory
    def save_image(self):
        if self.image:
            try:
                save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                          filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
                if save_path:
                    self.image.save(save_path)
                    messagebox.showinfo("Success", "Image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")
     
    # Function for cropping image       
    def crop_image(self):
        if self.image is not None:
            try:
                clone = np.array(self.image)  # Convert PIL image to OpenCV format

                # Show a window to select the region of interest (ROI)
                roi = cv2.selectROI("Select Region of Interest", clone, fromCenter=False, showCrosshair=True)
                cv2.destroyAllWindows()

                if all(roi):  # Check if a valid ROI was selected
                    # Ensure the selection is within the image bounds
                    roi = (max(0, roi[0]), max(0, roi[1]), min(roi[2], clone.shape[1] - roi[0]), min(roi[3], clone.shape[0] - roi[1]))

                    # Crop the image using the selected region
                    cropped_img = clone[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

                    # Convert the cropped OpenCV image back to PIL format
                    self.image = Image.fromarray(cropped_img)
                    
                    self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
                    self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)

                    # Display the cropped image on the canvas
                    #self.display_image_on_canvas(self.image)

                    # Update image history after cropping
                    self.update_image_history()

                    messagebox.showinfo("Crop", "Image cropped successfully.")
                else:
                    messagebox.showwarning("Warning", "No region selected.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to crop image: {e}")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")

    # Function for rotating image
    def rotate_image(self):
         if self.image:
            try:
                # Convert PIL Image to OpenCV format (numpy array)
                img_cv = np.array(self.image)

                # Perform image rotation using OpenCV (cv2)
                # Rotate the image by 90 degrees clockwise
                rotated_img = cv2.rotate(img_cv, cv2.ROTATE_90_CLOCKWISE)

                # Convert the resulting OpenCV image back to PIL format
                self.image = Image.fromarray(rotated_img)

                # Update displayed image
                self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
                self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)

                messagebox.showinfo("Success", "Image rotated successfully.")
                
                # Update image history when opening a new image
                self.update_image_history()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rotate image: {e}")
         else:
            messagebox.showwarning("Warning", "No image opened yet.")
     
    # Function for scaling image       
    def scale_image(self):
        if self.image:
            try:
                # Get user input for scaling factor
                scale_factor = simpledialog.askfloat("Scale Image", "Enter the scaling factor (e.g., 0.5 for half, 2 for double):")
                if scale_factor:
                    # Perform image scaling using PIL's resize method
                    new_width = int(self.image.width * scale_factor)
                    new_height = int(self.image.height * scale_factor)
                    scaled_image = self.image.resize((new_width, new_height))

                    # Update displayed image
                    self.image = scaled_image
                    self.display_image = ImageTk.PhotoImage(self.image)
                    self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)

                    # Update image history after scaling
                    self.update_image_history()

                    messagebox.showinfo("Success", "Image scaled successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to scale image: {e}")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")
    
    # Function for translating image        
    def translate_image(self):
        if self.image:
            try:
                # Get user input for translation distances in x and y directions
                input_text = "Enter translation distances in X and Y directions (separated by comma):"
                input_text += "\nFor example, '20,30' for X=20 and Y=30"
                translate_values = simpledialog.askstring("Translate", input_text)

                if translate_values:
                    translate_x, translate_y = map(int, translate_values.split(','))

                    # Perform translation using PIL's `Image` class method `transform`
                    self.image = self.image.transform(
                        self.image.size, Image.AFFINE, (1, 0, translate_x, 0, 1, translate_y)
                    )

                    # Update displayed image
                    self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
                    self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)

                    # Update image history after translation
                    self.update_image_history()

                    messagebox.showinfo("Translate", "Image translated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to translate image: {e}")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")
     
    # Function for flipping image horizontally       
    def flip_horizontal(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
            self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
            self.update_image_history()
            messagebox.showinfo("Flip", "Image flipped horizontally.")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")

    # Function for flipping image vertically
    def flip_vertical(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
            self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
            self.update_image_history()
            messagebox.showinfo("Flip", "Image flipped vertically.")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")

    # Function for image color conversions
    def perform_color_conversion(self):
        if self.image:
            try:
                conversion_choice = self.selected_conversion.get()
                img_cv = np.array(self.image)

                if "RGB to " in conversion_choice:
                    target_color_space = conversion_choice.split("RGB to ")[1]
                    target_code = getattr(cv2, f"COLOR_RGB2{target_color_space}")
                    converted_img = cv2.cvtColor(img_cv, target_code)
                elif "GRAY to " in conversion_choice:
                    target_color_space = conversion_choice.split("GRAY to ")[1]
                    target_code = getattr(cv2, f"COLOR_GRAY2{target_color_space}")
                    converted_img = cv2.cvtColor(img_cv, target_code)
                else:
                    messagebox.showerror("Error", "Invalid conversion choice.")
                    return
                
                self.image = Image.fromarray(converted_img)
                self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
                self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)

                messagebox.showinfo("Success", "Color conversion completed.")
                
                # Update image history when opening a new image
                self.update_image_history()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert color: {e}")
                
        else:
            messagebox.showwarning("Warning", "No image opened yet.")    
    
    # Functions for undo and redo function
    def update_image_history(self):
        print(f"Before update - Current index: {self.current_index}")
        print(f"Before update - History length: {len(self.image_history)}")

        if len(self.image_history) >= 10:
            self.image_history.pop(0)  # Limiting history to 10 steps

        # Store a copy of the current image in the history list
        self.image_history.append(self.image.copy())
        self.current_index = len(self.image_history) - 1  # Update the current index

        print(f"After update - Current index: {self.current_index}")
        print(f"After update - History length: {len(self.image_history)}")
    
    # Function for reverting actions    
    def undo(self):
        print("Undo method triggered")
        if self.current_index > 0:
            print("Undo triggered")
            self.current_index -= 1
            self.image = self.image_history[self.current_index]
            self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
            self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
            print(f"Current index after undo: {self.current_index}")
        else:
            print("No action to undo")

    # Function for redos
    def redo(self):
        print("Redo method triggered")
        if self.current_index < len(self.image_history) - 1:
            print("Redo triggered")
            self.current_index += 1
            self.image = self.image_history[self.current_index]
            self.display_image = ImageTk.PhotoImage(self.image.resize((500, 500)))
            self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
            print(f"Current index after redo: {self.current_index}")
        else:
            print("No action to redo")
 
    # Functions for draw and circle   
    def start_draw(self, event):
        if self.tool == "draw":
            self.run = True
            self.prev_x = event.x
            self.prev_y = event.y
            self.canvas.bind("<B1-Motion>", self.draw)
            self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def draw(self, event):
        if self.run and self.tool == "draw":
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.root.color_fg, width=2)
                self.prev_x = event.x
                self.prev_y = event.y

    def end_draw(self, event):
        if self.tool == "draw":
            self.run = False
            self.prev_x = None
            self.prev_y = None
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
    
    def toggle_draw_tool(self):
        if self.tool == "draw":
            self.tool = None
            self.draw_button.config(relief="raised")
            self.canvas.unbind("<Button-1>")  # Unbind the event when another tool is selected
        else:
            self.tool = "draw"
            self.circle_button.config(relief="raised")  # Unset the circle tool if draw tool is selected
            self.text_button.config(relief="raised")  # Unset the text tool if draw tool is selected
            self.draw_button.config(relief="sunken")
            self.canvas.bind("<Button-1>", self.start_draw)  # Bind to the draw tool function
    
    def draw_circle(self, event):
        # Draw circle upon clicking the mouse button
        if self.tool == "circle":
            x, y = event.x, event.y
            self.canvas.create_oval(x - 40, y - 40, x + 5, y + 5, outline='pink', width=2)

    def toggle_circle_tool(self):
        if self.tool == "circle":
            self.tool = None
            self.circle_button.config(relief="raised")
            self.canvas.unbind("<Button-1>")  # Unbind the event when another tool is selected
        else:
            self.tool = "circle"
            self.draw_button.config(relief="raised")  # Unset the draw tool if circle tool is selected
            self.text_button.config(relief="raised")  # Unset the text tool if circle tool is selected
            self.circle_button.config(relief="sunken")
            self.canvas.bind("<Button-1>", self.draw_circle)
    
    def on_click(self, event):
        
        if self.tool == "draw":
            self.start_draw(event)
        elif self.tool == "circle":
            self.draw_circle(event)
        else:
            self.change_pixel_color(event)

    def on_drag(self, event):
        if self.tool == "draw":
            self.draw(event)

    def on_release(self, event):
        if self.tool == "draw":
            self.end_draw(event)       
      
    def on_canvas_click(self, event):
        if self.tool == "draw":
            self.on_click(event)
        elif self.tool == "circle":
            self.draw_circle(event)
        else:
            pass  # Add any other handling or functionality for different tools
      
    # Functions for displaying image properties
    def img_property(self):
        
        if self.image:
            file_name = "Unknown"
            image_size = self.image.size if self.image.size else "Unknown"
            image_resolution = self.image.info.get("dpi") if self.image.info.get("dpi") else "Unknown"
            image_type = self.image.format if self.image.format else "Unknown"

            messagebox.showinfo("Image Properties", f"File name: {file_name}\nImage size: {image_size}\nImage resolution: {image_resolution}\nImage type: {image_type}")
        else:
            messagebox.showwarning("Warning", "No image opened yet.")
    
    # Functions for creating text on canvas  
    def create_text_on_canvas(self):
        self.text_tool_active = True
        self.canvas.bind("<Button-1>", self.handle_text)
        
    def handle_text(self, event):
        text = simpledialog.askstring("Text Input", "Enter text:")  # Show a dialog box to get user input
        if text:
            x, y = event.x, event.y
            self.canvas.create_text(x, y, text=text, fill=self.root.color_fg, font=("Arial", 12), anchor="nw")

    def toggle_text_tool(self):
        if self.text_tool_active:
            self.text_tool_active = False
            self.canvas.unbind("<Button-1>")  # Unbind the event
            self.text_button.config(relief="raised")
        else:
            self.text_tool_active = True
            self.canvas.bind("<Button-1>", self.handle_text)
            self.text_button.config(relief="sunken")
    
    # Function for changing drawing pen and text color
    def pick_color(self):
        color = colorchooser.askcolor(title="Choose color")
        if color:
            self.root.color_fg = color[1]            

        
def main():
    root = Tk()
    app = MyImageEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()