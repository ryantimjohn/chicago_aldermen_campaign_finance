var parsleyForm = $('#volunteer-form').parsley();
var alert_volunteer = $(".callout");
var v_loading = $("#volunteer-loading");
$("#volunteer-signup").on('click', function () {
    parsleyForm.validate();
    alert_volunteer.hide();
    v_loading.css('visibility', 'visible');
    var formData = $('#volunteer-form').serialize();
    var sendEmail = "smithsade13@gmail.com";
    // var sendEmail = "ReclaimFairElections@gmail.com";
    var mailUrl = "https://formspree.io/"+sendEmail;
    if(parsleyForm.isValid()){
        $.ajax({
            type: "POST",
            url: mailUrl,
            data: formData,
            success: function(data){
                console.log(data);
                v_loading.css('visibility', 'hidden');
                $("form")[0].reset();
                $(".callout.success").fadeIn(1200);
            },
            fail: function(data){
                v_loading.css('visibility', 'hidden');
                alert_volunteer.hide();
            }
        });
    }else{
        v_loading.css('visibility', 'hidden');
    }
});

