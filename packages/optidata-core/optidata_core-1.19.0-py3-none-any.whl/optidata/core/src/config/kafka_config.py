import json
import logging
import ssl
import sys
import traceback

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from retrying import retry

from ..config import settings

log = logging.getLogger(__name__)


class KafkaConfig:
    producer = None
    consumer = None

    def __get_context(self):
        # Create a new context using system defaults, disable all but TLS1.2
        self.context = ssl.create_default_context()
        self.context.options &= ssl.OP_NO_TLSv1
        self.context.options &= ssl.OP_NO_TLSv1_1

        return self.context

    @retry(wait_exponential_multiplier=500, wait_exponential_max=10000)
    def __set_producer(self, is_ssl=False):
        try:
            brokers = f'{settings.KAFKA_BOOSTRAP}:{settings.KAFKA_PORT}'
            log.info(f"Creating new kafka producer using brokers: {str(brokers)}")
            if is_ssl:
                self.producer = KafkaProducer(
                    bootstrap_servers=brokers,
                    sasl_plain_username=settings.KAFKA_USERNAME,
                    sasl_plain_password=settings.KAFKA_PASSWORD,
                    security_protocol=settings.KAFKA_SECURITY_PROTOCOL,
                    ssl_context=self.__get_context(),
                    sasl_mechanism=settings.KAFKA_SASL_MECHANISM,
                    value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                    api_version=(0, 10, 1),
                    retries=5
                )
            else:
                self.producer = KafkaProducer(
                    bootstrap_servers=brokers,
                    value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                    api_version=(0, 10, 1),
                    retries=5,
                    max_block_ms=5000
                )
        except KeyError as e:
            log.exception('Missing setting named ' + str(e), {'ex': traceback.format_exc()})
        except Exception:
            log.exception("Couldn't initialize kafka producer.", {'ex': traceback.format_exc()})
            raise

    @retry(wait_exponential_multiplier=500, wait_exponential_max=10000)
    def __set_consumer(self, topic, group_id):
        try:
            brokers = f'{settings.KAFKA_BOOSTRAP}:{settings.KAFKA_PORT}'
            log.info(f'Creating new kafka consumer using brokers: {str(brokers)} and topic {topic}')
            self.consumer = KafkaConsumer(
                topic,
                group_id=group_id,
                bootstrap_servers=brokers,
                auto_offset_reset=settings.KAFKA_OFFSET,
                consumer_timeout_ms=settings.KAFKA_CONSUMER_TIMEOUT,
                enable_auto_commit=settings.KAFKA_CONSUMER_AUTO_COMMIT_ENABLE,
                value_deserializer=json.loads
            )
        except KeyError as e:
            log.exception('Missing setting named ' + str(e), {'ex': traceback.format_exc()})
        except Exception:
            log.exception("Couldn't initialize kafka consumer for topic", {'ex': traceback.format_exc(), 'topic': topic})
            raise

    def send_message(self, topic, message):
        try:
            self.__set_producer()
            if self.producer is not None:
                self.producer.send(topic, message)
                self.producer.flush()
                self.producer.close(timeout=10)
        except KafkaError as e:
            log.exception("Unexpected error:" + str(e), sys.exc_info()[0])
            raise

    def get_message(self, topic, group_id):
        try:
            self.__set_consumer(topic, group_id)
            return self.consumer
        except KafkaError as e:
            log.exception("Unexpected error:" + str(e), sys.exc_info()[0])
            raise
