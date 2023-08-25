var box = document.getElementById('box');
var down = false;

function toggleNotifi() {
    if (down) {
        box.style.display = 'none';
        down = false;
    } else {
        box.style.display = 'block';
        down = true;
    }
}
