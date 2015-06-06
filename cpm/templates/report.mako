<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Critical Path Method - Results in HTML Report</title>
        <script src="https://code.jquery.com/jquery-latest.min.js"></script>
        <script src="http://unslider.com/unslider.min.js"></script>
        <style type="text/css">
            .graphs { position: relative; overflow: auto;}
            .graphs li { list-style: none; }
            .graphs ul li { float: left; }
        </style>
        <script>
        $(function() {
            $('.graphs').unslider();
        });
        </script>
    </head>
    <body>
        <div class="results">
            ${results}
        </div>
        <div class="graphs">
            <ul>
            % for image in images:
                <li><img src="${image}" width="500" height="500"></li>
            % endfor
            </ul>
        </div>
    </body>
</html>