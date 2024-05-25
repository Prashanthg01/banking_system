document.addEventListener('DOMContentLoaded', function () {
    const logoutForm = document.querySelector('form[action="/auth/logout"]');
    if (logoutForm) {
        logoutForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/auth/logout');
            xhr.setRequestHeader('Content-Type', 'application/json');

            const cookies = document.cookie.split('; ');
            let accessToken = '';
            cookies.forEach(cookie => {
                if (cookie.startsWith('access_token=')) {
                    accessToken = cookie.split('=')[1];
                }
            });

            if (accessToken) {
                xhr.setRequestHeader('Authorization', `Bearer ${accessToken}`);
            }

            xhr.onload = function () {
                if (xhr.status === 200) {
                    window.location.href = '/auth/login';
                } else {
                    alert('Logout failed');
                }
            };
            xhr.send();
        });
    }

    function refreshAccessToken() {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/auth/token/refresh');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                document.cookie = `access_token=${response.access_token}; path=/; httponly`;
            } else {
                window.location.href = '/auth/login';
            }
        };
        xhr.send();
    }

    setInterval(refreshAccessToken, 15 * 60 * 1000); // Refresh token every 15 minutes
});
