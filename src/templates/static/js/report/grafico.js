// Inicializando o gráfico com dados vazios
const ctx = document.getElementById('meuGrafico').getContext('2d');

const meuGrafico =  new Chart(ctx, {
    type: "bar",  // Gráfico de linhas
    data: {
        labels: [],  // Eixo X - meses
        datasets: []  // Eixo Y - dados de cortes
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Meses'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Quantidade de Serviços prestados'
                },
                beginAtZero: true
            }
        }
    }
});

// Função para buscar dados filtrados
function atualizarGrafico(url, type) {

    fetch(url)
        .then(response => response.json())
        .then(data => {
            
            const months = data.months;
            const datasets = [];
            let count = 0;
            
            for (const [serviceType, totalCuts] of Object.entries(data.cuts_by_type)) {
                
                datasets.push({
                    label: serviceType,
                    data: totalCuts,
                    borderColor: recoverColor(count),
                    backgroundColor: recoverBackgroundColor(count), 
                    borderWidth: 3
                });
                count=count+50
            }
            meuGrafico.type = type
            meuGrafico.data.labels = months;
            meuGrafico.data.datasets = datasets;
            meuGrafico.update();
        })
        .catch(error => console.error('Erro ao buscar os dados do gráfico:', error));
    
}

function recoverColor(index){

    return `hsl(${index}, 100%, 50%)`; 
}

function recoverBackgroundColor(index){

    return `hsl(${index}, 100%, 75%)`; 
}


document.getElementById('filtrar')?.addEventListener('click', function() {

    const mes = document.getElementById('mes').value;
    const tipoCorte = document.getElementById('tipoCorte').value;
    let url = `recover_data?mes=${mes}&tipo_corte=${tipoCorte}`

    atualizarGrafico(url, "bar");
});

document.getElementById('filtrar_count_week')?.addEventListener('click', function() {

    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const tipoCorte = document.getElementById('tipoCorte').value;

    if (!startDate || !endDate || !tipoCorte) {
        alert('Por favor, preencha todos os campos antes de continuar.');
    }
    else{    
        let url = `recover_data_week?start_date=${startDate}&end_date=${endDate}&tipo_corte=${tipoCorte}`
        newUrl = url.replace('/report_week', '');
        atualizarGrafico(newUrl, "line");
    }
});

document.getElementById('filtrar_amount')?.addEventListener('click', function() {

    const mes = document.getElementById('mes').value;
    const tipoCorte = document.getElementById('tipoCorte').value;
    let url = `recover_data_amount?mes=${mes}&tipo_corte=${tipoCorte}`
    newUrl = url.replace('/report_amoun', '')
    atualizarGrafico(newUrl, "bar");

});


