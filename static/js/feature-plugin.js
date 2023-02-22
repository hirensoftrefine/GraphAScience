$(document).ready(function () {


        $("#file1").change(function(){
                var file1 = document.querySelector('#file1');
                /*console.log(file1.files);*/
                document.getElementById("#file").value = '';
                var file2 = document.querySelector('#file');
                file2.files = file1.files;
        });


        var drift_status = 'drift';

        var today = new Date();

        var date = ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2) + '-' + today.getFullYear();

        $('#date').val(date);

        /* Toogle Button Code*/

        $("#drift-X").unbind().change(function () {


                if ($(event.target).prop('checked')) {

                        $('.graph-section-text').hide();
                        $("#drift-text-X").fadeIn();
                        $(".slider").addClass('male');

                        $('#X_Image').remove();
                        cutoff = $('#drift-limit').val();
                        
                        if (!cutoff) {
                        
                                cutoff = 400;
        
                        }
                        else {
                                cutoff = cutoff;
                        }
                        fd.append('cutoff', cutoff);
                        $.ajax({
                                url: '/inversegraph',
                                cache: false,
                                type: 'POST',
                                data: fd,
                                contentType: false,
                                processData: false,
                                success: function (result) {
                                      
                                        $('.x-graph').html(result);
                                        $('.graph-section').css('background-color', 'white');
                                        $('.x-graph').show();
                                        $('#drift-X').prop('checked', true);
                                        $("#drift-text-X").text("");
                                        $("#drift-text-X").text("Inverse");

                                },
                                error: function (xhr, status, error) {
                                }
                        });



                }
                else {

                        $("#drift-text-X").text("Drift");
                        $("#drift-text-X").fadeIn();
                        $(".slider").removeClass('male');


                        $('#X_Image').remove();

                        if (!cutoff) {
        
                                cutoff = 1 / 400;
                        }
                        else {
                                cutoff = 1 / cutoff;
                        }

                        fd.append('cutoff', cutoff);

                        $.ajax({
                                url: '/graph',
                                cache: false,
                                type: 'POST',
                                data: fd,
                                contentType: false,
                                processData: false,
                                success: function (result) {
                                
                                        $('.x-graph').html(result);
                                        $('.graph-section').css('background-color', 'white');
                                        $('.x-graph').show();
                                        $('.graph-section-text').hide();


                                        $('#drift-X').prop('checked', false);
                                        $("#drift-text-X").text("Drift");
                                },
                                error: function (xhr, status, error) {
                                }
                        });


                }
        });

        $("#drift-Y").unbind().change(function () {

        
                if ($(event.target).prop('checked')) {

                        $('.graph-section-text').hide();
                        $("#drift-text-Y").text("Inverse");
                        $("#drift-text-Y").fadeIn();
                        $(".slider").addClass('male');


                        $('#Y_Image').remove();
                        cutoff = $('#drift-limit').val();
                        if (!cutoff) {
                                cutoff = 400;
                        }
                        else {
                                cutoff = cutoff;
                        }

                        fd.append('cutoff', cutoff);

                        $.ajax({
                                url: '/yinversegraph',
                                cache: false,
                                type: 'POST',
                                data: fd,
                                contentType: false,
                                processData: false,
                                success: function (result) {
                                        
                                        $('.y-graph').html(result);
                                        $('.y-graph').show();
                                        $('.graph-section-text').hide();

                                        $('#drift-Y').prop('checked', true);
                                        $("#drift-text-Y").text("Inverse");


                                },
                                error: function (xhr, status, error) {
                                }
                        });

                }
                else {

                        $("#drift-text-Y").text("Drift");
                        $("#drift-text-Y").fadeIn();
                        $(".slider").removeClass('male');

                        $('#Y_Image').remove();
                        cutoff = $('#drift-limit').val();
                        if (!cutoff) {
                                cutoff = 1 / 400;
                        }
                        else {
                                cutoff = 1 / cutoff;
                        }

                        fd.append('cutoff', cutoff);

                        $.ajax({
                                url: '/ygraph',
                                cache: false,
                                type: 'POST',
                                data: fd,
                                contentType: false,
                                processData: false,
                                success: function (result) {
                                

                                        $('.y-graph').html(result);
                                        $('.y-graph').show();
                                        $('.graph-section-text').hide();

                                        $('#drift-Y').prop('checked', false);
                                        $("#drift-text-Y").text("Drift");


                                },
                                error: function (xhr, status, error) {
                                }
                        });

                }
        });


        var fd = new FormData();
        var cutoff = $('#drift-limit').val();
        fd.append('file1', $('input[type=file]')[0].files[0]);
        var favorite = [];

        $.each($("input[name='cdemos']:checked"), function () {
                favorite.push($(this).val());
        });

        fd.append('cdemos[]', favorite);

        fd.append('drift-status', drift_status);

        
        $('#save').unbind().click(function () {

                var form = $('#fileUploadForm')[0]
                var fd = new FormData(form)
                $.ajax({
                        url: '/regions',
                        cache: false,
                        type: 'POST',
                        data: fd,
                        contentType: false,
                        processData: false,
                        success: function (result,status) {

                
                                if (result.length == undefined) {
                                        $('#checkboxes').html('');
                                        $('#checkboxes').show();
                                        result['combos'].forEach(function (data) {
                                                $('#checkboxes').append('<input type="checkbox" name="cdemos" class="casecombos" style="margin-right: 9px" value="' + data[0] + '">' + data[0] + '<br />');
                                                $('#graph').show();
                                                $('#save-pdf').show();
                                                $("#proj-file-location").val(result['file-location']);
                                                $('#version').val(result['version']);
                                                $('.checkbox-control').show();
                                                $('.drift-limit').show();
                                                $('.etab-version').show();

                                        });

                                }
                                else
                                {
                                        
                                }


                        },
                        error: function (xhr, status, error) {
                                //console.log("Recorded inserted Sucessfully");
                        }
                });



        });

        $("#selectall").click(function () {
                $(".casecombos").prop('checked', $(this).prop('checked'));
                $("#clearall").prop('checked', false);
        });

        $("#clearall").click(function () {
                $(".casecombos").prop('checked', false);
                $("#selectall").prop('checked', false);
        });

        $('#graph').unbind().click(function (e) {

                var fd = new FormData();
                var cutoff = $('#drift-limit').val();
                fd.append('file1', $('input[type=file]')[0].files[0]);
                var favorite = [];
                if (!cutoff) {
                        cutoff = 1 / 400;
                }
                else {
                        cutoff = 1 / cutoff;
                }
                $.each($("input[name='cdemos']:checked"), function () {
                        favorite.push($(this).val());
                });

                fd.append('cdemos[]', favorite);
                fd.append('cutoff', cutoff);
                fd.append('drift-status', drift_status);

                $.ajax({
                        url: '/graph',
                        cache: false,
                        type: 'POST',
                        data: fd,
                        contentType: false,
                        processData: false,
                        success: function (result) {
                
                                $('#example').show();
                                $('.x-graph').html(result);
                                $("#drift-text-X").text("Drift");
                                /*$("#drift-text-X").text("");*/
                               
                                /**/
                                
                                $('#example').circlize({

                                                 radius: 100,
                                                /*perc: 60,*/
                                                percentage: 100,
                                                usePercentage: true,
                                                /*background: "red",*/
                                                /*foreground: "red",*/
                                                stroke: 10,
                                                /*duration: 2000,*/ 
                                                gradientColors: ["#274365", "#274365", "#274365"]
                                });

                                setTimeout(function () {

                                        $('#example').html(' ');
                                        $('#example').hide();
                                        /*c.remove();*/

                                }, 800);


                                $('.graph-section').css('background-color', 'white');
                                $('.x-graph').show();
                                $('.graph-section-text').hide();

                                $('.highcharts-button').css('transform', 'translate(173,10)');


                        },
                        error: function (xhr, status, error) {
                                //console.log("Get Graph Unsuccessfull");
                        }
                       

                });
                $('.highcharts-button').addClass('hs');

                $.ajax({
                        url: '/ygraph',
                        cache: false,
                        type: 'POST',
                        data: fd,
                        contentType: false,
                        processData: false,
                        success: function (result) {
                                //console.log("Get Graph Successfully");

                                $('#example-1').show();
                                $('.y-graph').html(result);
                                $("#drift-text-Y").text("Drift");
                                setTimeout(function () {

                                        $('#example-1').circlize({
                                                radius: 100,
                                                percentage: 100,
                                                usePercentage: true,
                                                /*background: "red",*/
                                                /*foreground: "red",*/
                                                stroke: 10,
                                                /*duration: 2000,*/
                                                gradientColors: ["#274365", "#274365", "#274365"]
                                        });



                                }, 1000);

                                setTimeout(function () {

                                        $('#example-1').html(' ');
                                        $('#example-1').hide();
                                        /*c.remove();*/

                                }, 2000);

                                $('.y-graph').show();
                                $('.graph-section-text').hide();
                        },
                        error: function (xhr, status, error) {
                                //console.log("Get Graph Unsuccessfull");
                        }
                });

                e.stopPropagation();


        });

        $("#reset-data").unbind().click(function () {
                //console.log('Reset Clicked');
                $('#fileUploadForm')[0].reset();

                $('#checkboxes').html('');
                $('#checkboxes').hide();
                $('.checkbox-control').hide();
                $('#graph').hide();
                $('#save-pdf').hide();
                $('.y-graph').hide();
                $('.x-graph').hide();
                $('.graph-section-text').show();
                $('.etab-version').hide();
                $('.drift-limit').hide();
                $("#date").val(date);

        });

});

