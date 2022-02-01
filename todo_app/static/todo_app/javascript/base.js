/**
 * button redirect to page
 * @param  {String} redirect redirect url
 */

function redirect(redirect, base = '/') {
    window.location.href = base + String(redirect);
}


/**
 * displays new list form on click of + button
 * @param {String} type add list or add task
 */

function addNewList(type) {
    if (type == 'list') {
        const form = document.getElementById("add-new-list");
        form.style.display = "block";
    } else {
        const form = document.getElementById("add-task");
        form.style.display = "block";
    }
}

/**
 * displays current time on navigation bar
 */

var dt = new Date().toDateString();
document.getElementById('date-time').innerHTML = dt;


/**
 * makes sortable list of lists items. Saves reordered to local storage
 */

let list = document.getElementById("lists-container");
Sortable.create(list, {
    options: {
        animation: 300,
        sort: true
    },
    store: {
        /**
         * Save the order of elements. Called onEnd (when the item is dropped).
         * @param {Sortable}  sortable
         */
        set: function (sortable) {
            const url = window.location.href;

            // get order of elements in list
            var order = []
            list.querySelectorAll('a').forEach(function (i) {
                order.push(i.innerHTML)
            })

            fetch(url, {
                method: "POST",
                body: JSON.stringify({
                    user: user,
                    order: order
                }),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
        }
    }
})


/**
 * activated by pressing edit button. Displays date input to change date and input field to change name
 * @param {String} id of the pressed task
 */

function editTask(id) {
    info = document.getElementById(id + '-task')
    form = document.getElementById("task-edit-" + id)
    edit = document.getElementById("edit-btn-" + id)
    task = document.getElementById("task-" + id)
    subnotes_edit = document.getElementById("subnotes-edit-" + id)
    subnotes = document.getElementById("subnotes-" + id)

    console.log(task)

    if (edit.classList.contains("fa-edit")) {
        info.style.display = 'none';
        form.style.display = 'flex';
        edit.classList.remove("fa-edit");
        edit.classList.add("fa-check");
        task.style.justifyContent = 'flex-end';
        subnotes_edit.style.display = 'block'
        subnotes.style.display = 'none'
    } else {
        edit.classList.add("fa-edit")
        form.submit();
    }
}

/**
 * closing and opening of sidebar on click of hamburger
 */

function openSidebar() {
    sidebar = document.querySelector(".sidebar");
    add_btn = document.querySelector(".add-btn");

    if (sidebar.classList.contains("closed")) {
        sidebar.classList.remove("closed")
        sidebar.style.width = "200px"

        sidebar.querySelectorAll('a').forEach(function (i) {
            i.style.visibility = "visible"
        })

        add_btn.style.visibility = "visible";

    } else {
        sidebar.classList.add("closed")
        sidebar.style.width = "70px"

        sidebar.querySelectorAll('a').forEach(function (i) {
            i.style.visibility = "hidden"
        })

        add_btn.style.visibility = "hidden";

    }
}
