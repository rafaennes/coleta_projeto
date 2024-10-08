use('gastospublicos')

db.EmendasParlamentares.aggregate([
    {
        $addFields: {
            // Convert "Ano da Emenda" to a complete DateTime
            "Ano da Emenda": {
                $dateFromString: {
                    dateString: { $concat: ["$Ano da Emenda", "-01-01"] },
                    format: "%Y-%m-%d",
                    onError: null // Handle errors by returning null
                }
            },
            // Convert specific fields to integers with error handling
            "Código do Autor da Emenda": {
                $cond: {
                    if: { $regexMatch: { input: "$Código do Autor da Emenda", regex: /^\d+$/ } },
                    then: { $toInt: "$Código do Autor da Emenda" },
                    else: null
                }
            },
            "Número da emenda": {
                $cond: {
                    if: { $regexMatch: { input: "$Número da emenda", regex: /^\d+$/ } },
                    then: { $toInt: "$Número da emenda" },
                    else: null
                }
            },
            "Código Subfunção": {
                $cond: {
                    if: { $regexMatch: { input: "$Código Subfunção", regex: /^\d+$/ } },
                    then: { $toInt: "$Código Subfunção" },
                    else: null
                }
            },
            // Convert monetary values to double with error handling
            "Valor Empenhado": {
                $cond: {
                    if: { 
                        $regexMatch: { 
                            input: "$Valor Empenhado", 
                            regex: /^[\s]*[0-9]+([.,][0-9]{1,2})?[\s]*$/ 
                        } 
                    },
                    then:
                        { 
                            $toDouble:
                            {
                                $replaceOne:
                                {
                                    input:
                                    {
                                        $trim:
                                        {
                                            input:"$Valor Empenhado"
                                        }
                                    },
                                    find:",",
                                    replacement:"." // Replace comma with dot for decimal point
                                }
                            }
                        },
                    else : 0 // Default value for invalid entries
                }
            },
            "Valor Liquidado": {
                $cond:{
                    if:{ 
                        $regexMatch:{
                            input:"$Valor Liquidado", 
                            regex:/^[\s]*[0-9]+([.,][0-9]{1,2})?[\s]*$/
                        }
                    },
                    then:
                        {$toDouble:
                        {
                            $replaceOne:
                            {
                                input:
                                {
                                    $trim:
                                    {
                                        input:"$Valor Liquidado"
                                    }
                                },
                                find:",",
                                replacement:"."
                            }
                        }},
                    else : 0
                }
            },
            "Valor Pago": {
                $cond:{
                    if:{ 
                        $regexMatch:{
                            input:"$Valor Pago", 
                            regex:/^[\s]*[0-9]+([.,][0-9]{1,2})?[\s]*$/
                        }
                    },
                    then:
                        {$toDouble:
                        {
                            $replaceOne:
                            {
                                input:
                                {
                                    $trim:
                                    {
                                        input:"$Valor Pago"
                                    }
                                },
                                find:",",
                                replacement:"."
                            }
                        }},
                    else : 0
                }
            },
            "Valor Restos A Pagar Inscritos": {
                $cond:{
                    if:{ 
                        $regexMatch:{
                            input:"$Valor Restos A Pagar Inscritos", 
                            regex:/^[\s]*[0-9]+([.,][0-9]{1,2})?[\s]*$/
                        }
                    },
                    then:
                        {$toDouble:
                        {
                            $replaceOne:
                            {
                                input:
                                {
                                    $trim:
                                    {
                                        input:"$Valor Restos A Pagar Inscritos"
                                    }
                                },
                                find:",",
                                replacement:"."
                            }
                        }},
                    else : 0
                }
            },
            "Valor Restos A Pagar Cancelados": {
                $cond:{
                    if:{ 
                        $regexMatch:{
                            input:"$Valor Restos A Pagar Cancelados", 
                            regex:/^[\s]*[0-9]+([.,][0-9]{1,2})?[\s]*$/
                        }
                    },
                    then:
                        {$toDouble:
                        {
                            $replaceOne:
                            {
                                input:
                                {
                                    $trim:
                                    {
                                        input:"$Valor Restos A Pagar Cancelados"
                                    }
                                },
                                find:",",
                                replacement:"."
                            }
                        }},
                    else : 0
                }
            },
            "Valor Restos A Pagar Pagos": {
                $cond:{
                    if:{ 
                        $regexMatch:{
                            input:"$Valor Restos A Pagar Pagos", 
                            regex:/^[\s]*[0-9]+([.,][0-9]{1,2})?[\s]*$/
                        }
                    },
                    then:
                        {$toDouble:
                        {
                            $replaceOne:
                            {
                                input:
                                {
                                    $trim:
                                    {
                                        input:"$Valor Restos A Pagar Pagos"
                                    }
                                },
                                find:",",
                                replacement:"."
                            }
                        }},
                    else : 0
                }
            }
        }
    },
    {
        $out: "slv_emendasparlamentares"// Specify the name for the new collection
    }
]);