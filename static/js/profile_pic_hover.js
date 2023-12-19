(function ($) {
    $(document).ready(function () {
        $(".profile-pic-container").hover(function () {
            var imageUrl = $(this).data("image");
            var popUpHtml = '<div class="profile-pic-popup"><img src="' + imageUrl + '" /></div>';
            $(this).append(popUpHtml);
        }, function () {
            $(".profile-pic-popup").remove();
        });
    });
})(django.jQuery);
