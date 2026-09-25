from ifitness import db, bcrypt


# ==========================================
# USUÁRIOS
# ==========================================

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    foto = db.Column(
        db.String(200),
        nullable=True
    )

    # ==========================================
    # TIPO DE USUÁRIO
    #
    # cliente
    # funcionario
    # admin
    # ==========================================

    tipo = db.Column(
        db.String(20),
        nullable=False,
        default="cliente"
    )

    # ==========================================
    # DADOS DO FUNCIONÁRIO
    # ==========================================

    data_entrada = db.Column(
        db.String(20),
        nullable=True
    )

    data_saida = db.Column(
        db.String(20),
        nullable=True
    )

    motivo_saida = db.Column(
        db.String(50),
        nullable=True
    )

    observacao_saida = db.Column(
        db.String(500),
        nullable=True
    )

    status_funcionario = db.Column(
        db.String(20),
        nullable=False,
        default="ativo"
    )
 

    # ==========================================
    # PONTOS DO JOGO
    # ==========================================

    pontos = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    recompensa_disponivel = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # ==========================================
    # PEDIDOS
    # ==========================================

    pedidos = db.relationship(
        "Pedido",
        backref="usuario",
        lazy=True
    )

    # ==========================================
    # SENHA
    # ==========================================

    @property
    def senha_criptografada(self):

        return self.senha

    @senha_criptografada.setter
    def senha_criptografada(
        self,
        senha_texto
    ):

        self.senha = (
            bcrypt
            .generate_password_hash(
                senha_texto
            )
            .decode("utf-8")
        )

    def verificar_senha(
        self,
        senha_texto
    ):

        return bcrypt.check_password_hash(
            self.senha,
            senha_texto
        )


# ==========================================
# PRODUTOS
# ==========================================

class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    categoria = db.Column(
        db.String(100),
        nullable=False
    )

    preco = db.Column(
        db.Float,
        nullable=False
    )

    img = db.Column(
        db.String(200),
        nullable=True
    )

    desc = db.Column(
        db.String(300),
        nullable=True
    )


# ==========================================
# PEDIDOS
# ==========================================

class Pedido(db.Model):

    __tablename__ = "pedidos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    itens = db.Column(
        db.Text,
        nullable=False
    )

    data = db.Column(
        db.String(20),
        nullable=False
    )

    hora = db.Column(
        db.String(10),
        nullable=False
    )

    tipo = db.Column(
        db.String(50),
        nullable=False
    )

    pessoas = db.Column(
        db.Integer,
        nullable=False
    )

    local = db.Column(
        db.String(200),
        nullable=False
    )

    descricao = db.Column(
        db.String(500),
        nullable=True
    )

    total = db.Column(
        db.Float,
        nullable=False
    )

    # ==========================================
    # STATUS
    # ==========================================

    status = db.Column(
        db.String(50),
        nullable=False,
        default="pendente"
    )

    prioridade = db.Column(
        db.String(50),
        nullable=False,
        default="normal"
    )

    # ==========================================
    # CLIENTE
    # ==========================================

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    # ==========================================
    # ORIGEM DO PEDIDO
    # ==========================================

    origem = db.Column(
        db.String(20),
        nullable=False,
        default="online"
    )

    # ==========================================
    # ENTREGADOR
    # ==========================================

    entregador = db.Column(
        db.String(100),
        nullable=True
    )