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
        const response = await fetch(`https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=alonsini51@gmail.com&pass=x]mvp7MN$gXu$X:&firstdate=2024-01-01&lastdate=2024-12-31&timeseries=${serie}&function=GetSeries`);
        const data = await response.json();
        
        const valorDivisa = data[divisa].last;
        tiposCambio[divisa] = parseFloat(valorDivisa);
    }

    return tiposCambio;
}

function convertirClpADivisa(montoClp, divisa, tiposCambio) {
    if (!(divisa in tiposCambio)) {
        console.log(`Divisa '${divisa}' no disponible.`);
        return null;
    }
    const valorDivisa = tiposCambio[divisa];
    const montoConvertido = montoClp / valorDivisa;
    return montoConvertido.toFixed(2);
}


