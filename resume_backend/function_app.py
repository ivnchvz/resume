import azure.functions as func
import logging
from azure.data.tables import TableClient
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Create a TableClient to interact with your local Azure Table Storage
table_client = TableClient.from_connection_string(os.getenv("COSMOS_CONNECTION_STRING"), "visitors")

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        # Retrieve the "counter" entity from the "visitors" table
        counter_entity = table_client.get_entity(partition_key="partition1", row_key="counter")
        print(counter_entity)
        # Increment the visitor count
        counter_entity["visitorCount"] += 1

        # Update the entity in the table
        table_client.upsert_entity(entity=counter_entity)

        # Return just the visitor count as a string
        return func.HttpResponse(str(counter_entity['visitorCount']), status_code=200)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
    except:  # Catch all other exceptions
        print("An unknown error ocurred.")
        return func.HttpResponse("An unknown error occurred.", status_code=500)
