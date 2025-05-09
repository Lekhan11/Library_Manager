document.addEventListener('DOMContentLoaded', function () {
  const userIdInput = document.getElementById('user_Id');
  const bookIdInput = document.getElementById('book_Id');
  const fineLabel = document.getElementById('fine_Info');
  const fineAmountSpan = document.getElementById('fine_Amount');
  const loadingSpinner = document.getElementById('loadingSpinner');

  if (!userIdInput || !bookIdInput || !fineLabel || !fineAmountSpan || !loadingSpinner) {
    console.error("One or more DOM elements not found. Check your HTML IDs.");
    return;
  }

  const today = new Date().toISOString().split('T')[0];

  let timeout;
  
  function debounce(func, delay) {
    clearTimeout(timeout);
    timeout = setTimeout(func, delay);
  }

  function checkFine() {
    const userId = userIdInput.value.trim();
    const bookId = bookIdInput.value.trim();

    if (userId && bookId) {
      loadingSpinner.style.display = 'block';
      fineLabel.style.display = 'none';

      fetch(`/get-fine/?user_id=${userId}&book_id=${bookId}&return_date=${today}`)
        .then(response => response.json())
        .then(data => {
          loadingSpinner.style.display = 'none';

          if (data.success) {
            fineAmountSpan.textContent = data.fine;
            fineLabel.style.display = 'block';
          } else {    
            fineLabel.textContent = data.message;
            fineLabel.style.display = 'block';
          }
        })
        .catch(error => {
          console.error('Error fetching fine:', error);
          loadingSpinner.style.display = 'none';
          fineLabel.style.display = 'none';
        });
    } else {
      console.log("Please enter both User ID and Book ID");
    }
  }

  userIdInput.addEventListener('input', function() {
    debounce(checkFine, 500);
  });

  bookIdInput.addEventListener('input', function() {
    debounce(checkFine, 500);
  });

  // ✅ No preventDefault() in submit => form will post normally
});
document.getElementById('returnBookForm').addEventListener('submit', function(event) {
  console.log("Submitting...");
  console.log("User ID:", document.getElementById('user_Id').value);
  console.log("Book ID:", document.getElementById('book_Id').value);
  console.log("Return Date:", document.getElementById('return_Date').value);
  console.log("Book Condition:", document.getElementById('bookCondition').value);
});
