$(document).ready(function(){

    ActivateAllButtons();

    $(document).on('submit', "#searchform", function(e){
        var selected = GetActivatedButtons();
        var search = $('#id_keyword').val();
        var dates = GetDates();

        $.ajax({
            url: "get-tweets/",
            type: "POST",
            data: {'dates': dates, 'selected': selected,'search': search},
            success: function(response) {
                $(".tweetcontainertitle h1").replaceWith("<h1>Search Results</h1>")
                $(".tweetcontainer").find("li").remove();
                $(".tweetcontainer").find("button").remove();
                $(".maxdata").remove();
                $(".tweetcontainer").append(response);
            }
        });
        $('html, body').animate({
            scrollTop: $(".tweetcontainer").offset().top
        }, 1600);

        e.preventDefault();
    });

    $(document).on('click', "#loadmore", function(e){
        var selected = GetActivatedButtons();
        var search = $('#id_keyword').val();
        var dates = GetDates();
        var max_id = $('.tweet').last().attr('id');
        $.ajax({
            url: "load-more/",
            type: "POST",
            data: {'dates': dates, 'selected': selected,'search': search, 'max_id': max_id},
            success: function(response) {
                $(".tweetcontainer").find("button").remove();
                $(".tweetcontainer").append(response);
            }
        });
        e.preventDefault();
    });

    $(document).on('click', "#optionbuttons", function(e){
        // Check if it's already activated
        if($(this).hasClass("activated")){
            DeactivateButton($(this))
            DeactivateButton($('#optionbuttons').eq(0))
        } else {
            ActivateButton($(this))
        }
        // If they hit the all button then activate all or deactivate all
        if($(this).text().includes("All")){
            if($(this).hasClass("activated")){
                ActivateAllButtons();
            } else{
                DeactivateAllButtons();
            }

        }
    });

    function ActivateButton(self){
        $(self).addClass("activated");
        $(self).css("background-color", "#F78181");
        $(self).css("color", "white");
    }

    function DeactivateButton(self){
        $(self).removeClass("activated");
        $(self).css("background-color", "white");
        $(self).css("color", "black");
    }

    function ActivateAllButtons(){
        $("#btngroup button").css("background-color", "#F78181");
        $("#btngroup button").css("color", "white");
        $("#btngroup button").addClass("activated");
    }

    function DeactivateAllButtons(){
        $("#btngroup button").css("background-color", "white")
        $("#btngroup button").css("color", "black")
        $("#btngroup button").removeClass("activated");
    }

    function GetActivatedButtons(){
        var activeButtons = [];
         $("#btngroup button").each(function(){
            if($(this).hasClass("activated")){
                activeButtons.push($(this).text())
            }
         });
         return activeButtons;
    }

    function GetDates(){
        var dates = [];
        dates.push(MonthToNum($("#startdate #month option:selected").text()));
        dates.push($("#startdate #day option:selected").text());
        dates.push($("#startdate #year option:selected").text());
        dates.push(MonthToNum($("#enddate #month option:selected").text()));
        dates.push($("#enddate #day option:selected").text());
        dates.push($("#enddate #year option:selected").text());
        return dates;
    }

    function MonthToNum(month){
        return{
            'January' : 01,
            'February' : 02,
            'March' : 03,
            'April' : 04,
            'May' : 05,
            'June' : 06,
            'July' : 07,
            'August' : 08,
            'September' : 09,
            'October' : 10,
            'November' : 11,
            'December' : 12
        }[month]
    }

    // Checks all checkboxes on the page
    $(document).on('change', "#checkAll", function(e){
        $("input:checkbox").prop('checked', $(this).prop("checked"));
    });

    $(document).on('click', "#erasebtn", function(e){
        SetTweetCount();
    });
    $(document).on('click', '#yeserasetweets', function(e){
        var ids = GetCheckedIds();
        $.ajax({
            url: "erase-tweets/",
            type: "POST",
            data: {'ids': ids},
            success: function(response) {
                for(var i=0; i<ids.length; i++){
                    var selector = "#" + String(ids[i]);
                    $(selector).parent().remove();
                }
            }
        });
    });

    function SetTweetCount(){
        var checksSelected = document.querySelectorAll('input[type="checkbox"]:checked').length;
        if($('#checkAll').is(':checked')){ checksSelected=checksSelected-1;  }
        if (checksSelected <= 0) { checksSelected=0; }
        $(".tweetcount").replaceWith("<span class='tweetcount'>"+ checksSelected + "</span>")
    }

    function GetCheckedIds(){
        var ids = [];
        // Grab the node list of all checked items and convert to regular array
        var isCheckedNodes= document.querySelectorAll('input[type="checkbox"]:checked'),
        isChecked = [].slice.call(isCheckedNodes);

        // If CheckAll is checked then ignore shift over first item in the array
        if($('#checkAll').is(':checked')){
            isChecked.shift();
        }
        for(var i=0; i<isChecked.length; i++){
            var currentId = $(isChecked[i]).next("div").attr('id');
            ids.push(currentId);
        }
        return ids
    }
});