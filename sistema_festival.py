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
        self.id=uuid.uuid4()

    def get_id(self):
        return self.id
        

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
        return self.nome
        
    def __str__(self):
        return f"{self.nome} ({self._cpf})"


class Ingresso:
    def __init__(self, codigo: str, tipo: str, preco: float):
        self.codigo = codigo
        self.tipo = tipo  # ex.: 'Pista', 'VIP', 'Backstage'
        self.preco = preco

    def __str__(self):
        return f"{self.codigo}] {self.tipo} – R$ {self.preco:.2f}"


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
        self.cargo=cargo
        self.registro=date.today()
    
    def exibir_dados(self): 
        return f"Funcionario: {self.nome} \ncargo {self.cargo} \nCPF:{self._cpf} \nRegistro: {self.registro}"
    
    def nome(self):
        return self.nome
    
    def logar_entrada(self):
        print(date.today())

    def log_evento(self, evento: str):
        return f"Você está participando do {evento}"

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
            if i.valor == ingresso.valor and i.tipo==ingresso.tipo and i.codigo==ingresso.codigo and self.palco.capacidade>=1:
                self.clientes.append(cliente)
                cliente.comprar_ingresso(i)
                self.ingressos.remove(i)
                self.palco.capacidade-=1
                break
            else:
                print("Não é possivel realizar a venda")
                return
    
    def adicionar_funcionario(self,func):
        self.equipe.append(func)
    
    def listar_equipe(self):
        print("EQUIPE:")
        for i in self.equipe:
            print(f"{i.exibir_dados()}")


    def listar_ingressos(self):
        print("INGRESSOS DIPONIVEIS:")
        for i in self.ingressos:
            print(f"{i.__str__}")

# -------------------------------------------------
# 9) EmpresaEventos                               🡇
# -------------------------------------------------
class EmpresaEventos:
    """Agrupa seus festivais (has‑a)."""
    def __init__(self, nome):
        # TODO: validar nome (≥ 3 letras) e criar lista vazia de festivais
        if not self.nome_set(nome):
            raise ValueError("esse nome não é compativel")
        self.nome=nome
        self.festivais=[]
    

    @property
    def nome(self):
        return self.nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        return len(novo_nome.strip())>= 3
    
    def adicionar_festival(self, festival):
        self.festivais.append(festival)

    def buscar_festival(self, nome: str):
        for f in self.festivais:
            if f.nome == nome:
                return f"{f.nome}"
            
    def listar_festivais(self):
        for f in self.festivais:
            return f"{f.nome}:{len(f.equipe)}funcionarios, possui {len(f.clientes)} clientes, contado com {len(f.ingressos)} para {f.data.strftime('%d/%m')} "

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
        self.nome=nome
    
    def logar_entrada(self):
        return f"entrada comfirmada"
    
    def auditar_festival(self,fest):
        if len(fest.clientes) <= len(fest.palco.capacidade):
            func=len(fest.equipe)
            if (len(fest.palco.capacidade) - len(fest.clientes)) > 0:
                return f"O palco {fest.palco} possui {len(fest.palco.capacidade) - len(fest.clientes)} assentoa disponivéis, contando com {func} funcioanrios disponiveis no festival {fest.nome}"
            else:
                return  f"O palco {fest.palco} não possui assentos disponivéis, contando com {func} funcioanrios disponivéis no festival {fest.nome}"
        else:
            return f"O palco está excedendo o limite, por favor reitirar {len(fest.clientes) - len(fest.palco.capacidade)} espectadores!"
        
    def __str__(self):
        return f"Auditor <{self.nome}> (ID: {self.id})"

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
    

    f1=Festival("masc","Los Angeles","zora", 1000)
    f2=Festival("dell", "París", "bita",1200)
    f3=Festival("mill","Pau dos Ferros","luL",500)
    

    emp= EmpresaEventos("multshow")


