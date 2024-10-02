const sourceCollectionName = "orcamento";
const targetCollectionName = "slv_" + sourceCollectionName;

const bulkOps = [];
const cursor = db[sourceCollectionName].find();

cursor.forEach(doc => {
  const toBudgetNumber = (value) => {
    return typeof value === 'string' ? parseFloat(value.replace(",", ".")) :
           typeof value === 'number' ? value : 0;
  };

  // Calculate modified fields
  const orcamentoRealizado = toBudgetNumber(doc["ORÇAMENTO REALIZADO (R$)"]);
  const orcamentoAtualizado = toBudgetNumber(doc["ORÇAMENTO ATUALIZADO (R$)"]);
  const orcamentoInicial = toBudgetNumber(doc["ORÇAMENTO INICIAL (R$)"]);
  const orcamentoEmpenhado = toBudgetNumber(doc["ORÇAMENTO EMPENHADO (R$)"]);
  const percentageRealizado = orcamentoAtualizado !== 0
    ? parseFloat((orcamentoRealizado / orcamentoAtualizado).toFixed(2))
    : 0;

  // Create a new document with all fields from 'doc'
  const newDoc = { ...doc }; // Copy all fields

  // Ensure 'exercicio' is converted to ISODate format if it's a valid year string
  if (doc.exercicio && /^\d{4}$/.test(doc.exercicio)) {
    // Correctly convert the year to an ISODate
    newDoc.exercicio = new Date(doc.exercicio, 0, 1); // Using Date(year, month, day)
  } else {
    // Handle invalid 'exercicio' as per your needs, e.g., setting it to null or leaving it unchanged
    newDoc.exercicio = null; // or leave it as doc.exercicio if you don't want to modify it
  }

  // Update the modified fields in the new document
  newDoc["ORÇAMENTO INICIAL (R$)"] = orcamentoInicial;
  newDoc["ORÇAMENTO ATUALIZADO (R$)"] = orcamentoAtualizado;
  newDoc["ORÇAMENTO EMPENHADO (R$)"] = orcamentoEmpenhado;
  newDoc["ORÇAMENTO REALIZADO (R$)"] = orcamentoRealizado;
  newDoc["% REALIZADO DO ORÇAMENTO (COM RELAÇÃO AO ORÇAMENTO ATUALIZADO)"] = percentageRealizado;

  bulkOps.push({
    insertOne: {
      document: newDoc 
    }
  });

  if (bulkOps.length === 500) {
    db[targetCollectionName].bulkWrite(bulkOps);
    bulkOps.length = 0;
  }
});

if (bulkOps.length > 0) {
  db[targetCollectionName].bulkWrite(bulkOps);
}
