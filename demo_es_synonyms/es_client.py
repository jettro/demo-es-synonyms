from elasticsearch import Elasticsearch

INDEX_NAME = 'remarks'
SYNONYM_SET_NAME = 'remarks-synonyms-set'


class EsClient:

    def __init__(self):

        self.es = self._connection()

    @staticmethod
    def _connection():
        # Connect to the Elasticsearch node
        es = Elasticsearch(hosts=['http://localhost:9200'])

        # Check if the connection is successful
        if es.ping():
            print("Connected to Elasticsearch")
        else:
            print("Could not connect to Elasticsearch")

        return es

    def create_synonym_set(self):
        if self.es.synonyms.get_synonym(id=SYNONYM_SET_NAME):
            return "Synonym set already exists"
        return self.es.synonyms.put_synonym(id=SYNONYM_SET_NAME, synonyms_set=[])

    def index_exists(self):
        # Connect to the Elasticsearch node
        return self.es.indices.exists(index=INDEX_NAME)

    def delete_index(self):
        print("Deleting index")
        return self.es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)

    def create_index(self):
        if self.index_exists():
            print("Index already exists")
            self.delete_index()

        settings = {
            "analysis": {
                "filter": {
                    "synonym_filter": {
                        "type": "synonym_graph",
                        "synonyms_set": SYNONYM_SET_NAME,
                        "updateable": True
                    }
                },
                "analyzer": {
                    "synonym_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "synonym_filter"]
                    }
                }
            },
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

        mappings = {
            "properties": {
                "remarks": {
                    "type": "text",
                    "analyzer": "standard",
                    "search_analyzer": "synonym_analyzer"
                }
            }
        }

        # return self.es.indices.create(index='remarks', mappings=mappings, settings=settings)
        return self.es.indices.create(index='remarks', body={'settings': settings, 'mappings': mappings})

    def add_synonym_rule(self, rule_id, synonym):
        return self.es.synonyms.put_synonym_rule(set_id=SYNONYM_SET_NAME, rule_id=rule_id, synonyms=synonym)

    def get_synonym_rules(self):
        return self.es.synonyms.get_synonym(id=SYNONYM_SET_NAME)

    def delete_synonym_rule(self, rule_id):
        return self.es.synonyms.delete_synonym_rule(set_id=SYNONYM_SET_NAME, rule_id=rule_id)

    def index_remark(self, remark):
        return self.es.index(index=INDEX_NAME, body={"remarks": remark})

    def search_remark(self, query):
        return self.es.search(index=INDEX_NAME, body={"query": {"match": {"remarks": {"query": query, "operator": "and"}}}})


if __name__ == '__main__':
    client = EsClient()
    print(client.create_synonym_set())
    print(client.create_index())

    print(client.index_remark("After eating that enormous burrito, I felt so stuffed, packed, crammed, and jam-packed "
                              "that I considered moving to a new zip code just to accommodate my bloated belly!"))

    print(client.add_synonym_rule("burrito", "burito => burrito"))
    print(client.search_remark("huge burito"))