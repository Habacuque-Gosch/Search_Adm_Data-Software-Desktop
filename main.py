from tkinter import *
import tkinter  as ttk
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import json
import re
import datetime as dt
from models import Informacao_geral
import DataUser
import smtplib
import email.message

# TELA GERAL DO PROGRAMA
tela = ctk.CTk()

# TELA DE INICIALIZAÇÃO DO PROGRAMA
frame_home = ctk.CTkFrame(master=tela, width=900, height=640, corner_radius=20, fg_color="#1d152c", bg_color="#4A70D3", border_color="#0056FD", border_width=1.5)
frame_home.place(x=0, y=0)

texto = "Bem vindo(a) ao Search Admin Data |"
cont = 0
txt = ''

# TITULO DA TELA DE INTRODUÇÃO DA INICIALIZAÇÃO
titulo_introducao_inicial = ctk.CTkLabel(master=frame_home, text=texto, font=('Krona', 30, 'bold'))
titulo_introducao_inicial.place(x=180, y=40)

def slider():
    global cont, txt
    if  cont >= len(texto):
        cont = -1 
        txt = ""
        titulo_introducao_inicial.configure(text=txt)
    else:
        txt = txt + texto[cont]
        titulo_introducao_inicial.configure(text=txt)
    cont += 1 
    titulo_introducao_inicial.after(80, slider)
slider()

# CARREGANDO A IMAGEM DA TELA DE INICIALIZAÇÃO
search_img = PhotoImage(file="fotos/banner/search.png")
search_label = ctk.CTkLabel(master=frame_home, text="", image=search_img)
search_label.place(x=300, y=90)

# FRAME(DIVISÃO/DIV) DO TEXTO DA TELA DE INICIALIZAÇÃO
frame_texto_introdução = ctk.CTkFrame(master=frame_home, width=590, height=150, fg_color="#D9D9D9", bg_color="#1d152c", corner_radius=20, border_width=1.5, border_color="#00B1FD")
frame_texto_introdução.place(x=155, y=390)

# TEXTO DE INTRODUÇÃO DA TELA DE INICIALIZAÇÃO
intro_label = ctk.CTkLabel(master=frame_texto_introdução, text="O SAD(Search Admin Data) é uma ferramenta avançada e eficaz para profi-\n" 
                                                      "ssionais, empresas e empreendedores que desejam acessar informações  \n"
                                                      "detalhadas e confiáveis de empresas brasileiras de forma rápidas e conve- \n"
                                                      "niente. Com uma interface intuitiva e recursos poderosos, o SAD simplifica  \n"
                                                      "o processo de obtenção de informações sobre empresas registradas no      \n"
                                                      "Brasil.                                                                                                                        \n", text_color="#151313" ,font=("Arial", 16))
                                                    
intro_label.place(x=30, y=20)


