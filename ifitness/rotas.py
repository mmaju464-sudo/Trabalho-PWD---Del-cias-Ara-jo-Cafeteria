import os
import json
import random
from datetime import datetime
from functools import wraps

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from werkzeug.utils import secure_filename

from ifitness import app, db
from ifitness.modelos import Usuario, Produto, Pedido


# =========================================================
# FUNÇÕES DE PERMISSÃO
# =========================================================

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("usuario_id"):
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


def cliente_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("usuario_id"):
            return redirect(url_for("login"))

        if session.get("tipo_usuario") != "cliente":
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


def funcionario_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("usuario_id"):
            return redirect(url_for("funcionario_login"))

        if session.get("tipo_usuario") not in [
            "funcionario",
            "admin"
        ]:
            return redirect(url_for("funcionario_login"))

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("usuario_id"):
            return redirect(url_for("login"))

        if session.get("tipo_usuario") != "admin":
            return redirect(url_for("produtos"))

        return f(*args, **kwargs)

    return decorated_function


# =========================================================
# LOGIN DO CLIENTE
# =========================================================

@app.route("/login")
def login():

    return render_template(
        "login.html",
        resultado=None
    )


@app.route("/autenticar", methods=["POST"])
def autenticar():

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    senha = request.form.get(
        "senha",
        ""
    )

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario and usuario.verificar_senha(senha):

        # Funcionário e admin entram pela área própria
        if usuario.tipo in [
            "funcionario",
            "admin"
        ]:

            return render_template(
                "login.html",
                resultado="funcionario_login"
            )

        session.permanent = True

        session["usuario_id"] = usuario.id
        session["usuario"] = usuario.email
        session["nome_usuario"] = usuario.nome
        session["tipo_usuario"] = usuario.tipo

        session.setdefault(
            "carrinho",
            []
        )

        return redirect(
            url_for("produtos")
        )

    return render_template(
        "login.html",
        resultado="falha"
    )


# =========================================================
# CADASTRO DE CLIENTE
# =========================================================

@app.route("/cadastro")
def cadastro():

    return render_template(
        "cadastro.html",
        resultado=None
    )


