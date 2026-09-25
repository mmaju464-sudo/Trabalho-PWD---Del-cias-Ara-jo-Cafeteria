import sqlite3
import os


# ==========================================
# LOCAL DO BANCO
# ==========================================

BANCO = os.path.join(
    "instance",
    "ifitness.db"
)


# ==========================================
# VERIFICAR BANCO
# ==========================================

if not os.path.exists(BANCO):

    print("ERRO: banco não encontrado!")
    print(
        "Execute este arquivo dentro da "
        "pasta projeto_flask."
    )

    raise SystemExit


# ==========================================
# CONECTAR AO BANCO
# ==========================================

conexao = sqlite3.connect(BANCO)

cursor = conexao.cursor()


# ==========================================
# FUNÇÃO PARA ADICIONAR COLUNA
# ==========================================

def adicionar_coluna(
    tabela,
    coluna,
    definicao
):

    colunas = [
        linha[1]
        for linha in cursor.execute(
            f"PRAGMA table_info({tabela})"
        ).fetchall()
    ]

    if coluna not in colunas:

        cursor.execute(
            f"""
            ALTER TABLE {tabela}
            ADD COLUMN {coluna} {definicao}
            """
        )

        print(
            f"Coluna {tabela}.{coluna} adicionada!"
        )

    else:

        print(
            f"Coluna {tabela}.{coluna} já existe."
        )


# ==========================================
# ATUALIZAR USUÁRIOS
# ==========================================

adicionar_coluna(
    "usuarios",
    "tipo",
    "VARCHAR(20) NOT NULL DEFAULT 'cliente'"
)

adicionar_coluna(
    "usuarios",
    "data_entrada",
    "VARCHAR(20)"
)

adicionar_coluna(
    "usuarios",
    "data_saida",
    "VARCHAR(20)"
)

adicionar_coluna(
    "usuarios",
    "motivo_saida",
    "VARCHAR(50)"
)

adicionar_coluna(
    "usuarios",
    "observacao_saida",
    "VARCHAR(500)"
)

adicionar_coluna(
    "usuarios",
    "status_funcionario",
    "VARCHAR(20) NOT NULL DEFAULT 'ativo'"
)
adicionar_coluna(
    "usuarios",
    "data_cadastro",
    "VARCHAR(20)"
)


# ==========================================
# ATUALIZAR PEDIDOS
# ==========================================

adicionar_coluna(
    "pedidos",
    "origem",
    "VARCHAR(20) NOT NULL DEFAULT 'online'"
)

adicionar_coluna(
    "pedidos",
    "entregador",
    "VARCHAR(100)"
)



# ==========================================
# TRANSFORMAR ADMIN EM ADMIN
# ==========================================

cursor.execute(
    """
    UPDATE usuarios
    SET tipo = 'admin'
    WHERE lower(email) = lower('admin@gmail.com')
    """
)


# ==========================================
# GARANTIR STATUS DOS FUNCIONÁRIOS
# ==========================================

cursor.execute(
    """
    UPDATE usuarios
    SET status_funcionario = 'ativo'
    WHERE tipo = 'funcionario'
    AND (
        status_funcionario IS NULL
        OR status_funcionario = ''
    )
    """
)


# ==========================================
# CRIAR ADMIN SE NÃO EXISTIR
# ==========================================

admin = cursor.execute(
    """
    SELECT id
    FROM usuarios
    WHERE lower(email) =
    lower('admin@gmail.com')
    """
).fetchone()


if not admin:

    from ifitness import bcrypt

    senha = (
        bcrypt
        .generate_password_hash(
            "Admin123!"
        )
        .decode("utf-8")
    )

    cursor.execute(
        """
        INSERT INTO usuarios
        (
            nome,
            email,
            senha,
            foto,
            pontos,
            recompensa_disponivel,
            tipo,
            data_entrada,
            data_saida,
            motivo_saida,
            observacao_saida,
            status_funcionario
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Administrador",
            "admin@gmail.com",
            senha,
            None,
            0,
            0,
            "admin",
            None,
            None,
            None,
            None,
            "ativo"
        )
    )

    print()
    print("Administrador inicial criado!")
    print("E-mail: admin@gmail.com")
    print("Senha: Admin123!")


# ==========================================
# SALVAR ALTERAÇÕES
# ==========================================

conexao.commit()

conexao.close()


print()
print("==========================================")
print("BANCO ATUALIZADO COM SUCESSO!")
print("==========================================")
print()
print("Novos campos de funcionários adicionados.")
print("Nenhum produto foi apagado.")
print("Nenhum pedido foi apagado.")
print("Nenhum cliente foi apagado.")
print("==========================================")