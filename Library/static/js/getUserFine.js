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

      const userInfoSection = document.getElementById('user_info');

      if (userId === "") {
        userInfoSection.style.display = 'none';
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
            userInfoSection.style.display = 'block';
          } else {
            currentUserName = "";
            currentUserRole = "";
            userInfoSection.style.display = 'none';
            document.getElementById('user_name_display').textContent = "";
            document.getElementById('user_role_display').textContent = "";
            document.getElementById('user_fine_display').textContent = "";
          }
        });
    });

    document.getElementById("fineForm").addEventListener("submit", function (e) {
      e.preventDefault();

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
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          if (data.success) {
            document.getElementById("user_fine_display").textContent = data.new_fine;
            document.getElementById("paid_amount").value = "";
          }
        });
    });
