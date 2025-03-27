
class Post:
    
    def __init__(self, data, tk, json,  path, image, show_detail):

        self.data = data

        self.name = data['name']
        self.author = data['author']
        self.date_created = data["date_created"]

        self.path = path
        
        # self.matrice  = data['matrice']
        self.image =  image
        self.apreciation = {
            "like": data['like'],
            "dislike": data["dislike"]
            }

        self.tk = tk
        self.json = json

        self.show_detail = show_detail

        self.liked = False
        self.disliked = False


    def draw_cell(self, frame):


        img = self.tk.Label(frame, image = self.image)

        title = self.tk.Label(frame, text=self.name)
        author = self.tk.Label(frame, text=f"made by {self.author}")
        date = self.tk.Label(frame, text=f"made the : {self.date_created}")

        likes = self.tk.LabelFrame(frame)
        self.like = self.tk.Button(likes, text = f"like : {self.apreciation['like']}", command = lambda : self.give_apreciation(True))
        self.dislike = self.tk.Button(likes, text = f"dislike : {self.apreciation['dislike']}", command = lambda : self.give_apreciation(False))
        self.like.grid(row=1, column = 1)
        self.dislike.grid(row=1, column = 2)
        
        detail = self.tk.Button(frame, text = 'see more', command = self.show_detail)


        img.grid(row=1, column=1, rowspan=4, pady= 2)
        title.grid(row=1, column=2, pady = 5)
        author.grid(row=2, column=2, pady = 5)
        date.grid(row=3, column=2, pady = 5)
        likes.grid(row=5, column=1, pady = 5)
        detail.grid(row = 5, column = 2, pady = 5)


    def give_apreciation(self, mode):
        update = self.data

        if mode and not self.liked: 

            update["like"] +=1
            self.like.config(text=f"like : {self.data['like']}")
            self.liked = True

            if self.disliked:
                self.disliked = False
                update["dislike"]-=1
                self.dislike.config(text=f"dislike : {self.data['dislike']}")

        elif not mode and not self.disliked :

            update["dislike"]+=1
            self.dislike.config(text=f"dislike : {self.data['dislike']}")
            self.disliked = True

            if self.liked:
                self.liked = False
                update["like"] -=1
                self.like.config(text=f"like : {self.data['like']}")                

        with open(self.path, "w") as f:
            self.json.dump(update, f, indent = 4)

    
            

    