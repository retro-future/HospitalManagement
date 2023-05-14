async function postData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token,
        },
        body: new URLSearchParams(data),
    });
    console.log(new URLSearchParams(data));

    if (!response.ok) {
        throw new Error(`Network response was not OK: ${response.statusText}`);
    }

    return response;
}

async function removeElements(user_id) {
    const button = document.getElementById('list-' + user_id);
    const listItem = document.getElementById('list-' + user_id + '-list');
    button.remove();
    listItem.remove();
}


async function sendAjaxData(user_id, action) {
    try{
        const data = {
            user_id: user_id,
            action: action,
        };
        const response = await postData(patient_review_url, data);
        if (response.ok){
            await removeElements(user_id);
        }
    } catch (error) {
        console.log(error);
    }

}
