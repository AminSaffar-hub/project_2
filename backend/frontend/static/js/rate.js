$(document).ready(function () {
    $(document).on('click', '.rating-button', function () {
        const button = $(this);
        const itemId = button.data('item-id');
        const isLike = button.data('like');

        const formData = new FormData();
        formData.append('like', isLike);

        $.ajax({
            url: `/rate/${itemId}/`,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (data) {
                const ratingCountElement = $(`#rating-count-${itemId}`);
                ratingCountElement.text(data.like_count - data.dislike_count);
                console.log(button)
                
                button[0].classList.toggle("btn-outline-primary")
                button[0].classList.toggle("btn-primary")
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

});