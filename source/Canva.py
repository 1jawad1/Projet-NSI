from numpy import array, uint8, sqrt
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
        self.click_nb = 1


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
    
    def putt_pixel(self, x, y, color):
        coords_x, coords_y = self.getPixelCoords(x, y)
        pixel_coords = (coords_x[0] + 1, coords_y[0] + 1, coords_x[1] + 1, coords_y[1] + 1)
        tag = f"{coords_x[0]}-{coords_y[0]}"
        if not self.pixel_existance(tag)[0]:
            self.canva.create_rectangle(*pixel_coords, fill=color, tags=(tag, color), width=0)
        else:
            self.canva.itemconfig(self.canva.find_withtag(tag), fill=color)
        
    def pixel_existance(self, tag:str):
        '''
        Fonction qui prend le tag d'un pixel et vérifie s'il existe ainsi que sa couleur. 
        Par défaut s'il n'existe pas renvoit blanc.
        
        :param str tag: tag qui caractérise un pixel, c'est ses "coordonnées"
        :return list[Bool, str]: existance ou non et couleur
        '''
        pixel_id = self.canva.find_withtag(tag)
        if pixel_id:
            color = self.canva.itemcget(pixel_id, "fill")
            return [True, color]
        else:
            return [False, "#FFFFFF"]

    def fill_zone(self, x : int, y : int):
        
        target_color = "#FFFFFF"
        replacement_color = self.current_color
        start_x, start_y = self.getPixelCoords(x, y)
        # sorte de file d'attente donc c'est l'ensemble des pixels à colorié. Au bot d'un moment on ne trouve plus de voisins (qui ne sont pas des bords) la boucle s'arrête
        stack = [(start_x[0], start_y[0])]
        # les voisins sont choisis toujours dans les quatres directions on évite les superpositions
        visited = set()
        #je prend le dernier élément de la pile et je teste et cherche ses voisins
        while stack:
            px, py = stack.pop()
            if (px, py) in visited:
                continue
            visited.add((px, py))
            tag = f"{px}-{py}"
            #info sur l'existance du pixel
            info = self.pixel_existance(tag)
            if info[0]:
                # Si le pixel existe on regarde sa couleur
                if info[1] != target_color:
                    continue
                # je modifie la couleur du pixel existant
                self.canva.itemconfig(self.canva.find_withtag(tag), fill=replacement_color)
            else:
                # Si le pixel n'existe pas je le crée et l'ajoute
                self.putt_pixel(px, py, replacement_color)
            # Ajoute les voisins à la pile si dans les limites et non visités
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = px + dx * 11, py + dy * 11
                if 0 <= nx < self.Nx*11 and 0 <= ny < self.Ny*11:
                    if (nx, ny) not in visited:
                        stack.append((nx, ny))

    def circle_click(self, start_x, start_y):
        if self.click_nb == 1:
            self.start_coords_circle = self.getPixelCoords(start_x, start_y)
            self.click_nb = 0
        else:
            end_coords = self.getPixelCoords(start_x, start_y)
            r = sqrt((self.start_coords_circle[0][0] - end_coords[0][0])**2 + (self.start_coords_circle[1][0] - end_coords[1][0])**2)
            self.circle(self.start_coords_circle[0][0]+1, self.start_coords_circle[1][0]+1, int(r))
            self.click_nb = 1

    def line_click(self, start_x, start_y):
        if self.click_nb == 1:
            self.start_coords_line = self.getPixelCoords(start_x, start_y)
            self.click_nb = 0
        else:
            end_coords = self.getPixelCoords(start_x, start_y)
            self.line((self.start_coords_line[0][0], self.start_coords_line[1][0]), (end_coords[0][0], end_coords[1][0]))
            self.click_nb = 1
    def square_click(self, start_x, start_y):
        if self.click_nb == 1:
            self.start_coords_square = self.getPixelCoords(start_x, start_y)
            self.click_nb = 0
        else:
            end_coords = self.getPixelCoords(start_x, start_y)
            self.square(self.start_coords_square[0][0], self.start_coords_square[1][0], end_coords[0][0], end_coords[1][0])
            self.click_nb = 1

    def circle(self, start_x, start_y, r):
        x = 0
        y = -r
        p = -r
        while x + y < 0:
            y_mid = y + self.pixel_size // 2
            x_mid = x + self.pixel_size // 2
            if x_mid**2 + y_mid**2 - r**2 > 0:
                y += self.pixel_size
            self.putt_pixel(x+start_x, y + start_y, self.current_color)
            self.putt_pixel(start_x - x, start_y - y, self.current_color)
            self.putt_pixel(start_x - x, start_y + y, self.current_color)
            self.putt_pixel(x + start_x, start_y - y, self.current_color)
            self.putt_pixel(y + start_x, x + start_y, self.current_color)
            self.putt_pixel(start_x - y, x + start_y, self.current_color)
            self.putt_pixel(start_x - y, start_y - x, self.current_color)
            self.putt_pixel(start_x + y, start_y - x, self.current_color)
            x += self.pixel_size


    def line(self, start: tuple, end: tuple):
        x0, y0 = start
        x0 += 5
        y0 += 5
        x1, y1 = end
        x1 += 5
        y1 += 5
        dx = x1 - x0
        dy = y1 - y0
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        step_x = self.pixel_size if dx >= 0 else -self.pixel_size
        step_y = self.pixel_size if dy >= 0 else -self.pixel_size
        if abs_dx > abs_dy:
            for x in range(x0, x1 + step_x, step_x):
                t = (x - x0) / dx if dx != 0 else 0
                y = int(y0 + t * dy)
                self.putt_pixel(x, y, self.current_color)
        else:
            for y in range(y0, y1 + step_y, step_y):
                t = (y - y0) / dy if dy != 0 else 0
                x = int(x0 + t * dx)
                self.putt_pixel(x, y, self.current_color)

        
    def square(self, start_x, start_y, end_x, end_y):
        self.line((start_x, start_y), (end_x, start_y))
        self.line((start_x, end_y), (end_x, end_y))
        self.line((start_x, start_y), (start_x, end_y))
        self.line((end_x, start_y), (end_x, end_y))

    # pour former la matrice avec les couleurs RGB des pixels du canva
    def matrix_pixels(self, width : int, height : int):
            matrix = []
            for j in range(height):
                matrix.append([])
                for i in range(width):
                    hex_color = self.pixel_existance(f"{11*i}-{11*j}")[1]
                    rgb_color = [int(hex_color[k:k+2], 16) for k in [1, 3, 5]]
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
                    self.putt_pixel(11*i, 11*j, color)

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
