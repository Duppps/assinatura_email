import tkinter as tk
import re
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
from tkinter import filedialog


root = tk.Tk()
root.minsize(920, 530)
root.title("Main")

tamanhoFonteNome = 48
tamanhoFonteFuncao = 38
tamanhoFonteTel = 32

posicaoElementosX = 609
posicaoNomeY = 20
posicaoFuncY = 76
posicaoTelY = 250

posFotoX = 93
posFotoY = 60
zoomFoto = 34
photo_x = 0
photo_y = 0

checkLimparInputs = tk.BooleanVar()

selected_image = None
nomeFuncionario = None
funcaoFuncionario = None
telefoneFuncionario = None
nome_arquivo = None
foto = None
template = Image.open("template.png")
fontNomeVis = ImageFont.truetype("Fonts/Montserrat-ExtraBold.ttf", tamanhoFonteNome/3)
fontFuncaoVis = ImageFont.truetype("Fonts/Montserrat-Medium.ttf", tamanhoFonteFuncao/3)
fontTelVis = ImageFont.truetype("Fonts/Montserrat-Regular.ttf", tamanhoFonteTel/3)
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

    fontNome = ImageFont.truetype("Fonts/Montserrat-ExtraBold.ttf", tamanhoFonteNome)
    fontFuncao = ImageFont.truetype("Fonts/Montserrat-Medium.ttf", tamanhoFonteFuncao)
    fontTel = ImageFont.truetype("Fonts/Montserrat-Regular.ttf", tamanhoFonteTel)

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
    draw.text((posicaoElementosX, posicaoNomeY), nomeFuncionario, (255, 0, 9), font=fontNome)
    draw.text((posicaoElementosX, posicaoFuncY), funcaoFuncionario, (0, 0, 0), font=fontFuncao)
    draw.text((posicaoElementosX, posicaoTelY), telefoneFuncionario, (0, 0, 0), font=fontTel)

    canvas.save("Assinaturas/"+nome_arquivo+".png")
    canvas.show()

    if (checkLimparInputs.get() == 1):
        inputNome.delete(0, tk.END)
        inputfuncao.delete(0, tk.END)
        inputTelefone.delete(0, tk.END)
        
def drag_handler(event):
    global photo_x, photo_y
    photo_x = event.x
    photo_y = event.y
    visualizacao()
    
def image_mouse_drag_handler(event):
    global zoomFoto
    if(event.delta):
        zoomFoto += -1 if event.delta < 0 else 1
        visualizacao()

def visualizacao():
    global template, foto, photo_x, photo_y, zoomFoto
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
    draw.text((posicaoElementosX/3, posicaoNomeY/3), inputNome.get(), (255, 0, 9), font=fontNomeVis)
    draw.text((posicaoElementosX/3, posicaoFuncY/3), inputfuncao.get(), (0, 0, 0), font=fontFuncaoVis)
    draw.text((posicaoElementosX/3, posicaoTelY/3), inputTelefone.get(), (0, 0, 0), font=fontTelVis)

    preview = ImageTk.PhotoImage(canvas)
    visualizacao_label.config(image=preview)
    visualizacao_label.image = preview


def format_phone_number(event):
    cleaned = inputTelefone.get().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

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

checkbutton = tk.Checkbutton(root, text="Limpar campos após envio?", variable=checkLimparInputs)

btnCriar = tk.Button(root, text="Criar Assinatura", command=criarAss)

inputTelefone.bind("<KeyRelease>", format_phone_number)

nome.grid(row=0, column=0, sticky="e", padx=10, pady=10)
inputNome.grid(row=0, column=1, sticky="w", padx=10, pady=10)
funcao.grid(row=1, column=0, sticky="e", padx=10, pady=10)
inputfuncao.grid(row=1, column=1, sticky="w", padx=10, pady=10)
telefone.grid(row=2, column=0, sticky="e", padx=10, pady=10)
inputTelefone.grid(row=2, column=1, sticky="w", padx=10, pady=10)

sendFoto.grid(row=0, column=0, padx=10, pady=10)

checkbutton.grid(row=6, columnspan=3)
btnCriar.grid(row=7, columnspan=2, pady=10)
visualizacao_label.grid(row=8, column=0, rowspan=7, columnspan=7 ,padx=10, pady=10)
visualizacao_label.bind("<B1-Motion>", drag_handler)
visualizacao_label.bind( "<MouseWheel>", image_mouse_drag_handler)

visualizacao()
root.mainloop()
