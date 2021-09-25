function logOut() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = '/';
}

document.getElementById("logout").addEventListener("click", logOut, false)