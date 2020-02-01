$(document).ready(function () {
    let folders = document.getElementsByClassName("nav-folder-label");
    for (let i = 0; i < folders.length; i++) {
        folders[i].innerHTML += "<i class=\"material-icons\">chevron_right</i>";
    }
});

// all prime numbers between 0 and 1000
const PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

function shorten_fraction(a, b) {
    for (let i_pr = 0; i_pr < PRIMES.length; i_pr++) {
        let num = PRIMES[i_pr];
        if (a < num || b < num) {
            break;
        }
        let a_bak = a;
        let b_bak = b;
        while ((a % 1 === 0) && (b % 1 === 0)) {
            a_bak = a;
            b_bak = b;
            a /= num;
            b /= num;
        }
        a = a_bak;
        b = b_bak;
    }
    return [a, b]
}

function round_number2places(num) {
    return Math.round((num + Number.EPSILON) * 100) / 100
}

function refresh_table_body() {
    let tbody = document.getElementById("at_tbody");
    while (tbody.lastChild) {
        tbody.removeChild(tbody.lastChild);
    }
    let span_exist = [];
    for (let i_row = 0; i_row < cells.length; i_row++) {
        let tr = document.createElement("tr");
        for (let i_col = 0; i_col < cells[i_row].length; i_col++) {
            let value = cells[i_row][i_col];
            if (span_exist[i_col] > 0) {
                span_exist[i_col]--;
            } else {
                let rowspan = 1;
                let ir = i_row + 1;
                span_exist[i_col] = 0;
                while (ir < cells.length && cells[ir][i_col] === value) {
                    span_exist[i_col]++;
                    rowspan++;
                    ir++;
                }
                let td = document.createElement("td");
                td.rowSpan = rowspan;
                switch (types[i_col]) {
                    case "file_image":
                        let img = document.createElement("img");
                        img.alt = value;
                        img.src = "/static/img/1mp/" + value;
                        td.appendChild(img);
                        break;
                    case "bool":
                        let i = document.createElement("i");
                        i.classList.add("material-icons");
                        if (value) {
                            i.style.color = "green";
                            i.innerText = "check";
                        } else {
                            i.style.color = "red";
                            i.innerText = "clear";
                        }
                        td.appendChild(i);
                        break;
                    case "number":
                        if (value_units[i_col] != null) {
                            td.innerText = value.toString() + value_units[i_col];
                        } else {
                            td.innerText = value;
                        }
                        break;
                    default:
                        td.innerText = value;
                }
                tr.appendChild(td);
            }
        }
        tbody.appendChild(tr);
    }
}

function render_table() {
    let table = document.getElementById("at_table");
    let thead = document.getElementById("at_thead");
    let head_tr = document.createElement("tr");
    thead.appendChild(head_tr);
    for (let i_col = 0; i_col < heads.length; i_col++) {
        let th = document.createElement("th");
        if (is_sortable_type(types[i_col])) {
            let i = document.createElement("i");
            i.classList.add("material-icons");
            i.innerText = get_sort_icon(sort_states[i_col]);
            i.onclick = function () {
                table_sort(i_col)
            };
            i.id = "at_th_i" + i_col;
            th.appendChild(i);
        }
        let txt = document.createElement("span");
        txt.innerText = heads[i_col];
        th.appendChild(txt);
        th.id = "at_th" + i_col;
        head_tr.appendChild(th);
    }

    refresh_table_body();
}

function table_sort(col_to_sort) {
    let new_mode;
    switch (sort_states[col_to_sort]) {
        case 0:
            new_mode = 1;
            break;
        case 1:
            new_mode = 2;
            break;
        case 2:
            new_mode = 1;
            break;
    }
    let old_col = 0;
    for (let i = 0; i < sort_states.length; i++) {
        if (sort_states[i] !== 0) {
            old_col = i;
            break;
        }
    }
    let old_i = document.getElementById("at_th_i" + old_col);
    old_i.innerText = get_sort_icon(0);
    sort_states[old_col] = 0;

    let new_i = document.getElementById("at_th_i" + col_to_sort);
    new_i.innerText = get_sort_icon(new_mode);
    sort_states[col_to_sort] = new_mode;

    cells.sort(function (a, b) {
        let is_num = types[col_to_sort] === "number";
        let val_a = a[col_to_sort];
        let val_b = b[col_to_sort];
        if (new_mode === 1) {
            if (is_num) {
                return val_a - val_b;
            } else {
                return val_a.localeCompare(val_b);
            }
        } else {
            if (is_num) {
                return val_b - val_a;
            } else {
                return val_b.localeCompare(val_a);
            }
        }
    });

    refresh_table_body();
}

function is_sortable_type(typeStr) {
    switch (typeStr) {
        case "str":
        case "number":
            return true;
        default:
            return false;
    }
}

function get_sort_icon(sort_state) {
    switch (sort_state) {
        case 0:
            return "unfold_more";
        case 1:
            return "keyboard_arrow_up";
        case 2:
            return "keyboard_arrow_down";
        default:
            return "";
    }
}
