import tkinter as tk            #Imported all necessary libraries
from reportlab.pdfgen import canvas
from PIL import Image
from tkinter import filedialog, messagebox
import os

class ImageToPdfConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []       #save images in this path
        self.output_pdf_name = tk.StringVar()       #store pdf name
        self.selected_image_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)      #list all pdf names

        self.initialize_ui()    #initialize the UI

    def initialize_ui(self):
        title_label = tk.Label(self.root, text = "Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text = "Select Images", command= self.select_images)
        select_images_button.pack(pady=(0, 10))

        self.selected_image_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40,   justify="center")
        pdf_name_entry.pack()   #so the user can make an entry

        convert = tk.Button(self.root, text = "Convert To PDF", command= self.convert_images_to_pdf)
        convert.pack(pady=(20, 40))         #This converts images in list to PDF

        #To make the program function by initializing the commands

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Images", "*.png, *.jpg, *.jpeg")])       #Opens up file directory
        self.update_selected_images_listbox()   #Image names update onto list

    def update_selected_images_listbox(self):
        self.selected_image_listbox.delete(0, tk.END)   #Any prev names will be deleted

        for image_path in self.image_paths:
            _, image_path = os.path.split(image_path)   #splitting so image path is not included on list
            self.selected_image_listbox(tk.END, image_path)     #new image names will update

    def convert_images_to_pdf(self):        #Command
        if not self.image_paths:        #If user provides a name for the pdf
            return
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"       #default name if name is not provided

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))   #Create the PDF

        for image_path in self.image_paths:     #to insert images sequentially
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width/img.width , available_height/img.height) 
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor      #resizing image in case it does not fit
            x_centered = (612 - new_width)/2
            y_cenetered = (792 - new_height)/2          #centering the images

            pdf.setFillColor(255, 255, 255)     #Document page colour
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_cenetered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

def main():
    root = tk.Tk()
    converter = ImageToPdfConverter(root)
    root.title("Image to PDF")
    root.geometry("400x600")
    root.mainloop()

    if __name__== "__main__":
        main()