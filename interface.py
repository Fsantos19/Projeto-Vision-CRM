import tkinter as tk
import sqlite3

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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# cores do app
# ========================
COR_FUNDO = "#0f172A"
COR_FRAME = "#1E293B"
COR_BOTAO = "#3B82F6"
COR_HOVER = "#2563EB"
COR_TEXTO = "#F8FAFC"
COR_INPUT = "#E2E8F0"
# =========================

BANCO = "clientes.db"

# função para banco de dados e manipular os dados


def criar_banco():
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    data_cadastro TEXT
    )""")
    conexao.commit()
    conexao.close()

# ============================================================================


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision CRM")
        self.root.geometry("900x550")
        self.root.configure(bg=COR_FUNDO)

        # conteiner ===============================
        self.container = ctk.CTkFrame(self.root, fg_color=COR_FUNDO)
        self.container.pack(side="right", expand=True, fill="both")
        self.frame_cadastro = ctk.CTkFrame(self.container, fg_color=COR_FUNDO)
        self.frame_clientes = ctk.CTkFrame(self.container, fg_color=COR_FUNDO)
        # ============================================

        # Botao excluir===============================
        self.btn_excluir = ctk.CTkButton(self.frame_clientes, text="❌ Excluir Cliente", command=self.excluir_cliente,
                                         fg_color="#A70B0B", text_color="white", font=("Arial", 15, "bold"), cursor="hand2")
        self.btn_excluir.pack(pady=10)
        # ===========================================

        # frames ===================================
        self.frame_cadastro.place(relwidth=1, relheight=1)
        self.frame_clientes.place(relwidth=1, relheight=1)

        # sidebar==================================
        self.sidebar = ctk.CTkFrame(self.root, fg_color="#111827", width=120)
        self.sidebar.pack(side="left", fill="y")
        self.logo = ctk.CTkLabel(self.sidebar, text="Vision Pro", fg_color="#111827",
                                 text_color="white", font=("Arial", 14, "bold"))
        self.logo.pack(pady=20)
        # =========================================

        # botões sidebar===========================
        self.btn_cadastro = ctk.CTkButton(self.sidebar, text="🏠 Cadastro", fg_color="#111827", text_color="white", hover_color="#1F2937",
                                          font=("Arial", 15), cursor="hand2", anchor="w", command=self.mostrar_cadastro)
        self.btn_cadastro.pack(fill="x", pady=5, padx=10)
        self.btn_config = ctk.CTkButton(self.sidebar, text="⚙️ Configurações", fg_color="#111827", text_color="white", hover_color="#1F2937",
                                        font=("Arial", 15), cursor="hand2", anchor="w", command=self.abrir_configuracoes)
        self.btn_config.pack(fill="x", pady=5, padx=10)
        self.btn_relatorios = ctk.CTkButton(self.sidebar, text="📁 Relatórios", fg_color="#111827", text_color="white", hover_color="#1F2937",
                                            font=("Arial", 15), cursor="hand2", anchor="w", command=self.abrir_relatorios)
        self.btn_relatorios.pack(fill="x", pady=5, padx=10)
        self.btn_sair = ctk.CTkButton(self.sidebar, text="🚪 Sair", fg_color="#111827", text_color="white", hover_color="#1F2937",
                                      font=("Arial", 15), cursor="hand2", anchor="w", command=self.sair_sistema)
        self.btn_sair.pack(fill="x", pady=5, padx=10)
        self.btn_clientes = ctk.CTkButton(self.sidebar, text="👥 Clientes", fg_color="#111827", text_color="white", hover_color="#1F2937",
                                          font=("Arial", 15), cursor="hand2", anchor="w", command=self.abrir_clientes)
        self.btn_clientes.pack(fill="x", pady=5, padx=10)

        # TITULO ========================================
        self.titulo = ctk.CTkLabel(self.frame_cadastro, text="Cadastro de clientes", font=(
            "Arial", 25, "bold"), fg_color="transparent", text_color=("black", "white"))
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

        # Pagina de configurações ============================
        self.frame_config = ctk.CTkFrame(self.container,fg_color=COR_FUNDO)
        self.frame_config.place(relwidth=1, relheight=1)
        self.switch_tema = ctk.CTkSwitch(self.frame_config, text="Modo Escuro", command=self.alterar_tema)
        self.switch_tema.pack(pady=20)
        self.switch_tema.select()
        self.texto_provisorio = ctk.CTkLabel(self.frame_config, text="EM BREVE MAIS", font=("Arial", 35, "bold"),
            text_color=("black", "white"))
        self.texto_provisorio.pack(pady=20)

        # TÍTULO =============================================
        self.titulo_relatorios = ctk.CTkLabel(
            self.scroll_relatorios,
            text="Dashboard de Relatórios",
            font=("Arial", 28, "bold"),
            text_color=("black", "white")
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
            fg_color="#1E293B",
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
            text_color="white"
        ).pack(pady=(15, 5))

        self.total_clientes = ctk.CTkLabel(
            self.card_total,
            text="0",
            font=("Arial", 32, "bold"),
            text_color="white"
        )

        self.total_clientes.pack()

        # =========================================================
        # CARD CLIENTES SEMANA
        # =========================================================

        self.card_semana = ctk.CTkFrame(
            self.frame_cards,
            fg_color="#1E293B",
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
            text_color="white"
        ).pack(pady=(15, 5))

        self.total_semana = ctk.CTkLabel(
            self.card_semana,
            text="0",
            font=("Arial", 32, "bold"),
            text_color="white"
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

# =========================================================
        
        # ===============================================================================

        # Frame de formulario
        self.frame_form = ctk.CTkFrame(
            self.frame_cadastro, fg_color=COR_FRAME, corner_radius=15)
        self.frame_form.pack(pady=10, padx=20)
        # ===============================================================================

        # captura e armazena o nome do cliente

        self.label_nome = ctk.CTkLabel(self.frame_form, text="Nome:", font=(
            "Arial", 18, "bold"), fg_color="transparent", text_color=("black", "White"))
        self.label_nome.pack(anchor="w", pady=(0, 5))
        self.entry_nome = ctk.CTkEntry(
            self.frame_form, width=300, font=("Arial", 15), fg_color=COR_INPUT, text_color="black")
        self.entry_nome.pack(pady=(0, 15))
        # ===================================================================================

        # captura e salva o telefone

        self.label_tel = ctk.CTkLabel(self.frame_form, text="Telefone:", font=(
            "Arial", 18, "bold"), fg_color="transparent", text_color=("black", "white"))
        self.label_tel.pack(anchor="w", pady=(0, 5))
        self.entry_tel = ctk.CTkEntry(
            self.frame_form, width=300, font=("Arial", 15), fg_color=COR_INPUT, text_color="black")
        self.entry_tel.pack(pady=(0, 15))
        # ====================================================================================

        # captura e salva o email

        self.label_email = ctk.CTkLabel(
            self.frame_form, text="E-mail:", font=("Arial", 18, "bold"), fg_color="transparent", text_color=("black","white"))
        self.label_email.pack(anchor="w", pady=(0, 5))
        self.entry_email = ctk.CTkEntry(
            self.frame_form, width=300, font=("Arial", 15), fg_color=COR_INPUT, text_color="black")
        self.entry_email.pack(pady=(0, 15))
        # ======================================================================================

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

        # tabela=======================================
        self.tabela = ttk.Treeview(self.frame_clientes, columns=(
            "nome", "telefone", "email", "data"), show="headings", height=15)
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("telefone", text="Telefone")
        self.tabela.heading("email", text="Email")
        self.tabela.column("nome", width=180)
        self.tabela.column("telefone", width=120)
        self.tabela.column("email", width=250)
        self.tabela.heading("data", text="Data Cadastro")
        self.tabela.column("data", width=120)
        self.tabela.pack(pady=20)
        # ===============================================

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

        if nome == "" or telefone == "" or email == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        data_cadastro = datetime.now().strftime("%d/%m/%Y")
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()
        cursor.execute(""" INSERT INTO clientes( 
                       nome, telefone, email, data_cadastro) VALUES (?,?,?,?)""", (nome, telefone, email, data_cadastro))
        conexao.commit()
        conexao.close()

        self.tabela.insert("", tk.END, values=(
            nome, telefone, email, data_cadastro))
        messagebox.showinfo("Sucesso", "Cliente salvo!")
        self.entry_nome.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
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
            """ SELECT nome,telefone, email, data_cadastro FROM clientes""")
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
        grafico.plot(dias, valores, marker="o")
        grafico.set_title("Clientes Cadastrados por Data")
        grafico.set_xlabel("Datas")
        grafico.set_ylabel("Quantidade")
        figura.tight_layout()
        canvas = FigureCanvasTkAgg(figura, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # função PDF =======================================================
    def exportar_pdf(self):
        arquivo = filedialog.asksaveasfilename( defaultextension=".pdf",
                                filetypes=[("PDF", "*.pdf")],
                                title="Salvar relatório")
        if not arquivo:
            return

        try:
            conexao = sqlite3.connect(BANCO)
            cursor = conexao.cursor()
            cursor.execute(""" SELECT nome, telefone, email, data_cadastro FROM clientes """)
            clientes = cursor.fetchall()
            conexao.close()
            pdf = canvas.Canvas(arquivo)
            pdf.setTitle("Relatorio de Clientes")
            pdf.drawString(50, 800,"Relatorio de Clientes")
            pdf.setFont("Helvetica", 10)
            y = 760 
            for cliente in clientes: 
              nome = cliente[0]
              telefone = cliente[1]
              email = cliente[2]
              data = cliente[3]

              linha = (
                f"Nome: {nome} | "
                f"Telefone: {telefone} | "
                f"Email: {email} | "
                f"Data: {data}"
               )

              pdf.drawString(50, y, linha)

              y -= 20

              if y < 50:
                pdf.showPage()
                y = 800

            pdf.save()

            messagebox.showinfo(
            "Sucesso",
            "PDF gerado com sucesso!\n\nRelatorio_Clientes.pdf")

        except Exception as erro:

           messagebox.showerror("Erro",f"Erro ao gerar PDF:\n{erro}")

    # função configurações =============================================
    def abrir_configuracoes(self):
        self.frame_config.tkraise()

    # função de alterar tema ===========================================
    def alterar_tema(self):
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        self.atualizar_cores()

    def atualizar_cores(self):
        if ctk.get_appearance_mode() == "Dark":
            fundo = "#0f172A"
            frame = "#1E293B"
            texto = "white"
        else:
            fundo = "#F8FAFC"
            frame = "#E2E8F0"
            texto = "black"
        self.frame_cadastro.configure(fg_color=fundo)
        self.frame_clientes.configure(fg_color=fundo)
        self.frame_relatorios.configure(fg_color=fundo)
        self.frame_config.configure(fg_color=fundo)

        self.frame_form.configure(fg_color=frame)

        self.card_total.configure(fg_color=frame)
        self.card_semana.configure(fg_color=frame)

        self.titulo.configure(text_color=texto)
        self.titulo_relatorios.configure(text_color=texto)                    

    #função de sair ====================================================
    def sair_sistema(self):
        confirmar = messagebox.askyesno("Encerrar Sistema", "Deseja realmente sair ?")
        if confirmar: 
            self.root.destroy()

if __name__ == "__main__":
    criar_banco()
    root = ctk.CTk()
    app = App(root)
    root.mainloop()

