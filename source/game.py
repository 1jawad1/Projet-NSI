import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd  #boite dialogue pour ouvrir un fichier
from tkinter.messagebox import showinfo
import json as js



from PIL import Image, ImageTk, ImageOps
import numpy as np

from datetime import date
import time
import Canva
 

class Game(ttk.Frame) : 
     
    def __init__(self, screen, data):
        super().__init__(screen)
        self.screen = screen

        self.data = data
        self.project_name = data["Nom du projet"]
        self.width = data["Largeur"]
        self.height = data["Hauteur"]
        self.bg = data["Fond"]

        

        self.canva = False
        self.name = "Anonyme"

        self.colors = data["Palette"]

        self.current_image = None
        self.label = ttk.Label(self, text="No image selected", style='Content.TLabel')


    def create_color_button(self, color, frame):
        button = tk.Canvas(frame, width=30, height=30, highlightthickness=0)
        button.create_oval(2, 2, 28, 28, fill=color, outline=color)
        button.bind("<Button-1>", lambda event, c=color: self.canva.select_color(c))
        button.pack(side="left", padx=5)   

    def display_game(self):

        title = ttk.Label(self, text='PIxelSolo', style="Title.TLabel")
        title.grid(column=2, row=1, columnspan=3, pady=10)

        if(self.canva): self.canva.canva.destroy()
            
        self.ecran = tk.Canvas(self)
        self.canva = Canva.Canva(self.width, self.height, 10, self.ecran, self,self.bg)
        self.canva.current_color = self.colors[0]


        share_button = ttk.Button(self, text='partager', command=self.get_project_data, style="TButton")
        share_button.grid(row=4, column=5)

        self.canva.draw()

        self.canva.canva.bind('<Motion>', self.canva.fillPixel)
        self.canva.canva.bind("<Button-1>", self.canva.fillPixel)  

        # clear_btn = tk.Button(self.screen, text="Effacer", command=self.clear_canvas)
        # clear_btn.grid(column=4, row=3)

        
        self.canva.canva.bind("<Button-3>", self.canva.fillPixel)
        self.canva.canva.grid(column=1, row=2, columnspan=4, rowspan=4, padx=25)


        color_buttons_frame = ttk.Frame(self, style="TFrame")
        color_buttons_frame.grid(column=1, row=6, columnspan=5, pady=20)

        for color in self.colors:
            self.create_color_button(color, color_buttons_frame)

        open_btn = ttk.Button(self, text="open a file", command=self.select_file, style="TButton")
        name = ttk.Label(self, text=self.name, style="Subtitle.TLabel")

        open_btn.grid(column=5, row=5, pady=10)
        name.grid(column=5, row=1)
        self.label.grid(column=5, row=2, columnspan=1, rowspan=1 , pady=10)

    



    def select_file(self):
        filetypes = (('image files', '*.png'),('All files', '*.*'))
        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    
        showinfo(title='Selected File', message=filename)
        self.editImage(filename, 50)

    def editImage(self, filename, w):
        image = Image.open(filename)

        width, height = image.size
        ratio = width / height

        image = image.resize((w, round(w/ratio)), Image.NEAREST)
        image = image.resize((200, round(200/ratio)), Image.NEAREST)
        image = image.quantize(colors=10, method=Image.Quantize.FASTOCTREE)

        self.current_image = ImageTk.PhotoImage(image)

        self.label.config(image=self.current_image)

    # ouvre la boite de dialogue pour récupérer le chemin où enregistrer l'image ou le txt

    def save(self, formats : list, factor=1):
        filename = fd.asksaveasfilename(initialfile=f"{self.name}-project{formats[0][1][1:]}", initialdir="/", title="Chemin d'enregistrement", filetypes=formats)
    
        #un peu tordu : si le chemin n'est pas vide je regarde si c'est une image ou un txt et enregistre
        if filename:
            if filename.lower().endswith(".txt"):
                with open(filename, 'w') as text:
                    text.write("#PIXEL_SOLO_MATRIX_CANVA_BACKUP \n\n")
                    text.write(str(self.canva.matrix_pixels(self.canva.Nx, self.canva.Ny)))
            else: 
                self.canva.fill_img(self.canva.matrix_pixels(self.canva.Nx, self.canva.Ny), filename, factor)

        
    # ouvre la page pour exporter le pixel art, faire une sauvegarde et à chaque fois appel la fonction pour log le json
    def download_pixel(self):

        message = tk.Toplevel()
        message.title("Options d'enregistrement")
        message.geometry('350x300')
        message.configure(bg="#2C2F33")

        def image_export():
            img_formats = [("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")]
            self.save(img_formats, factor=img_factor.get())
            message.destroy()

        def text_export():
            self.save([("text files", "*.txt")])
            message.destroy()

        export_label = tk.LabelFrame(message, text='Exporter', fg="white", bg="#2C2F33", font=("Helvetica", 12, "bold"), bd=2, relief="groove")
        export_label.grid(row=1, columnspan=3, padx=14, pady=10, sticky="ew")

        tk.Label(export_label, text="Facteur d'agrandissement :", fg="white", bg="#2C2F33", font=("Helvetica", 10)).grid(row=0, column=0, pady=5, padx=5, sticky="w")
        tk.Label(export_label, text="Taille de l'image :", fg="white", bg="#2C2F33", font=("Helvetica", 10)).grid(row=1, column=0, pady=5, padx=5, sticky="w")

        img_size_txt = tk.Label(export_label, text=f'{self.width} x {self.height} px', bg="white", fg="black", relief='ridge', width=15, font=("Helvetica", 10))
        img_size_txt.grid(row=1, column=1, pady=5, padx=5)

        img_factor = tk.IntVar(value=1)
        size_factor = tk.Spinbox(export_label, from_=1, to=100, textvariable=img_factor, wrap=True, font=("Helvetica", 10), width=5,
                                command=lambda: img_size_txt.config(text=f'{self.width * img_factor.get()} x {self.height * img_factor.get()} px'))
        size_factor.grid(row=0, column=1, pady=5, padx=5)

        export_button = tk.Button(export_label, text='Exporter', bg="#7289DA", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, command=image_export)
        export_button.grid(row=2, columnspan=2, pady=10)

        backup_label = tk.LabelFrame(message, text='Sauvegarder', fg="white", bg="#2C2F33", font=("Helvetica", 12, "bold"), bd=2, relief="groove")
        backup_label.grid(row=2, columnspan=3, padx=14, pady=10, sticky="ew")

        tk.Label(backup_label, text="Sauvegarde personnelle au format texte :", fg="white", bg="#2C2F33", font=("Helvetica", 10)).grid(row=0, column=0, pady=5, padx=5, sticky="w")

        backup_button = tk.Button(backup_label, text="Sauvegarder", bg="#7289DA", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, command=text_export)
        backup_button.grid(row=1, column=1, pady=10, padx=5)


        message.mainloop()


    def get_project_data(self, message = False):
        self.share_page = tk.Toplevel()
        self.share_page.configure(bg="#2C2F33")

        frame = tk.Frame(self.share_page, bg="#2C2F33")
        frame.pack(pady=20, padx=40)

        title = tk.Label(frame, text="Share your project !", fg="white", bg="#2C2F33", font=("Helvetica", 16, "bold"))
        title.pack(pady=(0, 10))

        if message:
            error = tk.Label(frame, text=message, fg='red', bg="#2C2F33", font=("Helvetica", 12))
            error.pack(pady=(0, 10))

        description_label = tk.Label(frame, text="A description of your project:", fg="white", bg="#2C2F33", font=("Helvetica", 12))
        description_label.pack(anchor="w", pady=(5, 0))

        project_description = tk.Entry(frame, width=30, bg="#3C3F43", fg="white", insertbackground="white", font=("Helvetica", 12), relief="flat", bd=5)
        project_description.pack(pady=(0, 10))

        tags_label = tk.Label(frame, text="Some tags (separate each tag with a space):", fg="white", bg="#2C2F33", font=("Helvetica", 12))
        tags_label.pack(anchor="w", pady=(5, 0))

        project_tags = tk.Entry(frame, width=30, bg="#3C3F43", fg="white", insertbackground="white", font=("Helvetica", 12), relief="flat", bd=5)
        project_tags.pack(pady=(0, 15))

        sub_button = tk.Button(frame, text='Share!', bg="#7289DA", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, command=lambda: self.user_log({"description": project_description.get(), "tags": project_tags.get()}))
        sub_button.pack(pady=10)


        
    def user_log(self, data):

        self.share_page.destroy()
        
        if( not (  data['description'] and data["tags"] ) ):
            self.get_project_data('please enter the required data !')
            return

        user_data = data
        user_data['name'] = self.project_name
        user_data["author"] = self.name
        user_data["width"] = self.canva.Nx
        user_data["height"] = self.canva.Ny
        user_data["date_created"] = date.today().isoformat()
        user_data["like"] = 0
        user_data["dislike"] = 0
        user_data["palette"] = self.colors
        user_data["matrice"] = self.canva.matrix_pixels(self.canva.Nx, self.canva.Ny)
        
        with open(f"./data/{data['name']}.json", 'w', encoding='utf8') as file_data:
            js.dump(user_data, file_data, indent=4)

    def start_game(self):
        self.display_game()

