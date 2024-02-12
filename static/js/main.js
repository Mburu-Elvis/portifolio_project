base_url = 'http://127.0.0.1:5000/api/v1.0/customers'

fetch(base_url)
.then( response => {
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();
})
.then( data => {
        if (!data.customers || !Array.isArray(data.customers)) {
            throw new Error('Invalid response format');
        }
        const customers = data.customers;
        customers.forEach(customer => {
            console.log(`Customer ID: ${customer.customer_id}`);
        })

})
.catch(error => {
    console.error(`Error fetching customers: ${error}`)
});
console.log('We printing and are OK');