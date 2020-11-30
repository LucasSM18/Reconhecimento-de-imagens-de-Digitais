import cv2 as cv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from mysql.connector import Error, connect
import os

#--------------------------------------------------------------------------------
#método que importa a imagem da digital
def import_image():
        text, okPressed = QtWidgets.QInputDialog.getText(tela_login_1_novo,
        "Digite o nome da imagem", "Imagem: ", QtWidgets.QLineEdit.Normal, "")
        if text and okPressed != '':
            tela_login_1_novo.image_label.setScaledContents(True)
            pixmap = QtGui.QPixmap(text)
            tela_login_1_novo.image_label.setPixmap(pixmap)
            tela_login_1_novo.image_label.repaint()
            QtWidgets.QApplication.processEvents()
            image = segmentador(text)
            return image
        else:
            print("Digite o nome da imagem para importa-la!")

#-----------------------------------------------------------------------------------------------
#segmentador de imagem
def segmentador(imagem):
    image = cv.imread(imagem)
    cinza = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    edged = cv.Canny(cinza, 30, 200)
    contours, hierarchy = cv.findContours(edged,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    #print(contours)
    #print('Numbers of contours found=' + str(len(contours)))
    data = cv.drawContours(image,contours,-1,(0,255,0),3)
    cv.imshow('Imagem Segmentada', image)
    return data
#--------------------------------------------------------------------------------------------
#cria um arquivo com os dados
def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
#--------------------------------------------------------------------------------------------
#método para puchar a imagem do banco
def blob_Image(nome):
    connection = connect(host='localhost',
                         database='APS',
                         user='root',
                         password='LucasMissalia20')
    cursor = connection.cursor()
    try:
        query = "SELECT IMG_Digital FROM Funcionarios WHERE NM_Funcionario = %s"
        cursor.execute(query,(nome,))
        record = cursor.fetchone()[0]

        if record is not None:
            print('Extraindo digital do Banco para comparação')
            write_file(record, nome+'.bmp')
            print('Extração completa')
            image = segmentador(nome+'.bmp')
            return image
        else:
            print('Digital não encontrada no Banco')
            return False
    except Error as e:
        print("Erro ao conectar no banco", e)
    finally:
        cursor.close()

#------------------------------------------------------------------------------------------------
#método para comparar imagens
def compara_Imagem(img1, img2):
   if img1 in img2:
       return True
   else:
       return False
#------------------------------------------------------------------------------------------------
#método para pegar o login
def submit():
    nome = linha.text()
    imagem = import_image()
    imagem2 = blob_Image(nome)
    compara = compara_Imagem(imagem, imagem2)
    chama_segunda_tela(nome, compara)
#-----------------------------------------------------------------------------------------------
#método que chama a tela de consulta
def chama_segunda_tela(nome, imagem):
    connection = connect(host='localhost',
                         database='APS',
                         user='root',
                         password='LucasMissalia20')
    cursor = connection.cursor()
    try:
        query = "SELECT NM_Funcionario FROM Funcionarios WHERE NM_Funcionario = %s"
        cursor.execute(query,(nome,))
        result = cursor.fetchall()

        for x in result:
            if nome in x and imagem is True:
                print("logado com sucesso")
                tela_banco.show()
                tela_login_1_novo.close()
            else:
                print('Nome ou digital não estão registrados no banco!')
            os.remove(nome+".bmp")

    except Error as e:
        print("Erro ao conectar no banco: ", e)
    finally:
            cursor.close()
            #print("Banco de dados fechado")

#----------------------------------------------------------------------------------------------------
#método que inicia o tela de consulta com a tabela de funcionarios
def host_cargo():
    connection = connect(host='localhost',
                         database='APS',
                         user='root',
                         password='LucasMissalia20')
    cursor = connection.cursor()
    try:
         nome = linha.text()
         comando_SQL = "SELECT DS_Cargo FROM Funcionarios Where NM_Funcionario = %s"
         cursor.execute(comando_SQL,(nome,))
         dados_lidos = cursor.fetchone()[0]

         return dados_lidos
    except Error as e:
        print("Erro ao conectar no banco: ", e)
    finally:
       cursor.close()

#------------------------------------------------------------------------------------------------
#método para fazer a consulta dos dados do banco
def mudancaconsulta():
    connection = connect(host='localhost',
                         database='APS',
                         user='root',
                         password='LucasMissalia20')
    cursor = connection.cursor()
    try:
        cargo = host_cargo()
        comboxtext = tela_banco.comboBox.currentText()

        #Nivel 2
        if comboxtext == "Funcionarios" and cargo == "Diretor de Divisão":
           comando_SQL = "SELECT * FROM Funcionarios"

           cursor.execute(comando_SQL)
           dados_lidos = cursor.fetchall()

           tela_banco.tableWidget.setRowCount(len(dados_lidos))
           tela_banco.tableWidget.setColumnCount(4)
           tela_banco.tableWidget.setColumnWidth(0, 75)
           tela_banco.tableWidget.setColumnWidth(1, 150)
           tela_banco.tableWidget.setColumnWidth(2, 300)
           tela_banco.tableWidget.setColumnWidth(3, 178)
           tela_banco.tableWidget.setHorizontalHeaderLabels(['ID', 'Nome', 'Cargo', 'Salario'])

           for linha in range(0, len(dados_lidos)):
              for coluna in range(0, 4):
                 tela_banco.tableWidget.setItem(linha, coluna,
                                               QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

        #Nivel 3
        elif comboxtext == "Agrotoxicos" and cargo == "Ministro do Meio Ambiente":
           comando_SQL = "SELECT * FROM Agrotoxicos"

           cursor.execute(comando_SQL)
           dados_lidos = cursor.fetchall()

           tela_banco.tableWidget.setRowCount(len(dados_lidos))
           tela_banco.tableWidget.setColumnCount(3)
           tela_banco.tableWidget.setColumnWidth(0, 75)
           tela_banco.tableWidget.setColumnWidth(1, 118)
           tela_banco.tableWidget.setColumnWidth(2, 510)
           tela_banco.tableWidget.setHorizontalHeaderLabels(['ID Agrotoxico', 'Nome Agrotoxico', 'Descrição Agrotoxico'])

           for linha in range(0, len(dados_lidos)):
              for coluna in range(0, 3):
                  tela_banco.tableWidget.setItem(linha, coluna,
                                               QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))
        #Nivel 1
        elif comboxtext == "Propriedades":
           comando_SQL = "SELECT * FROM propriedades"

           cursor.execute(comando_SQL)
           dados_lidos = cursor.fetchall()

           tela_banco.tableWidget.setRowCount(len(dados_lidos))
           tela_banco.tableWidget.setColumnCount(4)
           tela_banco.tableWidget.setColumnWidth(0, 90)
           tela_banco.tableWidget.setColumnWidth(1, 90)
           tela_banco.tableWidget.setColumnWidth(2, 255)
           tela_banco.tableWidget.setColumnWidth(3, 268)
           tela_banco.tableWidget.setHorizontalHeaderLabels(['ID Propriedade', 'ID Agrotoxico', 'Localização', 'Descrição'])

           for linha in range(0, len(dados_lidos)):
              for coluna in range(0, 4):
                  tela_banco.tableWidget.setItem(linha, coluna,
                                               QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

        #Nivel 3
        elif comboxtext == "Ambiente" and cargo == "Ministro do Meio Ambiente":
           comando_SQL = "SELECT * FROM Ambiente"

           cursor.execute(comando_SQL)
           dados_lidos = cursor.fetchall()

           tela_banco.tableWidget.setRowCount(len(dados_lidos))
           tela_banco.tableWidget.setColumnCount(4)
           tela_banco.tableWidget.setColumnWidth(0, 70)
           tela_banco.tableWidget.setColumnWidth(1, 100)
           tela_banco.tableWidget.setColumnWidth(2, 80)
           tela_banco.tableWidget.setColumnWidth(3, 453)
           tela_banco.tableWidget.setHorizontalHeaderLabels(['ID Ambiente', 'ID Propriedade', 'Ambiente', 'Descrição'])

           for linha in range(0, len(dados_lidos)):
              for coluna in range(0, 4):
                 tela_banco.tableWidget.setItem(linha, coluna,
                                               QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))
    except Error as e:
        print("Erro ao conectar no banco: ", e)
    finally:
       cursor.close()
#-----------------------------------------------------------------------------------------

#variaveis de controle
app =QtWidgets.QApplication([])
tela_login_1_novo = uic.loadUi("tela_login_1.ui")
tela_banco = uic.loadUi("tela_banco.ui")
tela_login_1_novo.login_botao.clicked.connect(submit)
linha = tela_login_1_novo.login_line_edit
tela_banco.botaoteste.clicked.connect(mudancaconsulta)

#inicia a aplicação
tela_login_1_novo.show()
app.exec()



#----------------------------------------------

