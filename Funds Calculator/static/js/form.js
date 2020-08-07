$(document).ready(function()
{

    $('.datepicker').datetimepicker({
        format: 'DD-MM-YYYY',
        minDate: '2015-04-01T00:00:00-00:01',
        maxDate: '2020-08-01T00:00:00-00:01',
        icons: {
          previous: "fas fa-chevron-left",
          next: "fas fa-chevron-right",
        },
    });

    $('.datepicker_code').click(function(){
        $('#investment_date_code').trigger('focus');
    });    

    $('.datepicker_cat').click(function(){
        $('#investment_date_cat').trigger('focus');
    });    

    $(".check-integer").keypress(function (e){
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) 
        {
            $(".alert-danger").html("Warning: Input digits (0 - 9)").show();
            setTimeout(function(){
                $(".alert-danger").fadeOut("slow");
            }, 3000);
            return false;
        }
    });

    $('#fund_category_cat').change(function(){
        let category = $( "#fund_category_cat option:selected" ).text();
        let url = '/get/sub/category';
        let data = {'category': category};

        $.ajax({
            type: "POST",
            url: url,
            async: false,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function (data) 
            {
                if (data.status == 1)
                {
                    $('#fund_sub_category_cat').empty();
                    for(let i=0; i<data.sub_category.length;i++)
                        $('#fund_sub_category_cat').append(new Option(data.sub_category[i]));
                }
            },                
        }); 
    })
    function current_value(url, fund_name, amount, date)
    {
        let data = {'fund_name': fund_name, 'amount': amount, 'date': date};

        $.ajax({
            type: "POST",
            url: url,
            async: false,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function (data) 
            {
                if (data.status == 1)
                {
                    var tbody = $('.net-value tbody');
                    tbody.empty();
                    tbody.append("<tr><td>1</td><td>"+fund_name+"</td><td>"+amount+"</td><td>"+date+"</td><td>"+data.data+" INR</td></tr>");
                    $('.net-value').show();                    
                }
                else
                {
                    var tbody = $('.net-value tbody');
                    tbody.empty();
                    tbody.append("<tr><td>1</td><td>"+fund_name+"</td><td>"+amount+"</td><td>"+date+"</td><td>"+data.data+"</td></tr>");
                    $('.net-value').show();                    
                }                
            },                
        });
    }

    $(".submit-data-cat").click(function( event ) {
        let count = 0;

        $(".required_cat").each(function(){
            if ($(this).val()==null || $(this).val()=="" )
            {
                $(this).css('border', '1px solid #ff0000');
                count++;
            }
            else
            {
                $(this).css('border', '1px solid #ced4da');
            }
        })
        if (count!=0)
            return false;
        else
        {
            let sub_category = $( "#fund_sub_category_cat option:selected" ).text();
            let url = '/get/current/value';
            let amount = $( "#invested_amount_cat" ).val();
            let date = $( "#investment_date_cat" ).val();

            current_value(url, sub_category, amount, date);
        }
    });

    $(".submit-data-code").click(function( event ) {
        let count = 0;

        $(".required_code").each(function(){
            if ($(this).val()==null || $(this).val()=="" )
            {
                $(this).css('border', '1px solid #ff0000');
                count++;
            }
            else
            {
                $(this).css('border', '1px solid #ced4da');
            }
        })
        if (count!=0)
            return false;
        else
        {
            let sub_category = $( "#fund_category_code option:selected" ).text();
            let url = '/get/current/value';
            let amount = $( "#invested_amount_code" ).val();
            let date = $( "#investment_date_code" ).val();

            current_value(url, sub_category, amount, date);
        }            
    });        
})
