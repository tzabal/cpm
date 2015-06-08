<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Critical Path Method | Results in HTML Report</title>
        <style type="text/css">
            #results_table table {border: 1px solid black; border-collapse: collapse; text-align: center;}
            #results_table table th {padding: 0.2em 1em; border-right: 1px solid black; border-bottom: 1px solid black}
            #results_table table td {padding: 0.1em 1em; border-right: 1px solid black;}
        </style>
    </head>
    <body>
        <div id="container">
            <h1>Critical Path Method</h1>
            <div id="results_table">
                <h2>Results</h2>
                ${results_table}
            </div>
            <div id="images">
                <h2>Network transformations throughout CPM</h2>
                % for iteration, image in enumerate(images):
                <p>Network in its ${iteration} iteration:</p>
                <img src="${image}" alt="network">
                <hr>
                % endfor
            </div>
        </div>
    </body>
</html>