@app.route(
    "/cadastro_usuario",
    methods=["GET", "POST"]
)
def cadastro_usuario():

    if request.method == "GET":

        return render_template(
            "cadastro_usuario.html",
            resultado=None
        )

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    senha = request.form.get(
        "senha",
        ""
    )

    if not nome or not email or not senha:

        return render_template(
            "cadastro_usuario.html",
            resultado="preencha"
        )

    existente = Usuario.query.filter_by(
        email=email
    ).first()

    if existente:

        return render_template(
        "gerenciar_funcionarios.html",
        funcionarios_ativos="funcionarios_ativos",
        funcionarios_desligados="funcionarios_desligados",
        mensagem="mensagem",
        data_atual=datetime.now().strftime("%d/%m/%Y")
)
    usuario = Usuario(
        nome=nome,
        email=email,
        tipo="cliente",
        status_funcionario="ativo",
        data_cadastro=datetime.now().strftime("%d/%m/%Y")
    )

    usuario.senha_criptografada = senha

    db.session.add(usuario)
    db.session.commit()

    return redirect(
        url_for("login")
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# PÁGINA INICIAL
# =========================================================

@app.route("/")
def inicio():

    if session.get("usuario_id"):

        if session.get("tipo_usuario") == "cliente":
            return redirect(
                url_for("produtos")
            )

        if session.get("tipo_usuario") == "funcionario":
            return redirect(
                url_for("funcionario_painel")
            )

        if session.get("tipo_usuario") == "admin":
            return redirect(
                url_for("admin")
            )

    return redirect(
        url_for("login")
    )


# =========================================================
# PRODUTOS / CARDÁPIO
# =========================================================

@app.route("/produtos")
@cliente_required
def produtos():

    categoria = request.args.get(
        "categoria",
        "todos"
    )

    busca = request.args.get(
        "busca",
        ""
    ).strip()

    query = Produto.query

    if categoria != "todos":

        query = query.filter(
            Produto.categoria.ilike(categoria)
        )

    if busca:

        query = query.filter(
            Produto.nome.ilike(
                f"%{busca}%"
            )
        )

    produtos_lista = query.order_by(
        Produto.nome
    ).all()

    return render_template(
        "produtos.html",
        produtos=produtos_lista,
        categoria=categoria,
        busca=busca
    )


# =========================================================
# CARRINHO
# =========================================================

@app.route("/adicionar/<int:id>")
@cliente_required
def adicionar_carrinho(id):

    produto = Produto.query.get(id)

    if not produto:
        return redirect(
            url_for("produtos")
        )

    carrinho = session.get(
        "carrinho",
        []
    )

    item_existente = None

    for item in carrinho:

        if item["id"] == produto.id:

            item_existente = item
            break

    if item_existente:

        item_existente["quantidade"] += 1

    else:

        carrinho.append({
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "img": produto.img,
            "quantidade": 1
        })

    session["carrinho"] = carrinho
    session.modified = True

    return redirect(
        url_for("carrinho")
    )


@app.route("/carrinho")
@cliente_required
def carrinho():

    carrinho_atual = session.get(
        "carrinho",
        []
    )

    total = 0

    for item in carrinho_atual:

        total += (
            float(item["preco"])
            * int(item["quantidade"])
        )

    return render_template(
        "carrinho.html",
        carrinho=carrinho_atual,
        total=total
    )


@app.route(
    "/remover_carrinho/<int:id>"
)
@cliente_required
def remover_carrinho(id):

    carrinho = session.get(
        "carrinho",
        []
    )

    novo_carrinho = []

    for item in carrinho:

        if item["id"] != id:
            novo_carrinho.append(item)

    session["carrinho"] = novo_carrinho
    session.modified = True

    return redirect(
        url_for("carrinho")
    )


@app.route(
    "/aumentar_carrinho/<int:id>"
)
@cliente_required
def aumentar_carrinho(id):

    carrinho = session.get(
        "carrinho",
        []
    )

    for item in carrinho:

        if item["id"] == id:
            item["quantidade"] += 1
            break

    session["carrinho"] = carrinho
    session.modified = True

    return redirect(
        url_for("carrinho")
    )


@app.route(
    "/diminuir_carrinho/<int:id>"
)
@cliente_required
def diminuir_carrinho(id):

    carrinho = session.get(
        "carrinho",
        []
    )

    for item in carrinho:

        if item["id"] == id:

            item["quantidade"] -= 1

            if item["quantidade"] <= 0:

                carrinho.remove(item)

            break

    session["carrinho"] = carrinho
    session.modified = True

    return redirect(
        url_for("carrinho")
    )


# =========================================================
# FINALIZAR PEDIDO
# =========================================================

@app.route(
    "/finalizar",
    methods=["GET", "POST"]
)
@cliente_required
def finalizar():

    carrinho = session.get(
        "carrinho",
        []
    )

    if not carrinho:

        return redirect(
            url_for("carrinho")
        )

    total = 0

    for item in carrinho:

        total += (
            float(item["preco"])
            * int(item["quantidade"])
        )

    if request.method == "GET":

        return render_template(
            "carrinho.html",
            carrinho=carrinho,
            total=total
        )

    data = request.form.get(
        "data",
        ""
    )

    hora = request.form.get(
        "hora",
        ""
    )

    tipo = request.form.get(
        "tipo",
        ""
    )

    local = request.form.get(
        "local",
        ""
    )

    descricao = request.form.get(
        "descricao",
        ""
    )

    try:

        pessoas = int(
            request.form.get(
                "pessoas",
                1
            )
        )

    except ValueError:

        pessoas = 1

    if pessoas < 50:

        prioridade = "baixa"

    elif pessoas <= 100:

        prioridade = "normal"

    else:

        prioridade = "alta"

    pedido = Pedido(
        itens=json.dumps(
            carrinho,
            ensure_ascii=False
        ),
        data=data,
        hora=hora,
        tipo=tipo,
        pessoas=pessoas,
        local=local,
        descricao=descricao,
        total=total,
        status="pendente",
        prioridade=prioridade,
        usuario_id=session["usuario_id"],
        origem="online",
        entregador=None
    )

    db.session.add(pedido)

    db.session.commit()

    session["carrinho"] = []

    session.modified = True

    return redirect(
        url_for("meus_pedidos")
    )


# =========================================================
# MEUS PEDIDOS
# =========================================================

@app.route("/meus_pedidos")
@cliente_required
def meus_pedidos():

    pedidos = Pedido.query.filter_by(
        usuario_id=session["usuario_id"]
    ).order_by(
        Pedido.id.desc()
    ).all()

    return render_template(
        "meus_pedidos.html",
        pedidos=pedidos
    )


# =========================================================
# CANCELAR PEDIDO
# =========================================================

@app.route(
    "/cancelar/<int:id>"
)
@cliente_required
def cancelar_pedido(id):

    pedido = Pedido.query.get(id)

    if not pedido:

        return redirect(
            url_for("meus_pedidos")
        )

    if pedido.usuario_id != session["usuario_id"]:

        return redirect(
            url_for("meus_pedidos")
        )

    if pedido.status == "pendente":

        pedido.status = "cancelado"

        db.session.commit()

    return redirect(
        url_for("meus_pedidos")
    )


# =========================================================
# API PARA ATUALIZAR STATUS DOS PEDIDOS
# =========================================================

@app.route("/api/meus_pedidos_status")
@cliente_required
def meus_pedidos_status():

    pedidos = Pedido.query.filter_by(
        usuario_id=session["usuario_id"]
    ).order_by(
        Pedido.id.desc()
    ).limit(20).all()

    return jsonify([
        {
            "id": pedido.id,
            "status": pedido.status,
            "entregador": pedido.entregador or ""
        }
        for pedido in pedidos
    ])


# =========================================================
# PERFIL
# =========================================================

@app.route("/perfil")
@cliente_required
def perfil():

    usuario = Usuario.query.get(
        session["usuario_id"]
    )

    if not usuario:

        session.clear()

        return redirect(
            url_for("login")
        )

    return render_template(
        "perfil.html",
        usuario=usuario
    )


@app.route(
    "/atualizar_perfil",
    methods=["POST"]
)
@cliente_required
def atualizar_perfil():

    usuario = Usuario.query.get(
        session["usuario_id"]
    )

    if not usuario:

        session.clear()

        return redirect(
            url_for("login")
        )

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    if nome:

        usuario.nome = nome

    arquivo = request.files.get(
        "foto"
    )

    if arquivo and arquivo.filename:

        nome_arquivo = secure_filename(
            arquivo.filename
        )

        if nome_arquivo:

            pasta = app.config.get(
                "UPLOAD_FOLDER",
                "ifitness/static/uploads"
            )

            os.makedirs(
                pasta,
                exist_ok=True
            )

            caminho = os.path.join(
                pasta,
                nome_arquivo
            )

            arquivo.save(caminho)

            usuario.foto = (
                "uploads/"
                + nome_arquivo
            )

    db.session.commit()

    session["nome_usuario"] = usuario.nome

    return redirect(
        url_for("perfil")
    )


# =========================================================
# LOGIN DOS FUNCIONÁRIOS
# =========================================================

@app.route("/funcionario/login")
def funcionario_login():

    return render_template(
        "funcionario_login.html",
        resultado=None
    )


@app.route(
    "/funcionario/autenticar",
    methods=["POST"]
)
def funcionario_autenticar():

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    senha = request.form.get(
        "senha",
        ""
    )

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if (
        usuario
        and usuario.verificar_senha(senha)
        and usuario.tipo in [
            "funcionario",
            "admin"
        ]
    ):

        # Funcionário desligado não entra
        if (
            usuario.tipo == "funcionario"
            and usuario.status_funcionario != "ativo"
        ):

            return render_template(
                "funcionario_login.html",
                resultado="desligado"
            )

        session.permanent = True

        session["usuario_id"] = usuario.id
        session["usuario"] = usuario.email
        session["nome_usuario"] = usuario.nome
        session["tipo_usuario"] = usuario.tipo
        session["carrinho"] = []

        if usuario.tipo == "admin":

            return redirect(
                url_for("admin")
            )

        return redirect(
            url_for("funcionario_painel")
        )

    return render_template(
        "funcionario_login.html",
        resultado="falha"
    )


# =========================================================
# PAINEL DOS FUNCIONÁRIOS
# =========================================================

@app.route("/funcionarios")
@funcionario_required
def funcionario_painel():

    pedidos = Pedido.query.order_by(
        Pedido.id.desc()
    ).all()

    clientes = Usuario.query.filter_by(
        tipo="cliente"
    ).order_by(
        Usuario.nome
    ).all()

    produtos = Produto.query.order_by(
        Produto.nome
    ).all()

    return render_template(
        "funcionarios.html",
        pedidos=pedidos,
        clientes=clientes,
        produtos=produtos
    )


# =========================================================
# FUNCIONÁRIO REGISTRAR PEDIDO
# =========================================================

@app.route(
    "/funcionario/novo_pedido",
    methods=["POST"]
)
@funcionario_required
def funcionario_novo_pedido():

    cliente_id = request.form.get(
        "cliente_id"
    )

    if not cliente_id:

        return redirect(
            url_for("funcionario_painel")
        )

    try:

        cliente_id = int(cliente_id)

    except ValueError:

        return redirect(
            url_for("funcionario_painel")
        )

    cliente = Usuario.query.filter_by(
        id=cliente_id,
        tipo="cliente"
    ).first()

    if not cliente:

        return redirect(
            url_for("funcionario_painel")
        )

    produto_ids = request.form.getlist(
        "produto_id"
    )

    quantidades = request.form.getlist(
        "quantidade"
    )

    sabores = request.form.getlist(
        "sabor"
    )

    itens = []

    total = 0

    for i, produto_id in enumerate(
        produto_ids
    ):

        if not produto_id:
            continue

        try:

            produto_id = int(produto_id)

        except ValueError:

            continue

        produto = Produto.query.get(
            produto_id
        )

        if not produto:
            continue

        try:

            quantidade = int(
                quantidades[i]
            )

        except (
            ValueError,
            IndexError
        ):

            quantidade = 1

        quantidade = max(
            1,
            quantidade
        )

        sabor = ""

        if i < len(sabores):

            sabor = sabores[i].strip()

        item = {
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "img": produto.img,
            "quantidade": quantidade
        }

        if sabor:

            item["sabor"] = sabor

        itens.append(item)

        total += (
            produto.preco
            * quantidade
        )

    if not itens:

        return redirect(
            url_for("funcionario_painel")
        )

    data = request.form.get(
        "data",
        ""
    )

    hora = request.form.get(
        "hora",
        ""
    )

    tipo = request.form.get(
        "tipo",
        ""
    )

    local = request.form.get(
        "local",
        ""
    )

    descricao = request.form.get(
        "descricao",
        ""
    )

    try:

        pessoas = int(
            request.form.get(
                "pessoas",
                1
            )
        )

    except ValueError:

        pessoas = 1

    if pessoas < 50:

        prioridade = "baixa"

    elif pessoas <= 100:

        prioridade = "normal"

    else:

        prioridade = "alta"

    pedido = Pedido(
        itens=json.dumps(
            itens,
            ensure_ascii=False
        ),
        data=data,
        hora=hora,
        tipo=tipo,
        pessoas=pessoas,
        local=local,
        descricao=descricao,
        total=total,
        status="pendente",
        prioridade=prioridade,
        usuario_id=cliente.id,
        origem="loja",
        entregador=None
    )

    db.session.add(pedido)

    db.session.commit()

    return redirect(
        url_for("funcionario_painel")
    )


# =========================================================
# FUNCIONÁRIO ATUALIZAR STATUS
# =========================================================

@app.route(
    "/funcionario/pedido/<int:id>/status",
    methods=["POST"]
)
@funcionario_required
def funcionario_atualizar_status(id):

    pedido = Pedido.query.get(id)

    if not pedido:

        return redirect(
            url_for("funcionario_painel")
        )

    novo_status = request.form.get(
        "status",
        "pendente"
    )

    status_permitidos = [
        "pendente",
        "em preparo",
        "pronto",
        "saiu para entrega",
        "entregue",
        "cancelado"
    ]

    if novo_status not in status_permitidos:

        return redirect(
            url_for("funcionario_painel")
        )

    pedido.status = novo_status

    if pedido.tipo == "entrega":

        pedido.entregador = request.form.get(
            "entregador",
            ""
        ).strip()

    db.session.commit()

    return redirect(
        url_for("funcionario_painel")
    )


# =========================================================
# GERENCIAR FUNCIONÁRIOS
# =========================================================

@app.route(
    "/gerenciar_funcionarios",
    methods=["GET", "POST"]
)
@app.route(
    "/admin/funcionarios",
    methods=["GET", "POST"]
)
@admin_required
def gerenciar_funcionarios():

    mensagem = None

    if request.method == "POST":

        nome = request.form.get(
            "nome",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        senha = request.form.get(
            "senha",
            ""
        )

        if not nome or not email or not senha:

            mensagem = (
                "Preencha todos os campos."
            )

        else:

            existente = Usuario.query.filter_by(
                email=email
            ).first()

            if existente:

                # Se for funcionário desligado,
                # não reutiliza o mesmo e-mail.
                mensagem = (
                    "Este e-mail já está cadastrado."
                )

            else:

                funcionario = Usuario(
                    nome=nome,
                    email=email,
                    tipo="funcionario",
                    status_funcionario="ativo",
                    data_entrada=datetime.now().strftime(
                        "%d/%m/%Y"
                    )
                )

                funcionario.senha_criptografada = senha

                db.session.add(
                    funcionario
                )

                db.session.commit()

                mensagem = (
                    "Funcionário cadastrado "
                    "com sucesso!"
                )

    funcionarios_ativos = Usuario.query.filter_by(
        tipo="funcionario",
        status_funcionario="ativo"
    ).order_by(
        Usuario.nome
    ).all()

    funcionarios_desligados = Usuario.query.filter_by(
        tipo="funcionario",
        status_funcionario="desligado"
    ).order_by(
        Usuario.id.desc()
    ).all()

    return render_template(
        "gerenciar_funcionarios.html",
        funcionarios_ativos=funcionarios_ativos,
        funcionarios_desligados=funcionarios_desligados,
        mensagem=mensagem
    )


# =========================================================
# DESLIGAR FUNCIONÁRIO
# =========================================================

@app.route(
    "/funcionario/desligar/<int:id>",
    methods=["POST"]
)
@admin_required
def desligar_funcionario(id):

    funcionario = Usuario.query.filter_by(
        id=id,
        tipo="funcionario"
    ).first()

    if not funcionario:

        return redirect(
            url_for("gerenciar_funcionarios")
        )

    data_saida = request.form.get(
        "data_saida",
        ""
    ).strip()

    motivo_saida = request.form.get(
        "motivo_saida",
        ""
    ).strip()

    observacao_saida = request.form.get(
        "observacao_saida",
        ""
    ).strip()

    if not data_saida:

        data_saida = datetime.now().strftime(
            "%d/%m/%Y"
        )

    else:

        try:

            data_obj = datetime.strptime(
                data_saida,
                "%Y-%m-%d"
            )

            data_saida = data_obj.strftime(
                "%d/%m/%Y"
            )

        except ValueError:

            pass

    if motivo_saida not in [
        "demitido",
        "pediu_demissao"
    ]:

        return redirect(
            url_for("gerenciar_funcionarios")
        )

    funcionario.data_saida = data_saida

    funcionario.motivo_saida = motivo_saida

    funcionario.observacao_saida = (
        observacao_saida
    )

    funcionario.status_funcionario = (
        "desligado"
    )

    db.session.commit()

    # Se o próprio funcionário estiver logado,
    # encerra a sessão.
    if session.get("usuario_id") == funcionario.id:

        session.clear()

    return redirect(
        url_for("gerenciar_funcionarios")
    )


# =========================================================
# ADMIN
# =========================================================

@app.route("/admin")
@admin_required
def admin():

    pedidos = Pedido.query.order_by(
        Pedido.id.desc()
    ).all()

    faturamento = 0

    for pedido in pedidos:

        if pedido.status != "cancelado":

            faturamento += float(
                pedido.total
            )

    total_pedidos = len(
        pedidos
    )

    pedidos_pendentes = len([
        pedido
        for pedido in pedidos
        if pedido.status == "pendente"
    ])

    # ==========================================
    # GRÁFICO DE MAIS VENDIDOS
    # ==========================================

    vendas = {}

    for pedido in pedidos:

        if pedido.status == "cancelado":
            continue

        try:

            itens = json.loads(
                pedido.itens
            )

        except (
            TypeError,
            json.JSONDecodeError
        ):

            itens = []

        for item in itens:

            nome = item.get(
                "nome",
                "Produto"
            )

            try:

                quantidade = int(
                    item.get(
                        "quantidade",
                        0
                    )
                )

            except (
                ValueError,
                TypeError
            ):

                quantidade = 0

            vendas[nome] = (
                vendas.get(nome, 0)
                + quantidade
            )

    mais_vendidos = sorted(
        vendas.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    nomes = [
        item[0]
        for item in mais_vendidos
    ]

    quantidades = [
        item[1]
        for item in mais_vendidos
    ]

    return render_template(
        "admin.html",
        pedidos=pedidos,
        faturamento=faturamento,
        total_pedidos=total_pedidos,
        pedidos_pendentes=pedidos_pendentes,
        nomes=nomes,
        quantidades=quantidades
    )


# =========================================================
# CONQUISTAS
# =========================================================

@app.route("/conquistas")
@cliente_required
def conquistas():

    usuario_id = session.get(
        "usuario_id"
    )

    usuario_atual = Usuario.query.get(
        usuario_id
    )

    if not usuario_atual:

        session.clear()

        return redirect(
            url_for("login")
        )

    pedidos = Pedido.query.filter(
        Pedido.usuario_id == usuario_id,
        Pedido.status != "cancelado"
    ).all()

    categorias = {
        "bolo": 0,
        "salgado": 0,
        "doce": 0,
        "bebida": 0,
        "café": 0,
        "chá": 0
    }

    for pedido in pedidos:

        try:

            itens = json.loads(
                pedido.itens
            )

        except (
            TypeError,
            json.JSONDecodeError
        ):

            itens = []

        for item in itens:

            try:

                produto_id = int(
                    item.get("id")
                )

            except (
                ValueError,
                TypeError
            ):

                continue

            try:

                quantidade = int(
                    item.get(
                        "quantidade",
                        0
                    )
                )

            except (
                ValueError,
                TypeError
            ):

                quantidade = 0

            produto = Produto.query.get(
                produto_id
            )

            if not produto:
                continue

            categoria = (
                produto.categoria
                .lower()
                .strip()
            )

            if categoria in categorias:

                categorias[categoria] += (
                    quantidade
                )

    nomes_categorias = {
        "bolo": "Bolos",
        "salgado": "Salgados",
        "doce": "Doces",
        "bebida": "Bebidas",
        "café": "Café",
        "chá": "Chá"
    }

    emojis = {
        "bolo": "🍰",
        "salgado": "🥟",
        "doce": "🍬",
        "bebida": "🥤",
        "café": "☕",
        "chá": "🍵"
    }

    conquistas_por_categoria = []

    for categoria, total in categorias.items():

        if total < 5:

            nivel = "Iniciante"
            proximo = "Bronze"
            restantes = 5 - total
            progresso = (
                total / 5
            ) * 100

        elif total < 10:

            nivel = "Bronze"
            proximo = "Prata"
            restantes = 10 - total
            progresso = (
                (total - 5) / 5
            ) * 100

        elif total < 15:

            nivel = "Prata"
            proximo = "Ouro"
            restantes = 15 - total
            progresso = (
                (total - 10) / 5
            ) * 100

        elif total < 20:

            nivel = "Ouro"
            proximo = "Platino"
            restantes = 20 - total
            progresso = (
                (total - 15) / 5
            ) * 100

        else:

            nivel = "Platino"
            proximo = None
            restantes = 0
            progresso = 100

        conquistas_por_categoria.append({
            "categoria": nomes_categorias[
                categoria
            ],
            "categoria_id": categoria,
            "total": total,
            "nivel": nivel,
            "emoji": emojis[categoria],
            "proximo": proximo,
            "restantes": restantes,
            "progresso": int(progresso)
        })

    return render_template(
        "conquistas.html",
        usuario=usuario_atual,
        conquistas=conquistas_por_categoria
    )


# =========================================================
# JOGO
# =========================================================

PERGUNTAS = [
    {
        "pergunta": "Qual produto é uma bebida?",
        "opcoes": [
            "Café",
            "Bolo",
            "Coxinha",
            "Brigadeiro"
        ],
        "resposta": "Café"
    },
    {
        "pergunta": "Qual desses é um doce?",
        "opcoes": [
            "Brigadeiro",
            "Coxinha",
            "Café",
            "Suco"
        ],
        "resposta": "Brigadeiro"
    },
    {
        "pergunta": "Qual desses é um salgado?",
        "opcoes": [
            "Coxinha",
            "Bolo",
            "Brigadeiro",
            "Café"
        ],
        "resposta": "Coxinha"
    },
    {
        "pergunta": "Qual bebida é normalmente feita com grãos torrados?",
        "opcoes": [
            "Café",
            "Suco",
            "Refrigerante",
            "Chá"
        ],
        "resposta": "Café"
    },
    {
        "pergunta": "Qual produto normalmente é feito com massa e recheio?",
        "opcoes": [
            "Salgado",
            "Café",
            "Suco",
            "Chá"
        ],
        "resposta": "Salgado"
    }
]


@app.route("/jogo")
@cliente_required
def jogo():

    usuario = Usuario.query.get(
        session["usuario_id"]
    )

    pergunta = random.choice(
        PERGUNTAS
    )

    session["resposta_jogo"] = (
        pergunta["resposta"]
    )

    return render_template(
        "jogos.html",
        pergunta=pergunta,
        usuario=usuario,
        resultado=None
    )


@app.route(
    "/jogo/responder",
    methods=["POST"]
)
@cliente_required
def responder_jogo():

    resposta = request.form.get(
        "resposta",
        ""
    )

    correta = session.get(
        "resposta_jogo"
    )

    usuario = Usuario.query.get(
        session["usuario_id"]
    )

    if resposta == correta:

        usuario.pontos += 10

        if usuario.pontos >= 50:

            usuario.recompensa_disponivel = True

        resultado = "acertou"

    else:

        resultado = "errou"

    db.session.commit()

    pergunta = random.choice(
        PERGUNTAS
    )

    session["resposta_jogo"] = (
        pergunta["resposta"]
    )

    return render_template(
        "jogos.html",
        pergunta=pergunta,
        usuario=usuario,
        resultado=resultado
    )


# =========================================================
# RECOMPENSA DO JOGO
# =========================================================

@app.route(
    "/jogo/resgatar",
    methods=["POST"]
)
@cliente_required
def resgatar_recompensa():

    usuario = Usuario.query.get(
        session["usuario_id"]
    )

    if (
        usuario
        and usuario.recompensa_disponivel
    ):

        usuario.recompensa_disponivel = False
        usuario.pontos = max(
            0,
            usuario.pontos - 50
        )

        db.session.commit()

    return redirect(
        url_for("jogo")
    )