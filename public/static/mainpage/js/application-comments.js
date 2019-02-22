function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie("csrftoken");
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function formatDate(date) {
	var monthNames = [
		"stycznia",
		"lutego",
		"marca",
		"kwietnia",
		"maja",
		"czerwca",
		"lipca",
		"sierpnia",
		"wrzesienia",
		"paźdźiernika",
		"listopada",
		"grudnia"
	];

	var day = date.getDate();
	var monthIndex = date.getMonth();
	var year = date.getFullYear();
	var hours = date.getHours();
	var minutes = date.getMinutes();
	return day + " " + monthNames[monthIndex] + " " + year + " " + hours + ":" + minutes;
}

$.ajax({
	url: "/api/applications-comments/",
	type: "get",
	dataType: "json",
	success: function(data) {
		let rows = "";
		console.log(data);
	}
});

$("#form-comments").on("submit", function(event) {
	event.preventDefault();
	$.ajax({
		type: "post",
		url: "/api/applications-comments/",
		dataType: "json",
		data: {
			content: $("#id_content").val(),
			application: $("#id_application").val(),
			owner: $("#id_owner").val(),
			owner_avatar: $("#id_owner_avatar").val(),
			owner_name: $("#id_owner_name").val(),
			csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
		},
		success: function(data) {
			//console.log(data);
			$("#id_content").val("");
			$(".comments-list").prepend(
				"<div class='media'><a class='pull-left author-info' href='#'><img class='img-fluid' src='" +
					data.owner_avatar +
					"'/></a><div class='media-body comment-info'><p class='pull-right media-meta'><small>" +
					formatDate(new Date(data.created)) +
					"</small></p>" +
					"<h4 class='media-heading user_name'>" +
					data.owner_name +
					"</h4>" +
					data.content +
					"</div></div>"
			);
			$(".no-com").hide();
		}
	});
});

$(".del-comment").click(function(event) {
	event.preventDefault();
	//console.log("Kliknięto");
	pk = $(this).data("pk");
	//console.log(pk);
	$.ajax({
		type: "delete",
		url: "/api/applications-comments/" + pk,
		dataType: "json",
		data: {
			id: pk
		},
		success: function(data) {
			$(".media")
				.filter("[data-pk='" + pk + "']")
				.slideUp();
		}
	});
});

$(".edit-comment").click(function(event) {
	event.preventDefault();
	pk = $(this).data("pk");
	$(".content-comment")
		.filter("[data-pk='" + pk + "']")
		.hide();
	//$(".editform-comment").filter("[data-pk='" + pk + "']").append("<form><input type=\"text\"><button type=\"submit\">Zapisz</button></form>").show();
	$.ajax({
		type: "put",
		url: "/api/applications-comments/" + pk,
		dataType: "json",
		data: {}
	});
});
