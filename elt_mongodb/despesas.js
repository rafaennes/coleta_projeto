const bulk = db.svl_despesas.initializeUnorderedBulkOp();
const batchSize = 1000; // Batch size for bulk operations
let count = 0;

db.despesas.find().forEach(function(doc) {
    // Create a new document with all original fields
    let newDoc = { ...doc };

    // Convert the currency fields from string to double
    const fieldsToConvert = [
        "Valor Empenhado (R$)",
        "Valor Liquidado (R$)",
        "Valor Pago (R$)",
        "Valor Restos a Pagar Inscritos (R$)",
        "Valor Restos a Pagar Cancelado (R$)",
        "Valor Restos a Pagar Pagos (R$)"
    ];

    // Process currency fields
    fieldsToConvert.forEach(function(field) {
        if (doc[field]) {
            // Replace comma with dot and convert to double
            const valueAsString = doc[field].replace(",", ".");
            newDoc[field] = parseFloat(valueAsString);
        }
    });

    // Convert "Ano e mês do lançamento" to timestamp (YYYY/MM format)
    if (doc["Ano e mês do lançamento"]) {
        const dateParts = doc["Ano e mês do lançamento"].split("/");
        const year = parseInt(dateParts[0]);
        const month = parseInt(dateParts[1]);

        // Create a date object with the first day of the given month
        const date = new Date(year, month - 1, 1);

        // Convert to timestamp
        newDoc["Ano e mês do lançamento"] = date.getTime();
    }

    // Add the transformed document to the bulk operation
    bulk.insert(newDoc);
    count++;

    // Execute bulk insert when the batch size is reached
    if (count % batchSize === 0) {
        bulk.execute();
        bulk = db.svl_despesas.initializeUnorderedBulkOp(); // Reinitialize bulk
    }
});

// Execute any remaining operations in the bulk queue
if (count % batchSize !== 0) {
    bulk.execute();
}
