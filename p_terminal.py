import json                            # para importar os arquivos JSON
import time                            # para fazer o programa dormir
from getpass import getpass            # para inserir senhas
from inquirer import list_input        # para interface interativa no terminal
from os import system, name as sysname # para limpar a linha de comando

# importante para importar os arquivos JSON
grupos = [
    ('id', 'nome', 'info', 'quantidade', 'tipo'),
    ('user', 'name', 'pass'),
    ('fabricante', 'modelo', 'placa', 'data', 'cor', 'saida', 'entrada', 'km_saida', 'km_final')
]

# sistema de estoque

class Estoque:

    # aqui, o programa realiza as seguintes ações:

    # - mostrar o estoque;
    # - adicionar um item;
    # - editar um item;
    # - remover um item;
    # - atualizar estoque.json (ao fechar o programa);
    # - verificar a existência do código de um produto (usado para editar e remover itens);
    # - modificar (ou criar) o tipo do item (usado para adicionar e editar itens).

    def __init__(self):

        self.estoque = []
        
        with open('data/estoque.json') as file:
            lst = json.load(file)

        for i in range(len(lst)):
            a = []
            self.estoque.append(a)
            for j in grupos[0]:
                a.append(lst[i][j])

    def showEstoque(self):

        clearcmd()

        print(' = Mostrando itens =')
        search_input = list_input('Escolha um método de pesquisa',
                                  choices=(('Pesquisar por código', 'code'),('Pesquisar por nome', 'nome'),
                                           ('Pesquisar por tipo', 'tipo'),('Mostrar todos os itens','tudo')),
                                  carousel=True)
        
        match search_input:
            case 'code':

                tipo_pesq = int(input('Qual o código do produto?\n > '))
                pos = 0
                
                print('')

            case 'nome':

                tipo_pesq = input('Qual o nome do produto?\n > ')
                pos = 1

                print('')

            case 'tipo':

                tipos_temp = set()

                for block in self.estoque:
                    tipos_temp.add(block[-1])

                tipos_ls = list(tipos_temp)
                tipos_ls.sort()

                tipo_pesq = list_input('Escolha um tipo', choices=tipos_ls, carousel=True)
                pos = 4

            case 'tudo':

                for ln in self.estoque:
                    print(f' --- \n\nCódigo: {ln[0]} | Nome: {ln[1]} | Quantidade: {ln[3]}\nDescrição: {ln[2]}\nTipo: {ln[4]}\n')
                
                getpass('\nPressione enter para voltar.')
                return

        for ln in self.estoque:
            if ln[pos] == tipo_pesq:
                print(f' --- \n\nCódigo: {ln[0]} | Nome: {ln[1]} | Quantidade: {ln[3]}\nDescrição: {ln[2]}\nTipo: {ln[4]}\n')
        
        getpass('\nPressione enter para voltar.')

    def addEstoque(self, nome, desc, quant):
        
        cod = self.estoque[-1][0] + 1

        tipo = Estoque.modTipo(self.estoque)

        self.estoque.append((cod, nome, desc, quant, tipo))

        print(f'\nItem {nome}, código {cod}, adicionado.')
        time.sleep(2)

    def editEstoque(self, cod):

        item = Estoque.verifCodigo(cod, self.estoque)
        
        if not item:
            print('\nEste item não existe.')
            time.sleep(2)
            return

        print(f'\nItem selecionado:\n\nCódigo: {cod} | Nome: {item[1]} | Quantidade: {item[3]}\nDescrição: {item[2]}\nTipo: {item[4]}\n\n---\n')

        print(' [!] Aperte "enter" no promp vazio para manter o valor atual [!]\n')
        new_nome = input('Alterar o nome do produto?\n > ')
        new_quant = input('\nAlterar a quantidade de produtos?\n > ')
        new_desc = input('\nAlterar a descrição do produto?\n > ')

        if new_nome != '':
            item[1] = new_nome
        
        if new_quant != '':
            item[3] = int(new_quant)
        
        if new_desc != '':
            item[2] = new_desc

        print('')
        new_tipo = list_input('Você deseja mudar o tipo do item?',
                              choices=('Sim', 'Não'))
        
        if new_tipo == 'Sim':
            item[4] = Estoque.modTipo(self.estoque)

        self.estoque = [item if block[0] == item[0] else block for block in self.estoque]

        print(f'\nItem de código {cod} modificado.')
        time.sleep(2)

    def removeEstoque(self, cod):

        item = Estoque.verifCodigo(cod, self.estoque)
        
        if not item:
            print('\nEste item não existe.')
            time.sleep(2)
            return

        print('')
        confirmar = list_input('Você tem certeza que você quer remover esse item?',
                               choices=('Sim','Não'))

        if confirmar == 'Sim':
            self.estoque.remove(item)
            
        else:
            print('Operação cancelada.')
            time.sleep(2)
            return
        
        print(f'Item de código {cod} removido.')
        time.sleep(2)

    def updateEstoque(self):

        print('Atualizando estoque...')

        new_estoque = []

        for block in self.estoque:
            estoque_ln = {
                'id':block[0],
                'nome':block[1],
                'info':block[2],
                'quantidade':block[3],
                'tipo':block[4]
                }
            
            new_estoque.append(estoque_ln)

        with open('data/estoque.json', 'w') as file:
            json.dump(new_estoque, file, indent=4)
        
        time.sleep(1)
        print('Estoque atualizado.')
    
    def verifCodigo(cod, estoque):
        
        # código repetido entre as funções de editar e remover itens

        item = int()

        for block in estoque:
            if block[0] == cod:
                item = block
                break
            else:
                continue
        
        return list(item)

    def modTipo(estoque):

        # código repetido entre as funções de adicionar e editar itens

        tipos_temp = set()

        for block in estoque:
            tipos_temp.add(block[-1])

        tipos_ls = list(tipos_temp)
        tipos_ls.sort()

        print('')
        tipo_q = list_input('Você quer usar um tipo que já existe ou criar um novo?',
                            choices=['Existente', 'Novo'])
        
        match tipo_q:
            case 'Existente':
                tipo = list_input('Qual o tipo do produto?', choices=tipos_ls, carousel=True)
            case 'Novo':
                tipo = input('Qual o tipo do item?\n > ')

        return tipo

