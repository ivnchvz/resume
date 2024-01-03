
param location string = resourceGroup().location
param staccname string = 'azr_stacc'
param appname string = 'azr_app'

resource stacc 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: staccname
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind:  'StorageV2'
}


resource resumeapp 'Microsoft.Web/sites@2023-01-01' = {
  name: appname
  location: location
}
