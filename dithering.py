"""""
GMU Dithering generator with tkinter in Python



"""""



import tkinter as tk
from tkinter import Entry, messagebox
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import threading
import random

class DitheringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Dithering")
        self.root.geometry("1400x900")
        self.root.configure(bg='white')
        self.root.resizable(False, False)
        self.root.attributes("-topmost", -1)

        #important variables that will be used.
        self.original_image = None
        self.displayed_image = None
        self.image_in_gray = None
        self.dithered_imagePIL = None

        self.method_by_user = tk.StringVar(value = "Red Channel") # red for default, so it will be converted automatically after uploading the image.
        self.algo_selected = tk.StringVar(value="Threshold")
        self.threshold_default_value = tk.DoubleVar(value=128)
        self.frame = tk.Frame(self.root, bg="bisque", width="1300", height="1000")
        self.frame.pack(padx=50, pady=30)
        self.frame.pack_propagate(False)

        self.selecting_image = Entry(self.frame, bg="white", borderwidth=1, width=40)
        #self.selecting_image.insert(0, " Write here your file path or press select")
        self.selecting_image.place(x=450, y=50)
        #self.selecting_image.bind("<FocusIn>", self.default_text)

        self.opening_button = tk.Button(self.frame, text="Open File", command=self.open_file, bg="blue")
        self.opening_button.place(x=800, y=43)



        #Options for algorithms (random and Threshold)
        self.label_algorithm = tk.Label(self.frame, text="Select the Dithering Algorithm:", borderwidth=3, relief="raised", bg="bisque", background="white", font=("Helvetica", 12))
        self.label_algorithm.place(x=350, y=700)

        self.algo_selection = tk.OptionMenu(self.frame, self.algo_selected, "Random", "Threshold")
        self.algo_selection.place(x=400, y=740)

        #Parameter for the threshold
        self.threshold_parameter = tk.Label(self.frame, text="Set Threshold Value:", bg="white", font=("Helvetica", 12), borderwidth=3, relief="raised")
        self.threshold_parameter.place(x=610, y=700)
        self.threshold_value = tk.Entry(self.frame, textvariable=self.threshold_default_value, width=10, font=("Arial", 12))
        self.threshold_value.place(x=660, y=740)


        self.generate = tk.Button(self.frame, text="Generate image",command=self.start_thread, borderwidth=3, relief="raised", bg="yellow",font=("Arial", 25), cursor="star")
        self.generate.place(x= 920, y=670)

        self.save_generated_image = tk.Button(self.frame, command=self.save_new_image, text="Save image", borderwidth=3, relief="raised", bg="yellow",font=("Arial", 25), cursor="star")
        self.save_generated_image.place(x=950, y=760)


    #canvas where we should display the image!

        self.canvas = tk.Canvas(self.frame, width=550, height=550, bg="lightblue", highlightthickness=1)
        self.canvas.place(x=50, y=100)

        self.canvas2 = tk.Canvas(self.frame, width=550, height=550, bg="lightblue", highlightthickness=1)
        self.canvas2.place(x=650, y=100)


    #Button for selecting method
        self.gray_convertor = tk.Button(self.frame, relief="raised",borderwidth=3, text="Select Grayscale Method", command=self.gray_methods, bg="white")
        self.gray_convertor.place(x=50, y=700)

        self.method_label = tk.Label(self.frame, textvariable=self.method_by_user, bg="white",font=("Helvetica", 12))
        self.method_label.place(x=85, y=750)    





    def open_file(self):
        file_path = self.selecting_image.get().strip()
        if file_path and os.path.isfile(file_path):
            self.open_file_path(file_path)
        else:
            file_path = filedialog.askopenfilename( filetypes=[
        ('All Image Files', '*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.tif;*.webp'),
        ('PNG Files', '*.png'),
        ('JPEG Files', '*.jpg;*.jpeg'),
        ('GIF Files', '*.gif'),
        ('BMP Files', '*.bmp'),
        ('TIFF Files', '*.tiff;*.tif'),
        ('WEBP Files', '*.webp')
    ], defaultextension=".png")
            if file_path:
                self.selecting_image.delete(0, "end")
                self.selecting_image.insert(0, file_path)
                self.image_load(file_path)
            else:
                messagebox.showwarning("Open File", "No file selected")

    def image_load(self, file_path):
        try:
            self.original_image = Image.open(file_path)
            self.displayed_image= ImageTk.PhotoImage(self.original_image.resize((550,550), Image.Resampling.LANCZOS))
            self.canvas.create_image(0,0, anchor=tk.NW, image= self.displayed_image)
            self.apply_gray_conversion()
        except Exception as e:
            messagebox.showerror("Error", f"We cant load image: {e}")
        
    def gray_methods(self):
        gray_conversion = ["Red Channel", "Green Channel", "Blue Channel"]
        method_by_user = tk.simpledialog.askstring("Please, select conversion Method", " Choose the grayscale conversion method (Red, Green, Blue):", initialvalue = self.method_by_user.get(), parent = self.root)
        if method_by_user in gray_conversion:
            self.method_by_user.set(method_by_user)
            self.apply_gray_conversion()
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid conversion: Red Channel, Green Channel or Blue Channel.")
    
    def apply_gray_conversion(self):
        if not self.original_image:
            return 
        method = self.method_by_user.get()
        image_in_gray = self.original_image.convert("RGB")
        if method == "Red Channel":
            channels = image_in_gray.split()
            image_in_gray = channels[0]
        elif method == "Green Channel":
            channels = image_in_gray.split()
            image_in_gray = channels[1]
        elif method == "Blue Channel":
            channels = image_in_gray.split()
            image_in_gray = channels[2]

        self.image_in_gray = ImageTk.PhotoImage(image_in_gray.resize((550, 550), Image.Resampling.LANCZOS))
        self.canvas2.create_image(0,0, anchor=tk.NW, image=self.image_in_gray)

    def start_thread(self):
        threading.Thread(target=self.dithering_application).start()

    def dithering_threshold(self, image, threshold):
        return image.point( lambda p: p> threshold and 255)
        

    def dithering_random(self, image):
        return image.point( lambda p:255 if random.random()> 0.5 else 0)
        





    def dithering_application(self):
        if not self.original_image:
            return
        
        image = self.original_image.convert("L")
        algo = self.algo_selected.get()
        threshold = self.threshold_default_value.get()

        if algo == "Threshold":
            image = self.dithering_threshold(image, threshold)
        elif algo == "Random":
            image = self.dithering_random(image)

        
        self.dithered_imagePIL = image
        self.image_dithered = ImageTk.PhotoImage(image.resize((550,550), Image.Resampling.LANCZOS))
        self.canvas2.create_image(0,0, anchor = tk.NW, image= self.image_dithered)


    def save_new_image(self):
        if self.dithered_imagePIL:
            save_path = filedialog.asksaveasfilename( filetypes=[
        ('All Image Files', '*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.tif;*.webp'),
        ('PNG Files', '*.png'),
        ('JPEG Files', '*.jpg;*.jpeg'),
        ('GIF Files', '*.gif'),
        ('BMP Files', '*.bmp'),
        ('TIFF Files', '*.tiff;*.tif'),
        ('WEBP Files', '*.webp')
    ], defaultextension=".png")
            if save_path:
                self.dithered_imagePIL.save(save_path)
            else:
                messagebox.showwarning("Save image" "No file found")
        else:
            messagebox.showwarning("Save image" "No file found")



 

    



if __name__ == "__main__":
    root = tk.Tk()
    app = DitheringApp(root)
    root.mainloop()
