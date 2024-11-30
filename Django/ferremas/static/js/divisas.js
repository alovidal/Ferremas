
// Definimos un objeto con las series de divisas
const seriesDivisas = {
    "ARS": "F072.CLP.ARS.N.O.D",   
    "BRL": "F072.CLP.BRL.N.O.D",   
    "CNY": "F072.CLP.CNY.N.O.D",   
    "COP": "F072.CLP.COP.N.O.D",   
    "CRC": "F072.CLP.CRC.N.O.D",   
    "MXN": "F072.CLP.MXN.N.O.D",   
    "PEN": "F072.CLP.PEN.N.O.D",   
    "PYG": "F072.CLP.PYG.N.O.D",   
    "USD": "F073.TCO.PRE.Z.D",   
    "EUR": "F072.CLP.EUR.N.O.D",   
    "GBP": "F072.CLP.GBP.N.O.D",   
    "AUD": "F072.CLP.AUD.N.O.D",                        
    "CAD": "F072.CLP.CAD.N.O.D"
};

// Función para obtener los tipos de cambio
async function obtenerTiposCambio() {
    const tiposCambio = {};

    for (let divisa in seriesDivisas) {
        const serie = seriesDivisas[divisa];
        try {
            const response = await fetch(`https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=alonsini51@gmail.com&pass=xmvp7MN$gXu$X:&firstdate=2024-01-01&lastdate=2024-12-31&timeseries=${serie}&function=GetSeries`);
            
            if (!response.ok) {
                console.error(`Error en la solicitud para ${divisa}: ${response.statusText}`);
                continue;
            }

            const data = await response.json();
            console.log(data); // Inspecciona la estructura de los datos

            // Asegúrate de que los datos estén en el formato esperado
            if (data && data[divisa] && data[divisa].last) {
                const valorDivisa = data[divisa].last;
                tiposCambio[divisa] = parseFloat(valorDivisa);
            } else {
                console.error(`Datos no válidos para ${divisa}`);
            }
        } catch (error) {
            console.error(`Error en la solicitud de la API para ${divisa}: ${error}`);
        }
    }

    return tiposCambio;
}

// Función para convertir CLP a otra divisa
async function convertirClpADivisa(montoClp, divisa) {
    // Asegúrate de que los tipos de cambio estén disponibles
    const tiposCambio = await obtenerTiposCambio();

    // Verifica si la divisa está disponible
    if (!(divisa in tiposCambio)) {
        console.log(`Divisa '${divisa}' no disponible.`);
        return null;
    }

    const valorDivisa = tiposCambio[divisa];
    const montoConvertido = montoClp / valorDivisa;
    return montoConvertido.toFixed(2);
}

// Ejemplo de uso de la función
convertirClpADivisa(10000, 'USD').then(resultado => {
    if (resultado !== null) {
        console.log(`El monto convertido es: ${resultado} USD`);
    }
});
