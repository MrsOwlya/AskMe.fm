// $(document).ready(function(){
//     $.ajax({
//         url: 'hot_tags',
//         data: hot_tags,
//     });
//     console.log("First");
//     $.ajax({
//         url: 'active_users',
//         data: active,
//     });
//     console.log("Second");
// });
$(document).ready(function(){
        var ask = $('.asklikes-button').attr("data-ans");
        var $like1 = $('#likeask' + ask);
        var $dis1 = $('#disask' + ask);
        $.post('/show_asklikes/', {ask_id: ask}, function(data) {
        if(data.like === true){
            $like1.css('color', 'rgb(102, 51, 153)');
        }else if(data.dislike === true){
            $dis1.css('color', 'rgb(102, 51, 153)');
        }
        });

        $.each($('.anslikes-button'), function(){
            var ans = $(this).attr("data-ans");
            var $like = $('#likeans' + ans);
            var $dis = $('#disans' + ans);
            $.post('/show_anslikes/', {answer_id: ans}, function(data) {
            if(data.like === true){
                $like.css('color', 'rgb(102, 51, 153)');
            }else if(data.dislike === true){
                $dis.css('color', 'rgb(102, 51, 153)');
            }
            });
        });
});

$('.anslikes-button').click(function(){
    var ans = $(this).attr("data-ans");
    var answer = $(this).attr("answer");
    var $like = $('#likeans' + ans);
    var $dis = $('#disans' + ans);
    var cur = parseInt($like.text());
    var cur2 = parseInt($dis.text());
    if(answer === "anslike"){
        if($like.css('color') === 'rgb(255, 255, 255)'){
            cur++;
            $like.text(cur);
            $like.css('color', 'rgb(102, 51, 153)');
            $dis.css('color', 'rgb(255, 255, 255)');
        }else{
            cur--;
            $like.text(cur);
            $like.css('color', 'rgb(255, 255, 255)');
        };
    }else{
        if($dis.css('color') === "rgb(255, 255, 255)"){
            cur2++;
            $dis.text(cur2);
            $dis.css('color', 'rgb(102, 51, 153)');
            $like.css('color', 'rgb(255, 255, 255)');
        }else{
            cur2--;
            $dis.text(cur2);
            $dis.css('color', 'rgb(255, 255, 255)');
        };
    };
    $.post('/add_anslike/', {answer_id: ans, answer: answer}, function(data) {
        $('#likeans' + ans).text(data.anslikes);
        $('#disans' + ans).text(data.ansdislikes);
    });
});

$('.asklikes-button').click(function(){
    var ans = $(this).attr("data-ans");
    var answer = $(this).attr("answer");
    var $like = $('#likeask' + ans);
    var $dis = $('#disask' + ans);
    var cur = parseInt($like.text());
    var cur2 = parseInt($dis.text());
    if(answer === "asklike"){
        if($like.css('color') === 'rgb(255, 255, 255)'){
            cur++;
            $like.text(cur);
            $like.css('color', 'rgb(102, 51, 153)');
            $dis.css('color', 'rgb(255, 255, 255)');
        }else{
            cur--;
            $like.text(cur);
            $like.css('color', 'rgb(255, 255, 255)');
        };
    }else{
        if($dis.css('color') === "rgb(255, 255, 255)"){
            cur2++;
            $dis.text(cur2);
            $dis.css('color', 'rgb(102, 51, 153)');
            $like.css('color', 'rgb(255, 255, 255)');
        }else{
            cur2--;
            $dis.text(cur2);
            $dis.css('color', 'rgb(255, 255, 255)');
        };
    };
    $.post('/add_asklike/', {answer_id: ans, answer: answer}, function(data) {
        $('#likeask' + ans).text(data.asklikes);
        $('#disask' + ans).text(data.askdislikes);
    });
});