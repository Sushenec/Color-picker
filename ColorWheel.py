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
        self.selected_color = {"hue" : 0, "saturation" : 100, "value" : 100}
        self.__selected_color = {"hue" : {"stringVar" : tkinter.StringVar(value = "0"), "intVar" : tkinter.IntVar(value = 0)},
                                 "saturation" : {"stringVar" : tkinter.StringVar(value = "100"), "intVar" : tkinter.IntVar(value = 100)},
                                  "value" : {"stringVar" : tkinter.StringVar(value = "100"), "intVar" : tkinter.IntVar(value = 100)}}

        canvas_border_color = "#000000"
        self.canvas = tkinter.Canvas(self.master, height = self.height, width = self.width,
                     highlightthickness = 1, highlightcolor = canvas_border_color, highlightbackground = canvas_border_color)

        self.canvas.grid(row = 0, padx = (self.width / 2) - self.master.winfo_reqwidth())
        self.__drawColorWheel()
        self.__createControlls()
        self.__initColorWheelInput()

    def selectColor(self, color : list[int]):
        """
        Input color list in HSV
        hue is in range [0, 360]
        saturation is in range [0, 100]
        value is in range [0, 100]
        """

        # change color selector outline to the oposite value
        self.canvas.itemconfig(self.color_selector, outline = self.__HSVToRGB(0, 0, 100 - self.selected_color["value"]))

        # input error check
        if len(color) < 3:
            print(f"need 3 color values {color}")
            return

        for i in range(3):
            # checks if input is list of ints
            if type(color[i]) != type(0):
                print(f"color[{i}] is of type {type(color[i])} not of type {type(0)}")

        # checks if the saturation or value changed
        change_in_saturation_or_value =  self.selected_color["saturation"] != color[1] or self.selected_color["value"] != color[2]

        # store selected color
        self.selected_color["hue"] = color[0]
        self.selected_color["saturation"] = color[1]
        self.selected_color["value"] = color[2]

        # update text fields
        self.__selected_color["hue"]["stringVar"].set(f"{color[0]}")
        self.__selected_color["saturation"]["stringVar"].set(f"{color[1]}")
        self.__selected_color["value"]["stringVar"].set(f"{color[2]}")

        # update number field
        self.__selected_color["hue"]["intVar"].set(color[0])
        self.__selected_color["saturation"]["intVar"].set(color[1])
        self.__selected_color["value"]["intVar"].set(color[2])

        # update displayed color and color selector
        self.canvas.config(background = self.__HSVToRGB(self.selected_color["hue"], self.selected_color["saturation"], self.selected_color["value"]))
        self.canvas.itemconfig(self.color_selector, fill = self.__HSVToRGB(self.selected_color["hue"], self.selected_color["saturation"], self.selected_color["value"]))

        # redraws color wheel when saturation or value changed
        if change_in_saturation_or_value:
            self.__drawColorWheel()


    def __createControlls(self):
        def handleHueEntry(*args):
            if self.__selected_color["hue"]["stringVar"].get() == "":
                self.selectColor([0, self.selected_color["saturation"], self.selected_color["value"]])
            elif not self.__selected_color["hue"]["stringVar"].get().isdigit() or not (0 <= int(self.__selected_color["hue"]["stringVar"].get()) <= 360):
                self.selectColor([0, self.selected_color["saturation"], self.selected_color["value"]])  
            else:
                self.selectColor([int(self.__selected_color["hue"]["stringVar"].get()), self.selected_color["saturation"], self.selected_color["value"]])
                
        def handleHueScale(*args):
            self.selectColor([self.__selected_color["hue"]["intVar"].get(), self.selected_color["saturation"], self.selected_color["value"]])

        def handleSaturationEntry(*args):
            if self.__selected_color["saturation"]["stringVar"].get() == "":
                self.selectColor([self.selected_color["hue"], 0, self.selected_color["value"]])
            elif not self.__selected_color["saturation"]["stringVar"].get().isdigit() or not (0 <= int(self.__selected_color["saturation"]["stringVar"].get()) <= 100):
                self.selectColor([self.selected_color["hue"], 100, self.selected_color["value"]])
            else:
                saturation = int(self.__selected_color["saturation"]["stringVar"].get())
                self.selectColor([self.selected_color["hue"], saturation, self.selected_color["value"]])

        def handleSaturationScale(*args):
            self.selectColor([self.selected_color["hue"], self.__selected_color["saturation"]["intVar"].get(), self.selected_color["value"]])

        def handleValueEntry(*args):
            if self.__selected_color["value"]["stringVar"].get() == "":
                self.selectColor([self.selected_color["hue"], self.selected_color["saturation"], 0])
            elif not self.__selected_color["value"]["stringVar"].get().isdigit() or not (0 <= int(self.__selected_color["value"]["stringVar"].get()) <= 100):
                self.selectColor([self.selected_color["hue"], self.selected_color["saturation"], 100])
            else:
                value = int(self.__selected_color["value"]["stringVar"].get())
                self.selectColor([self.selected_color["hue"], self.selected_color["saturation"], value])

        def handleValueScale(*args):
            self.selectColor([self.selected_color["hue"], self.selected_color["saturation"], self.__selected_color["value"]["intVar"].get()])

        # constrolls frame wraps all color inputs
        self.controlls_frame = tkinter.Frame(self.master)
        self.controlls_frame.grid(row = 1, pady = 10)
        
        font = "Arial 10"
        entry_width = 5
        scale_lenght = 180

        # hue inputs
        hue_frame = tkinter.Frame(self.controlls_frame)
        hue_frame.grid(row = 0)

        tkinter.Label(hue_frame, text = "hue", font = font).grid(row = 0, column = 0)

        self.__selected_color["hue"]["stringVar"].trace_add("write", handleHueEntry)
        hue_entry = tkinter.Entry(hue_frame, textvariable = self.__selected_color["hue"]["stringVar"], width = entry_width)
        hue_entry.grid(row = 0, column = 1, padx = 10)

        hue_scale = tkinter.Scale(hue_frame, from_ = 0, to = 360, showvalue = 0, 
                                    command = handleHueScale, orient = tkinter.HORIZONTAL,
                                    length = scale_lenght, variable = self.__selected_color["hue"]["intVar"])
        hue_scale.grid(row = 0, column = 2)


        # saturation inputs
        saturation_frame = tkinter.Frame(self.controlls_frame)
        saturation_frame.grid(row = 1)

        tkinter.Label(saturation_frame, text = "saturation", font = font).grid(row = 0, column = 0)

        self.__selected_color["saturation"]["stringVar"].trace_add("write", handleSaturationEntry)
        saturation_entry = tkinter.Entry(saturation_frame, textvariable = self.__selected_color["saturation"]["stringVar"], width = entry_width)
        saturation_entry.grid(row = 0, column = 1, padx = 10)

        saturation_scale = tkinter.Scale(saturation_frame, from_ = 0, to = 100, showvalue = 0,
                                            command = handleSaturationScale, orient = tkinter.HORIZONTAL,
                                            length = scale_lenght, variable = self.__selected_color["saturation"]["intVar"])
        saturation_scale.grid(row = 0, column = 2)

        # value inputs
        value_frame = tkinter.Frame(self.controlls_frame)
        value_frame.grid(row = 2)

        tkinter.Label(value_frame, text = "value", font = font).grid(row = 0, column = 0)

        self.__selected_color["value"]["stringVar"].trace_add("write", handleValueEntry)
        value_entry = tkinter.Entry(value_frame, textvariable = self.__selected_color["value"]["stringVar"], width = entry_width)
        value_entry.grid(row = 0, column = 1, padx = 10)

        value_scale = tkinter.Scale(value_frame, from_ = 0, to = 100, showvalue = 0,
                                        command = handleValueScale, orient = tkinter.HORIZONTAL,
                                        length = scale_lenght, variable = self.__selected_color["value"]["intVar"])
        value_scale.grid(row = 0, column = 2)


    def __HSVToRGB(self, hue, saturation, value):
        chroma = (value / 100)* (saturation / 100)
        secondary_component = chroma * (1 - abs((hue / 60) % 2 - 1))
        match_value = (value / 100) - chroma

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
        elif 300 <= hue <= 360:
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
            self.selected_color["hue"] = math.trunc(angle)

            # colors the color selector to selected color
            color = self.__HSVToRGB(self.selected_color["hue"], self.selected_color["saturation"], self.selected_color["value"])
            self.color_selector = self.canvas.create_oval(event.x - self.color_selector_radius, event.y - self.color_selector_radius,
                                                         event.x + self.color_selector_radius, event.y + self.color_selector_radius, 
                                                         outline = self.__HSVToRGB(0, 0, 100 - self.selected_color["value"]), fill = color, width = self.color_selector_radius / 5, tags = "color_selector")
            
            # change canvas color to selected color
            self.selectColor([self.selected_color["hue"], self.selected_color["saturation"], self.selected_color["value"]])


    def __initColorWheelInput(self):
        self.canvas.bind("<Button-1>", self.__handleMouseColorWheelInput)
        self.canvas.bind("<B1-Motion>", self.__handleMouseColorWheelInput)


    def __drawColorWheel(self):
        # deletes everyting except color selector
        for obj in self.canvas.find_all():
            if obj != self.color_selector:
                self.canvas.delete(obj)

        # draws colored lines to represent the color wheel
        line_width = math.ceil(math.pi * 2 * self.color_wheel_radius / 360) # calculates minimum line width to make the circle without holes # circle circumference divided by number of lines
        for degree in range(360):
            color = self.__HSVToRGB(degree, self.selected_color["saturation"], self.selected_color["value"])
            degree = math.radians(degree)

            self.canvas.create_line(self.center_of_canvas["x"], self.center_of_canvas["y"],
                                (math.cos(degree) * self.color_wheel_radius) + self.center_of_canvas["x"], -(math.sin(degree) * self.color_wheel_radius) + self.center_of_canvas["y"], 
                                fill = color, width = line_width)

        # draws outline of the color wheel    
        self.canvas.create_oval(self.center_of_canvas["x"] - self.color_wheel_radius, self.center_of_canvas["y"] - self.color_wheel_radius,
                                                self.center_of_canvas["x"] + self.color_wheel_radius, self.center_of_canvas["y"] + self.color_wheel_radius, width=line_width)

        # moves color selector to foreground
        self.canvas.tag_raise("color_selector")
        




