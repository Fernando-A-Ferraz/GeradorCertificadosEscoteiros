from pathlib import Path
from PIL import Image

entrada = Path("Certificado.png")
saida = Path("Certificado_cortado.png")

img = Image.open(entrada).convert("RGB")  # <- força RGB (sem transparência)

# cria máscara de "não branco"
# considera branco como (>=250 em cada canal)
pixels = img.load()
w, h = img.size

min_x, min_y = w, h
max_x, max_y = 0, 0
found = False

for y in range(h):
    for x in range(w):
        r, g, b = pixels[x, y]
        if not (r >= 250 and g >= 250 and b >= 250):  # não é branco
            found = True
            if x < min_x: min_x = x
            if y < min_y: min_y = y
            if x > max_x: max_x = x
            if y > max_y: max_y = y

if not found:
    # se não achou nada, salva original
    img.save(saida)
    print("Não detectei bordas brancas; salvei sem recorte:", saida.resolve())
else:
    # adiciona uma “folga” de 6px pra não cortar a borda
    pad = 6
    min_x = max(min_x - pad, 0)
    min_y = max(min_y - pad, 0)
    max_x = min(max_x + pad, w - 1)
    max_y = min(max_y + pad, h - 1)

    cortado = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    cortado.save(saida)
    print("OK! Gerado:", saida.resolve())
    print("Tamanho original:", (w, h), "-> tamanho cortado:", cortado.size)
