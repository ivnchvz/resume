param location string = resourceGroup().location
param staccname string = 'azrstaccresume'
param appname string = 'azrappresume'
param cosmosname string = 'azrcosmosresume'
param tablename string = 'visitors'
@secure()
param accountKey string


// Storage Account
resource stacc 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: staccname
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind:  'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
  }
}

// Function with Consumption plan, python
resource resumeapp 'Microsoft.Web/sites@2023-01-01' = {
  name: appname
  location: location
  kind: 'functionapp,linux'
  properties: {
    reserved: true
    siteConfig: {
      linuxFxVersion: 'python|3.11'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${staccname};AccountKey=${accountKey};EndpointSuffix=core.windows.net'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
      ]
    }
  }
}




//Cosmos DB account for Table API
resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' = {
  name: cosmosname
  location: location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    capabilities: [
      {
        name: 'EnableTable'
      }
    ]
  }
}

// Create a Cosmos DB table
resource cosmosDBTable 'Microsoft.DocumentDB/databaseAccounts/tables@2023-11-15' = {
  parent: cosmosDBAccount
  name: tablename
  properties: {
    resource: {
      id: tablename
    }
    options: {}
  }
}
