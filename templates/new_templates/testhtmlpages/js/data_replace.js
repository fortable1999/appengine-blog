//<![CDATA[
    function date_replace(date) {
        var da = date.split('.');
        var day = da[1], mon = da[0], year = da[2];
        var month = ['0','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        document.write("<div class='month'>"+month[mon]+"</div> <div class='day'>"+day+"</div>");
    }
//]]>
