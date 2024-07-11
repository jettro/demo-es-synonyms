# Elasticsearch Synonyms
This is a sample project to play around with the synonyms API from Elasticsearch. You can run the local elasticsearch docker version with the following command:

```bash
docker compose up
```

Then you can run the es_client.py script to test the synonyms API:

```bash
python es_client.py
```

Finally you can run the poetry command to run the application, add the synonyms and query the documents:

```bash
poetry run python run.py
```