all_project = {}
current_project =None

def game_systeme(screen, controler):

    global all_project, current_project

    game_page = ttk.Frame(screen, style="TFrame")

    
    PALETTES = {
            "Classique": ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"],
            "Pastel": ["#FFB6C1", "#FFD700", "#87CEEB", "#98FB98", "#DDA0DD", "#FFDEAD"],
            "Sombre": ["#8B0000", "#006400", "#00008B", "#808000", "#4B0082", "#2F4F4F"],
            "Nature": ["#137C8B", "#709CA7", "#B8CBD0", "#7A90A4", "#344D59"],
            "Pastel cold": ["#B0A1BA", "#A5B5BF", "#ABC8C7", "#B8E2C8", "#BFF0D4"],
            "Vintage": ["#F2EFE7", "#FFDAB3", "#C8AAAA", "#9F8383", "#574964", "#54473F"],
            "Vert": ["#D2D79F", "#90B77D", "#1B9C85", "#739072", "#304D30", "#12372A"],
            "Violet": ["#F5EFFF", "#DAD2FF", "#B2A5FF", "#B771E5", "#493D9E"],
            "Noël (Héloïse)": ["#6B240C", "#640D6B", "#727D73","#FF0000","#FFC100","#FBFBFB"],
            "Golden Hour": ["#FFD369", "#FFB200", "#FF9900", "#EB5B00", "#C70039", "#B70404"],
            "Winter": [ "#3E5879", "#D8C4B6", "#F5EFE7","#DFF5FF", "#608BC1", "#133E87"],
            "Bleu": ["#A7E6FF", "#3ABEF9", "#7EA1FF", "#3572EF", "#0E46A3", "#0B2F9F"]
    }
    
    BG={
    "Blanc":'#ffffff',
    "Noir":'#000000'
    }
    
    draw_areas = ttk.Notebook(game_page, style="TNotebook")
    get_data_frame = ttk.Frame(game_page, style="TFrame")

    draw_areas.bind("<<NotebookTabChanged>>", lambda x:on_tab_change(x, draw_areas, controler, get_data_frame))

    error = ttk.Label(get_data_frame, text='Please enter the required data !!', foreground = "red", style="TLabel")

    # Nom du projet
    ttk.Label(get_data_frame, text="Nom du Projet:", style="Content.TLabel").grid(row=0, column=0, padx=10, pady=(100, 0), sticky="e")
    project_name = ttk.Entry(get_data_frame, style="TEntry")
    project_name.grid(row=0, column=1, padx=10, pady=(100, 0), sticky="we")

    # Dimensions du canevas
