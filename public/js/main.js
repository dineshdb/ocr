const canvas = document.querySelector("#canvas")
const context = canvas.getContext('2d')
const img = document.querySelector("#source")
const inputFile = document.querySelector("#fileInput")
let front = false, mirror = false
var constraints = { video: { facingMode: (front? "user" : "environment") } };
img.onclick= function(e){
	inputFile.click()
}

inputFile.onchange = function(e) {
    var url = URL.createObjectURL(e.target.files[0]);
    img.src = url;
}

function mirrorVideo(){
    mirror = !mirror
    video.classList.toggle("camera-flip")
}
function setupCamera(){
	navigator.mediaDevices.getUserMedia(constraints)
    		.then(stream => video.srcObject = stream)
    		.then(()=>{
    		}).catch(console.log)        
}
function takePicture(){
   context.drawImage(video, 0, 0, canvas.width, canvas.height);
   video.pause()
   video.srcObject.getVideoTracks().forEach(track => track.stop());
}

