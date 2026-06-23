import tkinter as tk
import sqlite3
import hashlib
import os 
import shutil

from tkinter import filedialog
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from collections import Counter
from reportlab.pdfgen import canvas
from tkinter import filedialog
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# paleta de cores do app =======
COR_FUNDO = ("#F8FAFC", "#0F172A")
COR_FRAME = ("#FFFFFF", "#1E293B")
COR_SIDEBAR = ("#E5E7EB", "#111827")
COR_BOTAO = ("#2563EB", "#3B82F6")
COR_HOVER = ("#2563EB", "#3B82F6")
COR_TEXTO = ("#111827", "#F8FAFC")
COR_INPUT =  ("#FFFFFF", "#334155")
COR_CARD = ("#FFFFFF", "#1E293B")
COR_DANGER = ("#DC2626", "#B91C1C")
COR_GRAFICO = ("#FFFFFF", "#1E293B")
# ==============================

BANCO = os.path.join(os.path.dirname(__file__), "clientes.db")

# função para banco de dados e manipular os dados

def criptografar_senha(senha):
    return hashlib.sha256( senha.encode() ).hexdigest()

def criar_banco():
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    data_cadastro TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios( id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    data_criacao TEXT)""")
     
    cursor.execute(""" SELECT * FROM usuarios WHERE usuario = ? """, ("admin",))

    if cursor.fetchone() is None:

        senha_hash = criptografar_senha("admin123")

        cursor.execute(""" INSERT INTO usuarios (usuario, senha, data_criacao) VALUES (?,?,?)""", ("admin",senha_hash,
                            datetime.now().strftime("%d/%m/%Y")))

    conexao.commit()
    conexao.close()

# ============================================================================

class Login: 
    
    def __init__(self,root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x500")
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), dark_image=Image.open("assets/logo.png"),
                                size=(120,120))
        self.logo = ctk.CTkLabel(self.frame, image=logo, text="")
        self.logo.pack(pady=(20,10))
        ctk.CTkLabel(self.frame, text="VISION CRM", font=("Arial", 24, "bold")).pack(pady=20)
        
        self.entry_usuario = ctk.CTkEntry(self.frame,placeholder_text="Usuário")
        self.entry_usuario.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(self.frame,placeholder_text="Senha",show="*")
        self.entry_senha.pack(pady=10)

        ctk.CTkButton(self.frame,text="Entrar",command=self.validar_login).pack(pady=20)
    
    
    def validar_login(self):
        usuario = self.entry_usuario.get()
        senha = criptografar_senha(self.entry_senha.get())

        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        print("usuario:", usuario)
        print("senha:", senha)
        print("tipo senha:", type(senha))
        cursor.execute(""" 
                       SELECT * 
                       FROM usuarios 
                       WHERE usuario = ? 
                       AND senha = ? 
                       """ , (usuario, senha))
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            messagebox.showinfo("sucesso", "Login realizado!")
            self.frame.destroy()
            App(self.root)
            
        else:

            messagebox.showerror("Erro","Usuário ou senha inválidos.")
        
        


class App:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Vision CRM")
        self.root.geometry("900x650")
        self.root.configure(fg_color=COR_FUNDO)

        # conteiner ===============================
        self.container = ctk.CTkFrame(self.root, fg_color=COR_FUNDO)
        self.container.pack(side="right", expand=True, fill="both")
        self.frame_cadastro = ctk.CTkFrame(self.container, fg_color=COR_FUNDO)
        self.frame_clientes = ctk.CTkFrame(self.container, fg_color=COR_FUNDO)
        # ============================================

        # Botao excluir===============================
        self.btn_excluir = ctk.CTkButton(self.frame_clientes, text="❌ Excluir Cliente", command=self.excluir_cliente,
                                         fg_color=COR_DANGER, text_color="white", font=("Arial", 15, "bold"), cursor="hand2")
        self.btn_excluir.pack(pady=10)
        # ===========================================

        # frames ===================================
        self.frame_cadastro.place(relwidth=1, relheight=1)
        self.frame_clientes.place(relwidth=1, relheight=1)

        # sidebar==================================
        
        self.sidebar = ctk.CTkFrame(self.root, fg_color=COR_SIDEBAR, width=120)
        self.sidebar.pack(side="left", fill="y")
        logo_sidebar = ctk.CTkImage( light_image=Image.open("assets/logo.png"), dark_image=Image.open("assets/logo.png"),size=(70,70))
        self.logo = ctk.CTkLabel(self.sidebar,image=logo_sidebar,text="")
        self.logo.pack(pady=(20,10))

        # =========================================

        # botões sidebar===========================
        self.btn_cadastro = ctk.CTkButton(self.sidebar, text="🏠 Cadastro", fg_color="transparent", text_color=COR_TEXTO, hover_color=COR_FRAME,
                                          font=("Arial", 15), cursor="hand2", anchor="w", command=self.mostrar_cadastro)
        self.btn_cadastro.pack(fill="x", pady=5, padx=10)
        self.btn_config = ctk.CTkButton(self.sidebar, text="⚙️ Configurações", fg_color="transparent", text_color=COR_TEXTO, hover_color=COR_FRAME,
                                        font=("Arial", 15), cursor="hand2", anchor="w", command=self.abrir_configuracoes)
        self.btn_config.pack(fill="x", pady=5, padx=10)
        self.btn_relatorios = ctk.CTkButton(self.sidebar, text="📁 Relatórios", fg_color="transparent", text_color=COR_TEXTO, hover_color=COR_FRAME,
                                            font=("Arial", 15), cursor="hand2", anchor="w", command=self.abrir_relatorios)
        self.btn_relatorios.pack(fill="x", pady=5, padx=10)
        self.btn_sair = ctk.CTkButton(self.sidebar, text="🚪 Sair", fg_color="transparent", text_color=COR_TEXTO, hover_color=COR_FRAME,
                                      font=("Arial", 15), cursor="hand2", anchor="w", command=self.sair_sistema)
        self.btn_sair.pack(fill="x", pady=5, padx=10)
        self.btn_clientes = ctk.CTkButton(self.sidebar, text="👥 Clientes", fg_color="transparent", text_color=COR_TEXTO, hover_color=COR_FRAME,
                                          font=("Arial", 15), cursor="hand2", anchor="w", command=self.abrir_clientes)
        self.btn_clientes.pack(fill="x", pady=5, padx=10)

        # TITULO ========================================
        self.titulo = ctk.CTkLabel(self.frame_cadastro, text="Cadastro de clientes", font=(
            "Arial", 25, "bold"), fg_color="transparent", text_color=COR_TEXTO)
        self.titulo.pack(pady=20)
        # =================================================
        
        # PÁGINA RELATÓRIOS =========================================================

        self.frame_relatorios = ctk.CTkFrame(self.container,fg_color=COR_FUNDO
        )

        self.frame_relatorios.place(relwidth=1, relheight=1)

        # SCROLL DA PÁGINA
        self.scroll_relatorios = ctk.CTkScrollableFrame(
            self.frame_relatorios,
            fg_color=COR_FUNDO
        )

        self.scroll_relatorios.pack(fill="both", expand=True)
        # TÍTULO =============================================
        self.titulo_relatorios = ctk.CTkLabel(
            self.scroll_relatorios,
            text="Dashboard de Relatórios",
            font=("Arial", 28, "bold"),
            text_color=COR_TEXTO
        )

        self.titulo_relatorios.pack(pady=20)

        # =========================================================
        # FRAME DOS CARDS
        # =========================================================

        self.frame_cards = ctk.CTkFrame(
            self.scroll_relatorios,
            fg_color="transparent"
        )

        self.frame_cards.pack(fill="x", padx=20, pady=10)

        # =========================================================
        # CARD TOTAL CLIENTES
        # =========================================================

        self.card_total = ctk.CTkFrame(
            self.frame_cards,
            fg_color=COR_CARD,
            corner_radius=15,
            height=120
        )

        self.card_total.pack(
            side="left",
            expand=True,
            fill="both",
            padx=10
        )

        ctk.CTkLabel(
            self.card_total,
            text="Total Clientes",
            font=("Arial", 16),
            text_color=COR_TEXTO
        ).pack(pady=(15, 5))

        self.total_clientes = ctk.CTkLabel(
            self.card_total,
            text="0",
            font=("Arial", 32, "bold"),
            text_color=COR_TEXTO
        )

        self.total_clientes.pack()

        # =========================================================
        # CARD CLIENTES SEMANA
        # =========================================================

        self.card_semana = ctk.CTkFrame(
            self.frame_cards,
            fg_color=COR_CARD,
            corner_radius=15,
            height=120
        )

        self.card_semana.pack(
            side="left",
            expand=True,
            fill="both",
            padx=10
        )

        ctk.CTkLabel(
            self.card_semana,
            text="Clientes Semana",
            font=("Arial", 16),
            text_color=COR_TEXTO
        ).pack(pady=(15, 5))

        self.total_semana = ctk.CTkLabel(
            self.card_semana,
            text="0",
            font=("Arial", 32, "bold"),
            text_color=COR_TEXTO
        )

        self.total_semana.pack()

        # =========================================================
        # FRAME DO GRÁFICO
        # =========================================================

        self.frame_grafico = ctk.CTkFrame(
            self.scroll_relatorios,
            fg_color="#1E293B",
            corner_radius=15,
            height=450
        )

        self.frame_grafico.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.frame_grafico.pack_propagate(False)

        # =========================================================
        # BOTÃO PDF
        # =========================================================

        self.btn_pdf = ctk.CTkButton(
            self.scroll_relatorios,
            text="📄 Exportar Relatório PDF",
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.exportar_pdf
        )

        self.btn_pdf.pack(
            pady=(0, 30),
            padx=20,
            fill="x"
        )
        
        # ===============================================================================

        # Frame de formulario
        self.frame_form = ctk.CTkFrame(
            self.frame_cadastro, fg_color=COR_FRAME, corner_radius=15)
        self.frame_form.pack(pady=10, padx=20)
        # ===============================================================================

        # captura e armazena o nome do cliente

        self.label_nome = ctk.CTkLabel(self.frame_form, text="Nome:", font=(
            "Arial", 18, "bold"), fg_color="transparent", text_color=COR_TEXTO)
        self.label_nome.pack(anchor="w", pady=(0, 5))
        self.entry_nome = ctk.CTkEntry(
            self.frame_form, width=300, font=("Arial", 15), fg_color=COR_INPUT, text_color=COR_TEXTO, border_color=COR_BOTAO)
        self.entry_nome.pack(pady=(0, 15))
        # ===================================================================================

        # captura e salva o telefone

        self.label_tel = ctk.CTkLabel(self.frame_form, text="Telefone:", font=(
            "Arial", 18, "bold"), fg_color="transparent", text_color=COR_TEXTO)
        self.label_tel.pack(anchor="w", pady=(0, 5))
        self.entry_tel = ctk.CTkEntry(
            self.frame_form, width=300, font=("Arial", 15), fg_color=COR_INPUT,text_color=COR_TEXTO, border_color=COR_BOTAO)
        self.entry_tel.pack(pady=(0, 15))
        # ====================================================================================

        # captura e salva o email

        self.label_email = ctk.CTkLabel(
            self.frame_form, text="E-mail:", font=("Arial", 18, "bold"), fg_color="transparent", text_color=COR_TEXTO)
        self.label_email.pack(anchor="w", pady=(0, 5))
        self.entry_email = ctk.CTkEntry(
            self.frame_form, width=300, font=("Arial", 15), fg_color=COR_INPUT,text_color=COR_TEXTO, border_color=COR_BOTAO)
        self.entry_email.pack(pady=(0, 15))
        # ======================================================================================

        #observações dos clientes
        self.label_obs = ctk.CTkLabel(self.frame_form, text="Observações:", font=("Arial", 18, "bold"), text_color=COR_TEXTO)
        self.label_obs.pack(anchor="w", pady=(0,5))
        self.text_obs = ctk.CTkTextbox(self.frame_form, fg_color=COR_INPUT,text_color=COR_TEXTO, border_color=COR_BOTAO, width=300, height=100)
        self.text_obs.pack(pady=(0,15))

        
        # botão de salvar
        self.botao = ctk.CTkButton(self.frame_form, text="Salvar cliente", command=self.salvar,
                                   fg_color=COR_BOTAO, text_color="white", hover_color=COR_HOVER,
                                   font=("Arial", 18, "bold"),
                                   height=40, width=200, corner_radius=10)
        self.botao.pack(pady=10)

        self.entry_pesquisa = ctk.CTkEntry(
            self.frame_clientes, font=("Arial", 12))
        self.entry_pesquisa.pack(pady=10)
        self.entry_pesquisa.bind("<KeyRelease>", self.pesquisa_clientes)
        # =============================================

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1E293B", foreground="white", rowheight=25,
                        fieldbackground="#1E293B", bordercolor="#1E293B", borderwidth=0)
        style.map("Treeview", background=[("selected", "#2563EB")])
        style.configure("Treeview.Heading", background="#111827",
                        foreground="white", font=("Arial", 12, "bold"))
        
        # Pagina de configurações ============================
        self.frame_config = ctk.CTkFrame(self.container,fg_color=COR_FUNDO)
        self.frame_config.place(relwidth=1, relheight=1)
        self.switch_tema = ctk.CTkSwitch(self.frame_config, text="Modo Escuro", command=self.alterar_tema)
        self.switch_tema.pack(pady=20)
        self.switch_tema.select()
        self.btn_editar_clientes = ctk.CTkButton(self.frame_config, text="✏️ Editar Cliente", command=self.abrir_edicao_cliente, height=40)
        self.btn_editar_clientes.pack(pady=10)
        self.btn_alterar_senha = ctk.CTkButton(self.frame_config, text="🔑 Alterar Senha", command=self.alterar_senha)
        self.btn_alterar_senha.pack(pady=10)
        ctk.CTkButton(self.frame_config,text="📦 Fazer Backup",command=self.fazer_backup,height=40,fg_color="#2563EB",
                      hover_color="#1D4ED8").pack(pady=10)
        ctk.CTkButton(self.frame_config, text="📂 Restaurar Backup",command=self.restaurar_backup, height=40, fg_color="#EA580C", 
                      hover_color="#C2410C").pack(pady=10)
        

        #frame editar clientes da pg de config ===============
        self.frame_editar = ctk.CTkFrame(self.container, fg_color=COR_FUNDO)
        self.frame_editar.place(relwidth =1, relheight = 1)
        #==============
        ctk.CTkLabel(self.frame_editar, text="Pesquisar Cliente", font=("Ariel", 18,"bold")).pack(pady=10)
        self.entry_busca_edicao =ctk.CTkEntry(self.frame_editar, width=350)
        self.entry_busca_edicao.pack(pady=5)
        self.entry_busca_edicao.bind("<KeyRelease>", self.pesquisar_cliente_edicao)

        #Treeview para edição ==========
        self.tabela_edicao = ttk.Treeview(self.frame_editar, columns=("id", "nome", "telefone", "email"),show= "headings")
        self.tabela_edicao.heading("id", text="ID")
        self.tabela_edicao.heading("nome", text="Nome")
        self.tabela_edicao.heading("telefone", text = "Telefone")
        self.tabela_edicao.heading("email", text= "Email")
        self.tabela_edicao.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabela_edicao.column("id", width=60)
        self.tabela_edicao.column("nome", width=220)
        self.tabela_edicao.column("telefone", width=150)
        self.tabela_edicao.column("email", width=250)
        self.btn_editar = ctk.CTkButton(self.frame_editar, text="Editar Cliente", command=self.editar_cliente)
        self.btn_editar.pack(pady=10)


        # tabela da pagina de BD=======================================
        self.tabela = ttk.Treeview(self.frame_clientes, columns=("id",
            "nome", "telefone", "email", "data"), show="headings", height=15)
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("telefone", text="Telefone")
        self.tabela.heading("email", text="Email")
        self.tabela.heading("data", text="Data Cadastro")
        self.tabela.column("id", width=60)
        self.tabela.column("nome", width=180)
        self.tabela.column("telefone", width=120)
        self.tabela.column("email", width=250)
        self.tabela.column("data", width=120)
        self.tabela.pack(pady=20)
        # ===============================================
        #frame de obs =====
        self.frame_observacoes = ctk.CTkFrame(self.frame_clientes, corner_radius=10)
        self.frame_observacoes.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.frame_observacoes,text="📋 Observações do Cliente",font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        self.text_observacoes = ctk.CTkTextbox(self.frame_observacoes, height=120)
        self.text_observacoes.pack(fill="x", padx=10,pady=(0,10))
        self.tabela.bind("<<TreeviewSelect>>", self.mostrar_observacoes)

        self.frame_cadastro.tkraise()
        self.root.protocol("WM_DELETE_WINDOW", self.sair_sistema)

     # =================================================
     # FUNÇÕES ====
     # =================================================

    # função de salvamento de dados
    def salvar(self):
        nome = self.entry_nome.get()
        telefone = self.entry_tel.get()
        email = self.entry_email.get()
        observacoes = self.text_obs.get("1.0","end").strip()

        if nome == "" or telefone == "" or email == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        data_cadastro = datetime.now().strftime("%d/%m/%Y")
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        cursor.execute(""" INSERT INTO clientes( 
                       nome, telefone, email, data_cadastro, observacoes) VALUES (?,?,?,?,?)""", (nome, telefone, email, data_cadastro, observacoes))
        conexao.commit()
        conexao.close()

        self.tabela.insert("", tk.END, values=(
            nome, telefone, email, data_cadastro))
        messagebox.showinfo("Sucesso", "Cliente salvo!")
        self.entry_nome.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.text_obs.delete("1.0", "end")
        # ====================================

    # funçoes dos botoes ====================

    # =======================================
    def abrir_clientes(self):
        self.frame_clientes.tkraise()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        cursor.execute(
            """ SELECT id,nome,telefone, email, data_cadastro FROM clientes""")
        clientes = cursor.fetchall()
        for cliente in clientes:
            self.tabela.insert("", tk.END, values=cliente)
        conexao.close()
    # ===========================================================

    # ===============================
    def mostrar_cadastro(self):
        self.frame_cadastro.tkraise()
    # =====================================

    # função de pesquisa de clientes=============
    def pesquisa_clientes(self, event):
        termo = self.entry_pesquisa.get().lower()
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        try:
            conexao = sqlite3.connect(BANCO)
            cursor = conexao.cursor()
            cursor.execute("""SELECT nome, telefone, email, data_cadastro FROM clientes 
                              WHERE nome LIKE ? OR telefone LIKE ? OR email LIKE ? """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
            resultados = cursor.fetchall()
            for cliente in resultados:
                self.tabela.insert("", tk.END, values=cliente)
            conexao.close()
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao pesquisar:\n{erro}")
    # ===========================================

    # função para excluir clientes ==========================================
    def excluir_cliente(self):
        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente.")
            return
        item = selecionado[0]
        valores = self.tabela.item(item)["values"]
        nome = valores[0]
        telefone = valores[1]
        email = valores[2]
        confirmar = messagebox.askyesno(
            "Confirmar exclusão", f"Deseja excluir:\n{nome}?")
        if not confirmar:
            return
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        cursor.execute(""" DELETE FROM clientes WHERE
                          nome = ?
                          AND telefone = ?
                          AND email = ? """, (nome, telefone, email))

        conexao.commit()
        conexao.close()
        self.abrir_clientes()
        messagebox.showinfo("Sucesso", "Cliente excluido!")

    # função para abrir relatorios ====================================

    def abrir_relatorios(self):
        self.frame_relatorios.tkraise()
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
     # TOTAL CLIENTES
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total = cursor.fetchone()[0]
        self.total_clientes.configure(text=str(total))
     # CLIENTES DA SEMANA
        from datetime import timedelta
        hoje = datetime.now()
        semana = hoje - timedelta(days=7)
        cursor.execute("""
        SELECT data_cadastro
        FROM clientes
         """)
        datas = cursor.fetchall()
        total_semana = 0

        for data in datas:
            if data[0]:
                try:
                    data_cliente = datetime.strptime(data[0], "%d/%m/%Y")
                    if data_cliente >= semana:
                        total_semana += 1
                except ValueError:
                    print(f"Data invalida encontrada:{data[0]}")
        self.total_semana.configure(text=str(total_semana))
     # LIMPA GRAFICO ANTIGO
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
     # BUSCAR DADOS REAIS
        cursor.execute("""
        SELECT data_cadastro
        FROM clientes
         """)
        dados = cursor.fetchall()
        conexao.close()
        datas = [dado[0] for dado in dados if dado[0]]
        contador = Counter(datas)
        dias = list(contador.keys())
        valores = list(contador.values())
     # CRIAR FIGURA
        figura = Figure(figsize=(8, 4), dpi=100)
        grafico = figura.add_subplot(111)
        modo = ctk.get_appearance_mode()
        if modo == "Dark":
          cor_fundo = "#1E293B"
          cor_texto = "white"
        else:
          cor_fundo = "white"
          cor_texto = "black"
        figura.patch.set_facecolor(cor_fundo)
        grafico.set_facecolor(cor_fundo)

        grafico.tick_params(colors=cor_texto)

        grafico.xaxis.label.set_color(cor_texto)
        grafico.yaxis.label.set_color(cor_texto)

        grafico.title.set_color(cor_texto)

        for spine in grafico.spines.values():
          spine.set_color(cor_texto)
        grafico.bar(dias, valores)
        grafico.set_title("Clientes Cadastrados por Data")
        grafico.set_xlabel("Datas")
        grafico.set_ylabel("Quantidade")
        figura.tight_layout()
        canvas = FigureCanvasTkAgg(figura, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # função PDF =======================================================
    def exportar_pdf(self):

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Salvar relatório"
        )

        if not arquivo:
            return

        try:

            conexao = sqlite3.connect(BANCO)
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT nome, telefone, email, data_cadastro
                FROM clientes
            """)

            clientes = cursor.fetchall()
            conexao.close()

            pdf = canvas.Canvas(arquivo)

            largura = 595
            altura = 842

            # ======================================
            # CABEÇALHO
            # ======================================

            pdf.setFillColorRGB(0.15, 0.39, 0.92)
            pdf.rect(0, 790, largura, 52, fill=True)

            pdf.setFillColorRGB(1, 1, 1)
            pdf.setFont("Helvetica-Bold", 18)

            pdf.drawCentredString(
                largura / 2,
                810,
                "RELATÓRIO DE CLIENTES"
            )

            # ======================================
            # DATA
            # ======================================

            data_relatorio = datetime.now().strftime("%d/%m/%Y %H:%M")

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica", 10)

            pdf.drawString(
                40,
                770,
                f"Gerado em: {data_relatorio}"
            )

            pdf.drawString(
                40,
                755,
                f"Total de clientes: {len(clientes)}"
            )

            # ======================================
            # CABEÇALHO TABELA
            # ======================================

            y = 720

            pdf.setFillColorRGB(0.85, 0.85, 0.85)
            pdf.rect(30, y, 535, 22, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 10)

            pdf.drawString(40, y + 7, "Nome")
            pdf.drawString(200, y + 7, "Telefone")
            pdf.drawString(320, y + 7, "Email")
            pdf.drawString(500, y + 7, "Data")

            y -= 25

            # ======================================
            # DADOS
            # ======================================

            pdf.setFont("Helvetica", 9)

            pagina = 1

            for cliente in clientes:

                nome = cliente[0]
                telefone = cliente[1]
                email = cliente[2]
                data = cliente[3]

                pdf.drawString(40, y, str(nome)[:25])
                pdf.drawString(200, y, str(telefone))
                pdf.drawString(320, y, str(email)[:25])
                pdf.drawString(500, y, str(data))

                y -= 18

                if y < 60:

                    pdf.setFont("Helvetica", 9)

                    pdf.drawRightString(
                        560,
                        30,
                        f"Página {pagina}"
                    )

                    pdf.showPage()

                    pagina += 1

                    y = 780

            # ======================================
            # RODAPÉ
            # ======================================

            pdf.setFont("Helvetica-Oblique", 9)

            pdf.drawString(
                30,
                30,
                "ClientFlow CRM - Sistema de Gestão de Clientes"
            )

            pdf.drawRightString(
                560,
                30,
                f"Página {pagina}"
            )

            pdf.save()

            messagebox.showinfo(
                "Sucesso",
                "Relatório PDF gerado com sucesso!"
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Erro ao gerar PDF:\n{erro}"
            )

    # função configurações =============================================
    def abrir_configuracoes(self):
        self.frame_config.tkraise()

    # função de alterar tema ===========================================
    def alterar_tema(self):
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    #função de sair ====================================================
    def sair_sistema(self):
        confirmar = messagebox.askyesno("Encerrar Sistema", "Deseja realmente sair ?")
        if confirmar: 
            self.root.destroy()

    def abrir_edicao_cliente(self):
        self.frame_editar.tkraise()
        self.carregar_clientes_edicao()

    def editar_cliente(self):
        selecionado = self.tabela_edicao.selection()

        if not selecionado:
           messagebox.showwarning( "Aviso","Selecione um cliente para editar.")
           return

        item = selecionado[0]
        dados = self.tabela_edicao.item(item)["values"]

        id_cliente = dados[0]
        
        conexao = sqlite3.connect(BANCO)
        cursor =conexao.cursor()
        cursor.execute(""" SELECT observacoes FROM clientes WHERE id = ? """, (id_cliente,))

        resultado = cursor.fetchone()
        conexao.close()
        observacoes = ""

        if resultado and resultado[0]:
            observacoes = resultado[0]

        janela = ctk.CTkToplevel(self.root)
        janela.title("Editar Cliente")
        janela.geometry("550x550")
        janela.grab_set()

        ctk.CTkLabel(
                janela,
                text="Nome"
            ).pack(pady=(15, 5))

        entry_nome = ctk.CTkEntry(
                janela,
                width=300
            )
        entry_nome.pack()

        ctk.CTkLabel(
                janela,
                text="Telefone"
            ).pack(pady=(15, 5))

        entry_tel = ctk.CTkEntry(
                janela,
                width=300
            )
        entry_tel.pack()

        ctk.CTkLabel(
                janela,
                text="Email"
            ).pack(pady=(15, 5))

        entry_email = ctk.CTkEntry(
                janela,
                width=300
            )
        entry_email.pack()
        
        ctk.CTkLabel(
                janela,
                text="Observações"
            ).pack(pady=(15,5))
        
        text_obs = ctk.CTkTextbox(
                janela,
                width=300,
                height=100
            )

        text_obs.pack()

        entry_nome.insert(0, dados[1])
        entry_tel.insert(0, dados[2])
        entry_email.insert(0, dados[3])
        text_obs.insert("1.0", observacoes)

        def salvar_alteracoes():

            novo_nome = entry_nome.get()
            novo_tel = entry_tel.get()
            novo_email = entry_email.get()
            nova_observacao = text_obs.get("1.0", "end").strip()

            if (
                novo_nome == ""
                or novo_tel == ""
                or novo_email == ""
                ):
                messagebox.showwarning("Aviso","Preencha todos os campos!")
                return

            try:

                conexao = sqlite3.connect(BANCO)
                cursor = conexao.cursor()

                cursor.execute("""
                        UPDATE clientes
                        SET nome = ?,
                            telefone = ?,
                            email = ?,
                            observacoes = ?
                        WHERE id = ?
                    """, (
                        novo_nome,
                        novo_tel,
                        novo_email,
                        nova_observacao,
                        id_cliente
                    ))

                conexao.commit()
                conexao.close()

                self.carregar_clientes_edicao()

                messagebox.showinfo("Sucesso","Cliente atualizado com sucesso!")

                janela.destroy()

            except Exception as erro:
                messagebox.showerror("Erro",f"Erro ao atualizar cliente:\n{erro}")

        btn_salvar = ctk.CTkButton(
                janela,
                text="💾 Salvar Alterações",
                command=salvar_alteracoes,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                height=40,
                width=220,
                font=("Arial", 14, "bold")
            )

        btn_salvar.pack(pady=20)         

    def carregar_clientes_edicao(self):
         for item in self.tabela_edicao.get_children():
           self.tabela_edicao.delete(item)

         conexao = sqlite3.connect(BANCO)
         cursor = conexao.cursor()
         cursor.execute("""SELECT id,nome,telefone,email FROM clientes""")
         clientes = cursor.fetchall()
         conexao.close()

         for cliente in clientes:
             self.tabela_edicao.insert("",tk.END,values=cliente)

    def pesquisar_cliente_edicao(self, event):

       termo = self.entry_busca_edicao.get().lower()
       # Se campo vazio, recarrega todos os clientes
       if termo == "":
        self.carregar_clientes_edicao()
        return
       # Limpa a tabela
       for item in self.tabela_edicao.get_children():
         self.tabela_edicao.delete(item)

       try:
         conexao = sqlite3.connect(BANCO)
         cursor = conexao.cursor()

         cursor.execute("""
            SELECT id, nome, telefone, email
            FROM clientes
            WHERE nome LIKE ?
               OR telefone LIKE ?
               OR email LIKE ? """, (
            f"%{termo}%",
            f"%{termo}%",
            f"%{termo}%"
        ))

         resultados = cursor.fetchall()
         conexao.close()

         for cliente in resultados:
            self.tabela_edicao.insert(
                "",
                tk.END,
                values=cliente
            )

       except Exception as erro:
         messagebox.showerror("Erro",f"Erro ao pesquisar:\n{erro}")

    def alterar_senha(self):
        
        janela = ctk.CTkToplevel(self.root)
        entry_nova = ctk.CTkEntry(janela, show="*")
        entry_nova.pack(pady=10)
        entry_confirmar = ctk.CTkEntry(janela, show="*")
        entry_confirmar.pack(pady=10)
        
        janela.title("Alterar Senha")
        janela.geometry("400x300")
        ctk.CTkLabel(janela, text= "Nova Senha").pack(pady=10)
        
        
        def salvar():
            
            senha1 = entry_nova.get()
            senha2 = entry_confirmar.get()
            
            if senha1 != senha2 : 
                messagebox.showerror("Erro", "As senhas não coincidem")
                return
            senha_hash = criptografar_senha(senha1)
            conexao = sqlite3.connect(BANCO)
            cursor = conexao.cursor()
            cursor.execute("""UPDATE usuarios SET senha = ? WHERE usuario = ? """, (senha_hash, "admin"))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Senha alterada.")
            janela.destroy()
            #botao salvar===================================

        ctk.CTkButton(janela, text="💾 Salvar Nova Senha", command=salvar, fg_color="#2563EB", hover_color="#1D4ED8",
                            height=40).pack(pady=20)
  
    def fazer_backup(self):
        
        arquivo = filedialog.askopenfilename(defaultextension=".db", filetypes=[("Banco de dados", "*.db")], initialfile=f"Backup_{
                                                datetime.now().strftime('%d-%m-%Y')}.db")
        if not arquivo:
            return
        
        try:
            shutil.copy2(BANCO, arquivo)
            messagebox.showinfo("Sucesso", "Backup realizado com sucesso!")
            
        except Exception as erro:
            messagebox.showerror("Erro", f"Erro ao criar backup:\n{erro}")
            
    def restaurar_backup(self):
        arquivo = filedialog.askopenfilename(title="Selecionar Backup", filetypes=[("Banco de Dados", "*.db")])
        
        if not arquivo:
            return
        confirmar = messagebox.askyesno("Confirmação", "Restaurar um backup substituirá todos os dados atuais. \n\n Deseja continuar?")
        if not confirmar:
            return
        try: 
            shutil.copy2(arquivo, BANCO)
            messagebox.showinfo("Sucesso", "Backup restaurado com sucesso!\n\n Reinicie o sistema.")
        except Exception as erro :
            messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{erro}")
 
    def mostrar_observacoes(self, event=None):
        
        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = selecionado[0]

        dados = self.tabela.item(item)["values"]

        id_cliente = dados[0]

        try:

            conexao = sqlite3.connect(BANCO)
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT observacoes
                FROM clientes
                WHERE id = ?
            """, (id_cliente,))

            resultado = cursor.fetchone()

            conexao.close()

            self.text_observacoes.delete("1.0", "end")

            if resultado and resultado[0]:

                self.text_observacoes.insert(
                    "1.0",
                    resultado[0]
                )

            else:

                self.text_observacoes.insert(
                    "1.0",
                    "Nenhuma observação cadastrada."
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Erro ao carregar observações:\n{erro}"
            )                             
        
if __name__ == "__main__":
    criar_banco()
    root = ctk.CTk()
    Login(root)
    root.mainloop()

