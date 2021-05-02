/*
 * Draws the graph used by the stock page for displaying stock information.
 *
 * @author Zabir Rahman
 */
function drawIntradayChart(name, ticker, api_key) {
    fetch("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + ticker + "&interval=60min" + api_key).then(response => response.json())
    .then(data => intraday = data["Time Series (60min)"]).then(() => {
        let keys = Object.keys(intraday);
        let lbls = new Array(keys.length);
        let dats = new Array(keys.length);
        let i = 0;
        let j = keys.length - 1;
        for(; j >= 0; j--) {
            lbls[i] = keys[j];
            dats[i] = intraday[keys[j]]["1. open"];
            i++;
        }

        let col = "";
        if (dats[0] > dats[dats.length - 1]) {
            col = '#FF0000';
        } else {
            col = '#7CFC00';
        }

        new Chart(document.getElementById("line-chart"), {
            type: 'line',
            data: {
            labels: lbls,
            datasets: [{ 
                data: dats,
                label: ticker,
                borderColor: col,
                fill: false
                }
            ]
            },
            options: {
                title: {
                    display: false,
                },
                scales: {
                    xAxes: [{
                        gridLines: {
                           display: false
                        },
                        ticks: {
                            display: false 
                        }
                     }],
                     yAxes: [{
                        gridLines: {
                           display: false
                        }
                     }]
                },
                maintainAspectRatio: false,
                responsive: true
            }
        });
    });
}