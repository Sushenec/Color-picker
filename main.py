import tkinter, math 

WINDOW_SIZE = {"width":600, "height":600}

class CanvasColorWheel:
    def __init__(self, master : tkinter.Tk, width : int, height : int, canvasColor, colorWheelScale : float):
        self.master = master
        self.height = height
        self.width = width
        self.canvasColor = canvasColor
        self.colorWheelScale = colorWheelScale
        self.colorSelector = None

        self.canvas = tkinter.Canvas(self.master, height=self.height, width=self.width, background=self.canvasColor)
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
        overlapping = self.canvas.find_overlapping(event.x - tolerance, event.y - tolerance, event.x + tolerance, event.y + tolerance)
        for item in overlapping:
            if item == self.colorWheel:
                # destroys old color selector before drawing new one
                self.canvas.delete(self.colorSelector)

                # calculates angle relative to center of canvas
                angle = math.degrees(math.atan2(-(event.y - (self.height / 2)), event.x - (self.width / 2)))
                angle = angle + 360 if angle < 0 else angle 

                angle -= 90 # rotate 90 degree counter-clockwise
                angle = angle + 360 if angle < 0 else angle 
                
                # colors the color selector to selected color
                color = self.__HSVToRGB(math.trunc(angle),1,1)
                self.colorSelector = self.canvas.create_oval(event.x-10,event.y-10,event.x+10,event.y+10, outline="#EFEFEF", fill=color)


    def initColorWheelInput(self):
        self.canvas.bind("<Button-1>", self.__handleMouseColorWheelInput)
        self.canvas.bind("<B1-Motion>", self.__handleMouseColorWheelInput)


    def __drawColorWheel(self):
        wheelRadius = (min(self.width, self.height) * self.colorWheelScale) / 2

        self.colorWheel = self.canvas.create_oval((self.width / 2) - wheelRadius, (self.height / 2) - wheelRadius,
                                                (self.width / 2) + wheelRadius, (self.height / 2) + wheelRadius, fill="#000060")



def main():
    main_window = tkinter.Tk()
    main_window.title("Color Picker")

    # setting constant size
    main_window.geometry(f"{WINDOW_SIZE["width"]}x{WINDOW_SIZE["height"]}")
    main_window.resizable(False,False)

    # init canvas
    canvas = CanvasColorWheel(main_window, WINDOW_SIZE["width"]-100, WINDOW_SIZE["height"]-200, "#AF9FFF",0.9)
    canvas.initColorWheelInput()
    

    main_window.mainloop()
    pass



if __name__ == "__main__":
    main()