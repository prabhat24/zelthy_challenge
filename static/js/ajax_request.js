var submitBtn = document.getElementById('submit');
submitBtn[i].addEventListener('click', function () {
    console.lo;
    console.log('upadteChart');

    updateChart(this.value)
});

function updateChart(date) {
    url = "/chart/";
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'start_date': date,
        })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data)
            location.reload()
        })
}