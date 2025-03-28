import tkinter
class Detail_page:

    def __init__(self, tk, data, img, root):
        self.tk = tk
        self.root = root
        self.data = data

        self.name = data['name']
        self.author = data['author']
        self.date_created = data["date_created"]
        
        self.image =  img

        self.img_size = [data['width'], data['height']]
        self.apreciation = {
            "like": data['like'],
            "dislike": data["dislike"]
            }
        self.tags = data['tags']
        self.description = data['description']
        self.palette = data['palette']

        self.opened = False



    def show_details(self):
        if not self.opened : 
            self.opened = True

            self.details_page = tkinter.Toplevel(self.root)
            self.details_page.transient(self.root)  
            self.details_page.protocol("WM_DELETE_WINDOW", self.on_closing)

            self.details_page.geometry(f"600x300+{self.root.winfo_x()+self.root.winfo_width()//2-300}+{self.root.winfo_y()+self.root.winfo_height()//2-150}")


            for i in range(3):
                self.details_page.grid_columnconfigure(i, weight=1)  
            for i in range(9):
                self.details_page.grid_rowconfigure(i, weight=1) 

            img = self.tk.Label(self.details_page, image=self.image)
            img.image = self.image  

            title = self.tk.Label(self.details_page, text=self.name)
            author = self.tk.Label(self.details_page, text=f"made by {self.author}")
            date = self.tk.Label(self.details_page, text=f"made the : {self.date_created}")
            likes = self.tk.Label(self.details_page, text=f"likes : {self.apreciation['like']} | dislikes : {self.apreciation['dislike']}")
            size = self.tk.Label(self.details_page, text=f"{self.img_size[0]} * {self.img_size[1]}")
            description = self.tk.Label(self.details_page, text=f"description : {self.description}")

            tags = self.tk.Frame(self.details_page)
            tn = self.tk.Label(tags, text = 'tags : ')
            tn.pack(side = 'left')

            for i in self.tags:
                t = self.tk.Label(tags, text=i)
                t.pack(side="left")


            color_frame = self.tk.Frame(self.details_page)

            for i in self.palette:
                button = tkinter.Canvas(color_frame, width=15, height=15, bg=self.details_page.cget("bg"), highlightthickness=0)
                button.create_oval(1, 1, 14, 14, fill=i, outline=i)
                button.pack(side="left", padx=5)

            img.grid(column=1, row=2, rowspan=4, pady=5, sticky="n")
            title.grid(column=1, row=1, sticky='e')
            author.grid(column=2, row=2, pady=5, sticky = 'w')
            date.grid(column=2, row=3, pady=5, sticky = 'w')
            likes.grid(column=2, row=4, pady=5, sticky = 'w')
            description.grid(column=2, row=5,  pady=5, sticky = 'w')
            tags.grid(column=2, row=6, pady=5, sticky = 'w')
            size.grid(column=1, row=5)
            color_frame.grid(column=1, row=6, padx=5, pady=5)
    
    def on_closing(self):
        self.opened = False
        self.details_page.destroy()