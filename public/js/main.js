const canvas = document.querySelector("#canvas")
const context = canvas.getContext('2d')
const img = document.querySelector("#source")
const inputFile = document.querySelector("#fileInput")
let front = false, mirror = false
var constraints = { video: { facingMode: (front? "user" : "environment") } };

img.onclick= function(e){
    inputFile.click()
}

const upload = (e) => {
  fetch('/', { 
    method: 'POST',       
    body: e 
  }).then(
    response => response.json() 
  ).then(
    success => console.log(success) // Handle the success response object
  ).catch(
    error => console.log(error) // Handle the error response object
  );
};

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
  }).then(response => response.json()
  ).then( res => fetch('/predict/' + res.id)
  ).then(res => console.log(res)
  ).catch(
    error => console.log(error) // Handle the error response object
  );

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

