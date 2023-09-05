$(document).ready(function () {
    const likeButton = $('#like-button');
    const dislikeButton = $('#dislike-button');
    const ratingCountElement = $('#rating-count');

    function rate(button, isLike) {
        const itemId = button.data('item-id');
        const csrftoken = $('[name=csrfmiddlewaretoken]').val();

        const formData = new FormData();
        formData.append('like', isLike);
        formData.append('csrfmiddlewaretoken', csrftoken);

        // Disable the clicked button
        button.prop('disabled', true);

        $.ajax({
            url: `/rate/${itemId}/`,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (data) {
                ratingCountElement.text(data.like_count - data.dislike_count);
            },
            error: function (error) {
                console.error('Error:', error);
                // Re-enable the button in case of an error
                button.prop('disabled', false);
            }
        });
    }

    likeButton.on('click', function () {
        rate(likeButton, true);
    });

    dislikeButton.on('click', function () {
        rate(dislikeButton, false);
    });
});