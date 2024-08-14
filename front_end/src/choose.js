const axios = require('axios')
const buttons = document.getElementById('buttons')

const shootedContainer = document.getElementById('shooted')

shootedContainer.innerHTML =
    `
        <div data-selected="false">
            <img src="./images/0.jpg">
        </div>
        <div data-selected="false">
            <img src="./images/1.jpg">
        </div>
        <div data-selected="false">
            <img src="./images/2.jpg">
        </div>
        <div data-selected="false">
            <img src="./images/3.jpg">
        </div>
        <div data-selected="false">
            <img src="./images/4.jpg" onerror="this.style.display='none'">
        </div>
        <div data-selected="false">
            <img src="./images/5.jpg" onerror="this.style.display='none'">
        </div>
        <div data-selected="false">
            <img src="./images/6.jpg" onerror="this.style.display='none'">
        </div>
        <div data-selected="false">
            <img src="./images/7.jpg" onerror="this.style.display='none'">
        </div>
    `

const items = shootedContainer.getElementsByTagName("div");
const finalResult = document.getElementById('finalResult')

let selectedCount = 0;
let selectedIndices = [];

for (let index = 0; index < items.length; index++) {
    const item = items[index]

    item.addEventListener('click', () => {
        const isSelected = item.getAttribute('data-selected') === 'true';
        if (isSelected) {
            item.setAttribute('data-selected', 'false');
            item.classList.remove('selected');
            selectedCount--;
            const selectedIndex = selectedIndices.indexOf(index);
            selectedIndices.splice(selectedIndex, 1);
        } else {
            if (selectedCount < 2) {
                item.setAttribute('data-selected', 'true');
                item.classList.add('selected');
                selectedCount++;
                selectedIndices.push(index);
            }
            //  else {
            //     alert('You can only select up to 2 items.');
            // }
        }
        console.log("Selected Indices:", selectedIndices);

        finalResult.innerHTML = `
            <img src="./images/${selectedIndices[0]}.jpg" onerror="this.style.display='none'">
            <img src="./images/${selectedIndices[1]}.jpg" onerror="this.style.display='none'">
            `
    });
}

function prnn() {
    console.log('clicked')
    if (selectedIndices.length != 0) {
        buttons.innerHTML = `<p style="text-align: center">Đang in... 🥰</p>`
        axios.get(`http://127.0.0.1:5000/print?firstPic=${selectedIndices[0]}&secondPic=${selectedIndices[1]}`)
            .then(response => {
                if (response.data == 'hello') {
                    setTimeout(() => {
                        buttons.innerHTML = `<p style="text-align: center">Hãy đến quầy <br/> để nhận ảnh 😻</p>`
                    }, 5000)
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        buttons.innerHTML += `<p style="text-align: center">Vui lòng chọn hình</p>`
    }
}