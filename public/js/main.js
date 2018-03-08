const canvas = document.querySelector("#canvas")
const context = canvas.getContext('2d')
const img = document.querySelector("#source")
const inputFile = document.querySelector("#fileInput")
let front = false, mirror = false
var constraints = { video: { facingMode: (front? "user" : "environment") } };
let fileId;
var slider = document.getElementById('slider');
noUiSlider.create(slider, {
	start: [20, 80],
	connect: true,
	range: {
		'min': 0,
		'max': 100
	}
});

img.onclick= function(e){
    inputFile.click()
}

inputFile.onchange = function(e) {
    var url = URL.createObjectURL(e.target.files[0]);
    img.src = url;
    let form = new FormData()
    form.append('id', Date.now())
    form.append('files', inputFile.files[0])
//    upload(e.target.files[0]);
  fetch('/', {
    method: 'POST',
    body: form,
  }).then(response => response.json()).then( res => fileId = res.id).catch(console.log)
}

function fetchResult(id, minArea = 20, maxArea = 80){
	fileId = id
	return fetch('/predict/' + id + '?min=' + minArea + '&max='+ maxArea).then(res => res.json()).then(res => {
 	 	context.clearRect(0, 0, canvas.width, canvas.height);
 	 	res.data.forEach(function(dat){
 	 		let [x, y] = dat.coor
 	 		context.fillText(dat.label,x, y)
    		})
    	})
}

function regenerate(e){
	let [min, max] = slider.noUiSlider.get()
	return fetchResult(fileId, min, max).catch(console.log)
}
