import enum

BOOTSTRAP_SERVER: str = "localhost:29092"
SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
KAFKA_TOPIC = "article"


class Topic(str, enum.Enum):
    WORLD = "WORLD"
    NATION = "NATION"
    BUSINESS = "BUSINESS"
    TECHNOLOGY = "TECHNOLOGY"
    ENTERTAINMENT = "ENTERTAINMENT"
    SPORTS = "SPORTS"
    SCIENCE = "SCIENCE"
    HEALTH = "HEALTH"