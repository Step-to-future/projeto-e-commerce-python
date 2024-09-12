class Produto:
    nome: str
    descricao: str
    preco_compra: float
    preco_venda: float
    codigo: int
    
    def __init__(self, nome, descricao, preco_compra, preco_venda, codigo):
        return f"Produto: {self.nome}; Cód.: {self.codigo}; Descrição: {self.descricao}; Preço de compra: R$ {self.preco_compra}; Preço de venda: R$ {self.preco_venda}"