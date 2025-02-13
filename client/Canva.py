class Canva:
    
    def __init__(self, Nx, Ny, pixel_size, canva):
        self.Nx = Nx
        self.Ny = Ny
        self.pixel_size = pixel_size
        self.canva_X = self.Nx * self.pixel_size + self.Nx-1
        self.canva_Y = self.Ny * self.pixel_size + self.Ny-1
        self.canva = canva
        self.canva.config( width = self.canva_X , height = self.canva_Y, bg='white', highlightbackground='grey', highlightcolor='grey' )
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
                print('hover')

            case e.type if e.type == '4' or self.clicked:

                # print(pixel_tag, self.canva.find_withtag(pixel_tag))

                if e.num == 1 or num == 1:
                    self.clicked = True

                    if self.canva.find_withtag(pixel_tag):
                        self.canva.delete(pixel_tag)

                    self.canva.create_rectangle( *pixel_coords, fill=self.current_color, tags=(self.current_color, pixel_tag), width=0)
                    self.canva.tag_bind(pixel_tag, '<ButtonRelease-1>', lambda e: setattr(self, 'clicked', False))
                    print(self.clicked)

                    if self.clicked :
                        self.canva.tag_bind(pixel_tag, '<Leave>', lambda e: self.fillPixel(e, 1))
                    

                elif ( e.num == 3 or num ==3 ) and self.canva.find_withtag(pixel_tag):
                    print('delete')
                    self.canva.delete(pixel_tag)

    def select_color(self, color):
        self.current_color = color




