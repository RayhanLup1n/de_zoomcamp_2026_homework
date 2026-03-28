import json
from kafka import KafkaConsumer

# Configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'green-trips'
GROUP_ID = 'homework-consumer-group'


def main():
    # Create Kafka consumer
    print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id=GROUP_ID,
    )

    # Subscribe to topic
    consumer.subscribe([TOPIC])
    print(f"Subscribed to topic: {TOPIC}")
    print("Starting to consume messages...")

    # Count trips with distance > 5.0 km
    count_gt_5 = 0
    total_count = 0
    batch_count = 0

    # Poll for messages
    while True:
        messages = consumer.poll(timeout_ms=1000)

        if not messages:
            # No more messages, exit
            print("No more messages. Exiting...")
            break

        for topic_partition, message_list in messages.items():
            for message in message_list:
                try:
                    data = message.value
                    total_count += 1

                    # Check trip_distance
                    trip_distance = data.get('trip_distance')
                    if trip_distance is not None and trip_distance > 5.0:
                        count_gt_5 += 1

                    batch_count += 1
                    if batch_count % 10000 == 0:
                        print(f"Processed {batch_count} messages. Trips > 5 km: {count_gt_5}")

                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue

    print("\n" + "="*50)
    print(f"Total messages processed: {total_count}")
    print(f"Trips with distance > 5.0 km: {count_gt_5}")
    print("="*50)

    consumer.close()


if __name__ == '__main__':
    main()
