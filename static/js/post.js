console.log('JS is working!')
var count = 0
document.addEventListener('DOMContentLoaded', function() {
	console.log('DOM Loaded')

	let a = resetCounter()
	if (resetCounter() == true) {
		count = 0
		localStorage.setItem('ThanksCount', count)
	}
	else {
		count = parseInt(userCount.innerHTML)
		localStorage.setItem('ThanksCount', count)
	}
	counter = document.getElementById(`counterBadge`).innerHTML = parseInt(localStorage.getItem('ThanksCount'))
	document.querySelector('#submitThanks').addEventListener('click', () => checkCounter());
})


function like(val) {
currentLikes = document.getElementById(`badgeLike${val}`).innerText
	updatedLikes = parseInt(currentLikes) + 1
	console.log('current likes: ',currentLikes)
	console.log('updated likes: ',updatedLikes)
	const csrftoken = getCookie('csrftoken');
	console.log(val, 'like button id clicked')
	var msg = {id: val, dog:'Husky'};

	const options = {
		method: 'POST',
		body: JSON.stringify(msg),
		headers: {'X-CSRFToken': csrftoken}
	}
	fetch('/like', options)
	.then(res => res.text())
	.then(text => console.log(text))
	.catch(error => {
	console.error(error);
	});
	document.getElementById(`badgeUnlike${val}`).innerHTML = updatedLikes
	document.getElementById(`likeButton${val}`).style.display = 'none';
	document.getElementById(`unlikeButton${val}`).style.display = 'inline';

}

function unlike(val) {
	currentLikes = document.getElementById(`badgeUnlike${val}`).innerText
	updatedLikes = parseInt(currentLikes) - 1
	console.log('current likes: ',currentLikes)
	console.log('updated likes: ',updatedLikes)

	const csrftoken = getCookie('csrftoken');
	console.log(val, 'like button id clicked')
	var msg = {id: val, dog:'Husky'};

	const options = {
		method: 'POST',
		body: JSON.stringify(msg),
		headers: {'X-CSRFToken': csrftoken}
	}
	fetch('/like', options)
	.then(res => res.text())
	.then(text => console.log(text))
	.catch(error => {
	console.error(error);
	});
	document.getElementById(`unlikeButton${val}`).style.display = 'none';
	document.getElementById(`likeButton${val}`).style.display = 'inline';
	document.getElementById(`badgeLike${val}`).innerHTML = updatedLikes	
}

$(document).ready(function() {
      if (window.location.pathname == '/journal') {
      		var myClasses = document.querySelectorAll('.form-group')
	let i = 0
	let l = myClasses.length
	console.log(l)
	console.log('hi ya peeps')
	for (i; i < l; i++) {
    myClasses[i].style.display = 'none';
    	}
	}
          })

function editPost(id, value) {
	console.log('I pressed edit post')
	console.log(value)
	id = id
	console.log('OP')
	console.log(id)
	
	originalText = "blogText" + value
	post = 'editPostText'+ value
	list = 'li' + value
	editedPost = 'edit-post' + value
	originalText = document.getElementById(id).innerHTML;
	console.log(originalText)
	console.log('Next is value')
	document.getElementById(editedPost).placeholder= originalText;
	document.getElementById(post).style.display = 'initial';
	document.getElementById(list).style.display = 'none';
	
}


function resetCounter(){
	if (last_post.innerHTML == 'false'){
		return true
	}
	var today = new Date()
	var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
	postYear = last_post.innerHTML.slice(1,5)
	postMonth = last_post.innerHTML.slice(6,8)
	postDay = last_post.innerHTML.slice(9,11)
	lastPostDate = new Date(postYear, (postMonth-1), postDay)
	today.setHours(0,0,0,0)
	if (today.getTime()  != lastPostDate.getTime()){
		return true
	}
}

function checkCounter() {
	count = parseInt(localStorage.getItem('ThanksCount'))
	counter = document.getElementById(`counterBadge`).innerHTML = count
	count += 1
	document.getElementById(`counterBadge`).innerHTML = count
	localStorage.setItem('ThanksCount', count)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function submitPost(val) {
	console.log('Trying to submit post')
	console.log(val)
	const csrftoken = getCookie('csrftoken');
	url = 'edit/' + String(val)	

	console.log(url)
	originalText =document.getElementById(`edit-post${val}`).placeholder;
	console.log(originalText)
	editedText = document.getElementById(`edit-post${val}`).value;
	console.log(editedText)
	if (editedText === ""){
		console.log('Blank String')
		editedText = originalText
	}
	var edit = {text: editedText};

	const options = {
		method: 'POST',
		body: JSON.stringify(edit),
		headers: {'X-CSRFToken': csrftoken}	}

	fetch(url, options)
	.then(res => res.text())
	.then(text => console.log(text))
	.catch(error => {
		console.log(error);
		console.error(error);
	});
	document.getElementById(`li${val}`).innerHTML = editedText;
	console.log("did we get here?")
	post = 'editPostText'+ val
	list = 'li' + val
	listHtml = '<li>' + editedText + '</li>'
	document.getElementById(post).style.display = 'none';
	document.getElementById(list).style.display = 'initial';
	}

