$(document).ready(function () {
    let folders = document.getElementsByClassName("nav-folder-label");
    for (let i = 0; i < folders.length; i++) {
        folders[i].innerHTML += " %";//todo replace this with I> (triangle left) icon
    }
});