document.addEventListener('DOMContentLoaded', function () {
    const userInput = document.getElementById('user_id');
    const userDetailsDiv = document.getElementById('user_details');

    userInput.addEventListener('input', function () {
        const uid = userInput.value.trim();
        if (uid.length === 0) {
            userDetailsDiv.innerHTML = '';
            return;
        }

        fetch(`/ajax/search-user/?user_id=${uid}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const u = data.user;
                    if (data.user.role === 'student') {
                        userDetailsDiv.innerHTML = `
                            <p><strong>Name:</strong> ${u.name}<br>
                            <strong>Student Roll:</strong> ${u.roll_no}<br>
                            <strong>Class:</strong> ${u.class}<br>
                            <strong>Section:</strong> ${u.section}<br>
                            <strong>Issued Books:</strong> ${u.issued_books}<br>
                            <strong>Returned Books:</strong> ${u.returned_books}<br>
                            <strong>Pending Books:</strong> ${u.pending_books}<br>
                            <strong>Fine:</strong> ${u.fine}</p>
                        `;
                    } else if (data.user.role === 'teacher') {
                        userDetailsDiv.innerHTML = `
                            <p><strong>Name:</strong> ${u.name}<br>
                            <strong>Teacher ID:</strong> ${u.teacher_id}<br>
                            <strong>Department:</strong> ${u.department}<br>
                            <strong>Issued Books:</strong> ${u.issued_books}<br>
                            <strong>Returned Books:</strong> ${u.returned_books}<br>
                            <strong>Pending Books:</strong> ${u.pending_books}<br>
                            <strong>Fine:</strong> ${u.fine}</p>
                        `;
                    }
                } else {
                    userDetailsDiv.innerHTML = '<p class="text-danger">User not found</p>';
                }
            });
    });
});
