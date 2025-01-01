import tkinter
from ColorWheel import ColorWheel

WINDOW_SIZE = {"width":600, "height":600}


def main():
    main_window = tkinter.Tk()
    main_window.title("Color Picker")

    # setting constant size
    main_window.geometry(f"{WINDOW_SIZE["width"]}x{WINDOW_SIZE["height"]}")
    main_window.resizable(False, False)

    # init canvas
    color_wheel = ColorWheel(main_window, WINDOW_SIZE["width"] - 100, WINDOW_SIZE["height"] - 200, 0.9)
    

    main_window.mainloop()
    pass



if __name__ == "__main__":
    main()