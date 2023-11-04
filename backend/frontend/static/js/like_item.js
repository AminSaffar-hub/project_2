$(document).ready(function () {
    $(document).on('click', '.like-button', function () {
        const button = $(this);
        const itemId = button.data('item-id');

        $.ajax({
            url: `/like_item/${itemId}/`,
            type: 'POST',
            data: null,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (data) {
                const heartIcon = button.find('.fa');
                if (data.like) {
                    // Set the filled heart icon and change the color to red
                    heartIcon.removeClass('fa-heart-o').addClass('fa-heart');
                    heartIcon.css('color', 'red');
                } else {
                    // Set the empty heart icon and change the color to gray
                    heartIcon.removeClass('fa-heart').addClass('fa-heart-o');
                    heartIcon.css('color', 'gray');
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

});