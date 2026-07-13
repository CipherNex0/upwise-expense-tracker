const closeModalBtn = document.getElementById('closeModalBtn');
const openModalBtn = document.getElementById('openModalBtn');
const modalOverlay = document.getElementById('modalOverlay');
const newExpenseForm = document.getElementById('newExpenseForm');

//Filtering the table
const categoryFilter = document.getElementById('categoryFilter');
const table = document.getElementById('expenseTable');
const rows = table.querySelectorAll('tbody tr');

//Step 1 - Find the canvas element in your HTML by it's id
const ctx = document.getElementById('expenseChart').getContext('2d');

const expenseChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: categoryData.labels,      // ← real data from Flask
        datasets: [{
            data: categoryData.amounts,   // ← real data from Flask
            backgroundColor: [
                '#2F2FE4', '#162E93', '#1A1953', '#8888BB', '#F0F0FF'
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#F0F0FF' }
            }
        }
    }
});

//handle when the new expense button is clicked
openModalBtn.addEventListener('click', () =>{
    modalOverlay.classList.add('active');
});

//handles closing the pop up
closeModalBtn.addEventListener('click', () =>{
    modalOverlay.classList.remove('active');
});

//handle when a expense is created 
modalOverlay.addEventListener('click', (e) =>{
    if(e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
    }
});

//handle creating a new expense form
newExpenseForm.addEventListener('submit', async (e) =>{
    e.preventDefault();

    const formData = new FormData(newExpenseForm);

    try {
        const response = await fetch('/expenses/create', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if(data.status === 'success'){
            location.reload();//simplest way to show the new expense for now
        }else{
            alert(data.message);
        }
    }catch(error){
        console.error(error);
        alert('Something went wrong.')
    }
});

categoryFilter.addEventListener('change', () => {
    const query = categoryFilter.value.toLowerCase();

    rows.forEach(row => {
        const category = row.cells[1].textContent.toLowerCase();
        if (query === 'all') {
            row.style.display = '';
        } else {
            row.style.display = category.includes(query) ? '' : 'none';
        }
    });

    // chart update goes here — inside the event listener
    if (query === 'all') {
        expenseChart.data.labels = categoryData.labels;
        expenseChart.data.datasets[0].data = categoryData.amounts;
    } else {
        const index = categoryData.labels
            .findIndex(label => label.toLowerCase() === query);
        if (index !== -1) {
            expenseChart.data.labels = [categoryData.labels[index]];
            expenseChart.data.datasets[0].data = [categoryData.amounts[index]];
        }
    }
    expenseChart.update();
});