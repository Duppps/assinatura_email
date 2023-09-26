import tkinter as tk
import re
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
from tkinter import filedialog
import shutil

root = tk.Tk()
root.minsize(920, 530)
root.title("Main")

selected_image = None
nomeFuncionario = None
funcaoFuncionario = None
telefoneFuncionario = None
nome_arquivo = None
foto = None
template = Image.open("template.png")
fontNomeVis = ImageFont.truetype("Fonts/Montserrat-ExtraBold.ttf", 72/3)
fontFuncaoVis = ImageFont.truetype("Fonts/Montserrat-Medium.ttf", 60/3)
fontTelVis = ImageFont.truetype("Fonts/Montserrat-Regular.ttf", 42/3)
templateVis = template.resize((int(template.width/3), int(template.height/3)))

def open_image():
    global selected_image, nomeFuncionario, funcaoFuncionario, telefoneFuncionario, nome_arquivo, foto
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.jfif")])
    if file_path:
        img = Image.open(file_path)

        selected_image = img
        nomeFuncionario = inputNome.get()
        funcaoFuncionario = inputfuncao.get()
        telefoneFuncionario = inputTelefone.get()

        nome_arquivo = (re.sub(r'[^a-zA-Z0-9]', '', nomeFuncionario)).lower()
        uploaded_image_path = "Fotos/"+nome_arquivo+".png"
        selected_image.save(uploaded_image_path, format="PNG")

        foto = Image.open("Fotos/"+nome_arquivo+".png")

def criarAss():
    global template, photo_x, photo_y, foto, nome_arquivo

    nomeFuncionario = inputNome.get()
    funcaoFuncionario = inputfuncao.get()
    telefoneFuncionario = inputTelefone.get()
    nome_arquivo = (re.sub(r'[^a-zA-Z0-9]', '', nomeFuncionario)).lower()
    zoomFoto = int(zoom.get())

    fontNome = ImageFont.truetype("Fonts/Montserrat-ExtraBold.ttf", 72)
    fontFuncao = ImageFont.truetype("Fonts/Montserrat-Medium.ttf", 60)
    fontTel = ImageFont.truetype("Fonts/Montserrat-Regular.ttf", 42)

    new_width = int((foto.width*zoomFoto)/100)
    aspect_ratio = foto.width / foto.height
    new_height = int(new_width / aspect_ratio)

    adjusted_foto = foto.resize((new_width, new_height))

    adjusted_foto = adjusted_foto.convert('RGBA')
    alpha = adjusted_foto.getchannel("A")
    alpha = alpha.point(lambda p: 255)
    adjusted_foto.putalpha(alpha)

    canvas = Image.new("RGBA", template.size)

    canvas.paste(adjusted_foto, (photo_x, photo_y))
    canvas.paste(template, (0, 0), template)

    draw = ImageDraw.Draw(canvas)
    draw.text((754, 142), nomeFuncionario, (255, 0, 9), font=fontNome)
    draw.text((754, 226), funcaoFuncionario, (0, 0, 0), font=fontFuncao)
    draw.text((826, 492), telefoneFuncionario, (0, 0, 0), font=fontTel)

    canvas.save("Assinaturas/"+nome_arquivo+".png")
    canvas.show()

    inputNome.delete(0, tk.END)
    inputfuncao.delete(0, tk.END)
    inputTelefone.delete(0, tk.END)
    posicaoX.delete(0, "end")
    posicaoX.insert(0, 154)
    posicaoY.delete(0, "end")
    posicaoY.insert(0, 50)
    zoom.delete(0, "end")
    zoom.insert(0, 42)

def visualizacao():
    global template, photo_x, photo_y, foto

    photo_x = int(posicaoX.get())
    photo_y = int(posicaoY.get())
    zoomFoto = int(zoom.get())

    nome_arquivo = (re.sub(r'[^a-zA-Z0-9]', '', inputNome.get())).lower()

    canvas = Image.new("RGBA", templateVis.size)

    if (Path("Fotos/"+nome_arquivo+".png").exists()):
        foto = Image.open("Fotos/"+nome_arquivo+".png")
        new_width = int(((foto.width*zoomFoto)/100)/3)
        aspect_ratio = foto.width / foto.height
        new_height = int(new_width / aspect_ratio)
        adjusted_foto = foto.resize((new_width, new_height))
        adjusted_foto = adjusted_foto.convert('RGBA')
        alpha = adjusted_foto.getchannel("A")
        alpha = alpha.point(lambda p: 255)
        adjusted_foto.putalpha(alpha)
        pos_x = int(photo_x/3)
        pos_y = int(photo_y/3)
        canvas.paste(adjusted_foto, (pos_x, pos_y))

    canvas.paste(templateVis, (0, 0), templateVis)
    draw = ImageDraw.Draw(canvas)
    draw.text((754/3, 142/3), inputNome.get(), (255, 0, 9), font=fontNomeVis)
    draw.text((754/3, 226/3), inputfuncao.get(), (0, 0, 0), font=fontFuncaoVis)
    draw.text((826/3, 492/3), inputTelefone.get(), (0, 0, 0), font=fontTelVis)

    preview = ImageTk.PhotoImage(canvas)
    visualizacao_label.config(image=preview)
    visualizacao_label.image = preview

    root.after(50, visualizacao)

