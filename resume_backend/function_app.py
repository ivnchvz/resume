""" import azure.functions as func
import logging
from azure.data.tables import TableClient
import os """


# Create a TableClient to interact with your local Azure Table Storage
""" table_client = TableClient.from_connection_string("DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;", "visitors")

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
 """


import logging
import azure.functions as func

app = func.FunctionApp()


# Values from your code
database_name = "TablesDB"
container_name = "visitors"  # This is the table name in your code

@app.route("http_trigger", methods=["GET", "POST"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_output_v3(arg_name="outputDocument", database_name=database_name, collection_name=container_name, connection_string_setting="CosmosDbConnectionString")
@app.cosmos_db_input_v3(arg_name="inputDocument", database_name=database_name, collection_name=container_name, connection_string_setting="CosmosDbConnectionString")
def main(req: func.HttpRequest, inputDocument: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not inputDocument:
        # If the table is empty, create a new document with 'visitorCount' set to 1
        outputDocument.set(func.Document.from_dict({'id': 'visitorCount', 'visitorCount': 1}))
        return func.HttpResponse("1", status_code=200)
    # Increment the visitor count
    counter_entity = inputDocument[0]



    # Print the type and value of counter_entity and counter_entity['visitorCount']
    logging.info(f'Type of counter_entity: {type(counter_entity)}')
    logging.info(f'Value of counter_entity: {counter_entity}')
    logging.info(f'Type of counter_entity["visitorCount"]: {type(counter_entity["visitorCount"])}')
    logging.info(f'Value of counter_entity["visitorCount"]: {counter_entity["visitorCount"]}')


    counter_entity['visitorCount']['$v'] += 1

    # Assign the updated document to the output binding
    outputDocument.set(func.Document.from_dict(counter_entity))

    # Return just the visitor count as a string
    return func.HttpResponse(str(counter_entity['visitorCount']['$v']), status_code=200)    