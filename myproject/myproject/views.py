from django.shortcuts import render, redirect
from django.apps import apps

from neo4j import GraphDatabase

def get_driver():
    uri = "bolt://localhost:7687"  # Assure-toi que l'URI est correct
    user = "neo4j"  # Remplace par ton nom d'utilisateur
    password = "ibou1999"  # Remplace par ton mot de passe
    return GraphDatabase.driver(uri, auth=(user, password))


def create_person(request):
    driver = get_driver()
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']

        with driver.session() as session:
            session.run("CREATE (p:Person {name: $name, age: $age})", name=name, age=int(age))

        return redirect('list_person')
    return render(request, 'create_person.html')


def create_relation(request):
    driver = get_driver()
    if request.method == 'POST':
        name1 = request.POST['name1']
        name2 = request.POST['name2']
        relation = request.POST['relation']

        with driver.session() as session:
            # Find both persons and create the relationship
            session.run(
                "MATCH (p1:Person {name: $name1}), (p2:Person {name: $name2}) "
                "CREATE (p1)-[r:RELATIONSHIP {type: $relation}]->(p2)",
                name1=name1, name2=name2, relation=relation
            )

        return redirect('list_person')
    return render(request, 'create_relation.html')

def list_person(request):
    driver = get_driver()
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p.name AS name, p.age AS age, ID(p) AS id")
        persons = [{'name': record['name'], 'age': record['age'], 'id': record['id']} for record in result]

    return render(request, 'list_person.html', {'persons': persons})

def update_person(request, person_id):
    driver = get_driver()
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']

        with driver.session() as session:
            session.run("MATCH (p:Person) WHERE ID(p) = $id SET p.name = $name, p.age = $age", id=int(person_id), name=name, age=int(age))

        return redirect('list_person')

    with driver.session() as session:
        result = session.run("MATCH (p:Person) WHERE ID(p) = $id RETURN p.name AS name, p.age AS age", id=int(person_id))
        person = result.single()

    return render(request, 'update_person.html', {'person': person})

def delete_person(request, person_id):
    driver = get_driver()
    with driver.session() as session:
        session.run("MATCH (p:Person) WHERE ID(p) = $id DELETE p", id=int(person_id))

    return redirect('list_person')
