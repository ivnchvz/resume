from azure.data.tables import TableClient

# Create a TableClient
table_client = TableClient.from_connection_string("DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;", "visitors")

# Create the table if it doesn't exist
try:
    table_client.create_table()
    print("Table 'visitors' created successfully.")
except:
    print("Table 'visitors' already exists.")  # The table already exists

# Create an entity with a partition key
entity = {"PartitionKey": "partition1", "RowKey": "counter", "visitorCount": 0}
table_client.create_entity(entity)
print("Entity 'counter' created successfully.")

# Query the table
entities = table_client.query_entities("")
print("Querying entities...")

# Find the "counter" entity and print its partition key
for entity in entities:
    if entity['RowKey'] == 'counter':
        print(f"The partition key of the 'counter' entity is: {entity['PartitionKey']}")
