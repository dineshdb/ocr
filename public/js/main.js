const canvas = document.querySelector("#canvas")
const context = canvas.getContext('2d')
const img = document.querySelector("#source")
const inputFile = document.querySelector("#fileInput")
let front = false, mirror = false
var constraints = { video: { facingMode: (front? "user" : "environment") } };
img.onclick= function(e){
	console.log("hello", e)	
}

//document.getElementById('flip-button').onclick = function() { front = !front; };

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

