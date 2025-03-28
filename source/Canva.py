from numpy import array, uint8
from PIL import Image
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from ast import literal_eval

class Canva:
    
    def __init__(self, Nx, Ny, pixel_size, canva, screen,bg):
        self.Nx = Nx
        self.Ny = Ny
        self.screen = screen
        self.pixel_size = pixel_size
        self.bg=bg
        self.canva_X = self.Nx * self.pixel_size + self.Nx-1
        self.canva_Y = self.Ny * self.pixel_size + self.Ny-1
        self.canva = canva
        self.canva.config( width = self.canva_X , height = self.canva_Y, bg=self.bg, highlightbackground='grey', highlightcolor='grey' )
        self.current_color = '#000000'
        self.clicked = False

    def draw(self):

        n_x = 1
        n_y = 1

        for i in range(self.pixel_size, self.canva_X-self.Nx+1, self.pixel_size):
            self.canva.create_line(i+n_x, 0, i+n_x, self.canva_Y+1 , fill='#eeeeee', width = 1)
            n_x+=1
    
        for i in range(self.pixel_size, self.canva_Y-self.Ny+1, self.pixel_size):
                self.canva.create_line(0, i+n_y, self.canva_X+1,  i+n_y, fill='#eeeeee', width = 1)
                n_y+=1
    
    def getPixelCoords(self, x, y):

        x_ = (x//(self.pixel_size+1))*(self.pixel_size+1) 
        coords_x = (x_, x_+self.pixel_size) 

        y_ = (y//(self.pixel_size+1))*(self.pixel_size+1) 
        coords_y = (y_, y_+self.pixel_size) 

        return (coords_x, coords_y)
    

    def fillPixel(self, e, num = None):
        coords_x, coords_y  = self.getPixelCoords(e.x, e.y)

        pixel_coords = (coords_x[0]+1, coords_y[0]+1, coords_x[1]+1, coords_y[1]+1)
        pixel_tag = f"{coords_x[0]}-{coords_y[0]}"
        # print(e)

        match e.type:

            case '6':
                if not self.canva.find_withtag('hover'):
                    self.canva.create_rectangle(*pixel_coords, fill='#e0e0e0', tags='hover', width=0)
                    self.canva.tag_bind('hover', '<Leave>', lambda e: self.canva.delete('hover'))
                # print('hover')

            case e.type if e.type == '4' or self.clicked:

                # print(pixel_tag, self.canva.find_withtag(pixel_tag))

                if e.num == 1 or num == 1:
                    if self.canva.find_withtag(pixel_tag):
                        self.canva.delete(pixel_tag)

                    self.canva.create_rectangle( *pixel_coords, fill=self.current_color, tags=(self.current_color, pixel_tag, "pixel"), width=0)

                    if self.clicked :
                        self.canva.tag_bind(pixel_tag, '<Leave>', lambda e: self.fillPixel(e, 1))
                    

                elif ( e.num == 3 or num ==3 ) and self.canva.find_withtag(pixel_tag):
                    self.canva.delete(pixel_tag)
    
    def clear_canva(self):
        self.canva.delete()

    # pour former la matrice avec les couleurs RGB des pixels du canva
    def matrix_pixels(self, width : int, height : int):

        matrix = []
        for j in range(height):
            matrix.append([])
            for i in range(width):
                pix_tag = f'{10 * i + i}-{10 * j + j}'
                pixel_id = self.canva.find_withtag(pix_tag)

                if pixel_id:
                    hex_color = self.canva.itemcget(pixel_id, "fill")
                    rgb_color = [int(hex_color[k:k+2], 16) for k in [1, 3, 5]] 
                else:
                    rgb_color = [int(self.bg[k:k+2], 16) for k in [1, 3, 5]] 

                matrix[j].append(rgb_color)
        return matrix
                    
    def changeClickStatus(self):
        if self.clicked : 
            self.clicked = False
        else : 
            self.clicked = True


    def select_color(self, color):
        self.current_color = color

        # crée un fichier image à partir de la matrice de pixels
    def fill_img(self, pixels: list, path : str, factor : int):
        pixels = array(pixels, dtype=uint8)
        img = Image.fromarray(pixels, "RGB")
        img = img.resize((img.width*factor, img.height*factor), resample=0)
        img.save(path)

        # je parcours la matrice et à chaque fois je convertit en hexadecimal puis si c'est blanc je met pas de rectangle sinon j'appelle getPixelCoords() et je crée le rectangle
    def matrix_to_Canva(self, matrix, width : int, height : int):
        for j in range(height):
            for i in range(width):
                color = "#{:02x}{:02x}{:02x}".format(matrix[j,i][0], matrix[j,i][1], matrix[j,i][2])

                if color != "#ffffff":
                    coords_x, coords_y  = self.getPixelCoords(10*i+i, 10*j+j)

                    pixel_coords = (coords_x[0]+1, coords_y[0]+1, coords_x[1]+1, coords_y[1]+1)
                    pixel_tag = (f"{coords_x[0]}-{coords_y[0]}", color)
                    self.canva.create_rectangle(*pixel_coords, fill=color, tags=pixel_tag, width=0)

    # j'ouvre une boite de dialogue , j'ouvre le fichier txt je vérifie qu'il contient la bonne première phrase et j'envoit la matrice à l'autre fonction
    def canva_setup(self):
        file_path = askopenfilename(filetypes=(('Text Files', '*.txt'),), initialdir='/Documents')
        with open(file_path, 'r') as text_file:
            first_line = text_file.readline().strip()
            if first_line != '#PIXEL_SOLO_MATRIX_CANVA_BACKUP':
                showerror(title='Erreur', message='Le fichier sélectionner est incompatible.')
            else:
                text_file.readline()
                matrix = array(literal_eval(text_file.readline()), dtype=uint8)
                self.matrix_to_Canva(matrix, len(matrix[0]), len(matrix))

    def clear_canvas(self):
        if self.canva:
            self.canva.delete("pixel")



