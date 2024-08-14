// const Explode = document.getElementById('Explode')
// const Butterflies = document.getElementById('Butterflies')
// const Heart = document.getElementById('Heart')
// const None = document.getElementById('None')
const videoStream = document.getElementById('videoStream')
const clickme = document.getElementById('clickme')

const io = require('socket.io-client')
const socket = io('http://127.0.0.1:5000')


socket.on('connect', () => {
    console.log('Connected to Flask Socket.IO server');
});

socket.on('message_to_nodejs', (message) => {
    console.log('received', message)
    clickme.click()
});

socket.emit('message_from_nodejs', 'Hello from Node.js client');

// Explode.addEventListener('click', () => {
//     console.log("test render")
//     const selecting = document.getElementById('selecting')
//     selecting.remove()

//     Explode.innerHTML += `
//     <div id="selecting" class="selecting">
//         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>
//     </div>
//     `
//     videoStream.src = 'http://127.0.0.1:5000/video/explode'
// });

// Butterflies.addEventListener('click', () => {
//     const selecting = document.getElementById('selecting')
//     selecting.remove()
//     Butterflies.innerHTML += `
//     <div id="selecting" class="selecting">
//         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>
//     </div>
//     `
//     videoStream.src = 'http://127.0.0.1:5000/video/butterflies'
// });
// Heart.addEventListener('click', () => {
//     const selecting = document.getElementById('selecting')
//     selecting.remove()
//     Heart.innerHTML += `
//     <div id="selecting" class="selecting">
//         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>
//     </div>
//     `
//     videoStream.src = 'http://127.0.0.1:5000/video/heart'
// });
// None.addEventListener('click', () => {
//     const selecting = document.getElementById('selecting')
//     selecting.remove()
//     None.innerHTML += `
//     <div id="selecting" class="selecting">
//         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>
//     </div>
//     `
//     videoStream.src = 'http://127.0.0.1:5000/video'
// });

async function capture() {
    const url = 'http://127.0.0.1:5000/capture'
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
    } catch (error) {
        console.error(error.message);
    }
}