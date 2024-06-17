// toast notifications

const notifications = document.querySelector("#notifications")


function remove_toast(toast) {
	toast.classList.add("hide");

	if (toast.timeoutId) {
		clearTimeout(toast.timeoutId);
	}

	setTimeout(() => toast.remove(), 300);
}

function toast(text, type="error", timeout=5) {
	const toast = document.createElement("li");
	toast.className = `section ${type}`
	toast.innerHTML = `<span class=".text">${text}</span><a href="#">&#10006;</span>`

	toast.querySelector("a").addEventListener("click", async (event) => {
		event.preventDefault();
		await remove_toast(toast);
	});

	notifications.appendChild(toast);
	toast.timeoutId = setTimeout(() => remove_toast(toast), timeout * 1000);
}


// menu

const body = document.getElementById("container")
const menu = document.getElementById("menu");
const menu_open = document.querySelector("#menu-open i");
const menu_close = document.getElementById("menu-close");


function toggle_menu() {
	let new_value = menu.attributes.visible.nodeValue === "true" ? "false" : "true";
	menu.attributes.visible.nodeValue = new_value;
}


menu_open.addEventListener("click", toggle_menu);
menu_close.addEventListener("click", toggle_menu);

body.addEventListener("click", (event) => {
	if (event.target === menu_open) {
		return;
	}

	menu.attributes.visible.nodeValue = "false";
});

for (const elem of document.querySelectorAll("#menu-open div")) {
	elem.addEventListener("click", toggle_menu);
}


// misc

function get_date_string(date) {
	var year = date.getUTCFullYear().toString();
	var month = (date.getUTCMonth() + 1).toString().padStart(2, "0");
	var day = date.getUTCDate().toString().padStart(2, "0");

	return `${year}-${month}-${day}`;
}


function append_table_row(table, row_name, row) {
	var table_row = table.insertRow(-1);
	table_row.id = row_name;

	index = 0;

	for (var prop in row) {
		if (Object.prototype.hasOwnProperty.call(row, prop)) {
			var cell = table_row.insertCell(index);
			cell.className = prop;
			cell.innerHTML = row[prop];

			index += 1;
		}
	}

	return table_row;
}


async function request(method, path, body = null) {
	var headers = {
		"Accept": "application/json"
	}

	if (body !== null) {
		headers["Content-Type"] = "application/json"
		body = JSON.stringify(body)
	}

	const response = await fetch("/api/" + path, {
		method: method,
		mode: "cors",
		cache: "no-store",
		redirect: "follow",
		body: body,
		headers: headers
	});

	const message = await response.json();

	if (Object.hasOwn(message, "error")) {
		throw new Error(message.error);
	}

	if (Array.isArray(message)) {
		message.forEach((msg) => {
			if (Object.hasOwn(msg, "created")) {
				msg.created = new Date(msg.created);
			}
		});

	} else {
		if (Object.hasOwn(message, "created")) {
			console.log(message.created)
			message.created = new Date(message.created);
		}
	}

	return message;
}
