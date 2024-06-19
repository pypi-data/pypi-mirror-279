import logging

from kafka.errors import OffsetOutOfRangeError

from ..config.kafka_config import KafkaConfig

log = logging.getLogger(__name__)


class Messages:
    kafka_obj = KafkaConfig()

    def obtiene_mensajes(self, topico, grupo):
        mensajes = []
        try:
            consumer = self.kafka_obj.get_message(topico, grupo)
            for message in consumer:
                mensajes.append(message.value)
                consumer.commit()

        except OffsetOutOfRangeError:
            # consumer has no idea where they are
            self.kafka_obj.consumer.seek_to_end()
            log.exception("Kafka offset out of range error")
        except Exception as ex:
            log.exception(ex)
        else:
            log.exception(f"No message in topic: {topico}")

        return mensajes

    def envia_mensaje(self, topico, mensaje):
        try:
            self.kafka_obj.send_message(topico, mensaje)
        except Exception as ex:
            log.exception(ex)