def format_phone_number(event):
    # Remove qualquer caractere que não seja número
    cleaned = inputTelefone.get().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

    # Verifica se há pelo menos 10 dígitos
    if len(cleaned) >= 11:
        formatted = '({}) {}-{}'.format(cleaned[:2], cleaned[2:7], cleaned[7:])
        inputTelefone.delete(0, 'end')
        inputTelefone.insert(0, formatted)


frame_coluna_esquerda = tk.Frame(root)
frame_coluna_esquerda.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

frame_buttons_posicao = tk.Frame(frame_coluna_esquerda)
frame_buttons_posicao.grid(row=3, columnspan=2, padx=10, pady=10, sticky="s")

root.columnconfigure(0, weight=1)

visualizacao_label = tk.Label(root, image=None)

nome = tk.Label(frame_coluna_esquerda, text="Nome:")
inputNome = tk.Entry(frame_coluna_esquerda)

funcao = tk.Label(frame_coluna_esquerda, text="Função:")
inputfuncao = tk.Entry(frame_coluna_esquerda)

telefone = tk.Label(frame_coluna_esquerda, text="Telefone:")
inputTelefone = tk.Entry(frame_coluna_esquerda)

sendFoto = tk.Button(frame_buttons_posicao, text="Enviar Foto", command=open_image)

LabelPosicaoX = tk.Label(frame_buttons_posicao, text="X:")
posicaoX = tk.Spinbox(frame_buttons_posicao, from_=-1000, to=1000, increment=1, width=5)
posicaoX.delete(0, "end")
posicaoX.insert(0, 154)

LabelPosicaoY = tk.Label(frame_buttons_posicao, text="Y:")
posicaoY = tk.Spinbox(frame_buttons_posicao, from_=-1000, to=1000, increment=-1, width=5)
posicaoY.delete(0, "end")
posicaoY.insert(0, 50)

zoomLabel = tk.Label(frame_coluna_esquerda, text="Zoom:")
zoom = tk.Spinbox(frame_coluna_esquerda, from_=0, to=100, increment=1, width=5)
zoom.delete(0, "end")
zoom.insert(0, 42)

btnCriar = tk.Button(root, text="Criar Assinatura", command=criarAss)

#root.bind_all("<Any-KeyPress>", lambda event: visualizacao())
#root.bind_all("<Any-Button>", lambda event: visualizacao())
inputTelefone.bind("<KeyRelease>", format_phone_number)

nome.grid(row=0, column=0, sticky="e", padx=10, pady=10)
inputNome.grid(row=0, column=1, sticky="w", padx=10, pady=10)
funcao.grid(row=1, column=0, sticky="e", padx=10, pady=10)
inputfuncao.grid(row=1, column=1, sticky="w", padx=10, pady=10)
telefone.grid(row=2, column=0, sticky="e", padx=10, pady=10)
inputTelefone.grid(row=2, column=1, sticky="w", padx=10, pady=10)

sendFoto.grid(row=0, column=0, padx=10, pady=10)
LabelPosicaoX.grid(row=0, column=1, sticky="e", pady=10, padx=10)
posicaoX.grid(row=0, column=2,sticky="w", pady=10)
LabelPosicaoY.grid(row=0, column=3, sticky="e", pady=10, padx=10)
posicaoY.grid(row=0, column=4, sticky="w", pady=10)

zoomLabel.grid(row=4, column=0)
zoom.grid(row=4, column=1)

btnCriar.grid(row=6, columnspan=2, pady=10)
visualizacao_label.grid(row=7, column=0, rowspan=7, columnspan=7 ,padx=10, pady=10)

photo_x = int(posicaoX.get())
photo_y = int(posicaoY.get())

visualizacao()
root.mainloop()
