
    // Event listener for when the user types into the book_id field
    document.getElementById('book_id').addEventListener('input', function () {
        var bookId = this.value;

        // If the input is empty, clear the book details display
        if (bookId.length > 0) {
            fetch(`/get-book-details/?book_id=${bookId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the book details below the input field
                        document.getElementById('book_details').innerHTML = `
                            <h4>Book Details:</h4>
                            <ul>
                                <li><strong>Title:</strong> ${data.book_details.title}</li>
                                <li><strong>Author:</strong> ${data.book_details.author}</li>
                                <li><strong>ISBN:</strong> ${data.book_details.isbn}</li>
                                <li><strong>Quantity:</strong> ${data.book_details.quantity}</li>
                            </ul>
                        `;
                    } else {
                        // Show error if book is not found
                        document.getElementById('book_details').innerHTML = `
                            <div class="alert alert-danger">${data.message}</div>
                        `;
                    }
                });
        } else {
            // Clear book details if the input is empty
            document.getElementById('book_details').innerHTML = '';
        }
    });

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
    document.getElementById('book_id').addEventListener('input', function () {
        var bookId = this.value;

        // If the input is empty, clear the book details display
        if (bookId.length > 0) {
            fetch(`/get-book-details/?book_id=${bookId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the book details below the input field
                        document.getElementById('book_details').innerHTML = `
                            <h4>Book Details:</h4>
                            <ul>
                                <li><strong>Title:</strong> ${data.book_details.title}</li>
                                <li><strong>Author:</strong> ${data.book_details.author}</li>
                                <li><strong>ISBN:</strong> ${data.book_details.isbn}</li>
                                <li><strong>Quantity:</strong> ${data.book_details.quantity}</li>
                            </ul>
                        `;
                    } else {
                        // Show error if book is not found
                        document.getElementById('book_details').innerHTML = `
                            <div class="alert alert-danger">${data.message}</div>
                        `;
                    }
                });
        } else {
            // Clear book details if the input is empty
            document.getElementById('book_details').innerHTML = '';
        }
    });

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
    let currentUserRole = "";
    let currentUserName = "";
    let currentUserId = "";
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  
    document.getElementById('user_id').addEventListener('input', function () {
      const userId = this.value.trim();
      currentUserId = userId;
  
      if (userId === "") {
        document.getElementById('user_name_display').textContent = "";
        document.getElementById('user_role_display').textContent = "";
        document.getElementById('user_fine_display').textContent = "";
        return;
      }
  
      fetch(`/get-user-fine/?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            currentUserName = data.name;
            currentUserRole = data.role;
            document.getElementById('user_name_display').textContent = data.name;
            document.getElementById('user_role_display').textContent = data.role;
            document.getElementById('user_fine_display').textContent = data.fine;
          } else {
            currentUserName = "";
            currentUserRole = "";
            document.getElementById('user_name_display').textContent = "Not found";
            document.getElementById('user_role_display').textContent = "-";
            document.getElementById('user_fine_display').textContent = "0";
          }
        });
    });
  
    document.getElementById("fineForm").addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent form from submitting normally
      const amount = parseInt(document.getElementById("paid_amount").value);
      if (isNaN(amount) || amount <= 0 || currentUserId === "" || currentUserRole === "") {
        alert("Please enter valid details.");
        return;
      }
  
      fetch("/pay-user-fine/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          user_id: currentUserId,
          role: currentUserRole,
          amount_paid: amount,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          if (data.success) {
            document.getElementById("user_fine_display").textContent = data.new_fine;
            document.getElementById("paid_amount").value = "";
          }
        });
    });