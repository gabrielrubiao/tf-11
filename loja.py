class Cpf:
    """Representa e valida um CPF (11 caracteres)."""

    def __init__(self, valor: str):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor


class Email:
    """Representa e valida um email (nao vazio e contendo '@')."""

    def __init__(self, valor: str):
        if not valor:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self._valor = valor


class Cep:
    """Representa e valida um CEP (8 caracteres)."""

    def __init__(self, valor: str):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self._valor = valor


class Dinheiro:
    """Representa valores monetarios armazenados internamente em centavos (inteiro)."""

    def __init__(self, centavos: int):
        self._centavos = int(centavos)

    @classmethod
    from_reais(cls, reais: float):
    return cls(round(reais * 100))

    def somar(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar(self, quantidade: int) -> "Dinheiro":
        return Dinheiro(self._centavos * quantidade)

    def calcular_percentual(self, percentual: int) -> "Dinheiro":
        return Dinheiro(round(self._centavos * percentual / 100))

    def __str__(self) -> str:
        reais = self._centavos / 100
        return f"R$ {reais:.2f}"


class Status:
    """Representa o status de um pedido ('A', 'P' ou 'C')."""

    def __init__(self, codigo: str):
        self._codigo = codigo

    def descrever(self) -> str:
        if self._codigo == "A":
            return "aberto"
        if self._codigo == "P":
            return "pago"
        return "cancelado"

    def esta_aberto(self) -> bool:
        return self._codigo == "A"

    def esta_pago(self) -> bool:
        return self._codigo == "P"

    def definir_pago(self) -> "Status":
        return Status("P")

    def definir_cancelado(self) -> "Status":
        return Status("C")


class TipoNormal:
    """Define a regra de desconto para clientes normais (0%)."""

    def calcular_desconto(self, valor: Dinheiro) -> Dinheiro:
        return Dinheiro(0)


class TipoVip:
    """Define a regra de desconto para clientes VIP (10%)."""

    def calcular_desconto(self, valor: Dinheiro) -> Dinheiro:
        return valor.calcular_percentual(10)


class TipoFuncionario:
    """Define a regra de desconto para funcionarios (20%)."""

    def calcular_desconto(self, valor: Dinheiro) -> Dinheiro:
        return valor.calcular_percentual(20)


class Pessoa:
    """Guarda as informacoes pessoais de uma pessoa (nome, cpf, email)."""

    def __init__(self, nome: str, cpf: Cpf, email: Email):
        self._nome = nome
        self._cpf = cpf
        self._email = email

    def obter_nome(self) -> str:
        return self._nome


class Endereco:
    """Guarda as informacoes de localizacao (rua, cidade, cep)."""

    def __init__(self, rua: str, cidade: str, cep: Cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = cep

    def obter_cidade(self) -> str:
        return self._cidade


class Cliente:
    """Agrupa pessoa, endereco e tipo de cliente."""

    def __init__(self, pessoa: Pessoa, endereco: Endereco, tipo):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo

    def obter_nome_da_pessoa(self) -> str:
        return self._pessoa.obter_nome()

    def obter_cidade_do_endereco(self) -> str:
        return self._endereco.obter_cidade()

    def calcular_desconto(self, valor: Dinheiro) -> Dinheiro:
        return self._tipo.calcular_desconto(valor)


class Produto:
    """Representa um produto com nome e preco unitario."""

    def __init__(self, nome: str, preco: Dinheiro):
        self._nome = nome
        self._preco = preco

    def obter_nome(self) -> str:
        return self._nome

    def obter_preco(self) -> Dinheiro:
        return self._preco


class ItemDoPedido:
    """Representa um item contendo produto e quantidade."""

    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade

    def calcular_total(self) -> Dinheiro:
        return self._produto.obter_preco().multiplicar(self._quantidade)

    def imprimir(self):
        print(f"   {self._quantidade} x {self._produto.obter_nome()} = {self._produto.obter_preco().multiplicar(self._quantidade)}")


class ItensDoPedido:
    """Colecao de primeira classe para gerenciar os itens de um pedido."""

    def __init__(self, itens: list[ItemDoPedido]):
        self._itens = itens

    def esta_vazia(self) -> bool:
        return len(self._itens) == 0

    def calcular_total(self) -> Dinheiro:
        total = Dinheiro(0)
        for item in self._itens:
            total = total.somar(item.calcular_total())
        return total

    def imprimir(self):
        for item in self._itens:
            item.imprimir()


class Pedido:
    """Representa um pedido contendo cliente, itens e status."""

    def __init__(self, cliente: Cliente, itens: ItensDoPedido, status: Status):
        self._cliente = cliente
        self._itens = itens
        self._status = status

    def pagar(self) -> bool:
        if self._status.esta_pago():
            return True
        if not self._status.esta_aberto():
            return False
        if self._itens.esta_vazia():
            return False
        self._status = self._status.definir_pago()
        return True

    def cancelar(self) -> bool:
        if not self._status.esta_aberto():
            return False
        self._status = self._status.definir_cancelado()
        return True

    def esta_pago(self) -> bool:
        return self._status.esta_pago()

    def esta_aberto(self) -> bool:
        return self._status.esta_aberto()

    def calcular_valor_a_pagar(self) -> Dinheiro:
        total = self._itens.calcular_total()
        desconto = self._cliente.calcular_desconto(total)
        return total.subtrair(desconto)

    def imprimir(self, numero: str):
        print(f"Pedido {numero} - {self._cliente.obter_nome_da_pessoa()} - {self._cliente.obter_cidade_do_endereco()}")
        print(f"  status: {self._status.descrever()}")
        if self._status.esta_pago() or self._status.esta_aberto():
            self._itens.imprimir()
            total = self._itens.calcular_total()
            desconto = self._cliente.calcular_desconto(total)
            a_pagar = self._itens.calcular_total().subtrair(desconto)
            print(f"  total: {total} | desconto: {desconto} | a pagar: {a_pagar}")


class Pedidos:
    """Colecao de primeira classe para gerenciar o dicionario de pedidos."""

    def __init__(self, repositorio: dict[str, Pedido]):
        self._repositorio = repositorio

    def adicionar(self, numero: str, pedido: Pedido):
        self._repositorio[numero] = pedido

    def pagar(self, numero: str) -> bool:
        return self._repositorio[numero].pagar()

    def cancelar(self, numero: str) -> bool:
        return self._repositorio[numero].cancelar()

    def relatorio(self):
        for numero, pedido in self._repositorio.items():
            pedido.imprimir(numero)

    def calcular_arrecadado(self) -> Dinheiro:
        total = Dinheiro(0)
        for pedido in self._repositorio.values():
            if pedido.esta_pago():
                total = total.somar(pedido.calcular_valor_a_pagar())
        return total

    def contar_abertos(self) -> int:
        contador = 0
        for pedido in self._repositorio.values():
            if pedido.esta_aberto():
                contador += 1
        return contador


# Roteiro da Loja
try:
    cliente_ana = Cliente(
        Pessoa("Ana Souza", Cpf("12345678901"), Email("ana@email.com")),
        Endereco("Rua A", "Sorocaba", Cep("18000000")),
        TipoNormal()
    )
    cliente_diego = Cliente(
        Pessoa("Diego Rocha", Cpf("23456789012"), Email("diego@email.com")),
        Endereco("Rua B", "Itu", Cep("13300000")),
        TipoVip()
    )
    cliente_eva = Cliente(
        Pessoa("Eva Nunes", Cpf("34567890123"), Email("eva@email.com")),
        Endereco("Rua C", "Itu", Cep("13300000")),
        TipoVip()
    )
    cliente_gil = Cliente(
        Pessoa("Gil Alves", Cpf("45678901234"), Email("gil@email.com")),
        Endereco("Rua D", "Sorocaba", Cep("18000000")),
        TipoNormal()
    )

    produto_caderno = Produto("Caderno", Dinheiro.from_reais(15.50))
    produto_caneta = Produto("Caneta", Dinheiro.from_reais(2.50))
    produto_livro = Produto("Livro", Dinheiro.from_reais(89.50))
    produto_fone = Produto("Fone", Dinheiro.from_reais(60.00))

    colecao_pedidos = Pedidos({})

    colecao_pedidos.adicionar("1", Pedido(cliente_ana, ItensDoPedido([ItemDoPedido(produto_caderno, 2), ItemDoPedido(produto_caneta, 5)]), Status("A")))

    try:
        Pedido(cliente_ana, ItensDoPedido([ItemDoPedido(produto_caderno, 1)]), Status("A"))
    except ValueError as excecao:
        print(f"pedido 2 recusado: {excecao}")

    colecao_pedidos.adicionar("3", Pedido(cliente_ana, ItensDoPedido([ItemDoPedido(produto_livro, 1)]), Status("A")))

    try:
        Pedido(cliente_diego, ItensDoPedido([ItemDoPedido(produto_fone, 1)]), Status("A"))
    except ValueError as excecao:
        print(f"pedido 4 recusado: {excecao}")

    colecao_pedidos.adicionar("5", Pedido(cliente_diego, ItensDoPedido([ItemDoPedido(produto_fone, 1)]), Status("A")))
    colecao_pedidos.adicionar("6", Pedido(cliente_eva, ItensDoPedido([ItemDoPedido(produto_fone, 1)]), Status("A")))

    try:
        Pedido(cliente_gil, ItensDoPedido([ItemDoPedido(produto_caderno, 1)]), Status("A"))
    except ValueError as excecao:
        print(f"pedido 7 recusado: {excecao}")

    colecao_pedidos.adicionar("8", Pedido(cliente_gil, ItensDoPedido([ItemDoPedido(produto_fone, 2)]), Status("A")))

    print(f"pagar 1: {colecao_pedidos.pagar('1')}")
    print(f"pagar 3: {colecao_pedidos.pagar('3')}")
    print(f"pagar 5: {colecao_pedidos.pagar('5')}")
    print(f"pagar 6: {colecao_pedidos.pagar('6')}")
    print(f"cancelar 5: {colecao_pedidos.cancelar('5')}")
    print(f"cancelar 1: {colecao_pedidos.cancelar('1')}")

    colecao_pedidos.relatorio()
    print(f"arrecadado: {colecao_pedidos.calcular_arrecadado()}")
    print(f"abertos: {colecao_pedidos.contar_abertos()}")

except ValueError as excecao:
    pass