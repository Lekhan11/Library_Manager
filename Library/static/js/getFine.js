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
  
    returnDateInput.addEventListener('change', function () {
      const returnDate = returnDateInput.value;
      const userId = userIdInput.value.trim();
      const bookId = bookIdInput.value.trim();
  
      console.log("Return Date:", returnDate);
      console.log("User ID:", userId);
      console.log("Book ID:", bookId);
  
      if (returnDate && userId && bookId) {
        fetch(`/get-fine/?user_id=${userId}&book_id=${bookId}&return_date=${returnDate}`)
          .then(response => response.json())
          .then(data => {
            console.log("Response from server:", data);
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
            fineLabel.style.display = 'none';
          });
      } else {
        console.log("Some required fields are empty");
      }
    });
  });
  