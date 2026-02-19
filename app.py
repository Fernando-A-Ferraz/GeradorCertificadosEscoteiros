import sqlite3
from pathlib import Path
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit
from babel.dates import format_date

# =========================
# Config
# =========================
APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "membros.db"

# Troque aqui se o seu arquivo tiver outro nome:
TEMPLATE_PNG = APP_DIR / "Certificado_limpo.png"

PAGE_W, PAGE_H = A4

CHECK_OFF = "☐"
CHECK_ON = "☑"


# =========================
# Helpers
# =========================
def slug(text: str) -> str:
    """Deixa seguro para nome de arquivo no Windows."""
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        text = text.replace(ch, "")
    text = text.strip().replace(" ", "_")
    return text[:60] if text else "atividade"


# =========================
# Banco (SQLite)
# =========================
def db_init():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS membros(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                secao TEXT NOT NULL
            )
            """
        )
        conn.commit()


def db_add(nome, secao):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO membros(nome, secao) VALUES(?, ?)",
            (nome.strip(), secao.strip()),
        )
        conn.commit()


def db_list():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT id, nome, secao FROM membros ORDER BY nome")
        return cur.fetchall()


def db_delete(mid):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM membros WHERE id=?", (mid,))
        conn.commit()


# =========================
# Texto auto-ajustável
# =========================
def draw_center_fit(c, text, cx, y, max_width, font="Helvetica", max_font=12, min_font=8):
    size = max_font
    while size >= min_font:
        if stringWidth(text, font, size) <= max_width:
            break
        size -= 0.3
    c.setFont(font, size)
    c.drawCentredString(cx, y, text)


def draw_left_fit(c, text, x_left, y, max_width, font="Helvetica-Bold", font_size=13, min_size=9):
    size = font_size
    while size >= min_size:
        c.setFont(font, size)
        if c.stringWidth(text, font, size) <= max_width:
            c.drawString(x_left, y, text)
            return
        size -= 1
    c.setFont(font, min_size)
    c.drawString(x_left, y, text)


def draw_center_wrap(
    c,
    text,
    cx,
    y_top,
    max_width,
    line_height,
    font="Helvetica",
    font_size=11,
    max_lines=2,
):
    lines = simpleSplit(text, font, font_size, max_width)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1] + "..."

    y = y_top
    c.setFont(font, font_size)
    for line in lines:
        c.drawCentredString(cx, y, line)
        y -= line_height


# =========================
# PDF (3 por A4)
# =========================
def draw_cert(c, x, y, w, h, nome, atividade, local, dias, linha_evento, cidade, dt):
    # Fundo do certificado
    c.drawImage(
        str(TEMPLATE_PNG),
        x,
        y,
        width=w,
        height=h,
        preserveAspectRatio=True,
        mask="auto",
    )

    cx = x + w / 2
    max_w = w * 0.75

    # Linha: "Certificamos que" + Nome (na mesma linha)
    linha_y = y + h * 0.56

    c.setFont("Helvetica", 11)
    c.drawString(x + w * 0.22, linha_y, "Certificamos que")

    # Nome ao lado (começa depois do texto "Certificamos que")
    nome_x = x + w * 0.42
    nome_max_w = (x + w * 0.78) - nome_x
    draw_left_fit(c, nome, nome_x, linha_y, nome_max_w, "Helvetica-Bold", 13, 9)

    # Texto principal (atividade/local/dias)
    draw_center_wrap(
        c,
        f"Participou do {atividade}, realizada em",
        cx,
        y + h * 0.49,
        max_w,
        13,
        font="Helvetica",
        font_size=11,
        max_lines=2,
    )

    # Segunda linha: local + dias
    draw_center_wrap(
        c,
        f"{local} nos dias {dias}.",
        cx,
        y + h * 0.44,
        max_w,
        13,
        font="Helvetica",
        font_size=11,
        max_lines=2,
    )

    # Linha do evento (negrito)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cx, y + h * 0.34, linha_evento)

    # Cidade + data por extenso (lado direito)
    data_extenso = format_date(dt, format="d 'de' MMMM 'de' y", locale="pt_BR")
    c.setFont("Helvetica", 11)
    c.drawRightString(x + w * 0.88, y + h * 0.25, f"{cidade}, {data_extenso}")


def gerar_pdf(participantes, atividade, local, dias, linha_evento, cidade, dt, caminho=None):
    if not TEMPLATE_PNG.exists():
        raise FileNotFoundError(f"Não encontrei '{TEMPLATE_PNG.name}' na pasta do app.")

    # Se vier caminho, salva onde o usuário escolheu
    if caminho:
        out = Path(caminho)
    else:
        # fallback: salvar ao lado do app com nome padrão
        data_br = dt.strftime("%d-%m-%Y")
        nome_arquivo = f"{slug(atividade)}_{data_br}.pdf"
        out = APP_DIR / nome_arquivo

    c = canvas.Canvas(str(out), pagesize=A4)

    margin_x = 10 * mm
    margin_y = 10 * mm
    slot_w = PAGE_W - 2 * margin_x
    slot_h = (PAGE_H - 2 * margin_y) / 3

    i = 0
    while i < len(participantes):
        for pos in range(3):
            if i >= len(participantes):
                break
            x = margin_x
            y = PAGE_H - margin_y - (pos + 1) * slot_h

            draw_cert(
                c,
                x,
                y,
                slot_w,
                slot_h,
                nome=participantes[i],
                atividade=atividade,
                local=local,
                dias=dias,
                linha_evento=linha_evento,
                cidade=cidade,
                dt=dt,
            )
            i += 1
        c.showPage()

    c.save()
    return out


# =========================
# UI (Tkinter)
# =========================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Certificados Escoteiros")
        self.geometry("1020x650")
        self.minsize(1020, 650)

        db_init()

        left = ttk.Frame(self, padding=10)
        right = ttk.Frame(self, padding=10)
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        # ---------- Cadastro ----------
        ttk.Label(left, text="Cadastro de membro", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.nome_var = tk.StringVar()
        self.secao_var = tk.StringVar(value="Escoteiros")

        form = ttk.Frame(left)
        form.pack(fill="x", pady=6)

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.nome_var, width=40).grid(row=0, column=1, sticky="w", padx=6)

        ttk.Label(form, text="Seção:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(
            form,
            textvariable=self.secao_var,
            width=37,
            state="readonly",
            values=["Lobinhos", "Escoteiros", "Sênior", "Pioneiros", "Chefes", "Diretoria", "Outro"],
        ).grid(row=1, column=1, sticky="w", padx=6)

        ttk.Button(left, text="Adicionar", command=self.add_membro).pack(anchor="w", pady=6)

        ttk.Separator(left).pack(fill="x", pady=10)

        # ---------- Busca + Lista com Checkbox ----------
        ttk.Label(
            left,
            text="Membros (clique no ☑ para marcar)",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        self.busca_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.busca_var).pack(fill="x", pady=4)
        self.busca_var.trace_add("write", lambda *_: self.refresh_list())

        cols = ("sel", "nome", "secao")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
        self.tree.heading("sel", text="")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("secao", text="Seção")

        self.tree.column("sel", width=40, anchor="center")
        self.tree.column("nome", width=330, anchor="w")
        self.tree.column("secao", width=120, anchor="w")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.remover_tree_item)

        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="Marcar todos", command=self.marcar_todos).pack(side="left")
        ttk.Button(btns, text="Desmarcar todos", command=self.desmarcar_todos).pack(side="left", padx=6)

        self.itens = {}  # iid(mid) -> {"checked": bool, "nome": str, "secao": str}

        # ---------- Geração ----------
        ttk.Label(right, text="Gerar certificados", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.atividade_var = tk.StringVar()
        self.local_var = tk.StringVar()
        self.dias_var = tk.StringVar()
        self.cidade_var = tk.StringVar(value="Poços de Caldas")
        self.linha_evento_var = tk.StringVar(value="03/03/1991 – 34 anos da fundação do 103/MG – GEPIN")
        hoje = date.today()
        self.data_var = tk.StringVar(value=hoje.strftime("%d/%m/%Y"))

        def row(label, var):
            f = ttk.Frame(right)
            f.pack(fill="x", pady=5)
            ttk.Label(f, text=label, width=18).pack(side="left")
            ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

        row("Atividade:", self.atividade_var)
        row("Local:", self.local_var)
        row("Dias:", self.dias_var)
        row("Cidade:", self.cidade_var)
        row("Linha evento:", self.linha_evento_var)
        row("Data (DD/MM/AAAA):", self.data_var)

        ttk.Separator(right).pack(fill="x", pady=10)

        ttk.Button(right, text="Gerar PDF (3 por folha A4)", command=self.gerar).pack(anchor="w", pady=8)

        ttk.Label(
            right,
            text="Dica: duplo clique em um membro remove do cadastro.",
            foreground="#555",
        ).pack(anchor="w", pady=4)

        self.refresh_list()

    # ---------- Lista ----------
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.itens.clear()

        termo = self.busca_var.get().strip().lower()

        for mid, nome, secao in db_list():
            label = f"{nome} {secao}".lower()
            if termo and termo not in label:
                continue

            iid = str(mid)
            self.tree.insert("", "end", iid=iid, values=(CHECK_OFF, nome, secao))
            self.itens[iid] = {"checked": False, "nome": nome, "secao": secao}

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not row_id:
            return

        # Coluna 1 = sel
        if col == "#1":
            current = self.itens[row_id]["checked"]
            self.itens[row_id]["checked"] = not current
            self.tree.set(row_id, "sel", CHECK_ON if not current else CHECK_OFF)

    def remover_tree_item(self, event):
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        nome = self.itens[row_id]["nome"]
        if not messagebox.askyesno("Remover", f"Remover '{nome}' do cadastro?"):
            return
        db_delete(int(row_id))
        self.refresh_list()

    def marcar_todos(self):
        for iid in self.itens:
            self.itens[iid]["checked"] = True
            self.tree.set(iid, "sel", CHECK_ON)

    def desmarcar_todos(self):
        for iid in self.itens:
            self.itens[iid]["checked"] = False
            self.tree.set(iid, "sel", CHECK_OFF)

    def participantes_marcados(self):
        return [info["nome"] for info in self.itens.values() if info["checked"]]

    # ---------- Cadastro ----------
    def add_membro(self):
        nome = self.nome_var.get().strip()
        secao = self.secao_var.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Informe o nome.")
            return

        db_add(nome, secao)
        self.nome_var.set("")
        self.refresh_list()

    # ---------- Gerar ----------
    def gerar(self):
        participantes = self.participantes_marcados()
        if not participantes:
            messagebox.showerror("Erro", "Marque pelo menos 1 participante.")
            return

        atividade = self.atividade_var.get().strip()
        local = self.local_var.get().strip()
        dias = self.dias_var.get().strip()
        cidade = self.cidade_var.get().strip()
        linha_evento = self.linha_evento_var.get().strip()

        if not atividade or not local or not dias:
            messagebox.showerror("Erro", "Preencha Atividade, Local e Dias.")
            return

        data_txt = self.data_var.get().strip()

        # 1) Validar / converter data
        try:
            if "/" in data_txt:
                d, m, a = data_txt.split("/")
                dt = date(int(a), int(m), int(d))
            else:
                dt = date.fromisoformat(data_txt)
        except Exception:
            messagebox.showerror("Erro", "Data inválida. Use DD/MM/AAAA (ex: 19/02/2026).")
            return

        # 2) Janela "Salvar como"
        data_br = dt.strftime("%d-%m-%Y")
        nome_padrao = f"{slug(atividade)}_{data_br}.pdf"

        caminho = filedialog.asksaveasfilename(
            title="Salvar certificados",
            defaultextension=".pdf",
            initialfile=nome_padrao,
            filetypes=[("Arquivo PDF", "*.pdf")],
        )

        if not caminho:
            return

        # 3) Gerar PDF
        try:
            gerar_pdf(participantes, atividade, local, dias, linha_evento, cidade, dt, caminho)
            messagebox.showinfo("OK", f"PDF salvo em:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro ao gerar", str(e))


if __name__ == "__main__":
    App().mainloop()
