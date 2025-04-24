document.addEventListener("DOMContentLoaded", function () {
    const issueDateInput = document.getElementById('issue_date');
    const dueDateInput = document.getElementById('due_date');
    const userIdInput = document.getElementById('user_id');

    let dueDays = 0;

    userIdInput.addEventListener('blur', function () {
        const userId = userIdInput.value.trim();
        if (userId === '') return;

        fetch(`/get-user-role-due/?user_id=${userId}`)
            .then(response => response.json())
            .then(data => {
                dueDays = data.due_days || 0;
                autoUpdateDueDate();
            });
    });

    issueDateInput.addEventListener('change', autoUpdateDueDate);

    function autoUpdateDueDate() {
        const issueDate = new Date(issueDateInput.value);
        if (!isNaN(issueDate.getTime()) && dueDays > 0) {
            const dueDate = new Date(issueDate);
            dueDate.setDate(dueDate.getDate() + dueDays);
            dueDateInput.value = dueDate.toISOString().split('T')[0];
        }
    }
});


// Event listener for when the user types into the book_id field

