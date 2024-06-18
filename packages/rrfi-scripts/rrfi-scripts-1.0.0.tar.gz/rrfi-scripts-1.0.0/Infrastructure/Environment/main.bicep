param location string = resourceGroup().location
 
param mapsLocation string = 'uksouth'
 
param project string = 'rrfimain'
 
@description('Azure blob Storage Account resource.')
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-06-01' = {
  name: '${project}storage'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Cool'
  }
}
 
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2021-06-01' = {
  name: 'default'
  parent: storageAccount
}
 
@description('Azure storage container resource.')
resource storageContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-06-01' = {
  name: '${project}con'
  parent: blobService
  properties: {
    publicAccess: 'None'
  }
}
 
@description('Azure Search service resource.')
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: '${project}search'
  location: location
  tags: {}
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    networkRuleSet: {
      ipRules: []
    }
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    disableLocalAuth: false
    authOptions: {
      apiKeyOnly: {}
    }
    semanticSearch: 'disabled'
  }
  sku: {
    name: 'basic'
  }
}
 
@description('Azure Maps service resource.')
resource mapsAccount 'Microsoft.Maps/accounts@2023-06-01' = {
  name: '${project}maps'
  location: mapsLocation
  sku: {
    name: 'G2'
  }
}
 
@description('Azure App Service Plan resource.')
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: '${project}appserviceplan'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true  // Set to true for Linux-based plans
  }
}
 
@description('Azure Function App resource.')
resource functionApp 'Microsoft.Web/sites@2021-02-01' = {
  name: '${project}funcapp'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: []
    }
  }
  sku: {
    name: 'F1'
    tier: 'Consumption'
  }
}
 
@description('Azure Web App resource.')
resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: '${project}webapp'
  location: 'uksouth'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: []
      linuxFxVersion: 'NODE|20-lts' // Sets the runtime stack to Node.js 20
    }
  }
  sku: {
    name: 'F1'
    tier: 'Free'
  }
}
