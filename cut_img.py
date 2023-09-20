import tkinter as tk
from PIL import ImageGrab, Image, ImageDraw, ImageTk
import pyautogui

x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False

def on_move(event):
    global x_end, y_end, drawing

    if drawing:
        x_end, y_end = event.x_root, event.y_root
        draw_rectangle()

def draw_rectangle():
    screen_captured = ImageGrab.grab()
    mask = Image.new('L', screen_captured.size, 50)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x_start, y_start, x_end, y_end], fill=255)
    alpha = Image.new('L', screen_captured.size, 100)
    alpha.paste(mask, (0, 0), mask=mask)

    # Aplica a máscara na região selecionada da imagem
    img = Image.composite(screen_captured, Image.new('RGB', screen_captured.size, 'white'), alpha)

    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
    canvas.img_tk = img_tk

def on_click(event):
    global x_start, y_start, drawing

    x_start, y_start = event.x_root, event.y_root
    drawing = True

def finalizar_programa():
    global x_start, y_start, x_end, y_end
    width = abs(x_end - x_start)
    height = abs(y_end - y_start)
    print(f'Left: {x_start}, Top: {y_start}, Width: {width}, Height: {height}')
    img = pyautogui.screenshot(region=(x_start, y_start, width, height))
    img.save('oiaaaa.png')
    root.quit()

def on_release(_):
    global drawing

    drawing = False
    finalizar_programa()

# Cria a janela principal
root = tk.Tk()
root.overrideredirect(True)  # Remove a barra de título e bordas da janela
root.attributes('-topmost', True)  # Mantém a janela no topo de outras janelas
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Define o tamanho da janela para a tela inteira
root.attributes('-alpha', 0.5)  # Define a transparência da janela (0.5 = 50% de opacidade)

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),  highlightthickness=0)
canvas.pack()

# Configura os eventos do mouse
canvas.bind("<B1-Motion>", on_move)
canvas.bind("<ButtonPress-1>", on_click)
canvas.bind("<ButtonRelease-1>", on_release)

root.mainloop()