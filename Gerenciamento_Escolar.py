# ==========================================================
# Trabalho Pratico 01 - Sistema de Gerenciamento Escolar
# Disciplina: Coding
# Curso: Analise e Desenvolvimento de Sistemas
# Turma: Bloco II (2026.2)
# ==========================================================

# ----------------------------------------------------------
# Classe Endereco (entidade independente)
# ----------------------------------------------------------
class Endereco:
    def __init__(self, rua, numero, cidade, cep):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.cep = cep

    def formatar(self):
        return f"{self.rua}, {self.numero} - {self.cidade} - CEP: {self.cep}"

    def validar_cep(self):
        return len(self.cep.replace("-", "")) == 8

    def __str__(self):
        return self.formatar()


# ----------------------------------------------------------
# Classe Aluno (AGREGACAO com Endereco)
# ----------------------------------------------------------
class Aluno:
    def __init__(self, nome, matricula, idade, endereco):
        self.nome = nome
        self.matricula = matricula
        self.idade = idade
        self.endereco = endereco  # AGREGAÇÃO: endereço pode sobreviver

    def matricular(self):
        print(f"[OK] Aluno {self.nome} (mat. {self.matricula}) matriculado.")

    def estudar(self):
        print(f"[..] {self.nome} esta estudando...")

    def trocar_endereco(self, novo_endereco):
        print(f"[>>] {self.nome} mudou de endereco.")
        self.endereco = novo_endereco

    def __str__(self):
        return f"Aluno({self.nome}, mat={self.matricula}) -> {self.endereco}"


# ----------------------------------------------------------
# Classe Professor (ASSOCIACAO com Escola)
# ----------------------------------------------------------
class Professor:
    def __init__(self, nome, cpf, disciplina, salario):
        self.nome = nome
        self.cpf = cpf
        self.disciplina = disciplina
        self.salario = salario
        self.escolas = []  # ASSOCIACAO N:N

    def vincular_escola(self, escola):
        if escola not in self.escolas:
            self.escolas.append(escola)

    def desvincular_escola(self, escola):
        if escola in self.escolas:
            self.escolas.remove(escola)

    def lecionar(self):
        if not self.escolas:
            print(f"[!!] Prof. {self.nome} nao esta vinculado a nenhuma escola.")
        else:
            nomes = ", ".join(e.nome for e in self.escolas)
            print(f"[>>] Prof. {self.nome} lecionando {self.disciplina} em: {nomes}")

    def __str__(self):
        return f"Professor({self.nome}, {self.disciplina})"


# ----------------------------------------------------------
# Classe SalaDeAula (COMPOSICAO - existe so dentro da Escola)
# ----------------------------------------------------------
class SalaDeAula:
    def __init__(self, numero, capacidade, andar):
        self.numero = numero
        self.capacidade = capacidade
        self.andar = andar
        self._aberta = False

    def abrir(self):
        self._aberta = True
        print(f"[++] Sala {self.numero} aberta.")

    def fechar(self):
        self._aberta = False
        print(f"[--] Sala {self.numero} fechada.")

    def alocar_aluno(self, aluno):
        if self._aberta:
            print(f"[OK] {aluno.nome} alocado na sala {self.numero}.")
        else:
            print(f"[!!] Sala {self.numero} esta fechada!")

    def __str__(self):
        return f"Sala {self.numero} (cap={self.capacidade}, andar={self.andar})"


# ----------------------------------------------------------
# Classe Escola (COMPOSICAO com Sala + ASSOCIACAO com Professor)
# ----------------------------------------------------------
class Escola:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.salas = []          # COMPOSICAO: salas morrem com a escola
        self.professores = []    # ASSOCIACAO: professores sobrevivem

    # --- COMPOSICAO ---
    def adicionar_sala(self, numero, capacidade, andar):
        sala = SalaDeAula(numero, capacidade, andar)
        self.salas.append(sala)
        print(f"[++] Sala {numero} adicionada em {self.nome}.")
        return sala

    def remover_sala(self, numero):
        for s in self.salas:
            if s.numero == numero:
                self.salas.remove(s)
                print(f"[--] Sala {numero} destruida.")
                return

    # --- ASSOCIACAO ---
    def contratar_professor(self, prof):
        if prof not in self.professores:
            self.professores.append(prof)
            prof.vincular_escola(self)

    def demitir_professor(self, prof):
        if prof in self.professores:
            self.professores.remove(prof)
            prof.desvincular_escola(self)
            print(f"[--] Prof. {prof.nome} demitido (segue existindo).")

    # --- LISTAGENS ---
    def listar_salas(self):
        print(f"\nSalas de {self.nome}:")
        for s in self.salas:
            print(f"   - {s}")

    def listar_professores(self):
        print(f"\nProfessores de {self.nome}:")
        for p in self.professores:
            print(f"   - {p}")

    # --- FECHAMENTO (prova da composicao) ---
    def fechar_escola(self):
        print(f"\n[XX] Fechando escola {self.nome}...")
        self.salas.clear()              # COMPOSICAO: salas destruidas
        for p in self.professores:
            p.desvincular_escola(self)  # ASSOCIACAO: profs sobrevivem
        self.professores.clear()

    def __str__(self):
        return f"Escola({self.nome})"


# ==========================================================
# BLOCO DE TESTE
# ==========================================================
if __name__ == "__main__":

    print("=" * 60)
    print("DEMONSTRACAO DO SISTEMA ESCOLAR")
    print("=" * 60)

    # 1) Enderecos (entidades independentes)
    end1 = Endereco("Rua A", 100, "Sao Paulo", "01001-000")
    end2 = Endereco("Av. B", 500, "Campinas", "13000-000")

    # 2) Aluno (AGREGACAO com endereco)
    aluno = Aluno("Maria", "2026001", 20, end1)
    aluno.matricular()
    aluno.trocar_endereco(end2)
    print(f"Endereco antigo ainda existe: {end1}\n")

    # 3) Professor (ASSOCIACAO com escola)
    prof = Professor("Joao", "123.456.789-00", "Programacao", 5000.0)

    # 4) Escola (COMPOSICAO com salas)
    escola = Escola("FATEC ZL", "00.111.222/0001-33")

    # 5) Composicao: escola cria salas
    escola.adicionar_sala(101, 40, 1)
    escola.adicionar_sala(102, 35, 1)

    # 6) Associacao: vincula professor
    escola.contratar_professor(prof)

    # 7) Listagens
    escola.listar_salas()
    escola.listar_professores()
    prof.lecionar()

    # 8) Prova da composicao: fechar escola destroi salas
    escola.fechar_escola()
    print(f"\nSalas apos fechar: {escola.salas}")
    print(f"Professor ainda existe? {prof}")