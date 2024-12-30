import tkinter, math

class ColorWheel:
    def __init__(self, master : tkinter.Tk, width : int, height : int, colorWheelScale : float):
        self.master = master
        self.height = height
        self.width = width
        self.color_wheel_scale = colorWheelScale
        self.color_selector = None
        self.color_selector_radius = 10
        self.color_wheel_radius = (min(self.width, self.height) * self.color_wheel_scale) / 2
        self.center_of_canvas = {"x" : (self.width / 2), "y" : (self.height / 2)}
        self.selected_color = {"h" : 0, "s" : 1, "v" : 1}

        canvas_border_color = "#000000"
        self.canvas = tkinter.Canvas(self.master, height = self.height, width = self.width,
                     highlightthickness = 1, highlightcolor = canvas_border_color, highlightbackground = canvas_border_color)
        self.canvas.pack()
        self.__drawColorWheel()


    def __HSVToRGB(self, hue, saturation, value):
        chroma = value * saturation
        secondary_component = chroma * (1 - abs((hue / 60) % 2 - 1))
        match_value = value - chroma

        if 0 <= hue < 60:
            r, g, b = chroma, secondary_component, 0
        elif 60 <= hue < 120:
            r, g, b = secondary_component, chroma, 0
        elif 120 <= hue < 180:
            r, g, b = 0, chroma, secondary_component
        elif 180 <= hue < 240:
            r, g, b = 0, secondary_component, chroma
        elif 240 <= hue < 300:
            r, g, b = secondary_component, 0, chroma
        elif 300 <= hue < 360:
            r, g, b = chroma, 0, secondary_component


        r = int((r + match_value) * 255)
        g = int((g + match_value) * 255)
        b = int((b + match_value) * 255)

        # convert to hex
        r = hex(r)[2:]
        g = hex(g)[2:]
        b = hex(b)[2:]

        r = r if len(r) == 2 else "0" + r
        g = g if len(g) == 2 else "0" + g
        b = b if len(b) == 2 else "0" + b

        return "#" + r + g + b
        

    def __handleMouseColorWheelInput(self, event):
        # check if mouse is within tolerance of color wheel
        tolerance = 5

        if ((event.x - self.center_of_canvas["x"])**2 + (event.y - self.center_of_canvas["y"])**2) <= (self.color_wheel_radius + tolerance)**2:
            # destroys old color selector before drawing new one
            self.canvas.delete(self.color_selector)

            # calculates angle relative to center of canvas
            angle = math.degrees(math.atan2(-(event.y - self.center_of_canvas["y"]), event.x - self.center_of_canvas["x"]))
            angle = angle + 360 if angle < 0 else angle 
            
            # update hue
            self.selected_color["h"] = math.trunc(angle)

            # colors the color selector to selected color
            color = self.__HSVToRGB(self.selected_color["h"], self.selected_color["s"], self.selected_color["v"])
            self.color_selector = self.canvas.create_oval(event.x - self.color_selector_radius, event.y - self.color_selector_radius,
                                                         event.x + self.color_selector_radius, event.y + self.color_selector_radius, outline = "#EFEFEF", fill = color, width = self.color_selector_radius / 5)

            # change canvas color to selected color
            self.canvas.configure(background = color)


    def initColorWheelInput(self):
        self.canvas.bind("<Button-1>", self.__handleMouseColorWheelInput)
        self.canvas.bind("<B1-Motion>", self.__handleMouseColorWheelInput)


    def __drawColorWheel(self):
        # draws colored lines to represent the color wheel
        line_width = math.ceil(math.pi * 2 * self.color_wheel_radius / 360) # calculates minimum line width to make the circle without holes # circle circumference divided by number of lines
        for degree in range(360):
            degree = math.radians(degree)

            self.canvas.create_line(self.center_of_canvas["x"], self.center_of_canvas["y"],
                                (math.cos(degree) * self.color_wheel_radius) + self.center_of_canvas["x"], -(math.sin(degree) * self.color_wheel_radius) + self.center_of_canvas["y"], 
                                fill = self.__HSVToRGB(math.degrees(degree), 1, 1), width = line_width)

        # draws outline of the color wheel    
        self.canvas.create_oval(self.center_of_canvas["x"] - self.color_wheel_radius, self.center_of_canvas["y"] - self.color_wheel_radius,
                                                self.center_of_canvas["x"] + self.color_wheel_radius, self.center_of_canvas["y"] + self.color_wheel_radius, width=line_width)
        




