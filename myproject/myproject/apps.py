from django.apps import AppConfig
from neo4j import GraphDatabase
from django.conf import settings

class MyAppConfig(AppConfig):
    name = 'myproject'

    def ready(self):
        self.driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

    def get_driver(self):
        return self.driver