# sistema de entrada e saída de caminhões

class Trucks:

    # aqui, o programa faz as seguintes funções:

    # - mostrar uma lista de todos os caminhões registrados;
    # - adicionar o registro de um caminhão;
    # - editar o registro de um caminhão;
    # - remover o registro de um caminhão;
    # - verificar a existência de uma placa (usado para editar e remover registros);
    # - modificar (ou criar) o fabricante do caminhão (usado para adicionar e editar registros).

    def __init__(self):

        self.trucks = []
            
        with open('data/trucks.json') as file:
            lst = json.load(file)

        for i in range(len(lst)):
            a = []
            self.trucks.append(a)
            for j in grupos[2]:
                a.append(lst[i][j])

    def showTruck(self):

        clearcmd()

        print(' = Mostrando caminhões =')
        search_input = list_input('Escolha um método de pesquisa',
                                  choices=(('Pesquisar por placa', 'placa'),('Pesquisar por fabricante', 'fab'),
                                           ('Mostrar todos os itens','tudo')),
                                  carousel=True)
        
        match search_input:
            case 'placa':

                tipo_pesq = input('Qual a placa do veículo?\n > ')
                pos = 2
                
                print('')

            case 'fab':

                fab_temp = set()

                for block in self.trucks:
                    fab_temp.add(block[0])

                fab_ls = list(fab_temp)
                fab_ls.sort()

                tipo_pesq = list_input('Escolha um fabricante', choices=fab_ls, carousel=True)
                pos = 0

            case 'tudo':

                for block in self.trucks:
                    print(f' --- \n\nPlaca: {block[2]} | Fabricante: {block[0]} | Modelo: {block[1]}\nAno: {block[3]} | Cor: {block[4]}\nData de saída: {block[5]} | Data de entrada: {block[6]} \nQuilometragem de saída: {block[7]} | Quilometragem final: {block[8]}\n')
                
                getpass('\nPressione enter para voltar.')
                return

        print('')
        for block in self.trucks:
            if block[pos] == tipo_pesq:
                print(f' --- \n\nPlaca: {block[2]} | Fabricante: {block[0]} | Modelo: {block[1]}\nAno: {block[3]} | Cor: {block[4]}\nData de saída: {block[5]} | Data de entrada: {block[6]} \nQuilometragem de saída: {block[7]} | Quilometragem final: {block[8]}\n')
                break
        
        getpass('\nPressione enter para voltar.')

    def addTruck(self, mod, ano, cor, placa):

        fab = Trucks.modFabricante(self.trucks)

        saida_q = list_input('Você quer adicionar informações de saída e entrada?',
                             choices=('Sim', 'Não'))

        if saida_q == 'Sim':
            print(' [!] Para deixar uma resposta em branco, aperte "enter" no prompt vazio [!]\n')

            saida = input('Qual foi o dia e horário de saída?\n > ')
            entra = input('\nQual foi o dia e horário de entrada?\n > ')
            km_s = input('\nQual era a quilometragem na saída?\n > ')
            km_f = input('\nQual era a quilometragem na entrada?\n > ')
        else:
            saida = ''
            entra = ''
            km_s = ''
            km_f = ''

        self.trucks.append((fab, mod, placa, ano, cor, saida, entra, km_s, km_f))

        print(f'\nCaminhão {placa} adicionado!')
        time.sleep(2)
        
    def editTruck(self, placa):

        item = Trucks.verifPlaca(placa, self.trucks)
        
        if not item:
            print('\nEste veículo não existe.')
            time.sleep(2)
            return
        
        print(f'\nVeículo selecionado:\n\nPlaca: {placa} | Fabricante: {item[0]} | Modelo: {item[1]}\nAno: {item[3]} | Cor: {item[4]}\nData de saída: {item[5]} | Data de entrada: {item[6]} \nQuilometragem de saída: {item[7]} | Quilometragem final: {item[8]}\n\n---\n')

        print(' [!] Aperte "enter" no promp vazio para manter o valor atual [!]\n')
        new_mod = input('Alterar o modelo do veículo?\n > ')
        new_ano = input('\nAlterar o ano do veículo?\n > ')
        new_cor = input('\nAlterar a cor do veículo?\n > ')

        print('')
        saida_q = list_input('Você quer alterar informações de saída e entrada?',
                             choices=('Sim', 'Não'))

        if saida_q == 'Sim':
            print(' [!] Para deixar uma resposta em branco, aperte "enter" no prompt vazio [!]\n')

            item[5] = input('Qual foi o dia e horário de saída?\n > ')
            item[6] = input('\nQual foi o dia e horário de entrada?\n > ')
            item[7] = input('\nQual era a quilometragem na saída?\n > ')
            item[8] = input('\nQual era a quilometragem na entrada?\n > ')
        else:
            item[5] = ''
            item[6] = ''
            item[7] = ''
            item[8] = ''

        if new_mod != '':
            item[1] = new_mod
        
        if new_ano != '':
            item[3] = int(new_ano)
        
        if new_cor != '':
            item[4] = new_cor

        print('')
        new_tipo = list_input('Você deseja mudar o fabricante do veículo?',
                              choices=('Sim', 'Não'))
        
        if new_tipo == 'Sim':
            item[0] = Trucks.modFabricante(self.trucks)

        self.trucks = [item if block[0] == item[0] else block for block in self.trucks]

        print(f'\nVeículo de placa {placa} modificado.')
        time.sleep(2)

    def removeTruck(self, placa):

        item = Trucks.verifPlaca(placa, self.trucks)
        
        if not item:
            print('\nEste veículo não existe.')
            time.sleep(2)
            return

        print('')
        confirmar = list_input('Você tem certeza que você quer remover esse registro?',
                               choices=('Sim','Não'))

        if confirmar == 'Sim':
            self.trucks.remove(item)
        else:
            print('Operação cancelada.')
            time.sleep(2)
            return
        
        print(f'Veículo de placa {placa} removido.')
        time.sleep(2)
    
    def updateTruck(self):

        print('Atualizando controle de caminhões...')

        new_estoque = []

        for block in self.trucks:
            estoque_ln = {
                'fabricante':block[0],
                'modelo':block[1],
                'placa':block[2],
                'data':block[3],
                'cor':block[4],
                'saida':block[5],
                'entrada':block[6],
                'km_saida':block[7],
                'km_final':block[8]
                }
            
            new_estoque.append(estoque_ln)

        with open('data/trucks.json', 'w') as file:
            json.dump(new_estoque, file, indent=4)
        
        time.sleep(1)
        print('Controle de caminhões atualizado.')

    def verifPlaca(placa, trucks):
        
        # código repetido entre as funções de editar e remover registros

        item = str()

        for block in trucks:
            if block[2] == placa:
                item = block
                break
            else:
                continue
        
        return list(item)

    def modFabricante(trucks):

        # código repetido entre as funções de adicionar e editar registros

        fab_temp = set()

        for block in trucks:
            fab_temp.add(block[0])

        fab_ls = list(fab_temp)
        fab_ls.sort()

        print('')
        fab_q = list_input('Você quer usar um fabricante já registrado ou adicionar um novo?',
                            choices=['Existente', 'Novo'])
        
        match fab_q:
            case 'Existente':
                fab = list_input('Qual o fabricante do caminhão?', choices=fab_ls, carousel=True)
            case 'Novo':
                fab = input('Qual o fabricante do caminhão?\n > ')

        return fab