# Variables pour largeur et hauteur
    width_var = tk.IntVar(value=10)
    height_var = tk.IntVar(value=10)

    def update_width(val):
        width_var.set(int(float(val)))
    
    def update_height(val):
        height_var.set(int(float(val)))
    
    ttk.Label(get_data_frame, text="Largeur (px):", style="Content.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    width_scale = ttk.Scale(get_data_frame, from_=5, to=60, variable=width_var, orient="horizontal", command=update_width, style="TScale")
    width_scale.grid(row=1, column=2, padx=10, pady=5, sticky="w")
    width_spinbox = ttk.Spinbox(get_data_frame, from_=5, to=60, textvariable=width_var, command=lambda: width_scale.set(width_var.get()), style="TSpinbox")
    width_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="we")

    ttk.Label(get_data_frame, text="Hauteur (px):", style="Content.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    height_scale = ttk.Scale(get_data_frame, from_=5, to=40, variable=height_var, orient="horizontal", command=update_height, style="TScale")
    height_scale.grid(row=2, column=2, padx=10, pady=5, sticky="w")
    height_spinbox = ttk.Spinbox(get_data_frame, from_=5, to=40, textvariable=height_var, command=lambda: height_scale.set(height_var.get()), style="TSpinbox")
    height_spinbox.grid(row=2, column=1, padx=10, pady=5, sticky="we")


    # Palette de couleurs
    ttk.Label(get_data_frame, text="Palette de couleurs:", style="Content.TLabel").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    palettes = [i for i in PALETTES.keys()]
    palette_select = ttk.Combobox(get_data_frame, values=palettes, state="readonly")
    palette_select.grid(row=3, column=1, padx=10, pady=5, sticky="we")


    # Fond du canevas
    ttk.Label(get_data_frame, text="Fond du canevas:", style="Content.TLabel").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    backgrounds = ["Blanc", "Noir"]
    bg_select = ttk.Combobox(get_data_frame, values=backgrounds, state="readonly")
    bg_select.grid(row=5, column=1, padx=10, pady=5, sticky="we")

    def reset_fields():
        project_name.delete(0, tk.END)
        width_var.set(32)
        height_var.set(32)
        palette_select.set("")
        bg_select.set("")
        draw_areas.tkraise()

    def create_project():
        global current_project, get_data_frame
        error.grid_forget()

        data = {
            "Nom du projet" : project_name.get(),
            "Largeur" : width_var.get(),
            "Hauteur" : height_var.get(),
            "Palette" : palette_select.get(),
            "Fond" : BG[bg_select.get()]
        }

        if not (data["Nom du projet"] and data["Largeur"] and data["Hauteur"] and data["Palette"] and data["Fond"]):
            error.grid(row=8, column=0, columnspan=2)
            return
        
        data["Palette"] = PALETTES[data["Palette"]]
        all_project[data["Nom du projet"]] = Game(draw_areas, data)
        draw_areas.add(all_project[data["Nom du projet"]], text = data["Nom du projet"])
        all_project[data["Nom du projet"]].start_game()
        reset_fields()
    
        
        

    # Boutons
    btn_create = ttk.Button(get_data_frame, text="Créer Projet", command=create_project, style="TButton")
    btn_create.grid(row=6, column=0, columnspan=3, pady=10)

    btn_cancel = ttk.Button(get_data_frame, text="Annuler", command=reset_fields, style="TButton")
    btn_cancel.grid(row=7, column=0, columnspan=3, pady=5)


    draw_areas.grid(row=0, column=0, sticky='nsew')
    get_data_frame.grid(row=0, column=0, sticky='nsew')

    game_page.grid_columnconfigure(0, weight=1)  
    game_page.grid_rowconfigure(0, weight=1)

    get_data_frame.grid_columnconfigure((0,1,2), weight=1)

    return game_page

def on_tab_change(event,notebook,controler, get_data_frame):
    global current_project
    selected_tab = notebook.select()  # Récupère l'ID de l'onglet sélectionné
    if selected_tab:  # Vérifie qu'il y a bien une tab sélectionnée
        selected_widget = notebook.nametowidget(selected_tab)  # Récupère le widget correspondant à la tab sélectionnée
        for name, frame in all_project.items():
            if frame == selected_widget:
                current_project = name
                controler.draw_menu()
                controler.bind("<Shift_L>", lambda e: all_project[current_project].canva.changeClickStatus()) 
                controler.file_menu.entryconfigure("Nouveau Projet", command=get_data_frame.tkraise)
                break

    else:
        current_project = None