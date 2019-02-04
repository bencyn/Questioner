var serialize = function (form) {

	// Setup our serialized data
	var serialized = [];

	// Loop through each field in the form
	for (var i = 0; i < form.elements.length; i++) {

		var field = form.elements[i];

		// Don't serialize fields without a name, submits, buttons, file and reset inputs, and disabled fields
		if (!field.name || field.disabled || field.type === 'file' || field.type === 'reset' || field.type === 'submit' || field.type === 'button') continue;

		// If a multi-select, get all selections
		if (field.type === 'select-multiple') {
			for (var n = 0; n < field.options.length; n++) {
				if (!field.options[n].selected) continue;
				serialized.push(encodeURIComponent(field.name) + "=" + encodeURIComponent(field.options[n].value));
			}
		}

		// Convert field data to a query string
		else if ((field.type !== 'checkbox' && field.type !== 'radio') || field.checked) {
			serialized.push(encodeURIComponent(field.name) + "=" + encodeURIComponent(field.value));
		}
	}

	return serialized.join('&');

};
var parseJwt = (token) => {
	try {
	  return JSON.parse(atob(token.split('.')[1]));
	} catch (e) {
	  return null;
	}
  };

let base_url = 'http://127.0.0.1:5000/api/v2';

function logout(e){
	e.preventDefault()
	var result = confirm("Are sure you want to logout?");
	if (result) {
			localStorage.clear();
			window.location.href = '../UI/index.html'
	}
}
export {
	serialize,base_url,parseJwt,logout
}