# programa principal

class Main:

    # onde o programa mostra no terminal:

    # - uma tela de login, com código de usuário e senha;
    # - as ações de estoque, declaradas na classe Estoque;
    # - as ações de controle de caminhões, declaradas na classe Trucks.
    
    def login():
        
        loginfo = []

        with open('data/loginfo.json') as file:
            lst = json.load(file)

        for i in range(len(lst)):
            a = []
            loginfo.append(a)
            for j in grupos[1]:
                a.append(lst[i][j])

        while True:            
            print(' = Tela de login =\n')

            user_id = input('Código de usuário: ')
            user_pass = getpass('Digite sua senha: ')

            for i in loginfo:
                if user_id == i[0] and user_pass == i[2]:
                    Main.switchMenu(i[1])
                    break
                else:
                    continue
            
            clearcmd()
            print(' [!] Cadastro inválido. [!]\n')

    def switchMenu(user_nome):
        
        while True:
            clearcmd()

            print(' = Lista de sistemas =\n')
            escolha = list_input('Qual sistema você quer acessar?',
                                choices=('Estoque', ('Controle de caminhões', 'truck')))
            
            match escolha:
                case 'Estoque':
                    Main.estoqueMenu(user_nome)

                case 'truck':
                    Main.truckMenu(user_nome)

    def truckMenu(user_nome):
        
        trucks = Trucks()

        while True:

            clearcmd()

            print(f' = Bem-vindo ao sistema de controle de caminhões, {user_nome} =\n')
            escolha = list_input('Escolha uma opção',
                                 choices=[('Mostrar um caminhão registrado', 0), ('Adicionar um caminhão ao registro', 1),
                                          ('Editar um caminhão no registro', 2),('Remover um caminhão do registro', 3),
                                          ('Trocar de sistema', 'v'),('Atualizar dados e sair','x')],
                                          carousel=True)
        
            clearcmd()

            match escolha:
                case 0: trucks.showTruck()
                case 1:
                    print(' = Adicionando um registro =\n\n [!] Para deixar uma resposta em branco, aperte "enter" no prompt vazio [!]\n')

                    mod = input('Qual o modelo do veículo?\n > ')
                    ano = int(input('\nQual o ano do veículo?\n > '))
                    cor = input('\nQual a cor do veículo?\n > ')
                    placa = input('\nQual a placa do veículo?\n > ').upper()

                    trucks.addTruck(mod, ano, cor, placa)

                case 2:
                    print(' = Editando um registro =\n')

                    cod = input('Qual é a placa do veículo a ser editado?\n > ')
                    trucks.editTruck(cod)

                case 3:
                    print(' = Removendo um registro =\n')

                    cod = input('Qual é a placa do veículo a ser removido?\n > ')
                    trucks.removeTruck(cod)

                case 'v':
                    trucks.updateTruck()
                    return
                
                case 'x':
                    trucks.updateTruck()
                    print('Saindo do programa.')
                    
                    time.sleep(.5)
                    exit()

    def estoqueMenu(user_nome):

        estoque = Estoque()

        while True:

            clearcmd()

            print(f' = Bem-vindo ao sistema de gerenciamento de estoque, {user_nome} =\n')
            escolha = list_input('Escolha uma opção',
                                 choices=[('Mostrar itens no estoque', 0), ('Adicionar um item ao estoque', 1),
                                          ('Editar um item no estoque', 2),('Remover um item do estoque', 3),
                                          ('Trocar de sistema', 'v'),('Atualizar dados e sair', 'x')],
                                          carousel=True)
        
            clearcmd()

            match escolha:
                case 0: estoque.showEstoque()
                case 1:
                    print(' = Adicionando um item =\n\n [!] Para deixar uma resposta em branco, aperte "enter" no prompt vazio [!]\n')

                    nome = input('Qual o nome do produto?\n > ')
                    info = input('\nInformações adicionais?\n > ')
                    quant = int(input('\nQuantos itens se encontram no estoque?\n > '))
                    estoque.addEstoque(nome, info, quant)

                case 2:
                    print(' = Editando um item =\n')

                    cod = input('Qual é o código do item a ser editado?\n > ')
                    estoque.editEstoque(int(cod))

                case 3:
                    print(' = Removendo um item =\n')

                    cod = input('Qual é o código do item a ser removido?\n > ')
                    estoque.removeEstoque(int(cod))

                case 'v':
                    estoque.updateEstoque()
                    return

                case 'x':
                    estoque.updateEstoque()
                    print('Saindo do programa.')
                    
                    time.sleep(.5)
                    exit()

def clearcmd():

    system('cls' if sysname == 'nt' else 'clear')

if __name__ =='__main__':
    clearcmd()
    Main.login()
