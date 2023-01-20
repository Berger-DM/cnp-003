$(document).ready(function () {
    $('#carousel_select').change(function () {
        const selectedValue = this.value;
        $('#carousel_title').html(selectedValue);
    })
})

