from abc import ABC, abstractmethod
import uuid
from datetime import date,timedelta


class Logavel(ABC):
    # Qualquer classe logável DEVE implementar logar_entrada().
    """"terminar"""
    @abstractmethod
    def logar_entrada(self):
        pass

class IdentificavelMixin:
    # Gera um ID único; combine‑o com outras classes."
    
    def __init__(self):
        self.__id=uuid.uuid4()

    def get_id(self):
        return self.__id
        

class AuditavelMixin:
    # Fornece logs simples ao console
    ''''termianr'''
    def log_evento(self, evento: str):
        # TODO: imprimir no formato  [LOG] <evento>
        pass

class Pessoa:
    #Classe base para pessoas do sistema.
    def __init__(self, nome: str, cpf: str):
        self._nome=nome
        self._cpf=cpf

    @property
    def nome(self):
        return self._nome
        
    def __str__(self):
        return (f"{self._nome} ({self._cpf})")


class Ingresso:
    def __init__(self, codigo: str, tipo: str, preco: float):
        self.codigo = codigo
        self.tipo = tipo  # ex.: 'Pista', 'VIP', 'Backstage'
        self.preco = preco

    def __str__(self):
        return f"{self.codigo} - {self.tipo} – R$ {self.preco:.2f}"


class Cliente(Pessoa):
    """Herda de Pessoa e possui ingressos."""
    def __init__(self, nome: str, cpf: str, email: str):
        super().__init__(nome,cpf)
        self._email=email
        self._ingressos=[]

    def comprar_ingresso(self, ingresso: Ingresso):
        self._ingressos.append(ingresso)
        
    def listar_ingressos(self):
        
        for i in self._ingressos:
            return i.__str__
    
    def nome(self):
        return self.nome
    

        

# -------------------------------------------------
# 6) Funcionario (herança múltipla + mixins)      🡇
# -------------------------------------------------
# TODO: Implementar a classe Funcionario
# - Herda de Pessoa, IdentificavelMixin e Logavel (pode usar AuditavelMixin)
# - Atributos: cargo, registro
# - Métodos:
#   • exibir_dados()    → imprime nome, cargo, registro e ID
#   • logar_entrada()   → registra no log

class Funcionario(Pessoa,Logavel,IdentificavelMixin,AuditavelMixin): 
    """Terminar"""
    def __init__(self,cargo,nome,cpf,):
        super().__init__(nome,cpf)
        self._cargo=cargo
        self._registro=[]
    
    def exibir_dados(self): 
        return f"Funcionario: {self._nome} \ncargo {self._cargo} \nCPF:{self._cpf} \nRegistro: {self._registro}"
    
    def nome(self):
        return self._nome
    
    def logar_entrada(self):
        self._registro.append(date.today().strftime("%d/%m"))
        print(f"o Funcionario {self._nome} entrou em {date.today()}")

    def log_evento(self, evento: str):
         print(f"[LOG] <{evento}>")

# -------------------------------------------------
# 7) Palco (objeto de composição)                 🡇
# -------------------------------------------------


# -------------------------------------------------
# 8) Festival (composição com Palco)              🡇
# -------------------------------------------------
# TODO: Implementar a classe Festival
# - Atributos: nome, data, local, palco
# - Listas: clientes, equipe, ingressos
# - Métodos:
#   • vender_ingresso(cliente, ingresso)  (checar duplicidade & capacidade)
#   • adicionar_funcionario(func)
#   • listar_clientes()
#   • listar_equipe()
#   • listar_ingressos()
class Festival:
    def __init__(self,nome, local,nomep,capacidade,*valores): 
        self.nome=nome
        self.data=date.today()+timedelta(days=15)
        self.local=local
        self.palco= self.Palco(nomep,capacidade)
        self.clientes=[]
        self.equipe=[] 
        self.ingressos=[*valores]

    class Palco:
    
        def __init__(self, nome: str, capacidade: int):
            self.nome=nome
            self.capacidade=capacidade

        def resumo(self): 
            return f"Palco {self.nome} - cap. {self.capacidade} pessoas"
    
    def vender_ingresso(self,cliente, ingresso):
        for i in self.ingressos:
            if cliente in self.clientes:
                 print("Você ja fez uma compra")
            else:
                if i.preco == ingresso.preco and i.tipo==ingresso.tipo and i.codigo==ingresso.codigo and self.palco.capacidade>=1:
                    self.clientes.append(cliente)
                    cliente.comprar_ingresso(i)
                    self.ingressos.remove(i)
                    self.palco.capacidade-=1
                    return  
                
        print("Não é possivel realizar a venda")
           
        

    def adicionar_funcionario(self,*func):
        for f in func:
            self.equipe.append(f)

    def listar_clientes(self):
        print("Clientes:")
        for c in self.clientes:
            print(c)
    
    def listar_equipe(self):
        print("EQUIPE:")
        for i in self.equipe:
            print(i.exibir_dados())


    def listar_ingressos(self):
        print("INGRESSOS DIPONIVEIS:")
        for i in self.ingressos:
            print(f"{i}")

