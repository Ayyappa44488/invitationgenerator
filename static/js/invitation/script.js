let currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab


// function displayExistingImages() {
//     const container = document.getElementById('existing-images');
//     // container.innerHTML = '';
//     existingImages.forEach((src, index) => {
//         const imageDiv = document.createElement('div');
//         imageDiv.className = 'existing-image';

//         const img = document.createElement('img');
//         img.src = src;
//         img.alt = `Couple Image ${index + 1}`;

//         const removeBtn = document.createElement('button');
//         removeBtn.className = 'remove-btn';
//         removeBtn.innerHTML = '&times;';
//         removeBtn.onclick = () => removeImage(index);

//         imageDiv.appendChild(img);
//         imageDiv.appendChild(removeBtn);
//         container.appendChild(imageDiv);
//     });
// }


function showTab(n) {
    // This function will display the specified tab of the form...
    let tabs = document.getElementsByClassName("form-phase");
    tabs[n].style.display = "block";

    //... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }

    if (n == (tabs.length - 1)) {
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("submitBtn").style.display = "inline";
    } else {
        document.getElementById("nextBtn").style.display = "inline";
        document.getElementById("submitBtn").style.display = "none";
    }
    
    // Display existing images if on the couple images tab
    // if (n == 3) {
    //     // displayExistingImages();
    // }
}

function nextPrev(n) {
    // This function will figure out which tab to display
    let tabs = document.getElementsByClassName("form-phase");

    // Hide the current tab:
    tabs[currentTab].style.display = "none";

    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;

    // Display the correct tab:
    showTab(currentTab);
}



async function removeImage(index) {
    // Confirmation dialog
    const confirmation = confirm('Do you want to remove the image permanently?');
    if (!confirmation) {
        return; // Exit the function if the user cancels the confirmation
    }

    const data = {
        id: index  // Use the index as the id value
    };

    try {
        // Replace 'https://api.example.com/data' with your actual API endpoint
        const response = await fetch('http://127.0.0.1:5000/invitation/delete_image', {
            method: 'POST',  // Use POST method
            headers: {
                'Content-Type': 'application/json',
                // Add any other headers you need here
            },
            body: JSON.stringify(data)  // Convert data to JSON string
        });

        // Check if the response status is OK (200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Parse the JSON response
        const responseData = await response.json();

        // Log the data to the console (for debugging)
        console.log(responseData);

        // Remove the image element from the DOM
        const div = document.getElementById(index);
        if (div) {
            div.remove();
        } else {
            console.warn('Element not found:', index);
        }

    } catch (error) {
        // Handle any errors
        console.error('There was an error!', error);
    }
}


function loadBrideImage(event) {
    const output = document.getElementById('bride-img-preview');
    output.src = URL.createObjectURL(event.target.files[0]);
}

function loadGroomImage(event) {
    const output = document.getElementById('groom-img-preview');
    output.src = URL.createObjectURL(event.target.files[0]);
}

let fileInput = document.getElementById("new-couple-pic");
let imageContainer = document.getElementById("images");
let numOfFiles = document.getElementById("num-of-files");

function preview(){
    imageContainer.innerHTML = "";
    numOfFiles.textContent = `${fileInput.files.length} Files Selected`;

    for(i of fileInput.files){
        let reader = new FileReader();
        let figure = document.createElement("figure");
        let figCap = document.createElement("figcaption");
        figCap.innerText = i.name;
        figure.appendChild(figCap);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            figure.insertBefore(img,figCap);
        }
        imageContainer.appendChild(figure);
        reader.readAsDataURL(i);
    }
}


function addImage() {
    // Get the container for existing images
    var container = document.querySelector('.existing-images');
    var fileInput = document.getElementById('new-couple-pic');

    for (let i of fileInput.files) {
        let reader = new FileReader();

        // Capture the current number of images in the container
        let currentImageIndex = container.children.length + 1;

        // Create a new div for the new image
        var newDiv = document.createElement('div');
        newDiv.className = 'existing-image';
        var newId = 'image-' + currentImageIndex;
        newDiv.id = newId;
        console.log(newId);

        // Create a new remove button
        var newButton = document.createElement('button');
        newButton.type = 'button';
        newButton.className = 'remove-btn';
        newButton.innerHTML = '&times;';
        newButton.addEventListener('click', (function(newId) {
            return function() {
                removeImage(newId);
            };
        })(newId));

        // Create a new image element
        let img = document.createElement('img');
        
        reader.onload = (function(img, currentImageIndex) {
            return function(e) {
                img.setAttribute("src", e.target.result);
                img.alt = 'Couple Image ' + currentImageIndex;
            };
        })(img, currentImageIndex);

        // Append the new image and button to the new div
        newDiv.appendChild(img);
        newDiv.appendChild(newButton);

        // Append the new div to the container
        container.appendChild(newDiv);

        // Read the file as a Data URL
        reader.readAsDataURL(i);
    }
}


