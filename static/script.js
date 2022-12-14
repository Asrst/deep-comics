'use strict';

async function upload(file) {
    const data = new FormData()
    data.append('file', file)

    let status = 'Begining';

    const response = await fetch('/api/submit', {
        method: 'POST',
        body: data
    });

    if (!response.ok) {
        if (response.status === 413) {
            // File too long.
            status = 'Selected video is too long (max 25 MB or 300 Seconds)'
        }
        else {
            status = `Something Went Wrong. Error: ${response.statusText}.`;
        }
    }
    else {
        const img_blob = await response.blob();
        const img_url = URL.createObjectURL(img_blob);

        const img = document.getElementById('image');
        img.src = img_url;
        img.classList.remove('d-none');
    }

    const form = document.getElementById('form');
    form.remove();

    const msg = document.getElementById('msg');
    msg.innerText = status;
}

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('file_input');
    const button = document.getElementById('submit_button');

    input.addEventListener('change', event => {
        button.disabled = (event.target.value === '');
    });

    button.addEventListener('click', event => {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

        upload(input.files[0]);
    });
})
