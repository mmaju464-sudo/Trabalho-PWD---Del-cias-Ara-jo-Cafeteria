from ifitness import app, db
from ifitness.modelos import Produto


# ==========================================
# PRODUTOS DA DOCERIA
# ==========================================
# Cole aqui a lista PRODUTOS que já existe
# no seu app.py antigo.
#
# Exemplo:
#
# {
#     "nome": "Café Puro",
#     "categoria": "café",
#     "preco": 3.00,
#     "img": "cafe puro.webp",
#     "desc": "Intenso e aromático"
# }


PRODUTOS =[

    # BOLOS
    {
        "nome": "Bolo Decorado Chocolate Premium",
        "categoria": "bolo",
        "preco": 90.00,
        "img": "bolo_decorado_chocolate.jpg",
        "desc": "Recheio duplo e cobertura especial"
    },
    {
        "nome": "Bolo Decorado Tema Infantil",
        "categoria": "bolo",
        "preco": 120.00,
        "img": "bolo_infantil.jpg",
        "desc": "Personalizado com o tema da sua festa"
    },
    {
        "nome": "Bolo Decorado Casamento",
        "categoria": "bolo",
        "preco": 250.00,
        "img": "bolo_casamento.jpg",
        "desc": "Elegante e sofisticado para ocasiões especiais"
    },
    {
        "nome": "Bolo Decorado 15 Anos",
        "categoria": "bolo",
        "preco": 200.00,
        "img": "bolo_15anos.jpg",
        "desc": "Perfeito para comemorar um momento especial"
    },
    {
        "nome": "Bolo Decorado Chantilly",
        "categoria": "bolo",
        "preco": 85.00,
        "img": "bolo_chantilly.jpg",
        "desc": "Leve, bonito e delicioso"
    },


        {
        "nome": "Bolo de Cenoura",
        "categoria": "bolo",
        "preco": 35.00,
        "img": "cenoura.jpg",
        "desc": "Fofinho e saboroso"
    },
    {
        "nome": "Bolo de Milho",
        "categoria": "bolo",
        "preco": 35.00,
        "img": "milho.jpg",
        "desc": "Cremoso e saboroso"
    },
    {
        "nome": "Bolo de Arroz",
        "categoria": "bolo",
        "preco": 35.00,
        "img": "arroz.jpg",
        "desc": "Fofinho e cremoso"
    },
    {
        "nome": "Bolo de Banana",
        "categoria": "bolo",
        "preco": 35.00,
        "img": "Banana.jpg",
        "desc": "Fofinho com um toque de canela"
    },
    {
        "nome": "Bolo de Pink Lemonade",
        "categoria": "bolo",
        "preco": 35.00,
        "img": "PinkLimonade.jpg",
        "desc": "Fofinho e delicioso"
    },
    {
        "nome": "Bolo Red Velvet",
        "categoria": "bolo",
        "preco": 35.00,
        "img": "red.jpg",
        "desc": "Aveludado e delicioso"
    },

    # SALGADOS

    {
        "nome": "Coxinha de Frango",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "coxinha.jpg",
        "desc": "Recheio cremoso"
    },
    {
        "nome": "Coxinha de Costela",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "costela.jpg",
        "desc": "Deliciosa costela desfiada"
    },
    {
        "nome": "Coxinha de Brócolis",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "brocolis.jpg",
        "desc": "Vegana e cremosa"
    },
    {
        "nome": "Coxinha de Churros",
        "categoria": "doce",
        "preco": 3.00,
        "img": "coxinha_churros.jpg",
        "desc": "Massa de churros com doce de leite"
    },
    {
        "nome": "Coxinha de Carne Seca",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "carne_seca.jpg",
        "desc": "Carne seca com azeitona"
    },
    {
        "nome": "Coxinha de Camarão com Catupiry",
        "categoria": "salgado",
        "preco": 3.50,
        "img": "coxinha_catupiry.jpg",
        "desc": "Cremosa e saborosa"
    },
    {
        "nome": "Kibe com Queijo",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "kibe.jpg",
        "desc": "Crocante por fora e cremoso por dentro"
    },
    {
        "nome": "Esfiha de Carne",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "esfiha.jpg",
        "desc": "Bem temperada"
    },
    {
        "nome": "Enroladinho de Salsicha",
        "categoria": "salgado",
        "preco": 2.50,
        "img": "enroladinho.jpg",
        "desc": "Clássico de festa"
    },
    {
        "nome": "Bolinha de Queijo",
        "categoria": "salgado",
        "preco": 3.50,
        "img": "queijo.jpg",
        "desc": "Derrete na boca"
    },
    {
        "nome": "Pastel de 4 Queijos",
        "categoria": "salgado",
        "preco": 8.00,
        "img": "pastel_queijo.jpg",
        "desc": "Gorgonzola, mussarela, catupiry e provolone"
    },
    {
        "nome": "Pastel de Carne",
        "categoria": "salgado",
        "preco": 8.00,
        "img": "pastel_carne.jpg",
        "desc": "Carne bovina, milho e ervilha"
    },
    {
        "nome": "Pastel de Romeu e Julieta",
        "categoria": "doce",
        "preco": 8.00,
        "img": "pastel_R&J.jpg",
        "desc": "Queijo minas e goiabada"
    },
    {
        "nome": "Pastel de Banana com Canela",
        "categoria": "doce",
        "preco": 8.00,
        "img": "pastel_banana.jpg",
        "desc": "Banana, canela e leite condensado"
    },
    {
        "nome": "Pastel de Nutella",
        "categoria": "doce",
        "preco": 8.00,
        "img": "pastel_nutella.jpg",
        "desc": "Cremoso e delicioso"
    },
    {
        "nome": "Pastel de Pizza",
        "categoria": "salgado",
        "preco": 3.00,
        "img": "pastel_pizza.jpg",
        "desc": "Presunto, queijo, tomate e orégano"
    },
    {
        "nome": "Empadinha de Camarão",
        "categoria": "salgado",
        "preco": 4.00,
        "img": "empadinha_camarao.jpg",
        "desc": "Massa leve e recheio cremoso"
    },
    {
        "nome": "Empadinha de Doce de Leite",
        "categoria": "doce",
        "preco": 4.00,
        "img": "empadinha_doce_de_leite.jpg",
        "desc": "Massa leve e recheio cremoso"
    },
    {
        "nome": "Empadinha de Frango",
        "categoria": "salgado",
        "preco": 4.00,
        "img": "empadinha_frango.jpg",
        "desc": "Frango desfiado com catupiry"
    },
    {
        "nome": "Empadinha de Palmito",
        "categoria": "salgado",
        "preco": 4.00,
        "img": "empadinha_de_palmito.webp",
        "desc": "Palmito com requeijão"
    },
    {
        "nome": "Empadinha de Queijo",
        "categoria": "salgado",
        "preco": 4.00,
        "img": "empadinha_de_queijo.webp",
        "desc": "Queijo cremoso"
    },
   
    {
        "nome": "Alfajor",
        "categoria": "doce",
        "preco": 5.00,
        "img": "alfajor.jpg",
        "desc": "Delicioso e crocante"
    },
    {
        "nome": "Brigadeiro ",
        "categoria": "doce",
        "preco": 2.00,
        "img": "brigadeiro.webp",
        "desc": "Delicioso, cremoso e tradicional"
        
    },
    {
        "nome": "Beijinho",
        "categoria": "doce",
        "preco": 2.00,
        "img": "beijinho.jpg",
        "desc": "Delicioso, cremoso e tradicional"
        

    },
    {
        "nome": "Casadinho",
        "categoria": "doce",
        "preco": 2.00,
        "img": "brigadeiro_casadinho.jpg",
        "desc": "Delicioso e Misto de sabores"
    },
    {
        "nome": "Bicho de pé",
        "categoria": "doce",
        "preco": 2.00,
        "img": "bicho_de_pw.webp",
        "desc": "Delicioso e cremoso,sabor acentuado"
    },
    {
        "nome": "Brigadeiro de Churros",
        "categoria": "doce",
        "preco": 2.00,
        "img": "brigadeiro_de_churros.jpg",
        "desc": "Delicioso e cremoso"
    },
    {
        "nome": "Brigadeiro de Pistache",
        "categoria": "doce",
        "preco": 2.00,
        "img": "pistache.jpg",
        "desc": "Delicioso e cremoso"
    },
    {
        "nome": "Brigadeiro de Creme Brulée",
        "categoria": "doce",
        "preco": 2.00,
        "img": "Brigadeiro-de-creme-brulee.png",
        "desc": "Delicioso e cremoso"
    },
    { "nome": "Churros",
        "categoria": "doce",
        "preco": 5.00,
        "img": "churros.jpg",
        "desc": "Delicioso e crocante"
     },
     {
        "nome": "Bomba de chocolate",
        "categoria": "doce",
        "preco": 3.50,
        "img": "bomba_de_chocolate.jpg",
        "desc": "Macio  e cremoso"
     },
     {
        "nome": "Bomba de morango",
        "categoria": "doce",    
        "preco": 3.50,
        "img": "bomba_de_morango.jpg",
        "desc": "Macio, cremoso e um toque de morango cítrico"
     },
     {
        "nome": "Bomba de doce de leite",
        "categoria": "doce",
        "preco": 3.50,   
        "img": "bomba_de_doce_de_leite.webp",
        "desc": "Macio  e cremoso"
     },
   
     {
        "nome": "Bomba de creme com Ovomaltine",
        "categoria": "doce",
        "preco": 3.50,
        "img": "bomba_de_ovomaltine.jpg",
        "desc": "Macio  e cremoso"
     },
 
     {
        "nome": "Hacer fruta desidratada",
        "categoria": "doce",
        "preco": 5.00,
        "img": "Hacer-fruta-deshidratada.jpg",
        "desc": "Sabor intenso e natural"
     },
     {
         "nome": "Torta de Limão",
         "categoria": "doce",
         "preco": 12.00,
         "img": "torta-de-limao.webp",
         "desc": "Deliciosa, cremosa e refrescante"
     },
     {
        "nome": "Torta de Morango",
        "categoria": "doce",
        "preco": 12.00,
        "img": "torta_de_morango.jpg",
        "desc": "Deliciosa, cremosa e refrescante"
     },
     {
        "nome": "Torta Escocesa",
        "categoria": "doce",
        "preco": 8.00,
        "img": "torta_escocesa.webp",
        "desc": "Deliciosa, cremosa e refrescante"
     },
     {
        "nome": "Torta de Maracujá",
        "categoria": "doce",
        "preco": 12.00,
        "img": "Torta_de_Maracuja.webp",
        "desc": "Deliciosa e refrescante"
     },


    # BEBIDAS
   {
        "nome": "Coca-Cola 2L",
        "categoria": "bebida",
        "preco": 12.00,
        "img": "coca2l.jpg",
        "desc": "Clássico gelado"
    },
    {
        "nome": "Guaraná 2L",
        "categoria": "bebida",
        "preco": 10.00,
        "img": "guarana2l.jpg",
        "desc": "Sabor brasileiro"
    },
    {
        "nome": "Fanta Laranja 2L",
        "categoria": "bebida",
        "preco": 10.00,
        "img": "fanta2l.jpg",
        "desc": "Refrescante"
    },
    {
        "nome": "Coca-Cola Lata",
        "categoria": "bebida",
        "preco": 5.00,
        "img": "cocalata.jpg",
        "desc": "Prática e gelada"
    },
    {
        "nome": "Guaraná Lata",
        "categoria": "bebida",
        "preco": 5.00,
        "img": "guaranalata.jpg",
        "desc": "Ideal para uma pessoa"
    },
    {
        "nome": "Suco de Laranja",
        "categoria": "bebida",
        "preco": 7.00,
        "img": "suco_laranja.jpg",
        "desc": "Natural e refrescante"
    },
    {
        "nome": "Suco de Maracujá",
        "categoria": "bebida",
        "preco": 7.00,
        "img": "suco_maracuja.jpg",
        "desc": "Refrescante"
    },
    {
        "nome": "Suco de Uva",
        "categoria": "bebida",
        "preco": 8.00,
        "img": "suco_uva.jpg",
        "desc": "Doce e encorpado"
    },
    {
        "nome": "Suco de Morango",
        "categoria": "bebida",
        "preco": 8.00,
        "img": "suco_morango.jpg",
        "desc": "Delicioso"
    },
    {
        "nome": "Água Mineral",
        "categoria": "bebida",
        "preco": 3.00,
        "img": "agua.jpg",
        "desc": "Essencial"
    },
    {
        "nome": "Água com Gás",
        "categoria": "bebida",
        "preco": 4.00,
        "img": "agua_gas.jpg",
        "desc": "Refrescante"
    },
    {
        "nome": "Energético Lata 250ml",
        "categoria": "bebida",
        "preco": 6.00,
        "img": "refri5l.jpg",
        "desc": "Ideal para festas"
    },
    {
            "nome": "H2OH 500ml",
            "categoria": "bebida",
            "preco": 7.00,
            "img": "h2OH.jpg",
            "desc": "Refrescante e saboroso"
    },
    
    {
        "nome": "Chá Gelado",
        "categoria": "bebida",
        "preco": 6.00,
        "img": "cha.jpg",
        "desc": "Leve e saboroso"
    },
    {
        "nome": "Jarro  1L",
        "categoria": "bebida",
        "preco": 15.00,
        "img": "jarro_suco.jpg",
        "desc": "Serve várias pessoas"
    },
#CAFÉS

    {
        "nome": "Café Puro",
        "categoria": "café",
        "preco": 3.00,
        "img": "cafe puro.webp",
        "desc": "Intenso e aromático"
    },
    {
        "nome": "Café Espresso",
        "categoria": "café",
        "preco": 4.00,
        "img": "cafe espresso.jpg",
        "desc": "Concentrado, intenso e encorpado"
    },
    {
        "nome": "Espresso Duplo (Doppio)",
        "categoria": "café",
        "preco": 6.00,
        "img": "espresso duplo.jpg",
        "desc": "Duas doses de espresso, intenso e marcante"
    },
    {
        "nome": "Espresso Curto",
        "categoria": "café",
        "preco": 4.00,
        "img": "espresso curto.jpeg",
        "desc": "Pequeno, concentrado e intenso"
    },
    {
        "nome": "Espresso Longo",
        "categoria": "café",
        "preco": 4.50,
        "img": "espresso longo.jpg",
        "desc": "Mais longo, suave e aromático"
    },
    {
        "nome": "Ristretto",
        "categoria": "café",
        "preco": 4.50,
        "img": "ristretto.jpg",
        "desc": "Curto, intenso e muito concentrado"
    },
    {
        "nome": "Lungo",
        "categoria": "café",
        "preco": 4.50,
        "img": "lungo.webp",
        "desc": "Espresso mais longo e equilibrado"
    },
    {
        "nome": "Café Americano",
        "categoria": "café",
        "preco": 5.00,
        "img": "cafe americano.jpg",
        "desc": "Espresso diluído em água quente"
    },
    {
        "nome": "Café na Prensa Francesa",
        "categoria": "café",
        "preco": 7.00,
        "img": "prensa francesa.jpg",
        "desc": "Encorpado, aromático e de sabor marcante"
    },
    {
        "nome": "Café Moka",
        "categoria": "café",
        "preco": 6.00,
        "img": "cafe moka.jpg",
        "desc": "Intenso e encorpado, preparado na cafeteira italiana"
    },
    {
        "nome": "Café Turco",
        "categoria": "café",
        "preco": 7.00,
        "img": "cafe turco.jpg",
        "desc": "Tradicional, intenso e aromático"
    },
    {
        "nome": "Café Árabe",
        "categoria": "café",
        "preco": 7.00,
        "img": "cafe arabe.jpg",
        "desc": "Aromático e tradicional, com sabor marcante"
    },
    {
        "nome": "Café Grego",
        "categoria": "café",
        "preco": 7.00,
        "img": "cafe grego.webp",
        "desc": "Forte, encorpado e tradicional"
    },
    {
        "nome": "Café Vietnamita",
        "categoria": "café",
        "preco": 7.00,
        "img": "cafe viatnamita.webp",
        "desc": "Intenso e aromático, servido sem leite"
    },
    {
        "nome": "Café Etíope",
        "categoria": "café",
        "preco": 8.00,
        "img": "cafe etiope.jpg",
        "desc": "Aromático, delicado e tradicional"
    },

    {
        "nome": "Café com Leite",
        "categoria": "café",
        "preco": 5.00,
        "img": "cafe_leite.png",
        "desc": "Café tradicional combinado com leite quente"
    },
    {
        "nome": "Café Latte",
        "categoria": "café",
        "preco": 7.00,
        "img": "cafe latte.webp",
        "desc": "Espresso suave com bastante leite vaporizado"
    },
    {
        "nome": "Cappuccino",
        "categoria": "café",
        "preco": 8.00,
        "img": "cappuccino.jpg",
        "desc": "Espresso, leite vaporizado e espuma cremosa"
    },
    {
        "nome": "Flat White",
        "categoria": "café",
        "preco": 8.00,
        "img": "flat white.jpg",
        "desc": "Espresso intenso com leite vaporizado e cremoso"
    },
    {
        "nome": "Latte Macchiato",
        "categoria": "café",
        "preco": 8.00,
        "img": "latte macchiato.webp",
        "desc": "Leite cremoso marcado com espresso"
    },
    {
        "nome": "Espresso Macchiato",
        "categoria": "café",
        "preco": 6.00,
        "img": "espresso macchiato.webp",
        "desc": "Espresso intenso com um toque de espuma de leite"
    },
    {
        "nome": "Mocha",
        "categoria": "café",
        "preco": 9.00,
        "img": "mocha.webp",
        "desc": "Espresso, leite cremoso e chocolate"
    },
    {
        "nome": "Café Breve",
        "categoria": "café",
        "preco": 8.00,
        "img": "cafe breve.webp",
        "desc": "Espresso cremoso com leite e creme"
    },
    {
        "nome": "Cortado",
        "categoria": "café",
        "preco": 7.00,
        "img": "cortado.jpeg",
        "desc": "Espresso equilibrado com uma quantidade suave de leite"
    },
    {
        "nome": "Café Bombón",
        "categoria": "café",
        "preco": 8.00,
        "img": "cafe bombon.jpg",
        "desc": "Espresso cremoso combinado com leite condensado"
    },
    {
        "nome": "Café com Leite Condensado",
        "categoria": "café",
        "preco": 7.00,
        "img": "cafe com leite condensado.jpg",
        "desc": "Café intenso adoçado com leite condensado"
    },
    {
        "nome": "Café Au Lait",
        "categoria": "café",
        "preco": 6.00,
        "img": "cafe au lait.jpg",
        "desc": "Café filtrado combinado com leite quente"
    },
    {
        "nome": "Café Con Leche",
        "categoria": "café",
        "preco": 6.00,
        "img": "cafe con leche.jpg",
        "desc": "Café intenso combinado com leite quente"
    },
    {
        "nome": "Piccolo Latte",
        "categoria": "café",
        "preco": 7.00,
        "img": "piccolo latte.jpg",
        "desc": "Pequeno espresso com leite vaporizado e cremoso"
    },
    #CHÁS
    {
    "nome": "Chá de Camomila",
    "categoria": "chá",
    "preco": 5.00,
    "img": "cha de camomila.jpg",
    "desc": "Suave, aromático e delicado"
},
{
    "nome": "Chá de Hortelã",
    "categoria": "chá",
    "preco": 5.00,
    "img": "cha de hortela.webp",
    "desc": "Refrescante e aromático"
},
{
    "nome": "Chá Verde",
    "categoria": "chá",
    "preco": 5.50,
    "img": "cha verde.webp",
    "desc": "Leve, refrescante e tradicional"
},
{
    "nome": "Chá Preto",
    "categoria": "chá",
    "preco": 5.50,
    "img": "cha preto.jpg",
    "desc": "Intenso, encorpado e aromático"
},
{
    "nome": "Chá de Hibisco",
    "categoria": "chá",
    "preco": 5.50,
    "img": "cha de hibisco.webp",
    "desc": "Aromático, marcante e levemente ácido"
},
{
    "nome": "Chá de Frutas Vermelhas",
    "categoria": "chá",
    "preco": 6.00,
    "img": "cha frutas vermelhas.webp",
    "desc": "Frutado, aromático e saboroso"
},

{
    "nome": "Chá de Canela",
    "categoria": "chá",
    "preco": 5.50,
    "img": "cha de canela.jpg",
    "desc": "Aromático, quente e levemente adocicado"
},
{
    "nome": "Chá de Limão",
    "categoria": "chá",
    "preco": 5.50,
    "img": "cha de limao.webp",
    "desc": "Leve, cítrico e refrescante"
},
{
    "nome": "Chá Gelado de Pêssego",
    "categoria": "chá",
    "preco": 7.00,
    "img": "cha gelado de pessego.webp",
    "desc": "Refrescante, frutado e suave"
},
{
    "nome": "Chá Gelado de Limão",
    "categoria": "chá",
    "preco": 7.00,
    "img": "cha gelado de limao.webp",
    "desc": "Refrescante e com sabor cítrico"
},
{
    "nome": "Chá Gelado de Frutas Vermelhas",
    "categoria": "chá",
    "preco": 7.50,
    "img": "cha gelado frutas vermelhos.webp",
    "desc": "Frutado, refrescante e aromático"
}
]

