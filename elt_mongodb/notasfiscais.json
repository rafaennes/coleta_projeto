// Select the database to use.
use('gastospublicos');

db.notasfiscais.aggregate([
    {
      $addFields: {
        "VALOR NOTA FISCAL": {
        $toDouble: {
          $replaceOne: {
            input: "$VALOR NOTA FISCAL",
            find: ",",
            replacement: "."
          }
        }
      },
        "DATA EMISSÃO": {
          $dateFromString: {
            dateString: "$DATA EMISSÃO",
            format: "%d/%m/%Y %H:%M:%S"
          }
        },
        "DATA/HORA EVENTO MAIS RECENTE": {
          $dateFromString: {
            dateString: "$DATA/HORA EVENTO MAIS RECENTE",
            format: "%d/%m/%Y %H:%M:%S"
          }
        }
      }
    },
    {
      $out: "slv_notasfiscais"
    }
  ]);
