document.addEventListener('DOMContentLoaded', function () {
  const returnDateInput = document.getElementById('return_Date');
  const userIdInput = document.getElementById('user_Id');
  const bookIdInput = document.getElementById('book_Id');
  const fineLabel = document.getElementById('fine_Info');
  const fineAmountSpan = document.getElementById('fine_Amount');

  if (!returnDateInput || !userIdInput || !bookIdInput || !fineLabel || !fineAmountSpan) {
    console.error("One or more DOM elements not found. Check your HTML IDs.");
    return;
  }

function fetchIssuedUser() {
    const bookId = bookIdInput.value.trim();
    if (bookId) {
      fetch(`/get-issued-user/?book_id=${bookId}`)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            userIdInput.value = data.user_id;
            console.log("User ID fetched:", data.user_id);
            checkFine();  // After auto-filling user, immediately check fine
          } else {
            userIdInput.value = '';
            fineLabel.textContent = data.message;
            fineAmountSpan.textContent = '0';
          }
        })
        .catch(error => {
          console.error('Error fetching issued user:', error);
        });
    }
  }



  function checkFine() {
    const returnDate = returnDateInput.value;
    const userId = userIdInput.value.trim();
    const bookId = bookIdInput.value.trim();

    console.log("Return Date:", returnDate);
    console.log("User ID:", userId);
    console.log("Book ID:", bookId);

    if (returnDate && userId && bookId) {
      // Show loading text
      fineLabel.style.display = 'block';
      fineLabel.textContent = 'Checking fine...';
      fineAmountSpan.textContent = '';

      fetch(`/get-fine/?user_id=${userId}&book_id=${bookId}&return_date=${returnDate}`)
        .then(response => response.json())
        .then(data => {
          console.log("Response from server:", data);

          if (data.success) {
            fineAmountSpan.textContent = data.fine;
            fineLabel.textContent = 'Fine Amount: '+data.fine;
          } else {    
            fineLabel.textContent = data.message;
            fineAmountSpan.textContent = '0';
          }
        })
        .catch(error => {
          console.error('Error fetching fine:', error);
          fineLabel.style.display = 'none';
        });
    } else {
      console.log("Some required fields are empty");
    }
  }

  // Listen to typing on all 3 fields
  bookIdInput.addEventListener('input', fetchIssuedUser);
});
