window.onload = function () {
	var elt = new Croppie(document.getElementById('picture'), {
		enableExif: true,
		enableOrientation: true,
		viewport: {
			width: 200,
			height: 200
		},
		boundary: {
			width: 300,
			height: 300
		}
	});
	var src = document.getElementById('pic').getAttribute('src');

	if (src === '/pic/picture?t=person.svg') {
		console.log('Default picture - No bind');
	} else {
		elt.bind({
			url: src,
			zoom: true
		});
		console.log('Existing picture - Bind');
	}

	function readFile(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
			reader.onload = function(event) {
				elt.bind({
					url: event.target.result,
					zoom: true
				}).then(function() {
					console.log('Bind complete');
					document.getElementById('save').disabled = false;
					document.getElementById('delete').disabled = false;
					document.getElementById('rotate-left').disabled = false;
					document.getElementById('rotate-right').disabled = false;
				});
			};
			reader.readAsDataURL(input.files[0]);
		};
	};

	function rotateFile(deg) {
		elt.rotate(deg);
	}

	function saveFile() {
		elt.result({
			type: 'blob',
			size: 'viewport',
			format: 'jpeg'
		}).then(function (blob) {
			var xhr = new XMLHttpRequest();
			var formData = new FormData();
			var url = '/pic/save_avatar';
			var token = document.getElementById('csrfToken').value;

			formData.append('file', blob, "test.png"); // Raw blob file

			xhr.open('POST', url, true);
			xhr.setRequestHeader('X-CSRF-Token', token);
			xhr.onload = function () {
				if (xhr.readyState === xhr.DONE) {
					if (xhr.status === 200) {
						var res = JSON.parse(xhr.responseText);
						console.log(res);
						document.getElementById('pic').classList.add('d-none');
						elt.destroy();
						window.location.replace('/');
					}
				}
			};
			xhr.onerror = function() {
				var res = JSON.parse(xhr.responseText);
				console.log(res);
				elt.destroy();
				window.location.replace('/pic/avatar');
			};
			xhr.send(formData);
		});
	};

	function deleteFile() {
		swal({
			title: "Are you sure?",
			text: "Once deleted, you will not be able to recover it!",
			icon: "warning",
			closeOnClickOutside: true,
			closeOnEsc: true,
			buttons: {
				cancel: true,
				confirm: true,
			},
			dangerMode: true,
		}).then((isConfirm) => {
			if (isConfirm) {
				var xhr = new XMLHttpRequest();
				var url = '/pic/delete_avatar';
				var token = document.getElementById('csrfToken').value;

				xhr.open('POST', url, true);
				xhr.setRequestHeader('X-CSRF-Token', token);
				xhr.onload = function () {
					if (xhr.readyState === xhr.DONE) {
						if (xhr.status === 200) {
							var res = JSON.parse(xhr.responseText);
							console.log(res);
							document.getElementById('pic').setAttribute('src', '/pic/picture?t=person.svg');
							elt.destroy();
							elt = new Croppie(document.getElementById('picture'), {
								enableExif: true,
								enableOrientation: true,
								viewport: {
									width: 200,
									height: 200
								},
								boundary: {
									width: 300,
									height: 300
								}
							});
							document.getElementById('delete').disabled = true;
							document.getElementById('save').disabled = true;
							document.getElementById('rotate-left').disabled = true;
							document.getElementById('rotate-right').disabled = true;
						}
					}
				};
				xhr.onerror = function () {
					var res = JSON.parse(xhr.responseText);
					console.log(res);
					window.location.replace('/pic/avatar');
				};
				xhr.send();
			}
		});
	};

	function cancel() {
		document.getElementById('pic').classList.add('d-none');
		elt.destroy();
		window.location.replace('/');
	}

	document.addEventListener('change', function(event) {
		if (event.target.matches('#file-input')) readFile(event.target);
		// console.log(event.target);

	}, false);

	document.addEventListener('click', function (event) {
		if (event.target.matches('#rotate-left')) rotateFile(-90);
		if (event.target.matches('#rotate-right')) rotateFile(90);
		if (event.target.matches('#save')) saveFile();
		if (event.target.matches('#delete')) deleteFile();
		if (event.target.matches('#cancel')) cancel();
		// console.log(event.target);
	}, false);
};