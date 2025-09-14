document.addEventListener('DOMContentLoaded', function () {
    const bookIdInput = document.getElementById('isbn');
    const name = document.getElementById('book_name');
    const author = document.getElementById('author');
    const publisher = document.getElementById('publications');
    const category = document.getElementById('category');

    // Listen to input event on ISBN field
    bookIdInput.addEventListener('input', function () {
        const bookId = bookIdInput.value.trim();
        if (bookId === '') return;

        fetch(`/get-add-book-details/?book_id=${bookId}`)
            .then(response => response.json())
            .then(data => {
                const book = data.book_details;
                console.log("Response from server:", data);
                if (book.title) name.value = book.title;
                if (book.author) author.value = book.author;
                if (book.publisher) publisher.value = book.publisher;
                if (book.category) category.value = book.category[0];
            })
            .catch(error => console.error('Error fetching book details:', error));
    });
});