# ==========================================
# INSERIR PRODUTOS
# ==========================================

with app.app_context():

    print()
    print("===================================")
    print("  CADASTRANDO PRODUTOS NO BANCO")
    print("===================================")
    print()


    # Garante que as tabelas existem
    db.create_all()


    adicionados = 0
    existentes = 0


    for produto in PRODUTOS:

        # Verifica se o produto já existe
        produto_existente = Produto.query.filter_by(
            nome=produto["nome"]
        ).first()


        if produto_existente:

            print(
                f"Já existe: {produto['nome']}"
            )

            existentes += 1

            continue


        novo_produto = Produto(

            nome=produto["nome"],

            categoria=produto["categoria"],

            preco=produto["preco"],

            img=produto.get("img"),

            desc=produto.get("desc")

        )


        db.session.add(
            novo_produto
        )


        print(
            f"Adicionado: {produto['nome']}"
        )

        adicionados += 1


    # Salva tudo no banco
    db.session.commit()


    print()
    print("===================================")
    print("          FINALIZADO!")
    print("===================================")
    print(
        f"Produtos adicionados: {adicionados}"
    )
    print(
        f"Produtos que já existiam: {existentes}"
    )
    print(
        f"Total no banco: {Produto.query.count()}"
    )
    print("===================================")
    print()