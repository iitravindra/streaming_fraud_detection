from kafka import KafkaProducer
import json
import time

class TransactionProducer:
    def __init__(self, brokers, topic):
        self.producer = KafkaProducer(bootstrap_servers=brokers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic

    def produce_transactions(self):
        while True:
            # Generate mock transaction data
            transaction = {
                'timestamp': int(time.time()),
                'amount': random.uniform(1, 1000),
                'merchant': random.choice(['Amazon', 'Walmart', 'Target']),
                'customer_id': random.randint(1, 1000)
            }

            # Send transaction data to Kafka topic
            self.producer.send(self.topic, value=transaction)

            # Sleep for a certain interval before producing the next transaction
            time.sleep(1)

if __name__ == '__main__':
    brokers = ['localhost:9092', 'localhost:9093']
    topic = 'raw_transactions'

    producer = TransactionProducer(brokers, topic)
    producer.produce_transactions()