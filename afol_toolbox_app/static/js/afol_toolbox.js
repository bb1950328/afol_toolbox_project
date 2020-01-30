$(document).ready(function () {
    let folders = document.getElementsByClassName("nav-folder-label");
    for (let i = 0; i < folders.length; i++) {
        folders[i].innerHTML += "<i class=\"material-icons\">chevron_right</i>";
    }
});