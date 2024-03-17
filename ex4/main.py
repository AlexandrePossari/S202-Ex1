from database import Database
from helper.writeAJson import writeAJson

db = Database(database="mercado", collection="compras")
#db.resetDatabase()

# 1- Média de gasto total:
#result = db.collection.aggregate([
#    {"$unwind": "$produtos"},
#    {"$group": {"_id": "$cliente_id", "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
#    {"$group": {"_id": None, "media": {"$avg": "$total"}}}
#])
#
#writeAJson(result, "Média de gasto total")

# 2- Cliente que mais comprou em cada dia:
#result = db.collection.aggregate([
#     {"$unwind": "$produtos"},
#     {"$group": {"_id": {"cliente": "$cliente_id", "data": "$data_compra"}, "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
#     {"$sort": {"_id.data": 1, "total": -1}},
#     {"$group": {"_id": "$_id.data", "cliente": {"$first": "$_id.cliente"}, "total": {"$first": "$total"}}}
#])
#
#writeAJson(result, "Cliente que mais comprou em cada dia")

# 3- Produto mais vendido:
# result = db.collection.aggregate([
#     {"$unwind": "$produtos"},
#     {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
#     {"$sort": {"total": -1}},
#     {"$limit": 1}
# ])

result = db.collection.aggregate([
    {"$unwind": "$produtos"},
    {"$group": {"_id": "$data_compra", "totalDeVendas": {"$sum": "$produtos.quantidade"}}},
    {"$sort": {"total": -1}}
])

writeAJson(result, "Total de vendas por dia")

result = db.collection.aggregate([
    {"$unwind": "$produtos"},
    {"$group": {"_id": "$produtos.descricao", "totalVendido": {"$sum": "$produtos.quantidade"}}},
    {"$sort": {"totalVendido": -1}},
    {"$limit": 1},
    {"$project": {"_id": 1, "totalVendido": 1}},
])

writeAJson(result, "Produto mais vendido em todas as compras")

result = db.collection.aggregate([
    {"$unwind": "$produtos"},
    {"$group": {"_id": "$cliente_id", "gastos": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
    {"$sort": {"gastos": -1}},
    {"$limit": 1}
])

writeAJson(result, "Cliente que mais gastou em uma única compra")

result = db.collection.aggregate([
    {"$unwind": "$produtos"},
    {"$match": {"produtos.quantidade": {"$gt": 1}}},
    {"$group": {"_id": "$produtos.descricao", "totalVendido": {"$sum": "$produtos.quantidade"}}},
    {"$sort": {"totalVendido": -1}},
    {"$project": {"_id": 1, "totalVendido": 1}},
])

writeAJson(result, "Todos os produtos que tiveram quantidade vendida acima de 1 unidade")