
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
                                <li><strong>Availability:</strong> ${data.book_details.availability_status}</li>
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

    