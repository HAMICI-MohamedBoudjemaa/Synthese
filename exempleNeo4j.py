from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Cm!ucp:2019"))

def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Bayo {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Bayo)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])

with driver.session() as session:
    session.write_transaction(add_friend, "Arthur", "Sylla")
    session.write_transaction(add_friend, "Arthur", "camara")
    session.write_transaction(add_friend, "Arthur", "Toure")
    session.read_transaction(print_friends, "Arthur")