import math
from tkinter import *
from tkinter import ttk
import json
from datetime import date
from datetime import datetime
import requests
import os

# Programmer: Igor Pereira Lins
# Tag: IgortBr
# GitHub: https://github.com/MrigortBr
# Date: 2021/11/22


#Caso for executar pelo VSCODE usar o LOCAL = "Dir Do codigo ex: G:/Scripts/PY/Calculadora/"
LOCAL = str(os.getcwd()).replace(os.path.sep, '/')+"/"

class openAPP:
    def __init__(self):
        #Cria a Janela Principal (self.JanelaApp)
        self.JanelaApp = Tk()

        #Iniciarliza informações do usuario, historico, ultimo aberto e tema escolhido pelo usuario 
        self.lerInformacoes()
        self.checarTema()
        self.checharUltimoAberto()
        

        #Define configurações para Janela Principal
        self.JanelaApp.title('Calculadora')
        self.JanelaApp.geometry('314x538+15+15')
        self.JanelaApp.resizable(width=False, height=False)


        #Salva as definicoes do usuario ao fechar o Aplicativo
        self.JanelaApp.protocol('WM_DELETE_WINDOW', self.salvarPreferencias)

        #Cria o mainloop para Janela Principal
        self.JanelaApp.mainloop()

    def lerInformacoes(self):
        #Abre os tipos de informações necessarias para executar a calculadora da mesma maneira...
        
        #-Lê definições que o usuario usa
        with open(f'{LOCAL}files/data/settings.json', 'r', encoding="utf8") as definicoes:
            self.definicoesUsuario = json.load(definicoes)

        #-Lê Historico do Usuario
        with open(f'{LOCAL}files/data/historics.json', 'r', encoding="utf8") as historico:
            self.historicoCalculadoras = json.load(historico)  
        
    def checharUltimoAberto(self):
        #Inseta informações da ultima calculadora utilizada pelo usuario em uma variavel local
        tipoDeCalculadora = self.definicoesUsuario[0]["Type"]

        #Inserta informações sobre a calculadora de datas, o modo
        self.tipoDatas = self.definicoesUsuario[0]["TypeDate"]

        #Inseta informações sobre a calculadora de Temperatura
        self.temperaturaPrimaria = self.definicoesUsuario[0]["temp1"]
        self.temperaturaSecundaria = self.definicoesUsuario[0]["temp2"]
        self.Moeda1 = self.definicoesUsuario[0]["moeda1"] 
        self.Moeda2 = self.definicoesUsuario[0]["moeda2"] 

        #Abre ultima calculadora
        eval(tipoDeCalculadora)

        #Deleta variavel... para evitar variaveis inuteis no processo
        del tipoDeCalculadora

    def checarTema(self):
        #Inserta informações de tema do usuario em uma variavel local
        
        tema = self.definicoesUsuario[0]["Theme"]
        corTema = self.definicoesUsuario[0]["Color"]
        self.tema = {"BackGround1": '',
                     "BackGround2": '',
                     "BackGround3": '',
                     "BackGround4": '',
                     "ForeGround1": '',
                     "ForeGround2": '',
                     "ColorTheme1": '',
                     "TypeTheme01": ''}

        #If's abaixo são para setar os valores do tema do usuario
        if tema == "Dark":
            self.tema["BackGround1"] = ('#0f0f0f')
            self.tema["BackGround2"] = ("#202020")
            self.tema["BackGround4"] = ('#272727')
            self.tema["ForeGround1"] = ('#c2c2c2')
            self.tema["ForeGround2"] = ("#ffffff")
            self.tema["TypeTheme01"] = ("Dark")

        if tema == "White":
            self.tema["BackGround1"] = ('#bec3c6')
            self.tema["BackGround2"] = ("#dadcdc")
            self.tema["BackGround4"] = ('#f2f3f4')
            self.tema["ForeGround1"] = ('#252626')
            self.tema["ForeGround2"] = ("#252626")
            self.tema["TypeTheme01"] = ("White")

        if corTema == "Purple":
            self.tema["BackGround3"] = ("#571a50")
            self.tema["ColorTheme1"] = ("Purple")
        
        if corTema == "Green":
            self.tema['BackGround3'] = ("#2c993b")
            self.tema["ColorTheme1"] = ("Green")
        
        if corTema == "Blue":
            self.tema['BackGround3'] = ("#1a1a70")
            self.tema['ColorTheme1'] = ("Blue")

        if corTema == "Red":
            self.tema['BackGround3'] = ("#5e0811")
            self.tema['ColorTheme1'] = ("Red")

        #Deleta variavel... para evitar variaveis inuteis no processo
        del tema
        del corTema

    def salvarPreferencias(self):
        #salva as preferencias do usuario para que quando ele reabra a calculadora seus temas e preferencias
        #Continuem igual
        self.definicoesUsuario[0]["Type"] = self.atualCalculdoraFuncao
        self.definicoesUsuario[0]["Theme"] = self.tema["TypeTheme01"]
        self.definicoesUsuario[0]["Color"] = self.tema["ColorTheme1"]
        self.definicoesUsuario[0]["TypeDate"] = self.tipoDatas
        self.definicoesUsuario[0]["temp1"] = self.temperaturaPrimaria
        self.definicoesUsuario[0]["temp2"] = self.temperaturaSecundaria
        self.definicoesUsuario[0]["moeda1"] = self.Moeda1
        self.definicoesUsuario[0]["moeda2"] = self.Moeda2
        

        with open(f'{LOCAL}files/data/settings.json', 'w', encoding="utf8") as definicoes:
            json.dump(self.definicoesUsuario, definicoes)

        self.JanelaApp.destroy()

    def abrirCalculadoraPadrao(self):
        #Tenta destruir o frame da calculadora para a colocar os temas e evitar para que abra mais
        #de um frame Igual
        try:
            self.fundoFramePadrao.destroy()
        except:
            pass
        #Cria todos os Widgets para a calculadora Padrão funcionar
        self.fundoFramePadrao = Frame(self.JanelaApp, width=328, height=538)
        self.fundoFramePadrao.place(x=0)

        self.menuButton = Button(self.fundoFramePadrao, text='☰', font=('Arial', 20, 'bold'), bd=0, command= lambda: self.abrirMenu(5))
        self.menuButton.place(x=0, y=10)
        self.tipoCalculadoraLabel = Label(self.fundoFramePadrao, text='Padrão', width=9, font=('Arial', 20, 'bold'), anchor="w")
        self.tipoCalculadoraLabel.place(x=40, y=15)
        self.historicoPadraoButton = Button(self.fundoFramePadrao, text='◶', font=('Arial', 20, 'bold'), bd=0, command=self.abrirHistoricoPadrao)
        self.historicoPadraoButton.place(x=270, y=10)

        self.resultadoPadraoFrame = Frame(self.fundoFramePadrao, width=328, height=100)
        self.resultadoPadraoFrame.place(x=0,y=75)
        self.resultadoPadraoLabel = Label(self.resultadoPadraoFrame, text='0', font='arial 45', width=9, anchor="e")
        self.resultadoPadraoLabel.place(x=-15, y=25)
        self.resultadoAnteriorPadraoLabel = Label(self.resultadoPadraoFrame, text='', height=1, width=46, anchor="e")
        self.resultadoAnteriorPadraoLabel.place(x=-15, y=0)
        



        self.porcentagemPadraoButton = Button(self.fundoFramePadrao, text='%', height=3, width=10, bd=0, command= self.clickPorcentagemPadrao)
        self.porcentagemPadraoButton.place(x=2, y=209)
        self.limparLinhaPadraoButton = Button(self.fundoFramePadrao, text='CE', height=3, width=10, bd=0, command = self.apagarLinhaValorPadrao)
        self.limparLinhaPadraoButton.place(x=80, y=209)
        self.limparGeralPadraoButton = Button(self.fundoFramePadrao, text='C', height=3, width=10, bd=0, command= self.apagarGeralValorPadrao)
        self.limparGeralPadraoButton.place(x=158, y=209)
        self.limparUltimoPadraoButton = Button(self.fundoFramePadrao, text='<-', height=3, width=10, bd=0, command= self.apagarUltimoValorPadrao)
        self.limparUltimoPadraoButton.place(x=236, y=209)

        self.bt00 = Button(self.fundoFramePadrao, text='', height=3, width=10, bd=0)
        self.bt00.place(x=2, y=264)
        self.bt01 = Button(self.fundoFramePadrao, text='x²', height=3, width=10, bd=0, command=self.clickAoQuadradoPadrao)
        self.bt01.place(x=80, y=264)
        self.bt02 = Button(self.fundoFramePadrao, text='√', height=3, width=10, bd=0, command=self.clickRaizPadrao)
        self.bt02.place(x=158, y=264)
        self.divisaoPadraoButton = Button(self.fundoFramePadrao, text='/', height=3, width=10, bd=0, command= lambda:self.clickTipoSinalPadrao("/"))
        self.divisaoPadraoButton.place(x=236, y=264)

        self.numeroSetePadraoButton = Button(self.fundoFramePadrao, text='7', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("7"))
        self.numeroSetePadraoButton.place(x=2, y=319)
        self.numeroOitoPadraoButton = Button(self.fundoFramePadrao, text='8', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("8"))
        self.numeroOitoPadraoButton.place(x=80, y=319)
        self.numeroNovePadraoButton = Button(self.fundoFramePadrao, text='9', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("9"))
        self.numeroNovePadraoButton.place(x=158, y=319)
        self.multiplicacaoPadraoButton = Button(self.fundoFramePadrao, text='X', height=3, width=10, bd=0, command=lambda:self.clickTipoSinalPadrao("*"))
        self.multiplicacaoPadraoButton.place(x=236, y=319)

        self.numeroQuatroPadraoButton = Button(self.fundoFramePadrao, text='4', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("4"))
        self.numeroQuatroPadraoButton.place(x=2, y=374)
        self.numeroCincoPadraoButton = Button(self.fundoFramePadrao, text='5', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("5"))
        self.numeroCincoPadraoButton.place(x=80, y=374)
        self.numeroSeisPadraoButton = Button(self.fundoFramePadrao, text='6', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("6"))
        self.numeroSeisPadraoButton.place(x=158, y=374)
        self.subtracaoPadraoButton = Button(self.fundoFramePadrao, text='-', height=3, width=10, bd=0, command= lambda:self.clickTipoSinalPadrao("-"))
        self.subtracaoPadraoButton.place(x=236, y=374)

        self.numeroUmPadraoButton = Button(self.fundoFramePadrao, text='1', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("1"))
        self.numeroUmPadraoButton.place(x=2, y=429)
        self.numeroDoisPadraoButton = Button(self.fundoFramePadrao, text='2', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("2"))
        self.numeroDoisPadraoButton.place(x=80, y=429)
        self.numeroTresPadraoButton = Button(self.fundoFramePadrao, text='3', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("3"))
        self.numeroTresPadraoButton.place(x=158, y=429)
        self.somaPadraoButton = Button(self.fundoFramePadrao, text='+', height=3, width=10, bd=0, command=lambda:self.clickTipoSinalPadrao("+"))
        self.somaPadraoButton.place(x=236, y=429)

        self.maisOuMenosPadraoButton = Button(self.fundoFramePadrao, text='+/-',  height=3, width=10, bd=0, command= self.colocarNegativoPadrao)
        self.maisOuMenosPadraoButton.place(x=2, y=484)
        self.numeroZeroPadraoButton = Button(self.fundoFramePadrao, text='0', height=3, width=10, bd=0, command=lambda: self.clickNumeroPadrao("0"))
        self.numeroZeroPadraoButton.place(x=80, y=484)
        self.virgulaPadraoButton = Button(self.fundoFramePadrao, text=',', height=3, width=10, bd=0, command = self.clickVirgulaPadrao)
        self.virgulaPadraoButton.place(x=158, y=484)
        self.igualPadraoButton = Button(self.fundoFramePadrao, text='=', height=3, width=10, bd=0, command= lambda:self.realizarCalculoPadrao("igual"))
        self.igualPadraoButton.place(x=236, y=484)

        #Variaveis da Calculadora Padrão
        self.atualCalculadora = "self.fundoFramePadrao"
        self.atualCalculdoraFuncao = "self.abrirCalculadoraPadrao()"
        self.valorPrimeiraLinhapadrao = ""
        self.tipoPadrao = ""
        self.tipoDoResultadoPadrao = ""
        self.valorSegundaLinhaPadrao = ""
        self.resultadoDeCalculoPadrao = 0
        self.virgulasPrimeiroLadoPadrao = 0
        self.virgulasSegundoLadoPadrao = 0
        self.ladoPadrao = 0
        self.strValorPrimeiraPadrao = ""
        self.strValorSegundaPadrao = ""

        #Binds de telcado
        self.JanelaApp.bind("1", lambda x: self.clickNumeroPadrao("1"))
        self.JanelaApp.bind("2", lambda x: self.clickNumeroPadrao("2"))
        self.JanelaApp.bind("3", lambda x: self.clickNumeroPadrao("3"))
        self.JanelaApp.bind("4", lambda x: self.clickNumeroPadrao("4"))
        self.JanelaApp.bind("5", lambda x: self.clickNumeroPadrao("5"))
        self.JanelaApp.bind("6", lambda x: self.clickNumeroPadrao("6"))
        self.JanelaApp.bind("7", lambda x: self.clickNumeroPadrao("7"))
        self.JanelaApp.bind("8", lambda x: self.clickNumeroPadrao("8"))
        self.JanelaApp.bind("9", lambda x: self.clickNumeroPadrao("9"))
        self.JanelaApp.bind("0", lambda x: self.clickNumeroPadrao("0"))
        self.JanelaApp.bind(",", lambda x: self.clickVirgulaPadrao())
        self.JanelaApp.bind("=", lambda x: self.realizarCalculoPadrao("igual"))
        self.JanelaApp.bind("<BackSpace>", lambda x: self.apagarUltimoValorPadrao())
        self.JanelaApp.bind("+", lambda x: self.clickTipoSinalPadrao(" + "))
        self.JanelaApp.bind("-", lambda x: self.clickTipoSinalPadrao(" - "))
        self.JanelaApp.bind("*", lambda x: self.clickTipoSinalPadrao(" * "))
        self.JanelaApp.bind("/", lambda x: self.clickTipoSinalPadrao(" / "))
        self.JanelaApp.bind("<Return>	", lambda x: self.realizarCalculoPadrao(("igual")))

        #aplicação de tema
        self.fundoFramePadrao.config(bg=self.tema['BackGround4'])
        self.menuButton.config(bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.tipoCalculadoraLabel.config(bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.historicoPadraoButton.config(bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.resultadoPadraoFrame.config(bg=self.tema['BackGround4'])
        self.resultadoPadraoLabel.config(bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.resultadoAnteriorPadraoLabel.config(bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.porcentagemPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.limparLinhaPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.limparGeralPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.limparUltimoPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.bt00.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.bt01.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.bt02.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.divisaoPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.numeroSetePadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroOitoPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroNovePadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.multiplicacaoPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.numeroQuatroPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroCincoPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroSeisPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.subtracaoPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.numeroUmPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroDoisPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroTresPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.somaPadraoButton.config(bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.maisOuMenosPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroZeroPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.virgulaPadraoButton.config(bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.igualPadraoButton.config(bg=self.tema['BackGround3'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround3'], activeforeground=self.tema['ForeGround1'])

    def abrirHistoricoPadrao(self):
        #Cria o frame do historio
        self.YHistoricoPadrao = 0
        self.fundoHistoricoJanelaPadrao = Frame(self.JanelaApp, width=328, height=329, bg=self.tema['BackGround2'])
        self.fundoHistoricoJanelaPadrao.place(x=0, y=209)
        self.fundoHistoricoPadrao = Frame(self.fundoHistoricoJanelaPadrao, width=328, height=50000, bg=self.tema['BackGround2'])
        self.fundoHistoricoPadrao.place(x=0, y=self.YHistoricoPadrao)

        #Faz o historico lendo o ultimo historico do usuario e detecta o tamanho o historico para pode colocar
        #a barra de rolar e o button para apagar o historico
        valoresHitorico = []
        y = 0
        varlen = (len(self.historicoCalculadoras)) - 1
        for cont in range(len(self.historicoCalculadoras)):
            contador = abs(varlen-cont)
            valoresHitorico.append(Button(self.fundoHistoricoPadrao, bg=self.tema['BackGround2'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround3'], bd=0 ,text =self.historicoCalculadoras[contador], 
            justify ="right", width =70, height =3, 
            command=lambda c=contador: self.definirEquacaoDoHistoricoPadrao(self.historicoCalculadoras[c])))
            valoresHitorico[cont].place(x=0, y=y)
            y += 60


        if len(self.historicoCalculadoras) > 6:
            self.setaSubirPadrao = Button(self.fundoHistoricoJanelaPadrao, text='˄', bd=0, command=lambda: self.scrollPadrao("subir"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround3'], width=3)
            self.setaSubirPadrao.place(x=290, y=0)

            self.setaBaixarPadrao = Button(self.fundoHistoricoJanelaPadrao, text='˅', bd=0, command=lambda: self.scrollPadrao("baixar"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround3'], width=3)
            self.setaBaixarPadrao.place(x=290, y=308)
        
        if len(self.historicoCalculadoras) > 0:
            self.apagarHistoricoPadrao = Button(self.fundoHistoricoJanelaPadrao, text='C', bd=0, width= 5, height=2, bg=self.tema['BackGround3'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround3'], command=self.apagarHistoricoCalculadoraPadrao)
            self.apagarHistoricoPadrao.place(x=15, y=280)
        
        if len(self.historicoCalculadoras) == 0:
            self.semHistoricoLabel = Label(self.fundoHistoricoPadrao, text='Não existe historico', bg=self.tema['BackGround2'], fg=self.tema['ForeGround2'], width=15)
            self.semHistoricoLabel.place(x=15,y=15)

        #Coloca o command no button para poder fechar o historico
        self.historicoPadraoButton.config(command=self.fecharHistoricoPadrao)

    def apagarHistoricoCalculadoraPadrao(self):
        #Def para apagar o historico do usuario (GERAL)
        with open(f'{LOCAL}files/data/historics.json', 'w', encoding="utf8") as historico:
            json.dump([], historico)
        self.lerInformacoes()
        self.fecharHistoricoPadrao()
        self.abrirHistoricoPadrao()

    def scrollPadrao(self, var):
        #def do Scroll / barra de rolagem
        if var == "baixar":
            self.YHistoricoPadrao -= 15
        elif var == "subir":
            self.YHistoricoPadrao += 15
        
        self.fundoHistoricoPadrao.place(x=0, y=self.YHistoricoPadrao)

    def definirEquacaoDoHistoricoPadrao(self, var):
        #coloca as equações no qual o usuario fez... (historico)
        if   var.find("+") > 0:
            afind = var.find("+")
        elif var.find("*") > 0:
            afind = var.find("*")
        elif var.find("/") > 0:
            afind = var.find("/")
        elif var.find("-") > 0:
            afind = var.find("-")
        
        afind2 = var.find("=")
        self.valorPrimeiraLinhapadrao = var[0:afind]
        self.valorSegundaLinhaPadrao =  var[afind+1:afind2]
        self.tipoPadrao = var[afind]
        self.resultadoDeCalculoPadrao = var[3+afind2:]
        self.tipoDoResultadoPadrao = "historico"

        if str(self.resultadoDeCalculoPadrao).count(".") >= 1:
            self.virgulasPrimeiroLadoPadrao = 1

        self.ladoPadrao = 1
        self.colocarNaTelaAnteriorPadrao(f"{self.valorPrimeiraLinhapadrao} {self.tipoPadrao} {self.valorSegundaLinhaPadrao} = ", True)
        self.colocarNaTelaPadrao(self.resultadoDeCalculoPadrao)
        self.valorPrimeiraLinhapadrao = self.resultadoDeCalculoPadrao
        self.valorSegundaLinhaPadrao = ""
        self.fecharHistoricoPadrao()

    def fecharHistoricoPadrao(self):
        #Fecha o historico 
        self.fundoHistoricoJanelaPadrao.destroy()
        self.historicoPadraoButton.config(command=self.abrirHistoricoPadrao)

    def clickPorcentagemPadrao(self):
        #Calcula 1% do valor que o usuario digitou caso ele nao tenho escolhido mais de um valor
        if self.ladoPadrao == 0:
            self.resultadoAnteriorPadraoLabel.config(text=(f'1% {self.valorPrimeiraLinhapadrao} = {str(float(self.valorPrimeiraLinhapadrao) * 0.01)}').replace(".", ","))
            self.valorPrimeiraLinhapadrao = str(float(self.valorPrimeiraLinhapadrao) * 0.01)
            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)
        #Calcula a porcentagem com base no primeiro valor colocado pelo usuario
        #Ex: primeiro valor = 1000, segundo valor = 1, ele ira calcular quanto é 1% de 1000
        elif self.ladoPadrao == 1:
            if float(self.valorSegundaLinhaPadrao) < 10:
                self.valorSegundaLinhaPadrao = "0.0"+self.valorSegundaLinhaPadrao.replace(".","")
            else:
                self.valorSegundaLinhaPadrao = "0."+self.valorSegundaLinhaPadrao.replace(".","")

            self.valorSegundaLinhaPadrao = float(self.valorPrimeiraLinhapadrao) * float(self.valorSegundaLinhaPadrao)
            self.valorSegundaLinhaPadrao = str(self.valorSegundaLinhaPadrao)

            self.resultadoAnteriorPadraoLabel.config(text=((f"{self.valorPrimeiraLinhapadrao} {self.tipoPadrao} {self.valorSegundaLinhaPadrao}").replace("*", "x")).replace(".",","))
            self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)
            
    def clickRaizPadrao(self):
        #Calcula a raiz quadrada que o usario colocou
        if self.ladoPadrao == 0:
            self.strValorPrimeiraPadrao = (f"√({self.valorPrimeiraLinhapadrao})")
            self.valorPrimeiraLinhapadrao = math.sqrt(float(self.valorPrimeiraLinhapadrao))
            self.valorPrimeiraLinhapadrao = '{:.2f}'.format(self.valorPrimeiraLinhapadrao)

            self.colocarNaTelaAnteriorPadrao(self.strValorPrimeiraPadrao)
            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)

        
        if self.ladoPadrao == 1:
            self.strValorSegundaPadrao = (f"√({self.valorSegundaLinhaPadrao})")
            self.valorSegundaLinhaPadrao = math.sqrt(float(self.valorSegundaLinhaPadrao))
            self.valorSegundaLinhaPadrao = '{:.2f}'.format(self.valorSegundaLinhaPadrao)

            if self.strValorPrimeiraPadrao == "":
                self.colocarNaTelaAnteriorPadrao(f"{self.valorPrimeiraLinhapadrao} {self.tipoPadrao} {self.strValorSegundaPadrao}")
            else:
                self.colocarNaTelaAnteriorPadrao(f"{self.strValorPrimeiraPadrao} {self.tipoPadrao} {self.strValorSegundaPadrao}")

            self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)
 
    def clickAoQuadradoPadrao(self):
        #Calcula o valor ao quadrado que o usuario colocou
        self.strValorPrimeiraPadrao = ""
        self.strValorSegundaPadrao = ""
        

        if self.ladoPadrao == 0:
            self.strValorPrimeiraPadrao = (f"x²({self.valorPrimeiraLinhapadrao})")
            self.valorPrimeiraLinhapadrao = float(self.valorPrimeiraLinhapadrao) * float(self.valorPrimeiraLinhapadrao)
            self.resultadoAnteriorPadraoLabel.config(text=(self.strValorPrimeiraPadrao).replace(".",","))
            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)

        if self.ladoPadrao == 1:
            self.strValorSegundaPadrao = (f"x²({self.valorSegundaLinhaPadrao})")
            self.valorSegundaLinhaPadrao = float(self.valorSegundaLinhaPadrao) * float(self.valorSegundaLinhaPadrao)
            valor = f"{self.valorPrimeiraLinhapadrao} {self.tipoPadrao} {self.strValorSegundaPadrao}"

            self.resultadoAnteriorPadraoLabel.config(text=valor.replace(".",","))

            self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)
 
    def clickNumeroPadrao(self, var):
        #Coloca o valor clicado na tela ou digitado no teclado
        if self.tipoDoResultadoPadrao == "igual":
            self.tipoDoResultadoPadrao = ""
            self.valorSegundaLinhaPadrao = ""
            self.valorPrimeiraLinhapadrao = ""
            self.virgulasPrimeiroLadoPadrao = 0
            self.virgulasSegundoLadoPadrao = 0
            self.apagarGeralValorPadrao()


        #Lado 01
        if self.ladoPadrao == 0 and len(self.valorPrimeiraLinhapadrao) < 16:
            if not (self.valorPrimeiraLinhapadrao == "" and var == "0"):
                self.valorPrimeiraLinhapadrao += var
                self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)
                self.resultadoAnteriorPadraoLabel.config(text="")

        #Lado 02
        elif self.ladoPadrao == 1 and len(self.valorSegundaLinhaPadrao) < 16:
            if not (self.valorSegundaLinhaPadrao == "" and var == "0"):
                self.valorSegundaLinhaPadrao += var
                self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)  

    def colocarNaTelaPadrao(self, var, analisar = False):
        #Coloca na tela abaixo substituindo pontos por virgulas e retira os ,0
        var = str(var)
        var2 = float(var)

        if analisar == True:
            if int(var2) != float(var2):
                self.resultadoPadraoLabel.config(text= var.replace(".",","))
            else:
                self.resultadoPadraoLabel.config(text= str(int(var2)).replace(".",","))
        else:
            self.resultadoPadraoLabel.config(text= var.replace(".",","))

        #Detecta o tamanho do valor colocado para poder diminuir a fonte 
        if len(var) > 9:
            self.resultadoPadraoLabel.config(font='arial 25', width=17)

    def colocarNaTelaAnteriorPadrao(self, var, analisar=False):
        #Coloca na tela acima da normal a equação anterior e substitui os ,0 e os * por X e pontos por virgulas
        if analisar == True:
            self.resultadoAnteriorPadraoLabel.config(text=((var).replace("*", "x")).replace(".",","))
        else:
            try: 
                var2 = int(self.valorPrimeiraLinhapadrao)
            except:
                var2 = float(self.valorPrimeiraLinhapadrao)
            if int(var2) != float(self.valorPrimeiraLinhapadrao):
                self.resultadoAnteriorPadraoLabel.config(text=(var.replace("*", "x",)).replace(".",","))
            else:
                self.resultadoAnteriorPadraoLabel.config(text=(f'{int(var2)} {self.tipoPadrao}').replace("*", "x",))

    def colocarNegativoPadrao(self):
        #Transforma o valor em negativo e caso ele ja tenha calculado e tido o resultado coloca o valor de
        #reusltado como negativo
        if self.tipoDoResultadoPadrao == "igual":
            self.tipoDoResultadoPadrao = ""
            self.valorSegundaLinhaPadrao == ""
            self.virgulasSegundoLadoPadrao = 0
            self.virgulasPrimeiroLadoPadrao = str(self.resultadoDeCalculoPadrao.find("."))
            self.valorPrimeiraLinhapadrao = self.resultadoDeCalculoPadrao
            self.valorPrimeiraLinhapadrao = f"-{self.valorPrimeiraLinhapadrao}"
            self.colocarNaTelaAnteriorPadrao("")
            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)
            self.ladoPadrao = 0
            return

        if self.ladoPadrao == 0:
            if str(self.valorPrimeiraLinhapadrao).count("-") == 1:
                try:
                   self.valorPrimeiraLinhapadrao = str(self.valorPrimeiraLinhapadrao).replace("-", "")
                except:
                    pass
                self.valorPrimeiraLinhapadrao = f"{self.valorPrimeiraLinhapadrao}"
            else:
                try:
                    self.valorPrimeiraLinhapadrao = str(self.valorPrimeiraLinhapadrao).replace("+", "")
                except:
                    pass
                self.valorPrimeiraLinhapadrao = f"-{self.valorPrimeiraLinhapadrao}"

            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)

        if self.ladoPadrao == 1:
            if str(self.valorSegundaLinhaPadrao).count("-") == 1:
                try:
                    self.valorSegundaLinhaPadrao = str(self.valorSegundaLinhaPadrao).replace("-", "")
                except:
                    pass
                self.valorSegundaLinhaPadrao = f"{self.valorSegundaLinhaPadrao}"
            else:
                try:
                    self.valorSegundaLinhaPadrao = str(self.valorSegundaLinhaPadrao).replace("+", "")
                except:
                    pass
                self.valorSegundaLinhaPadrao = f"-{self.valorSegundaLinhaPadrao}"

            
            self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)

    def clickVirgulaPadrao(self):
        #Def Responsavel por colocar as virgulas e evitar que exista mais de uma virgula na tela
        #E caso nao exista valor ele colocar 0,

        if self.tipoDoResultadoPadrao == "igual":
            self.tipoDoResultadoPadrao = ""
            self.valorPrimeiraLinhapadrao = "0."
            self.valorSegundaLinhaPadrao = ""
            self.colocarNaTelaAnteriorPadrao("")
        #Lado 01
        if self.virgulasPrimeiroLadoPadrao == 0 and self.ladoPadrao == 0:
            if self.valorPrimeiraLinhapadrao == "":
                self.valorPrimeiraLinhapadrao += ("0")
                self.valorPrimeiraLinhapadrao += (".")
            else:
                self.valorPrimeiraLinhapadrao += (".")

            self.virgulasPrimeiroLadoPadrao = 1
            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)

        #Lado 02
        if self.virgulasSegundoLadoPadrao == 0 and self.ladoPadrao == 1:
            if self.valorSegundaLinhaPadrao == "":
                self.valorSegundaLinhaPadrao += ("0")
                self.valorSegundaLinhaPadrao += (".")
            else:
                self.valorSegundaLinhaPadrao += (".")

            self.virgulasSegundoLadoPadrao = 1
            self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)  

    def clickTipoSinalPadrao(self, tipo):
        if self.ladoPadrao == 0 and float(self.valorPrimeiraLinhapadrao) != 0 :
            #Cria variavel com o sinal escolhido do usuario
            self.tipoPadrao = tipo

            self.colocarNaTelaAnteriorPadrao(f'{self.valorPrimeiraLinhapadrao} {self.tipoPadrao}')
            self.ladoPadrao = 1

        #Faz o calculo e deixa pronto para fazer o calculo novamente e permite a alteracao de sinais no meio da operação
        elif self.ladoPadrao == 1:
            if self.valorSegundaLinhaPadrao == "":
                self.tipoPadrao = tipo
                self.colocarNaTelaAnteriorPadrao(f'{self.valorPrimeiraLinhapadrao} {self.tipoPadrao}')
            else:
                self.tipoPadraoDois = tipo
                self.realizarCalculoPadrao("tipo")
                self.valorPrimeiraLinhapadrao = self.resultadoDeCalculoPadrao
                self.colocarNaTelaAnteriorPadrao(f'{self.resultadoDeCalculoPadrao} {self.tipoPadraoDois}')
                self.valorSegundaLinhaPadrao = ""

    def realizarCalculoPadrao(self, var):
        #Faz os calculos da equação e ja coloca na tela
        self.resultadoDeCalculoPadrao = str(eval(f'{float(self.valorPrimeiraLinhapadrao)} {self.tipoPadrao} {float(self.valorSegundaLinhaPadrao)}'))
        self.resultadoDeCalculoPadrao = str(self.resultadoDeCalculoPadrao)
        self.colocarNaTelaPadrao(self.resultadoDeCalculoPadrao, True)
        self.colocarNaTelaAnteriorPadrao(f'{self.valorPrimeiraLinhapadrao} {self.tipoPadrao} {self.valorSegundaLinhaPadrao} =', True)
        self.historicoCalculadoras.append(f"{self.valorPrimeiraLinhapadrao} {self.tipoPadrao} {self.valorSegundaLinhaPadrao} =\n {self.resultadoDeCalculoPadrao}")
        #Salva o calculo no historico
        with open(f'{LOCAL}files/data/historics.json', 'w', encoding="utf8") as historico:
            json.dump(self.historicoCalculadoras, historico)
        
        #Detecta o tipo de button que chamou a função para pode fazer ou calculos constantes ou fechar ja o resutlado
        if var == "tipo":
            self.tipoDoResultadoPadrao = "tipo"
        elif var == "igual":
            self.tipoDoResultadoPadrao = "igual"

    def apagarUltimoValorPadrao(self):
        #Apaga o ultimo valor do calculo e se ficar vazio ele coloca um zero
        if self.tipoDoResultadoPadrao == "igual":
            self.tipoDoResultadoPadrao = ""
            self.ladoPadrao = 0
            self.tipoPadrao = ""
            self.valorSegundaLinhaPadrao = ""
            self.valorPrimeiraLinhapadrao = str(self.resultadoDeCalculoPadrao)
            self.virgulasSegundoLadoPadrao = 0
            self.virgulasPrimeiroLadoPadrao = 0
            self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)
            self.colocarNaTelaAnteriorPadrao("")
            if self.valorPrimeiraLinhapadrao.find(".") > 0:
                self.virgulasPrimeiroLadoPadrao = 1
            else:
                self.virgulasPrimeiroLadoPadrao = 0
            self.virgulasSegundoLadoPadrao = 0

            return
    
        if self.ladoPadrao == 0:
            if str(self.valorPrimeiraLinhapadrao[:-1]).find(".") == -1:
                self.virgulasPrimeiroLadoPadrao = 0
            self.valorPrimeiraLinhapadrao = self.valorPrimeiraLinhapadrao[:-1]
            if self.valorPrimeiraLinhapadrao == "" or self.valorPrimeiraLinhapadrao == "0":
                self.valorPrimeiraLinhapadrao = ""
                self.colocarNaTelaPadrao("0")
            else:
                self.colocarNaTelaPadrao(self.valorPrimeiraLinhapadrao)
        if self.ladoPadrao == 1:
            if str(self.valorSegundaLinhaPadrao[:-1]).find(".") == -1:
                self.virgulasSegundoLadoPadrao = 0
            self.valorSegundaLinhaPadrao = self.valorSegundaLinhaPadrao[:-1]
            if self.valorSegundaLinhaPadrao == "0" or self.valorSegundaLinhaPadrao == "":
                self.valorSegundaLinhaPadrao = ""
                self.colocarNaTelaPadrao("0")
            else:
                self.colocarNaTelaPadrao(self.valorSegundaLinhaPadrao)

    def apagarLinhaValorPadrao(self):
        #Apaga a linha completa atual
        if self.tipoDoResultadoPadrao == "igual":
            self.apagarGeralValorPadrao()

        if self.ladoPadrao == 0:
            self.virgulasPrimeiroLadoPadrao = 0
            self.valorPrimeiraLinhapadrao = ""
            self.colocarNaTelaPadrao("0")

        if self.ladoPadrao == 1:
            self.virgulasSegundoLadoPadrao = 0
            self.valorSegundaLinhaPadrao = ""
            self.colocarNaTelaPadrao("0")

    def apagarGeralValorPadrao(self):
        #Apaga toda a equação
            self.valorPrimeiraLinhapadrao = ""
            self.valorSegundaLinhaPadrao = ""
            self.virgulasSegundoLadoPadrao = 0
            self.virgulasPrimeiroLadoPadrao = 0
            self.ladoPadrao = 0
            self.resultadoDeCalculoPadrao = ""

            self.resultadoAnteriorPadraoLabel.config(text='')
            self.resultadoPadraoLabel.config(text="0")

    def abrirCalculadoraDeDatas(self):
        #Sistema de seguraça para evitar dois frames no codigo
        try:
            self.fundoFrameDatas.destroy()
        except:
            pass
        #Cria os Widgets da calculadora de datas
        self.fundoFrameDatas = Frame(self.JanelaApp, width=328, height=538, bg=self.tema['BackGround4'])
        self.fundoFrameDatas.place(x=0)

        self.menuButton = Button(self.fundoFrameDatas, text='☰', font=('Arial', 20, 'bold'), bd=0, command= lambda: self.abrirMenu(5), bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.menuButton.place(x=0, y=10)

        self.tipoCalculadoraLabel = Label(self.fundoFrameDatas, text='Calculo de datas', width=15, font=('Arial', 20, 'bold'), anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.tipoCalculadoraLabel.place(x=40, y=15)

        self.tipoButtonDatas = Button(self.fundoFrameDatas, font=('Arial', 15, 'bold'), text= "Diferença entre datas >", bd=0, bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'], command=lambda:self.trocarTipoDatas(1)) 
        self.tipoButtonDatas.place(x=15, y=92)
        

        #Variaveis para funcionamento da calculadora de datas
        

        #Cria o tema para os combobox
        try:
            comboStyle = ttk.Style()

            comboStyle.theme_create('comboStyle', parent="alt",
                            settings = {'TCombobox':
                                    {'configure':
                                    {'foreground': self.tema['ForeGround1'],
                                        'background': self.tema['BackGround4'],
                                        'selectbackground': self.tema['BackGround4'],
                                        'fieldbackground': self.tema['BackGround4']}}})

            comboStyle.theme_use('comboStyle')
        except:
            comboStyle.theme_settings('comboStyle',
                                     settings = {'TCombobox':
                                                {'configure':
                                                {'foreground': self.tema['ForeGround1'],
                                                 'background': self.tema['BackGround4'],
                                                 'selectbackground': self.tema['BackGround4'],
                                                 'fieldbackground': self.tema['BackGround4'],
                                                 'bordercolor': self.tema['BackGround4']}}})

        
        #Pega a data Atual
        data_atual = date.today()

        self.dataAtualMes = data_atual.month
        dataAtualDia = data_atual.day
        dataAtualAno = data_atual.year

        #Dependendo do tipo da calculadora ele abre widgets diferentes
        if self.tipoDatas == 1:
            self.tipoButtonDatas.config(text='< Adicionar ou subtrair dias', command=lambda: self.trocarTipoDatas(2))

        elif self.tipoDatas == 2:
            self.mesDatas = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', "Julho", 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
            self.anoDatas = ['2021','2022','2023','2024','2025'] 
            self.diaDatas = 0

            self.frameFundoTipo2Data = Frame(self.JanelaApp, width=328, height=388, bg=self.tema['BackGround4'])
            self.frameFundoTipo2Data.place(x=0, y=150)
            self.tipoButtonDatas.config(text='Diferença entre datas >', command=lambda: self.trocarTipoDatas(1))
            self.deLabelDatas = Label(self.frameFundoTipo2Data, text='De:', font=('Arial', 15, 'bold'), bd=0, bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
            self.deLabelDatas.place(x=22, y=0)
            self.diaComboDatas = ttk.Combobox(self.frameFundoTipo2Data, state="readonly", font=('Arial', 13, 'bold'), width = 3, values=self.diaDatas, postcommand= lambda:self.detectarDiasDoMesDatas(self.anoComboDatas, self.mesComboDatas,self.diaComboDatas))
            self.diaComboDatas.place(x=22, y=40)
            self.mesComboDatas = ttk.Combobox(self.frameFundoTipo2Data, state="readonly", font=('Arial', 13, 'bold'), width = 15, values=self.mesDatas)
            self.mesComboDatas.place(x=65, y=40)
            self.anoComboDatas = ttk.Combobox(self.frameFundoTipo2Data, state="readonly", font=('Arial', 13, 'bold'), width = 5, values=self.anoDatas)
            self.anoComboDatas.place(x=218, y=40)

            self.diaComboDatas.set(dataAtualDia)
            self.mesComboDatas.set(f'de {self.mesDatas[self.dataAtualMes-1]} de')
            self.anoComboDatas.set(dataAtualAno)

            self.diaComboDatas.bind("<<ComboboxSelected>>", self.calcularDatasTipo2)
            self.mesComboDatas.bind("<<ComboboxSelected>>", self.calcularDatasTipo2)
            self.anoComboDatas.bind("<<ComboboxSelected>>", self.calcularDatasTipo2)

            self.deLabelDatas = Label(self.frameFundoTipo2Data, text='Até:', font=('Arial', 15, 'bold'), bd=0, bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
            self.deLabelDatas.place(x=22, y=100)
            self.diaComboDoisDatas = ttk.Combobox(self.frameFundoTipo2Data, state="readonly", font=('Arial', 13, 'bold'), width = 3, values=self.diaDatas, postcommand= lambda:self.detectarDiasDoMesDatas(self.anoComboDoisDatas, self.mesComboDoisDatas,self.diaComboDoisDatas))
            self.diaComboDoisDatas.place(x=22, y=140)
            self.mesComboDoisDatas = ttk.Combobox(self.frameFundoTipo2Data, state="readonly", font=('Arial', 13, 'bold'), width = 15, values=self.mesDatas)
            self.mesComboDoisDatas.place(x=65, y=140)
            self.anoComboDoisDatas = ttk.Combobox(self.frameFundoTipo2Data, state="readonly", font=('Arial', 13, 'bold'), width = 5, values=self.anoDatas)
            self.anoComboDoisDatas.place(x=218, y=140)

            self.diaComboDoisDatas.set(dataAtualDia)
            self.mesComboDoisDatas.set(f'de {self.mesDatas[self.dataAtualMes-1]} de')
            self.anoComboDoisDatas.set(dataAtualAno)

            self.diaComboDoisDatas.bind("<<ComboboxSelected>>", self.calcularDatasTipo2)
            self.mesComboDoisDatas.bind("<<ComboboxSelected>>", self.calcularDatasTipo2)
            self.anoComboDoisDatas.bind("<<ComboboxSelected>>", self.calcularDatasTipo2)

            self.respostaLabelTipo2DoisData = Label(self.frameFundoTipo2Data, text='', font=('Arial', 12, 'bold'), bd=0, bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'], anchor=W)            
            self.respostaLabelTipo2DoisData.place(x=22, y=200)
            self.respostaLabelTipo2Data = Label(self.frameFundoTipo2Data, text='Mesma Data', font=('Arial', 12, 'bold'), bd=0, bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'], anchor=W)            
            self.respostaLabelTipo2Data.place(x=22, y=190)

            self.calcularDatasTipo2()

        #Variaveis da Calculadora de datas para geral
        self.atualCalculadora = "self.fundoFrameDatas"
        self.atualCalculdoraFuncao = "self.abrirCalculadoraDeDatas()"

    def detectarDiasDoMesDatas(self, anoWidget, mesWidget, diaWidget):
        #Calcula a quantidade de dias do mes, analisando ano bissexto e o mes colocado
        mesesEdias = [{"janeiro" : 31}, {"fevereiro" : 28}, {"março" : 31},{"abril" : 30},
                      {"maio" : 31},{"junho" : 30},{"julho" : 31},{"agosto" : 31},
                      {"setembro" : 30},{"outubro" : 31},{"novembro" : 30}, {"dezembro" : 30}]

        ano = anoWidget.get()
        mes = ((mesWidget.get()).replace("de", '')).replace(" ", "")
        dia = 0

        if (int(ano) % 4) == 0:
            mesesEdias[1]["fevereiro"] = 29

        for cont in range(len(mesesEdias)):
            try:
                dia = mesesEdias[cont][mes.lower()]
            except:
                pass
                
        



        self.diaDatas = []
        for cont in range(0,dia):
            self.diaDatas.append(str(cont+1)) 

        diaWidget.config(values=self.diaDatas)

    def trocarTipoDatas(self, var):
        #Troca o tipo de calculo de data
        if var == 1:
            self.tipoButtonDatas.config(text='< Adicionar ou subtrair dias', command=lambda: self.trocarTipoDatas(2))
            self.tipoDatas = 1
            self.frameFundoTipo2Data.destroy()

        elif var == 2:
            self.tipoButtonDatas.config(text='Diferença entre datas >', command=lambda: self.trocarTipoDatas(1))
            self.tipoDatas = 2

        self.fundoFrameDatas.destroy()
        self.abrirCalculadoraDeDatas()

    def calcularDatasTipo2(self, *args):
        #Configuração: 1 = Primeira data, 2 = Segunda data, ex: mes2 = mes da segunda data
        #pega os valores que o usuario escolheu atraves do combobox
        ano1 = self.anoComboDatas.get()
        mes1 = ((self.mesComboDatas .get()).replace("de", '')).replace(" ", "")
        dia1 = self.diaComboDatas.get()

        self.mesComboDatas.set(f"de {mes1} de")

        ano2 = self.anoComboDoisDatas.get()
        mes2 = ((self.mesComboDoisDatas.get()).replace("de", '')).replace(" ", "")
        dia2 = self.diaComboDoisDatas.get()

        self.mesComboDoisDatas.set(f"de {mes2} de")

        #Transforma o mes em numero ex: novembro = 11
        mes1 = (self.mesDatas.index(mes1) + 1) 
        mes2 = (self.mesDatas.index(mes2) + 1)
        
        #Transforma os valores em um type datatime para pode usar a biblioteca e calcular o valor em dias 
        #sem margem de erro
        data1 = datetime.strptime(f'{ano1}-{mes1}-{dia1}', '%Y-%m-%d')

        data2 = datetime.strptime(f'{ano2}-{mes2}-{dia2}', '%Y-%m-%d')

        self.resultadoData = abs((data1 - data2).days)

        #Criar variaveis de AnoInicial/final e bissexto para poder ter os valores mais precisos
        anoInicial = 0
        anoFinal = 0
        bissexto = 0

        #Detecta qual o menor ano para poder ver onde inica o calculo
        if int(ano1) > int(ano2):
            anoInicial = int(ano2)
            anoFinal = int(ano1)
        else:
            anoInicial = int(ano1)
            anoFinal = int(ano2)

        #Calcula a diferenca entre os anos
        diferencaDosAnos = anoFinal - anoInicial

        #Calculaa qual ano dentro da margem escolhida é bissexto 
        for cont in range(diferencaDosAnos+1):
            if (anoInicial + cont) % 4 == 0:
                bissexto += 1

        #Se os dias dos anos forem mais do que os dias totais subtrai um tendo em vista que nao passou um ano
        if ((diferencaDosAnos * 365) + bissexto) > self.resultadoData:
            diferencaDosAnos -= 1   

        #Calcula a quantidade de meses e dias
        meses = abs(((diferencaDosAnos * 365) + bissexto) - self.resultadoData)
        quantidadeMeses = 0

        while meses > 30:
            quantidadeMeses += 1
            meses -= 30

        #Ve se ainda tem semanas e se tiver calcula a quantidade de semanas
        semanas = int(meses / 7)

        #Calcula a quantidade de dias
        dias = abs((int(semanas) * 7) - meses)
        data = ""

        #Faz o tratamento de String para poder entregar apenas valores objetivos e evitar valore como
        #0 dias ou etc
        if self.resultadoData == 0:
            data = "Mesmas Datas"
            self.respostaLabelTipo2DoisData.config(text='')
        else:
            self.respostaLabelTipo2DoisData.config(text=f'\n{self.resultadoData} dias ')
        if int(diferencaDosAnos) > 0: 
            data += f'{diferencaDosAnos} anos '
        if int(quantidadeMeses) > 0:
            data += f'{quantidadeMeses} meses '
        if int(semanas) > 0:
            data += f'{semanas} semanas '
        if int(dias) > 0:
            data += f'{dias} dias '

        #Coloca os valores na tela
        self.respostaLabelTipo2Data.config(text=data)

    def abrirConversorMoedas(self):
        #Sistema de seguraça para evitar dois frames no codigo
        try:
            self.fundoFrameMoedas.destroy()
        except:
            pass

        #Cria o tema para os combobox
        try:
            comboStyle = ttk.Style()

            comboStyle.theme_create('comboStyle', parent="alt",
                            settings = {'TCombobox':
                                    {'configure':
                                    {'foreground': self.tema['ForeGround1'],
                                        'background': self.tema['BackGround4'],
                                        'selectbackground': self.tema['BackGround4'],
                                        'fieldbackground': self.tema['BackGround4'],
                                        'bordercolor': self.tema['BackGround4']}}})

            comboStyle.theme_use('comboStyle')
        except:
            comboStyle.theme_settings('comboStyle',
                            settings = {'TCombobox':
                                    {'configure':
                                    {'foreground': self.tema['ForeGround1'],
                                        'background': self.tema['BackGround4'],
                                        'selectbackground': self.tema['BackGround4'],
                                        'fieldbackground': self.tema['BackGround4'],
                                        'bordercolor': self.tema['BackGround4']}}})

        #Variaveis necessarias
        self.moedas =["Real Brasileiro - BRL",
                      "Peso Uruguaio - UYU",
                      "Guarani Paraguaio - PYG",
                      "Franco CFA Ocidental - XOF",
                      "Dólar do Caribe Oriental - XCD",
                      "Nova Libra Turca - TRY",
                      "Dólar Namíbio - NAD",
                      "Coroa Islandesa - ISK",
                      "Peso Argentino - ARS",
                      "Boliviano - BOB",
                      "Peso Chileno - CLP",
                      "Rial Catarense - QAR",
                      "Rúpia Paquistanesa - PKR",
                      "Dólar de Cingapura - SGD",
                      "Dólar Australiano - AUD",
                      "Litecoin - LTC",
                      "Dólar Taiuanês - TWD",
                      "Balboa Panamenho - PAB",
                      "Euro - EUR",
                      "Dólar Americano - USD",
                      "Peso Mexicano - MXN",
                      "Iene Japonês - JPY"]   
        self.cifroes = []
        self.ciglasMoedas =["BRL",
                            "UYU",
                            "PYG",
                            "XOF",
                            "XCD",
                            "TRY",
                            "NAD",
                            "ISK",
                            "ARS",
                            "BOB",
                            "CLP",
                            "QAR",
                            "PKR",
                            "SGD",
                            "AUD",
                            "LTC",
                            "TWD", 
                            "PAB",
                            "EUR",
                            "USD",
                            "MXN",
                            "JPY"]
        self.primeiroValorMoeda = ''
        self.segundoValorMoeda = ''
        self.virgulasMoedas = False

        #Cria os Widgets da calculadora de datas
        self.fundoFrameMoedas = Frame(self.JanelaApp, width=328, height=538, bg=self.tema['BackGround4'])
        self.fundoFrameMoedas.place(x=0)

        self.menuButton = Button(self.fundoFrameMoedas, text='☰', font=('Arial', 20, 'bold'), bd=0, command= lambda: self.abrirMenu(5), bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.menuButton.place(x=0, y=10)

        self.tipoConversorLabel = Label(self.fundoFrameMoedas, text='Moedas', width=15, font=('Arial', 20, 'bold'), anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.tipoConversorLabel.place(x=40, y=15)

        self.MoedasAtualLabel = Label(self.fundoFrameMoedas, text='0', font='arial 40', width=40, anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.MoedasAtualLabel.place(x=22, y=50)
        self.Moeda1ComboBox = ttk.Combobox(self.fundoFrameMoedas, state="readonly", font=('Arial', 10, 'bold'), width = 35, values=self.moedas)
        self.Moeda1ComboBox.place(x=22, y=120)
        self.MoedasResultadoLabel = Label(self.fundoFrameMoedas, text='0', font='arial 40', width=40, anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.MoedasResultadoLabel.place(x=22, y=150)
        self.Moeda2ComboBox = ttk.Combobox(self.fundoFrameMoedas, state="readonly", font=('Arial', 10, 'bold'), width = 35, values=self.moedas)
        self.Moeda2ComboBox.place(x=22, y=220)
        self.MoedasResultadoOutrosLabel = Label(self.fundoFrameMoedas, text='', font='arial 30', width=9, anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.MoedasResultadoOutrosLabel.place(x=22, y=250)
        
        self.Moeda1ComboBox.bind("<<ComboboxSelected>>", self.trocarMoeda)
        self.Moeda2ComboBox.bind("<<ComboboxSelected>>", self.trocarMoeda)

        #Lê informações ou coloca para o usuario
        self.Moeda1ComboBox.set(self.Moeda1)
        self.Moeda2ComboBox.set(self.Moeda2)

        #Teclado Numerico
        self.numeroSeteMoedasButton = Button(self.fundoFrameMoedas, text='7', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("7"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroSeteMoedasButton.place(x=2, y=319)
        self.numeroOitoMoedasButton = Button(self.fundoFrameMoedas, text='8', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("8"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroOitoMoedasButton.place(x=80, y=319)
        self.numeroNoveMoedasButton = Button(self.fundoFrameMoedas, text='9', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("9"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroNoveMoedasButton.place(x=158, y=319)

        self.numeroQuatroMoedasButton = Button(self.fundoFrameMoedas, text='4', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("4"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroQuatroMoedasButton.place(x=2, y=374)
        self.numeroCincoMoedasButton = Button(self.fundoFrameMoedas, text='5', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("5"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroCincoMoedasButton.place(x=80, y=374)
        self.numeroSeisMoedasButton = Button(self.fundoFrameMoedas, text='6', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("6"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroSeisMoedasButton.place(x=158, y=374)

        self.numeroUmMoedasButton = Button(self.fundoFrameMoedas, text='1', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("1"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroUmMoedasButton.place(x=2, y=429)
        self.numeroDoisMoedasButton = Button(self.fundoFrameMoedas, text='2', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("2"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroDoisMoedasButton.place(x=80, y=429)
        self.numeroTresMoedasButton = Button(self.fundoFrameMoedas, text='3', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("3"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroTresMoedasButton.place(x=158, y=429)

        self.numeroZeroMoedasButton = Button(self.fundoFrameMoedas, text='0', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("0"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroZeroMoedasButton.place(x=80, y=484)
        self.virgulaMoedasButton = Button(self.fundoFrameMoedas, text=',', height=3, width=10, bd=0, command = self.clickVirgulaMoedas, bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.virgulaMoedasButton.place(x=158, y=484)

        self.limparGeralMoedasButton = Button(self.fundoFrameMoedas, text='C', height=3, width=10, bd=0, command= self.apagarGeralValorMoedas, bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.limparGeralMoedasButton.place(x=236, y=319)
        self.limparUltimoMoedasButton = Button(self.fundoFrameMoedas, text='<-', height=3, width=10, bd=0, command= self.apagarUltimoValorMoedas, bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.limparUltimoMoedasButton.place(x=236, y=374)
        self.numeroZeroZeroMoedasButton = Button(self.fundoFrameMoedas, text='00', height=3, width=10, bd=0, command=lambda: self.clickNumeroMoedas("00"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroZeroZeroMoedasButton.place(x=236, y=429)

        #Binds's telcado
        self.JanelaApp.bind("1", lambda x: self.clickNumeroMoedas("1"))
        self.JanelaApp.bind("2", lambda x: self.clickNumeroMoedas("2"))
        self.JanelaApp.bind("3", lambda x: self.clickNumeroMoedas("3"))
        self.JanelaApp.bind("4", lambda x: self.clickNumeroMoedas("4"))
        self.JanelaApp.bind("5", lambda x: self.clickNumeroMoedas("5"))
        self.JanelaApp.bind("6", lambda x: self.clickNumeroMoedas("6"))
        self.JanelaApp.bind("7", lambda x: self.clickNumeroMoedas("7"))
        self.JanelaApp.bind("8", lambda x: self.clickNumeroMoedas("8"))
        self.JanelaApp.bind("9", lambda x: self.clickNumeroMoedas("9"))
        self.JanelaApp.bind("0", lambda x: self.clickNumeroMoedas("0"))
        self.JanelaApp.bind(",", lambda x: self.clickVirgulaMoedas())
        self.JanelaApp.bind("<BackSpace>", lambda x: self.apagarUltimoValorMoedas())


        #Variaveis do conversor de moedas para geral
        self.atualCalculadora = "self.fundoFrameMoedas"
        self.atualCalculdoraFuncao = "self.abrirConversorMoedas()"

        #Inicializa as diferenças das moedas
        self.trocarMoeda()

    def clickNumeroMoedas(self, var):
        if len(self.primeiroValorMoeda) < 16:
            if not(self.primeiroValorMoeda == "" and var == "0"):
                self.primeiroValorMoeda += var
                self.MoedasAtualLabel.config(text=self.primeiroValorMoeda)
            if len(self.primeiroValorMoeda) > 5:
                self.MoedasAtualLabel.config(font="arial 20")
                self.MoedasAtualLabel.place(y=70)
            self.converterMoedas()

    def clickVirgulaMoedas(self):
        if self.virgulasMoedas == False:
            if self.primeiroValorMoeda == "":  
                self.primeiroValorMoeda = "0"
            self.virgulasMoedas = True
            self.primeiroValorMoeda += "."
            self.MoedasAtualLabel.config(text=self.primeiroValorMoeda.replace(".", ","))
        self.converterMoedas()

    def apagarGeralValorMoedas(self):
        self.primeiroValorMoeda = ""
        self.virgulasMoedas = False
        self.MoedasAtualLabel.config(text="0")
        self.MoedasResultadoLabel.config(text="0")

    def apagarUltimoValorMoedas(self):

        self.primeiroValorMoeda = str(self.primeiroValorMoeda[:-1])

        if str(self.primeiroValorMoeda[:-1]).find(".") == -1:
            self.virgulasMoedas = False
        
        if str(self.primeiroValorMoeda) == "":
            self.MoedasAtualLabel.config(text="0")
            self.MoedasResultadoLabel.config(text="0")
            self.primeiroValorMoeda = ""
        else:
            self.MoedasAtualLabel.config(text=self.primeiroValorMoeda.replace(".", ","))
            self.converterMoedas()
            
    def trocarMoeda(self, *args):
        self.Moeda1 = self.Moeda1ComboBox.get()
        self.Moeda2 = self.Moeda2ComboBox.get()
        self.siglaMoeda1 = self.ciglasMoedas[self.moedas.index(self.Moeda1)]
        self.siglaMoeda2 = self.ciglasMoedas[self.moedas.index(self.Moeda2)]
        requisicao = requests.get(f'https://economia.awesomeapi.com.br/all/{self.siglaMoeda1}-{self.siglaMoeda2}')
        self.cotacao = requisicao.json()
        self.converterMoedas()

    def converterMoedas(self, *args):
        self.Moeda1 = self.Moeda1ComboBox.get()
        self.Moeda2 = self.Moeda2ComboBox.get()
        try:
            self.segundoValorMoeda = float(self.cotacao[self.siglaMoeda1]['bid']) * float(self.primeiroValorMoeda)
            self.segundoValorMoeda = "{:.2f}".format(self.segundoValorMoeda)
            if len(str(self.segundoValorMoeda)) < 8:
                self.MoedasResultadoLabel.config(font="arial 40")
                self.MoedasResultadoLabel.place(y=150)
            if len(str(self.segundoValorMoeda)) > 8:
                self.MoedasResultadoLabel.config(font="arial 20")
                self.MoedasResultadoLabel.place(y=160)
            if len(str(self.segundoValorMoeda)) > 17:
                self.MoedasResultadoLabel.config(font="arial 15")
                self.MoedasResultadoLabel.place(y=170)
            self.MoedasResultadoLabel.config(text=self.segundoValorMoeda)
        except:
            try:
                if (self.cotacao['status']) == 404:
                    self.MoedasResultadoLabel.config(text='Erro na converção de moedas\n tente novamente mais tarde', font="arial 15")
            except:
                    self.MoedasResultadoLabel.config(text=0, font="arial 40")

    def abrirConversorTemperatura(self):
        #Sistema de seguraça para evitar dois frames no codigo
        try:
            self.fundoFrameTemperatura.destroy()
        except:
            pass
        
        #Cria o tema para os combobox
        try:
            comboStyle = ttk.Style()
            

            comboStyle.theme_create('comboStyle', parent="alt",
                            settings = {'TCombobox':
                                    {'configure':
                                    {'foreground': self.tema['ForeGround1'],
                                        'background': self.tema['BackGround4'],
                                        'selectbackground': self.tema['BackGround4'],
                                        'fieldbackground': self.tema['BackGround4'],
                                        'bordercolor': self.tema['BackGround4']}}})

            comboStyle.theme_use('comboStyle')
        except:
            comboStyle.theme_settings('comboStyle',
                            settings = {'TCombobox':
                                    {'configure':
                                    {'foreground': self.tema['ForeGround1'],
                                        'background': self.tema['BackGround4'],
                                        'selectbackground': self.tema['BackGround4'],
                                        'fieldbackground': self.tema['BackGround4'],
                                        'bordercolor': self.tema['BackGround4']}}})


        #Variaveis necessarias para o funcionamento do conversor
        self.temperaturas = ["Celcius", "Fahrenheit", "Kelvin"]
        self.valorConveterTemperatura = ''
        self.valorConvertidoTemperatura = 0
        self.virgulaTemperatura = False

        #Cria os Widgets do conversor de Temperatura
        self.fundoFrameTemperatura = Frame(self.JanelaApp, width=328, height=538, bg=self.tema['BackGround4'])
        self.fundoFrameTemperatura.place(x=0)

        self.menuButton = Button(self.fundoFrameTemperatura, text='☰', font=('Arial', 20, 'bold'), bd=0, command= lambda: self.abrirMenu(5), bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.menuButton.place(x=0, y=10)

        self.tipoConversorLabel = Label(self.fundoFrameTemperatura, text='Temperatura', width=10, font=('Arial', 20, 'bold'), anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'], activebackground=self.tema['BackGround4'], activeforeground=self.tema['ForeGround2'])
        self.tipoConversorLabel.place(x=40, y=15)

        self.temperaturaAtualLabel = Label(self.fundoFrameTemperatura, text='0', font='arial 40', width=9, anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.temperaturaAtualLabel.place(x=22, y=50)
        self.tipoTemperaturaComboBox = ttk.Combobox(self.fundoFrameTemperatura, state="readonly", font=('Arial', 15, 'bold'), width = 10, values=self.temperaturas)
        self.tipoTemperaturaComboBox.place(x=22, y=120)
        self.temperaturaResultadoLabel = Label(self.fundoFrameTemperatura, text='0', font='arial 40', width=9, anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.temperaturaResultadoLabel.place(x=22, y=150)
        self.tipoConverterTemperaturaComboBox = ttk.Combobox(self.fundoFrameTemperatura, state="readonly", font=('Arial', 15, 'bold'), width = 10, values=self.temperaturas)
        self.tipoConverterTemperaturaComboBox.place(x=22, y=220)
        self.temperaturaResultadoOutrosLabel = Label(self.fundoFrameTemperatura, text='', font='arial 30', width=9, anchor="w", bg=self.tema['BackGround4'], fg=self.tema['ForeGround2'])
        self.temperaturaResultadoOutrosLabel.place(x=22, y=250)

        self.tipoTemperaturaComboBox.bind("<<ComboboxSelected>>", self.converterTemperaturas)
        self.tipoConverterTemperaturaComboBox.bind("<<ComboboxSelected>>", self.converterTemperaturas)

        #Teclado Numerico
        self.numeroSeteTemperaturaButton = Button(self.fundoFrameTemperatura, text='7', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("7"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroSeteTemperaturaButton.place(x=2, y=319)
        self.numeroOitoTemperaturaButton = Button(self.fundoFrameTemperatura, text='8', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("8"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroOitoTemperaturaButton.place(x=80, y=319)
        self.numeroNoveTemperaturaButton = Button(self.fundoFrameTemperatura, text='9', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("9"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroNoveTemperaturaButton.place(x=158, y=319)

        self.numeroQuatroTemperaturaButton = Button(self.fundoFrameTemperatura, text='4', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("4"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroQuatroTemperaturaButton.place(x=2, y=374)
        self.numeroCincoTemperaturaButton = Button(self.fundoFrameTemperatura, text='5', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("5"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroCincoTemperaturaButton.place(x=80, y=374)
        self.numeroSeisTemperaturaButton = Button(self.fundoFrameTemperatura, text='6', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("6"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroSeisTemperaturaButton.place(x=158, y=374)


        self.numeroUmTemperaturaButton = Button(self.fundoFrameTemperatura, text='1', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("1"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroUmTemperaturaButton.place(x=2, y=429)
        self.numeroDoisTemperaturaButton = Button(self.fundoFrameTemperatura, text='2', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("2"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroDoisTemperaturaButton.place(x=80, y=429)
        self.numeroTresTemperaturaButton = Button(self.fundoFrameTemperatura, text='3', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("3"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroTresTemperaturaButton.place(x=158, y=429)


        self.maisOuMenosTemperaturaButton = Button(self.fundoFrameTemperatura, text='+/-',  height=3, width=10, bd=0, command= self.colocarNegativoTemperatura, bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.maisOuMenosTemperaturaButton.place(x=2, y=484)
        self.numeroZeroTemperaturaButton = Button(self.fundoFrameTemperatura, text='0', height=3, width=10, bd=0, command=lambda: self.clickNumeroTemperatura("0"), bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.numeroZeroTemperaturaButton.place(x=80, y=484)
        self.virgulaTemperaturaButton = Button(self.fundoFrameTemperatura, text=',', height=3, width=10, bd=0, command = self.clickVirgulaTemperatura, bg=self.tema['BackGround1'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround1'], activeforeground=self.tema['ForeGround1'])
        self.virgulaTemperaturaButton.place(x=158, y=484)

        self.limparGeralTemperaturaButton = Button(self.fundoFrameTemperatura, text='C', height=3, width=10, bd=0, command= self.apagarGeralValorTemperatura, bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.limparGeralTemperaturaButton.place(x=236, y=319)
        self.limparUltimoTemperaturaButton = Button(self.fundoFrameTemperatura, text='<-', height=3, width=10, bd=0, command= self.apagarUltimoValorTemperatura, bg=self.tema['BackGround2'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround2'], activeforeground=self.tema['ForeGround1'])
        self.limparUltimoTemperaturaButton.place(x=236, y=374)
        self.pegarTemperaturaButton = Button(self.fundoFrameTemperatura,text='TP', height=7, width=10, bd=0, bg=self.tema['BackGround3'], fg=self.tema['ForeGround1'], activebackground=self.tema['BackGround3'], activeforeground=self.tema['ForeGround1'], command=self.pegarValorDaCidade)
        self.pegarTemperaturaButton.place(x=236, y=429)
        self.entryText = StringVar()
        self.entryText.set( "Insira a cidade e clique e clique no botão TP" )

        #Função para permitir apenas a entrada de letras dentro do entry
        def Escrevendo(*args):
            s = self.entryText.get()
            if len(s) > 0:
                if not s[-1].isalpha(): 
                    self.entryText.set(s[:-1])
        self.entryText.trace("w", Escrevendo)

        self.nomeCidadeEntry = Entry(self.fundoFrameTemperatura, textvariable=self.entryText, width=52, bg=self.tema['BackGround3'], fg=self.tema['ForeGround1'])
        self.nomeCidadeEntry.place(x=0, y=295)
        self.nomeCidadeEntry.bind("<1>", self.clickBotaoTemperatura)
        
        self.framar = Frame(self.fundoFrameTemperatura, width=1500, height=2, bg=self.tema['BackGround4'])
        self.framar.place(x=0, y=536)

        #Bind's de telcaod Numerico     
        self.JanelaApp.bind("1", lambda x: self.clickNumeroTemperatura("1"))
        self.JanelaApp.bind("2", lambda x: self.clickNumeroTemperatura("2"))
        self.JanelaApp.bind("3", lambda x: self.clickNumeroTemperatura("3"))
        self.JanelaApp.bind("4", lambda x: self.clickNumeroTemperatura("4"))
        self.JanelaApp.bind("5", lambda x: self.clickNumeroTemperatura("5"))
        self.JanelaApp.bind("6", lambda x: self.clickNumeroTemperatura("6"))
        self.JanelaApp.bind("7", lambda x: self.clickNumeroTemperatura("7"))
        self.JanelaApp.bind("8", lambda x: self.clickNumeroTemperatura("8"))
        self.JanelaApp.bind("9", lambda x: self.clickNumeroTemperatura("9"))
        self.JanelaApp.bind("0", lambda x: self.clickNumeroTemperatura("0"))
        self.JanelaApp.bind(",", lambda x: self.clickVirgulaTemperatura())
        self.JanelaApp.bind("<BackSpace>", lambda x: self.apagarUltimoValorTemperatura())

        #Le as ultimas temperaturas utilizadas
        self.tipoTemperaturaComboBox.set(self.temperaturaPrimaria)
        self.tipoConverterTemperaturaComboBox.set(self.temperaturaSecundaria)


        #Variaveis do conversor de moedas para geral
        self.atualCalculadora = "self.fundoFrameTemperatura"
        self.atualCalculdoraFuncao = "self.abrirConversorTemperatura()"

    def clickBotaoTemperatura(self, *args):
        self.entryText.set("")
        self.nomeCidadeEntry.config(textvariable=self.entryText)

    def pegarValorDaCidade(self):
        nomeCidade= self.nomeCidadeEntry.get()
        
        base_url = f"http://api.weatherapi.com/v1/current.json?key=01f78e7b239a4fe196b71551211711&q={nomeCidade}&aqi=no"
        response = requests.get(base_url) 
        
        temperaturaCidade = response.json() 

        try:
            temperaturaParaConverter = self.tipoTemperaturaComboBox.get()
            self.valorConveterTemperatura = temperaturaCidade['current']['temp_c']
            if temperaturaParaConverter == "Celcius":
                self.valorConveterTemperatura = float(self.valorConveterTemperatura)
            elif temperaturaParaConverter == "Fahrenheit":
                 self.valorConveterTemperatura = 1.8 * float(self.valorConveterTemperatura) + 32
            elif temperaturaParaConverter == "Kelvin":
                self.valorConveterTemperatura =  + 274.15  
            
            self.temperaturaAtualLabel.config(text=str(self.valorConveterTemperatura).replace(".",","))
            self.converterTemperaturas()
        except:
            self.entryText.set("Cidade Inexistente")
            self.nomeCidadeEntry.config(textvariable=self.entryText)
        
    def apagarGeralValorTemperatura(self):
        self.valorConveterTemperatura = ""
        self.valorConvertidoTemperatura = ""
        self.virgulaTemperatura = False
        self.temperaturaAtualLabel.config(text= 0)
        self.temperaturaResultadoLabel.config(text= 0) 

    def apagarUltimoValorTemperatura(self):

        if str(self.valorConveterTemperatura[:-1]).find(".") == -1:
            self.virgulaTemperatura = False
        if self.valorConveterTemperatura[:-1] == "":
            self.valorConveterTemperatura = ""
            self.temperaturaAtualLabel.config(text= 0)
            self.temperaturaResultadoLabel.config(text=0)
        else:
            self.valorConveterTemperatura = self.valorConveterTemperatura[:-1]
            self.temperaturaAtualLabel.config(text= self.valorConveterTemperatura.replace(".", ","))
            self.converterTemperaturas()

    def colocarNegativoTemperatura(self):
        if self.valorConveterTemperatura != "":
            self.valorConveterTemperatura = f"-{self.valorConveterTemperatura}"
            self.converterTemperaturas()

    def clickVirgulaTemperatura(self):

        if self.virgulaTemperatura == False:
            if self.valorConveterTemperatura == "":
                self.valorConveterTemperatura += "0"
            self.virgulaTemperatura = True
            self.valorConveterTemperatura += "."
            self.temperaturaAtualLabel.config(text= self.valorConveterTemperatura.replace(".", ","))
            self.converterTemperaturas()

    def clickNumeroTemperatura(self, var):
        if self.valorConveterTemperatura == "" and var == "0":
            pass
        else:
            if len(str(self.valorConveterTemperatura)) < 7:
                self.valorConveterTemperatura += var
                self.temperaturaAtualLabel.config(text= self.valorConveterTemperatura.replace(".", ","))
                self.converterTemperaturas()

    def converterTemperaturas(self, *args):
        temperaturaConverter = self.tipoTemperaturaComboBox.get()
        temperaturaParaConverter = self.tipoConverterTemperaturaComboBox.get()

        self.temperaturaPrimaria = temperaturaConverter
        self.temperaturaSecundaria = temperaturaParaConverter

        if self.valorConveterTemperatura != "":
            if temperaturaConverter == "Celcius":
                if temperaturaParaConverter == "Celcius":
                    self.valorConvertidoTemperatura = float(self.valorConveterTemperatura)
                elif temperaturaParaConverter == "Fahrenheit":
                    self.valorConvertidoTemperatura = 1.8 * float(self.valorConveterTemperatura) + 32
                elif temperaturaParaConverter == "Kelvin":
                    self.valorConvertidoTemperatura =  + 274.15
            
            elif temperaturaConverter == "Fahrenheit":
                if temperaturaParaConverter == "Celcius":
                    self.valorConvertidoTemperatura = (float(self.valorConveterTemperatura) - 32) * 5/9
                elif temperaturaParaConverter == "Fahrenheit":
                    self.valorConvertidoTemperatura = float(self.valorConveterTemperatura)
                elif temperaturaParaConverter == "Kelvin":
                    self.valorConvertidoTemperatura = (float(self.valorConveterTemperatura) - 32) * (5.0/9.0) + 273.15

            elif temperaturaConverter == "Kelvin":
                if temperaturaParaConverter == "Celcius":
                    self.valorConvertidoTemperatura = float(self.valorConveterTemperatura) - 273.15
                elif temperaturaParaConverter == "Fahrenheit":
                    self.valorConvertidoTemperatura = (float(self.valorConveterTemperatura) * 1.8 - 459.7)
                elif temperaturaParaConverter == "Kelvin":
                    self.valorConvertidoTemperatura = float(self.valorConveterTemperatura)

        try:
            self.valorConvertidoTemperatura = '{0:.2f}'.format(self.valorConvertidoTemperatura)
            self.temperaturaResultadoLabel.config(text=self.valorConvertidoTemperatura.replace(".",","))
        except:
            pass

    def abrirMenu(self, tick):
        #Cria o menu e iniciar a animação dele
        self.x = -240
        self.frameMenu = Frame(self.JanelaApp, width=250, height=548, bg=self.tema["BackGround2"], highlightbackground=self.tema["ColorTheme1"], highlightthickness=1, bd=0)
        self.frameMenu.place(x=self.x, y=-2)
        self.configuracoes = Button(self.frameMenu, text='☰', font=('Arial', 20, 'bold'),bd=0, bg=self.tema["BackGround2"], fg=self.tema["ForeGround2"], activebackground=self.tema["BackGround2"], activeforeground=self.tema["ForeGround2"], command=self.fecharMenuAnimacao)
        self.configuracoes.place(x=10, y=10)
        self.calculadoraLabel = Label(self.frameMenu, text='Calculadora', width=9, font=('Arial', 12, 'bold'), anchor="w", bg=self.tema["BackGround2"], fg= self.tema["ForeGround2"], activeforeground=self.tema["ForeGround2"])
        self.calculadoraLabel.place(x=20, y=75)
        self.calculadoraPadrao = Button(self.frameMenu, text='📘 Padrão', font=('Arial', 12, 'bold'),bd=0, bg=self.tema["BackGround2"], fg=self.tema["ForeGround2"], activebackground=self.tema["BackGround2"], activeforeground=self.tema["ForeGround2"], command= lambda: self.abrirDoisFrames("self.abrirCalculadoraPadrao()"))
        self.calculadoraPadrao.place(x=20, y=110)
        self.calculadoraDatas = Button(self.frameMenu, text='🗓 Datas', font=('Arial', 12, 'bold'),bd=0, bg=self.tema["BackGround2"], fg=self.tema["ForeGround2"], activebackground=self.tema["BackGround2"], activeforeground=self.tema["ForeGround2"], command=self.abrirCalculadoraDeDatas)
        self.calculadoraDatas.place(x=20, y=145)
        self.configuracoes = Button(self.frameMenu, text='⚙ Configurações', font=('Arial', 12, 'bold'),bd=0, bg=self.tema["BackGround2"], fg=self.tema["ForeGround2"], activebackground=self.tema["BackGround2"], activeforeground=self.tema["ForeGround2"], command=self.abrirConfiguracoes)
        self.configuracoes.place(x=20, y=500)
        self.conversorLabel = Label(self.frameMenu, text='Conversor', width=9, font=('Arial', 12, 'bold'), anchor="w", bg=self.tema["BackGround2"], fg= self.tema["ForeGround2"], activeforeground=self.tema["ForeGround2"])
        self.conversorLabel.place(x=20, y=200)
        self.conversorMoeda = Button(self.frameMenu, text='💲 Moedas', font=('Arial', 12, 'bold'),bd=0, bg=self.tema["BackGround2"], fg=self.tema["ForeGround2"], activebackground=self.tema["BackGround2"], activeforeground=self.tema["ForeGround2"], command=self.abrirConversorMoedas)
        self.conversorMoeda.place(x=20, y=235)
        self.conversorTemperatura = Button(self.frameMenu, text='🌡Temperatura', font=('Arial', 12, 'bold'),bd=0, bg=self.tema["BackGround2"], fg=self.tema["ForeGround2"], activebackground=self.tema["BackGround2"], activeforeground=self.tema["ForeGround2"], command=self.abrirConversorTemperatura)
        self.conversorTemperatura.place(x=20, y=270)

        self.abrirMenuAnimacao(tick)
    
    def abrirMenuAnimacao(self, tick):
        #Inicia o tick e render de animação do menu
        self.frameMenu.place(x=self.x)
        self.tickMenuAnimacaoAbrir(tick)

    def tickMenuAnimacaoAbrir(self, tick):
        #Tick de animação do menu, aumenta o x dele e vai para o render para rederizar o place
        if self.x != -10:
            self.x += 10
            self.JanelaApp.after(tick, lambda:self.abrirMenuAnimacao(tick))

    def fecharMenuAnimacao(self):
        #Fecha o menu
        self.frameMenu.place(x=self.x)
        self.tickMenuAnimcaoFechar()

    def tickMenuAnimcaoFechar(self):
        #Tick para animação de fechar menu
        if self.x != -250:
            self.x -= 10
            self.JanelaApp.after(5,self.fecharMenuAnimacao)
            
    def abrirDoisFrames(self, var):
        #destroi a antiga calculadora utilizada
        eval(self.atualCalculadora).destroy()

        #Abre a nova calculadora
        eval(var)

        #executa a animação de fechar o menu        
        self.frameMenu.destroy()
        self.abrirMenu(0)
        self.x = -10
        self.fecharMenuAnimacao()
        
    def abrirConfiguracoes(self):
        #Widgets do menu de configurações 
        self.fundoFrameConfiguracoes = Frame(self.JanelaApp, width=328, height=538, bg=self.tema['BackGround2'])
        self.fundoFrameConfiguracoes.place(x=0)
        self.fecharConfiguracoesButton = Button(self.fundoFrameConfiguracoes, font=('Arial', 20, 'bold'), text='X', bg=self.tema['BackGround2'],  fg= self.tema['ForeGround2'], activebackground=self.tema['BackGround2'], activeforeground= self.tema['ForeGround2'], bd=0, command= self.fecharConfiguracoes)
        self.fecharConfiguracoesButton.place(x=260, y=15)
        self.configuracoesLabel = Label(self.fundoFrameConfiguracoes, text='⚙ Configurações', width=14, font=('Arial', 20, 'bold'), anchor="w", bg=self.tema["BackGround2"], fg= self.tema["ForeGround2"], activeforeground=self.tema["ForeGround2"])
        self.configuracoesLabel.place(x=15, y=25)
        self.corTemaConfiguracoesLabel = Label(self.fundoFrameConfiguracoes, text='Clique na cor de tema que deseja:', bg=self.tema["BackGround2"], fg= self.tema["ForeGround2"], font=('Arial', 12, 'bold'))
        self.corTemaConfiguracoesLabel.place(x=15, y=100)
        self.corTemaConfiguracoesVerdeButton = Button(self.fundoFrameConfiguracoes, width=2, bg='#2c993b', command= lambda: self.trocarColor("Green"), bd=0, activebackground='#2c993b')
        self.corTemaConfiguracoesVerdeButton.place(x=30, y=135) 
        self.corTemaConfiguracoesRoxoButton = Button(self.fundoFrameConfiguracoes, width=2, bg='#571a50', command= lambda: self.trocarColor("Purple"), bd=0, activebackground='#571a50')
        self.corTemaConfiguracoesRoxoButton.place(x=70, y=135)
        self.corTemaConfiguracoesAzulButton = Button(self.fundoFrameConfiguracoes, width=2, bg='#1a1a70', command= lambda: self.trocarColor("Blue"), bd=0, activebackground='#1a1a70')
        self.corTemaConfiguracoesAzulButton.place(x=110, y=135)
        self.corTemaConfiguracoesVermelhoButton = Button(self.fundoFrameConfiguracoes, width=2, bg='#5e0811', command= lambda: self.trocarColor("Red"), bd=0, activebackground='#5e0811')
        self.corTemaConfiguracoesVermelhoButton.place(x=150, y=135)
        self.temaConfiguracoesLabel = Label(self.fundoFrameConfiguracoes, text="Escolha o tema:", bg=self.tema["BackGround2"], fg= self.tema["ForeGround2"], font=('Arial', 12, 'bold'))  
        self.temaConfiguracoesLabel.place(x=15, y=200)
        self.temaEscuroConfiguracoesButton = Button(self.fundoFrameConfiguracoes, text="Tema Dark", bg='#0f0f0f', fg="#c2c2c2", command= lambda: self.trocarTema("Dark"), bd=0, activebackground='#0f0f0f', activeforeground="#c2c2c2")
        self.temaEscuroConfiguracoesButton.place(x=30, y=235)
        self.temaClaroConfiguracoesButton = Button(self.fundoFrameConfiguracoes, text="Tema White", bg='#bec3c6', fg="#252626", command= lambda: self.trocarTema("White"), bd=0, activebackground='#bec3c6', activeforeground="#252626")
        self.temaClaroConfiguracoesButton.place(x=150, y=235)

    def trocarColor(self, var):
        #Seta a cor escolhida pelo usuario e refaz a janela de Calculadora Atual
        if var == "Green":
            self.tema['BackGround3'] = "#2c993b"
            self.tema['ColorTheme1'] = "Green"

        if var == "Purple":
            self.tema['BackGround3'] = "#571a50"
            self.tema['ColorTheme1'] = "Purple"

        if var == "Blue":
            self.tema['BackGround3'] = "#1a1a70"
            self.tema['ColorTheme1'] = "Blue"

        if var == "Red":
            self.tema['BackGround3'] = "#5e0811"
            self.tema['ColorTheme1'] = "Red"

        self.criarNotificacao()

    def trocarTema(self, var):
        #Troca o tema geral (White e Black)
        self.tema['TypeTheme01'] = var

        self.definicoesUsuario[0]["Type"] = self.atualCalculdoraFuncao
        self.definicoesUsuario[0]["Theme"] = self.tema["TypeTheme01"]
        self.definicoesUsuario[0]["Color"] = self.tema["ColorTheme1"]

        with open(f'{LOCAL}files/data/settings.json', 'w', encoding="utf8") as definicoes:
            json.dump(self.definicoesUsuario, definicoes)

        self.checarTema()
        self.fundoFrameConfiguracoes.destroy()
        self.abrirConfiguracoes()
        self.criarNotificacao()

    def fecharConfiguracoes(self):
        #Fecha o menu de configurações e encerra o tick caso estja aberto
        eval(self.atualCalculadora).destroy()
        self.fundoFrameConfiguracoes.destroy()
        self.frameMenu.destroy()
        eval(self.atualCalculdoraFuncao)
        self.abrirMenu(0)

    def criarNotificacao(self):
        #Cria uma notificação na bara inferior falando do tema escolhido e a cor de tema
        try:
            self.textNotification.destroy()
            self.frameNotification.destroy()
            self.linhaNotification.destroy()
            self.JanelaApp.after_cancel(self.tickNoti)
        except:
            pass

        self.xNotificao = 0
        self.frameNotification = Frame(self.fundoFrameConfiguracoes, width=350, height=30, bg= self.tema["BackGround1"])
        self.textNotification = Label(self.frameNotification, text=(f"O tema foi trocado para o tema: {self.tema['TypeTheme01']}, cor: {self.tema['ColorTheme1']}"), width=45, height=1, bg= self.tema["BackGround1"] ,fg= self.tema["ForeGround2"])
        self.linhaNotification = Frame(self.fundoFrameConfiguracoes, width=0, height=100, bg= self.tema["BackGround3"])
        self.frameNotification.place(x=0 ,y=510)
        self.textNotification.place(x=0, y=0)
        self.linhaNotification.place(x=0, y=537)
             
        self.tickNotificacao()
         
    def renderNotificacao(self):
        #Renderiza as animações da notificação de troca de tema
        try:
            if self.xNotificao < 315:
                self.linhaNotification.config(width=self.xNotificao)
                self.tickNotificacao()
            else:
                self.textNotification.destroy()
                self.frameNotification.destroy()
                self.linhaNotification.destroy()
        except:
            pass

    def tickNotificacao(self):
        #Responsavel por fazer o tick da animação
        self.xNotificao += 1
        self.tickNoti = self.JanelaApp.after(5, self.renderNotificacao)

start = openAPP()