# -------------------------------------------------
# 9) EmpresaEventos                               🡇
# -------------------------------------------------
class EmpresaEventos:
    """Agrupa seus festivais (has‑a)."""
    def __init__(self, nome):
        self.festivais=[]
        if len(nome)>=3:    
            self.nome=nome
        else:
             raise ValueError ("Nome invalido")
    

    @property
    def nome(self):
        return self.nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        return len(novo_nome)>= 3
    
    def adicionar_festival(self, festival):
        self.festivais.append(festival)

    def buscar_festival(self, nome: str):
        for f in self.festivais:
            if f.nome == nome:
                return f"{f.nome}"
            
    def listar_festivais(self):
        for f in self.festivais:
            print(f"{f.nome}:{len(f.equipe)}funcionarios, possui {len(f.clientes)} clientes, contado com {len(f.ingressos)} para {f.data.strftime('%d/%m')}")

# -------------------------------------------------
# 10) Auditor (Identificável + Logável)           🡇
# -------------------------------------------------
# TODO: Implementar a classe Auditor
# - Herda de IdentificavelMixin e Logavel
# - Atributo: nome
# - Métodos:
#   • logar_entrada() → registra entrada no sistema
#   • auditar_festival(fest) → verifica:
#         ▸ Nº de clientes ≤ capacidade do palco
#         ▸ existe ao menos 1 funcionário
#     imprime relatório de conformidade
#   • __str__() → "Auditor <nome> (ID: ...)"

class Auditor(IdentificavelMixin,Logavel):
    def __init__(self,nome):
        super().__init__()
        self._nome=nome
    
    def logar_entrada(self):
        print(f"Nome: {self._nome} - Entrada: {date.today()}")

    def auditar_festival(self,fest):
        func=len(fest.equipe)
        if (fest.palco.capacidade - len(fest.clientes)) > 0:
            if func > 0:
                return f"O palco possuí {fest.palco.capacidade - len(fest.clientes)} disponiveis, contando com {func} funcionarios"
        else:
            return  f"O palco {fest.palco.nome} está lotado"
      
    def __str__(self):
        return f"Auditor <{self._nome}> (ID: {self.get_id()})"
    
    

# -------------------------------------------------
# 11) Bloco de teste                              🡇
# -------------------------------------------------
if __name__ == "__main__":
    """
    TODO:
      • Crie 1 empresa, 2 festivais, clientes, equipe e auditor.
      • Venda ingressos, liste participantes, audite festivais.
      • Mostre saídas no console para validar implementações.
    """
    c1= Cliente("Pedro","12349416095","Pedro@gmail.com")
    c2=Cliente("Carol","12434647689","Carol@gmail.com")
    c3=Cliente("Ana","33259451492","Ana@gmail.com")

    fu1=Funcionario("Gerente","Hiudezia","12425654675657")
    fu2=Funcionario("Jardineiro","Leila","2336475675868")
    fu3=Funcionario("Atendente","jalison","3234536457457")

    i1=Ingresso("233464574","VIP",15.5)
    i2=Ingresso("1456586","Comum",5.0)
    i3=Ingresso("14788097","Plus",10.0)
    i4=Ingresso("5489795","Vip",15.5)
    i5=Ingresso("1249878","Comum",5.0)
    i6=Ingresso("1453535","Comum",5.0)
    i7=Ingresso("5746747","Comum",5.0)

    ing=Ingresso("5746747","Comum",5.0)
    iing=Ingresso("1453535","Comum",5.0)
    io=Ingresso("1249878","Comum",5.0)
    igres=Ingresso("1456586","Comum",5.0)
    soo=Ingresso("14788097","Plus",10.0)

    f1=Festival("masc","Los Angeles","zora", 1000,i1,i2,i3,i4,i5,i6,i7)
    f2=Festival("dell", "París", "bita",1200,i1,i2,i3,i4,i5,i6,i7)

    Au=Auditor("Feliz")

    emp= EmpresaEventos("multshow")

    p=Pessoa("Pato","345457547e6")
    fu1.logar_entrada()
    fu2.logar_entrada()
    fu3.logar_entrada()

    f1.adicionar_funcionario(fu1,fu2,fu3)
    f1.vender_ingresso(c1,ing)
    f1.vender_ingresso(c2,iing)
    f1.vender_ingresso(c3,soo)
    f1.listar_clientes()
    f1.listar_equipe()
    f1.listar_ingressos()

    f2.adicionar_funcionario(fu1,fu3)
    f2.vender_ingresso(c1,ing)
    f2.vender_ingresso(c2,igres)
    

    emp.adicionar_festival(f1)
    emp.adicionar_festival(f2)
    print(emp.buscar_festival("dell"))
    emp.listar_festivais()

    print(Au.auditar_festival(f1))
    print(Au)

