from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key="csk-w6fkff52m9x3mmx9xxv5wc5yv5eenyd4cn2t3wc44ph5dmx9"
)

models = client.models.list()

print(models)