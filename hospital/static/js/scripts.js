

async function sendAjaxData(user_id, action) {
    const formData = new FormData();
    formData.set('user_id', user_id);
    formData.set('action', action);
    formData.set("csrfmiddlewaretoken", csrf_token);
    console.log(formData);
    const response = await fetch(patient_review_url, {
        method: 'POST',
        body: formData
    });
    if (response.ok) {
        let button = document.getElementById('list-' + user_id);
        let listItem = document.getElementById('list-'+user_id+'-list');
        button.remove();
        listItem.remove();
    }


}
