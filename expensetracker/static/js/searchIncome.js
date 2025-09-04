const searchField = document.querySelector('#searchField');
const appTable = document.querySelector(".appTable");
const tableOutput = document.querySelector(".tableOutput");
const paginationContainer = document.querySelector(".pagination-container");
const tableBody = document.querySelector(".table-body");


tableOutput.style.display = "none";


searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tableBody.innerHTML = "";

        fetch("/income/search-income", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);

                appTable.style.display = "none";
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center">No result found.</td>
                    </tr>`;
                }
                else {
                    tableBody.innerHTML = "";
                    data.forEach(item => {
                        tableBody.innerHTML += `
                        <tr>
                            <td>${item.amount}</td>
                            <td>${item.source}</td>
                            <td>${item.description}</td>
                            <td>${item.date}</td>
                            <td><a href="/income/${item.id}/edit/" class="btn btn-secondary btn-sm">Edit</a></td>
                        </tr>
                        `;

                    });
                };
            });
    }
    else {
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        tableOutput.style.display = "none";
    }
});