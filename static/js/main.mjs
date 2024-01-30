fetch('http://127.0.0.1:5000/api/v1.0/customers',
{
    method: "GET",
    headers: {
        'Content-Type': 'application/json'
    },
}
) .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then (data => {
    console.log(data);
}).catch(error => {
    console.log('Fetch error:', error);
})