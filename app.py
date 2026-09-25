from ifitness import app, db
from ifitness.modelos import Usuario, Produto, Pedido


# ==========================================
# CRIA AS TABELAS
# ==========================================

with app.app_context():

    db.create_all()


# ==========================================
# INICIA O SISTEMA
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )