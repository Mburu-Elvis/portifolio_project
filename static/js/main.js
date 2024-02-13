const customerDisplay = document.querySelector("div");


fetch('http://127.0.0.1:5000/api/v1.0/products')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then(json => initialize(json.products))
    .catch(err => console.error(`Fetch problem: ${err.message}`));

function initialize(products) {
    // the elements we want to work with
    const category = document.querySelector('#category');
    const searchTerm = document.querySelector('#searchTerm');
    const searchBtn = document.querySelector("button");
    const main = document.querySelector('main');

    /* keep rocord or the last category and search term were */
    let lastCategory = category.value;
    let lastSearch = '';

    /* the variables contain the results of filtering by category and search term
    finalGroup contains the products that need to be displayed after the searching has been done
    each will be an array containing objects
    each object represents a product */
    let categoryGroup;
    let finalGroup;

    /* To start with, set the finalGroup to equal the entire products database
    then run updateDisplay, so that all products are displayed initially */
    finalGroup = products;
    updateDisplay();

    /* set both to be equal to an empty array in time for searches to be run */
    categoryGroup = [];
    finalGroup = [];

    /* when the search button is clicked, invoke selectCategory() to start
    a search running to select the category of products we want to display
    */
    searchBtn.addEventListener("click", selectCategory);

    function selectCategory(e) {
        e.preventDefault();

        // set these back to empty arrays
        categoryGroup = [];
        finalGroup = [];

        /* if the category and search term are the same as they were the last time a 
            search was run, the results will be the same */
        if (category.value === lastCategory && searchTerm.value.trim() === lastSearch) {
            return;
        } else {
            // update the record of last category and search term
            lastCategory = category.value;
            lastSearch = searchTerm.value.trim();

            /* selecting all products then filter them by the search term */
            if (category.value === 'All') {
                categoryGroup = products;

                selectProducts();
            } else {
                const lowerCaseType = category.value.toLowerCase();

                /* filter category group to only contain products whose type includes the category */

                const base_url = 'http://127.0.0.1:5000/api/v1.0/products/' + lowerCaseType;
                fetch(base_url)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(filteredProducts => {
                        categoryGroup = filteredProducts.products;
                        selectProducts();
                    })
                    .catch(err => console.error(`Filter problem: ${err.message}`));
            }
        }
    }
    function selectProducts() {
        /* if no search term make the finalGroup equal to the categoryGroup */
        if (searchTerm.value === '') {
            finalGroup = categoryGroup;
        } else {
            const lowerCaseSearchTerm = searchTerm.value.trim().toLowerCase();
            finalGroup = categoryGroup.filter(product => product.product_name.includes(lowerCaseSearchTerm));
        }
        updateDisplay();
    }

    function updateDisplay() {
        while (main.firstChild) {
            main.removeChild(main.firstChild);
        }
        if (finalGroup.length === 0) {
            const para = document.createElement('p');
            para.textContent = 'No results to display!';
            main.appendChild(para);
        } else {
            for (const product of finalGroup) {
                fetchBlob(product);
            }
        }
    }

    function fetchBlob(product) {
        showProduct(product);


    }
    function showProduct(product) {
        const section = document.createElement('section');
        const heading = document.createElement('h2');
        const para = document.createElement('p');

        section.setAttribute('class', product.category_id);

        heading.textContent = product.product_name.replace(product.product_name.charAt(0), product.product_name.charAt(0).toUpperCase());
        para.textContent = `Ksh ${product.price.toFixed(2)}`;

        main.appendChild(section);
        section.appendChild(heading);
        section.appendChild(para);
    }

}