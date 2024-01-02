import azure.functions as func
import logging
from azure.data.tables import TableClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Create a TableClient to interact with your local Azure Table Storage
table_client = TableClient.from_connection_string("DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;", "visitors")

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the "counter" entity from the "visitors" table
    counter_entity = table_client.get_entity(partition_key="partition1", row_key="counter")

    # Increment the visitor count
    counter_entity["visitorCount"] += 1

    # Update the entity in the table
    table_client.upsert_entity(entity=counter_entity)

    # Return just the visitor count as a string
    return func.HttpResponse(str(counter_entity['visitorCount']), status_code=200)


#comment