import logging

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer

from build.gen import article_pb2
from build.gen.article_pb2 import Article

log = logging.getLogger(__name__)

from constant import SCHEMA_REGISTRY_URL, BOOTSTRAP_SERVER, KAFKA_TOPIC


class News_Producer:
    def __init__(self):
        schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        protobuf_serializer = ProtobufSerializer(
            article_pb2.Article, schema_registry_client, {"use.deprecated.format": True}
        )

        producer_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": protobuf_serializer,
        }

        self.producer = SerializingProducer(producer_conf)
    
    def produce_to_topic(self, article: Article):
        self.producer.produce(
            topic=KAFKA_TOPIC, partition=-1, key=str(article.id), value=article
        )

        self.producer.poll()
        