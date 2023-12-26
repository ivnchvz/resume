// Import Azure SDK
const { TableServiceClient, TablesSharedKeyCredential } = require("@azure/data-tables");

// Connection details
const table = "table";
const account = "account";
const key = "key";

// Create client
const cred = new TablesSharedKeyCredential(account, key);
const client = new TableServiceClient(`https://${account}.table.core.windows.net`, cred);

// Function to get count
async function getCount() {
    const entity = await client.getEntity(table, "partition", "row");
    return entity.count;
}

// Function to increase count
async function increaseCount() {
    const count = await getCount();
    const updatedEntity = { partitionKey: "partition", rowKey: "row", count: count + 1 };
    await client.updateEntity(updatedEntity, "Replace");
}

// Update count on page load
window.onload = async function() {
    await increaseCount();
    document.getElementById("viewNumber").innerText = await getCount();
}