# CLASSE RESPONSÁVEL POR TODA A APLICAÇÃO
class Application():
    def __init__(self):
        self.tela = tela
        self.tema()
        self.layout()
        self.funcoes_da_aplicacao()
        self.tela.mainloop()

    @staticmethod
    def tema():
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def layout(self):
        self.tela.geometry("900x640")
        self.tela.title("Search Admin Data")
        self.tela.iconbitmap("fotos/icones/ico.ico")
        self.tela.resizable(width=False, height=False)
        self.tela.config(bg="#4A70D3")

    @staticmethod
    def funcoes_da_aplicacao():
        def tela_de_login():
            frame_login.place(x=190, y=130)
            frame_home.destroy()

        # bg_black_hole = PhotoImage(file='fotos/banner/black_hole.png')
        # fundo_tela_login = ctk.CTkLabel(master=tela, image=bg_black_hole, text="")
        
        # FRAME DE LOGIN
        frame_login = ctk.CTkFrame(master=tela, width=520, height=420, corner_radius=20, fg_color="#1d152c", bg_color="#4A70D3", border_color="#0056FD", border_width=1.5)

        botao_iniciar = PhotoImage(file='fotos/icones/inicializacao/iniciar.png')
        iniciar_button = ctk.CTkButton(master=frame_home, text=None, image=botao_iniciar, fg_color="transparent", font=("Roboto", 14, 'bold') , width=250, height=48, hover=None, corner_radius=10, command=tela_de_login)
        iniciar_button.place(x=299, y=560)

        sis_login = ctk.CTkLabel(master=frame_login, text="Bem vindo(a) ao Sad", font=('krona_one', 30, 'bold'))
        sis_login.place(x=110, y=40)

        EntryName = ctk.CTkEntry(master=frame_login, placeholder_text="   Usuário", font=('krona_one', 16) ,border_color="#00B1FD" , width=350, height=35)
        EntryName.place(x=85, y=125)

        EntryPassword = ctk.CTkEntry(master=frame_login, placeholder_text="   Senha", font=('krona_one', 16), border_color="#00B1FD", width=350, height=35, show="*")
        EntryPassword.place(x=85, y=190)

        chekbox_lembrar = ctk.CTkCheckBox(master=frame_login, text="  Lembrar-me", checkmark_color="white", fg_color="#0047FD", width=25, height=15, onvalue=1, offvalue=0)
        chekbox_lembrar.place(x=85, y=240)

        hb_software_Label = ctk.CTkLabel(master=frame_login, text="HB Software", font=('krona_one', 12, 'bold'), width=100,height=15)
        hb_software_Label.place(x=215, y=390)

        def Login():
            marck = chekbox_lembrar.get()
            if marck == 1:
                EntryName._text = EntryName.get()
            User = EntryName.get()
            Pass = EntryPassword.get()
            DataUser.cursor.execute("""
            SELECT * FROM Users
            WHERE User = ? and Password = ?
            """, (User, Pass))
            VerifyLogin = DataUser.cursor.fetchone()
            try:
                if User in VerifyLogin and Pass in VerifyLogin:
                    def tela_de_consulta():
                        # FRAME DE LOGIN
                        frame_consulta = ctk.CTkFrame(master=tela, width=900, height=640, corner_radius=0, fg_color="#4A70D3")
                        frame_consulta.place(x=0, y=0)

                        def logout():
                            frame_consulta.destroy()
                            tela_de_login()

                        img_logout = PhotoImage(file="fotos/icones/frame_consulta/sair.png")
                        botao_logout = ctk.CTkButton(master=frame_consulta, text="", image=img_logout, fg_color="#4A70D3", width=40, command=logout)
                        botao_logout.place(x=805, y=120)

                        frame_clock = ctk.CTkFrame(master=frame_consulta, width=160, height=30, fg_color="#4A70D3",)
                        frame_clock.place(x=730, y=605)

                        # FRAME DE LOGIN
                        def relogio():
                            data = dt.datetime.today()
                            string_data = str(data)
                            data_atual = string_data[0:19]

                            data_label = ctk.CTkLabel(master=frame_clock, text='{}'.format(data_atual), font=('Roboto', 14, 'bold'))
                            data_label.place(x=6, y=3)
                            data_label.after(200, relogio)
                        relogio()

                        sad_label = ctk.CTkLabel(master=frame_consulta, text="Search Admin Data(SAD)", font=('Krona', 25, 'bold'))
                        sad_label.place(x=40, y=40)

                        cnpj_entry = ctk.CTkEntry(master=frame_consulta, corner_radius=10, text_color="#564D4D" , placeholder_text="   Digite o CNPJ desejado", font=('inter', 16), fg_color="#D9D9D9",border_color="#00B1FD", width=300, height=35)
                        cnpj_entry.place(x=40, y=100)

                        user_frame_consulta = PhotoImage(file="fotos/icones/frame_consulta/user.png")

                        user = ctk.CTkLabel(master=frame_consulta, image=user_frame_consulta, text="",
                        bg_color="white",fg_color="white")
                        
                        upload_foto_user = ttk.Button(frame_consulta, text='', bg="#4A70D3",
                        fg="#4A70D3", image=user_frame_consulta, background="#4A70D3", width=40)
                        upload_foto_user.place(x=800, y=60)

                        #TROCAR FOTO DE USUARIO NO FRAME DE APPS
                        def trocar_de_foto():
                            global img
                            filename =  filedialog.askopenfilename(initialdir="C:", title="selecione a imagem", filetypes=(("png images","*.png"),("jpeg images","*.jpeg")))
                            img = Image.open(filename)
                            upload_foto_user['width'] = 60
                            upload_foto_user['height'] = 60
                            upload_foto_user.place(x=790, y=50)
                            resize_img = img.resize((60, 60))
                            img = ImageTk.PhotoImage(resize_img)
                            upload_foto_user['image'] = img        

                        upload_foto_user['command'] = trocar_de_foto
                        

                        nome_user = EntryName.get()
                        boas_vindas_label = ctk.CTkLabel(master=frame_consulta, text='Bem vindo, {}'.format(nome_user), font=('inter', 20, 'bold'))
                        boas_vindas_label.place(x=550, y=65)
                                    
                        def consultar_cnpj():
                            entrada_cnpj = cnpj_entry.get()
                            cnpj_entry.delete("0", "end")     
                                                        
                            if len(entrada_cnpj) != 14:
                                atencao_label = ctk.CTkLabel(master=frame_consulta, text="Quantidade de dígitos inválida!")
                                atencao_label.place(x=40, y=138)
                                
                                            
                            request_cnpj = requests.get('https://receitaws.com.br/v1/cnpj/{}'.format(entrada_cnpj))

                            consulta_data = request_cnpj.json()

                            informacoes_label = ctk.CTkLabel(master=frame_consulta, text="Informações de registro", font=("Roboto", 20, 'bold'))
                            informacoes_label.place(x=50, y=160)


                            frame_principais_info = ctk.CTkFrame(master=frame_consulta, width=700, height=220, corner_radius=10, fg_color="white", border_color="#00B1FD", border_width=2)
                            frame_principais_info.place(x=40, y=200)

                            # CONSULTANDO CNPJ
                            if 'erro' not in consulta_data:
                                
                                nome = consulta_data['nome']
                                nome_label = Label(frame_principais_info , text='Nome: {}'.format(nome), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                nome_label.place(x=10, y=10)

                                fantasia = consulta_data['fantasia']
                                nome_fantasia = Label(frame_principais_info , text='Nome Fantasia: {}'.format(fantasia), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                nome_fantasia.place(x=10, y=30)

                                tipo = consulta_data['tipo']
                                tipo_label = Label(frame_principais_info , text='Tipo: {}'.format(tipo), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                tipo_label.place(x=10, y=50)
                    
                                atividade_principal = consulta_data['atividade_principal']
                                atividade_principal_texto = str(atividade_principal)
                                atividade_principal_texto = re.sub("}]", '', atividade_principal_texto)
                                atividade_principal_label = Label(frame_principais_info , text='Atividade principal: {}'.format(atividade_principal_texto[33:128]), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                atividade_principal_label.place(x=10, y=70)
                                
                                abertura = consulta_data['abertura']
                                abertura_label = Label(frame_principais_info , text='Data de Abertura: {}'.format(abertura), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                abertura_label.place(x=10, y=90)

                                status = consulta_data['status']
                                status_label = Label(frame_principais_info , text='Status: {}'.format(status), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                status_label.place(x=10, y=110)

                                situacao = consulta_data['situacao']
                                situacao_label = Label(frame_principais_info , text='Situação: {}'.format(situacao), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                situacao_label.place(x=10, y=130)

                                capital = consulta_data['capital_social']
                                capitala_label = Label(frame_principais_info , text='Capital social: {}'.format(capital), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                capitala_label.place(x=10, y=150)

                                porte = consulta_data['porte']
                                porte_label = Label(frame_principais_info , text='Porte: {}'.format(porte), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                porte_label.place(x=10, y=170)
                        
                                qsa_todos = consulta_data['qsa']
                                qsa_presidente_texto = str(qsa_todos)
                                qsa_label = Label(frame_principais_info , text='Presidente: 'f'{qsa_presidente_texto[125:149]}', font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                qsa_label.place(x=10, y=190)

                                endereco_label = ctk.CTkLabel(master=frame_consulta, text="Endereço", font=("Roboto", 20, 'bold'))
                                endereco_label.place(x=50, y=430)

                                # ENDEREÇO FRAME
                                frame_endereco = ctk.CTkFrame(master=frame_consulta, width=400, height=130, corner_radius=10, fg_color="white",border_color="#00B1FD", border_width=2)
                                frame_endereco.place(x=40, y=465)

                                cep = consulta_data['cep']
                                cep_label = Label(frame_consulta, text='Cep: {}'.format(consulta_data['cep']), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                cep_label.place(x=50, y=470)

                                rua_label = Label(frame_consulta, text='Logradouro: {}'.format(consulta_data['logradouro']), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                rua_label.place(x=50, y=490)

                                complemento_label = Label(frame_consulta, text='Complemento: {}'.format(consulta_data['complemento']), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                complemento_label.place(x=50, y=510)

                                bairro_label = Label(frame_consulta, text='Bairro: {}'.format(consulta_data['bairro']), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                bairro_label.place(x=50, y=530)

                                municipio_label = Label(frame_consulta, text='Cidade: {}'.format(consulta_data['municipio']), font=('Roboto', 10), width=0, height=0, bg="white", justify=LEFT)
                                municipio_label.place(x=50, y=550)

                                estado_label = Label(frame_consulta, text='Estado: {}'.format(consulta_data['uf']), width=0, height=0, bg="white", justify=LEFT)
                                estado_label.place(x=50, y=570)

                                def val_barr():
                                    cont = 0 
                                    steps = 10000/100
                                    while cont < steps:
                                        cont = cont + 1
                                        i = 0
                                        while i < 100000:
                                            i = i + 1

                                        var_barra.set(cont)
                                        tela.update()
                                val_barr()

                                # ENTRADA DE EMAIL PARA EXPORTAÇÃO DE DADOS
                                entry_user_email = ctk.CTkEntry(master=frame_consulta, placeholder_text="   Digite seu email para exeportação de dados", width=290, height=35,font=("krona_one", 12), fg_color="#D9D9D9" , text_color="#564D4D" ,border_color="#00B1FD")
                                entry_user_email.place(x=490, y=530)

                                def exportar():
                                    email_dest = entry_user_email.get()

                                    if email_dest == "":
                                        atencao_label = ctk.CTkLabel(master=frame_consulta, text="Preencha o campo de email!")
                                        atencao_label.place(x=490, y=570)

                                    corpo_email = f"""
                                    <h1><b>Informações de registro</B></p>
                                    <br>
                                    <p><b>Nome: </B>{consulta_data['nome']}</p>
                                    <p><b>Nome Fantasia: </B>{consulta_data['fantasia']}</p>
                                    <p><b>Tipo: </B>{consulta_data['tipo']}</p>
                                    <p><b>Atividade principal: </B>{atividade_principal_texto[33:128]}</p>
                                    <p><b>Data de abertura: </B>{consulta_data['abertura']}</p>
                                    <p><b>Status: </B>{consulta_data['status']}</p>
                                    <p><b>Situação: </B>{consulta_data['situacao']}</p>
                                    <p><b>Capital social: </B>{consulta_data['capital_social']}</p>
                                    <p><b>Porte: </B>{consulta_data['porte']}</p>
                                    <p><b>Presidente: </B>{qsa_presidente_texto[125:149]}</p>
                                    <br>
                                    <h1><b>Endereço</B></p>
                                    <br>
                                    <p><b>Cep: </b>{consulta_data['cep']}</p>
                                    <p><b>Logradouro: </b>{consulta_data['logradouro']}</p>
                                    <p><b>Complemento: </b>{consulta_data['complemento']}</p>
                                    <p><b>Bairro: </b>{consulta_data['bairro']}</p>
                                    <p><b>Cidade: </b>{consulta_data['municipio']}</p>
                                    <p><b>Estado: </b>{consulta_data['uf']}</p>
                                    """
                                    
                                    data = dt.datetime.today()
                                    string_data = str(data)
                                    data_atual = string_data[0:19]

                                    msg = email.message.Message()
                                    msg['Subject'] = f"Dados da consulta de {data_atual}"
                                    msg['From'] = 'habacuke14@gmail.com'
                                    msg['To'] = f'{email_dest}'
                                    password = 'lnkwowmfdhqnljuj' 
                                    msg.add_header('Content-Type', 'text/html')
                                    msg.set_payload(corpo_email)

                                    s = smtplib.SMTP('smtp.gmail.com: 587')
                                    s.starttls()
                                    s.login(msg['From'], password)
                                    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

                                    frame_dados_exportados = ctk.CTkFrame(master=frame_consulta, width=360, height=270, corner_radius=20, fg_color="#4A70D3", bg_color="#4A70D3", border_color="#0047FD", border_width=1.5)
                                    frame_dados_exportados.place(x=270,y=180)

                                    label_dados_exportados = ctk.CTkLabel(master=frame_dados_exportados, text="Dados enviados com sucesso", font=('krona_one', 16, 'bold'))
                                    label_dados_exportados.place(x=45, y=20)

                                    img_exporta = PhotoImage(file='fotos/banner/exporta.png')
                                    label_exporta = ctk.CTkLabel(master=frame_dados_exportados, text="", image=img_exporta)
                                    label_exporta.place(x=96.5, y=50)

                                    def okay():
                                        frame_dados_exportados.place(x=5000)

                                    botao_okay = ctk.CTkButton(master=frame_dados_exportados, text="Continuar",font=('krona_one', 18, 'bold'), width=100, height=30, fg_color="#0047FD", corner_radius=10,command=okay)
                                    botao_okay.place(x=130, y=210)
                                
                                img_email = PhotoImage(file='fotos/icones/frame_consulta/email.png')
                                botao_exportar = ctk.CTkButton(master=frame_consulta, image=img_email, text="", width=40, height=40, fg_color="#4A70D3", command=exportar)
                                botao_exportar.place(x=795, y=525)

                            else:
                                print('CNPj Inválido: {}'.format(entrada_cnpj))
                        
                        pesquisa_img = PhotoImage(file="fotos/icones/frame_consulta/lupa.png")
                        botao_consulta_cnpj = ctk.CTkButton(master=frame_consulta, fg_color="#4A70D3" , text=None, width= 25, height= 25, image=pesquisa_img, command=consultar_cnpj)
                        botao_consulta_cnpj.place(x=350, y=98)

                        var_barra = DoubleVar()
                        var_barra.set(0)
                        carregando_o_app = ttk.ttk.Progressbar(frame_consulta, variable=var_barra, maximum=100)
                        carregando_o_app.place(x=40, y=610, width=400, height=15)

                    # Chama a função que inicia a tela de consulta caso o usuário esteja cadastrado
                    tela_de_consulta()

            except:
                label_acesso_negado = ctk.CTkLabel(master=frame_login, text="Nome de usuário ou senha incorreto", font=('krona_one', 12))
                label_acesso_negado.place(x=230, y=230)

        botao_entrar = PhotoImage(file="fotos/icones/frame_login/entrar.png")
        # CHAMA A FUNÇÃO DE LOGIN QUE 
        LoginButton = ctk.CTkButton(master=frame_login, text="Entrar",font=('krona_one', 18, 'bold'), width=240, height=40, fg_color="#0047FD", hover_color="#4095B9" , corner_radius=10, command=Login)
        LoginButton.place(x=144.5, y=280)

        # FUNÇÃO QUE CHAMA O FRAME DE CADASTRO
        def tela_de_cadastro():
            LoginButton.place(x=5000)
            RegisterButton.place(x=5000)
            frame_login.place(x=5000)
           
            # FRAME DE CADASTRO
            frame_cadastro = ctk.CTkFrame(master=tela, width=520, height=500, corner_radius=20, bg_color="#4A70D3", fg_color="#1d152c", border_color="#0056FD", border_width=1.5)
            frame_cadastro.place(x=190, y=70)

            cadastre_tema = ctk.CTkLabel(master=frame_cadastro, text="Faça suas consultas em outro nível\n"
                                                                "com dados preciosos em um único lugar. \n", font=('krona_one', 20, 'bold'))
            cadastre_tema.place(x=70, y=40)

            name_full = ctk.CTkEntry(master=frame_cadastro, placeholder_text="   Nome completo", border_color="#00B1FD", width=350, height=35,
            font=('krona_one', 16))
            name_full.place(x=85, y=125)

            entry_email = ctk.CTkEntry(master=frame_cadastro, placeholder_text="   Email", border_color="#00B1FD", width=350, height=35,
            font=('krona_one', 16))
            entry_email.place(x=85, y=180)

            user_name = ctk.CTkEntry(master=frame_cadastro, placeholder_text="   Nome de usuário", border_color="#00B1FD", width=350, height=35,
            font=('krona_one', 16))
            user_name.place(x=85, y=235)

            password = ctk.CTkEntry(master=frame_cadastro, placeholder_text="   Senha", border_color="#00B1FD", width=350, height=35,
            font=('krona_one', 16), show="*")
            password.place(x=85, y=290)

            chekbox: CTkCheckBox = ctk.CTkCheckBox(master=frame_cadastro, text="  Eu aceito todos os termos e política de privacidade", checkmark_color="white", fg_color="#0047FD")
            chekbox.place(x=85, y=360)

            cnpj_img = PhotoImage(file='fotos/banner/cnpj.png')
            cnpj_label = ctk.CTkLabel(master=tela, image=cnpj_img, text="", fg_color="transparent", bg_color="#4A70D3")
            cnpj_label.place(x=20, y=120)

            rocket_img = PhotoImage(file='fotos/banner/rocket.png')
            rocket_label = ctk.CTkLabel(master=tela, image=rocket_img, text="", fg_color="transparent", bg_color="#4A70D3")
            rocket_label.place(x=750, y=120)


            # Função de registro de dados no DataBase via Sqlite
            def RegisterDataUser():
                Name = name_full.get()
                Email = entry_email.get()
                User = user_name.get()
                Pass = password.get()
                

                if Name == "" or Email == "" and User == "" or Pass == "":
                    atencao_label = ctk.CTkLabel(master=frame_cadastro, text="Por favor preencha todos os campos!")
                    atencao_label.place(x=85, y=330)
                else:
                    DataUser.cursor.execute("""
                        INSERT INTO Users(Name, Email, User, Password) VALUES(?,?,?,?)
                    """, (Name, Email, User, Pass))
                    # Atualizando os dados do banco do DataBase(refresh)
                    DataUser.conn.commit()
                    frame_conta_criada = ctk.CTkFrame(master=tela, width=360, height=250, corner_radius=20, fg_color="#4A70D3", bg_color="#141B2E", border_color="#0047FD", border_width=1.5)

                    label_conta_criada = ctk.CTkLabel(master=frame_conta_criada, text="Parabéns conta criada com sucesso", font=('krona_one', 16, 'bold'))
                    label_conta_criada.place(x=45, y=15)

                    img_happy = PhotoImage(file='fotos/banner/happy.png')
                    label_happy = ctk.CTkLabel(master=frame_conta_criada, text="", image=img_happy)
                    label_happy.place(x=96.5, y=50)

                    def ok():
                        frame_conta_criada.place(x=5000)

                    botao_ok = ctk.CTkButton(master=frame_conta_criada, text="Continuar",font=('krona_one', 18, 'bold'), width=100, height=30, fg_color="#0047FD", corner_radius=10,command=ok)
                    botao_ok.place(x=130, y=210)

                    voltar_para_login()
                    frame_conta_criada.place(x=270, y=242)

            # Botão de cadastro(chama a função de registro de dados no DataBase)
            Register = ctk.CTkButton(frame_cadastro, text="Cadastre-se", font=('krona_one', 18, 'bold'), width=200, height=35, fg_color="#0047FD", hover_color="#4095B9" , corner_radius=10, command=RegisterDataUser)
            Register.place(x=235, y=410)

            def voltar_para_login():
                frame_cadastro.place(x=5000)
                frame_login.place(x=190, y=130)
                Register.place(x=5000)
                LoginButton.place(x=149, y=280)
                RegisterButton.place(x=180, y=343)
                cnpj_label.place(x=5000)
                rocket_label.place(x=5000)
            
            #Botão de voltar(chama o frame de login e remove o frame de cadastro)
            back = ctk.CTkButton(master=frame_cadastro, text="Voltar",font=('krona_one', 14, 'bold'), width=100, height=35, fg_color="#636363", corner_radius=10,command=voltar_para_login)
            back.place(x=85, y=410)

        # Botão de redirecionamento que chama o frame de Cadastro
        RegisterButton = ctk.CTkButton(master=frame_login, text="Cadastre-se", text_color="#00A2FD", font=('krona', 14, 'bold') , width=18, height=20, hover=None, fg_color="#1d152c", corner_radius=80, command=tela_de_cadastro)
        RegisterButton.place(x=180, y=343)

        RegisterLabel = ctk.CTkLabel(master=frame_login, text="Não registrado?", font=('krona_one', 14))
        RegisterLabel.place(x=85, y=340)

# Iniciando a APLICAÇÃO
Application()
