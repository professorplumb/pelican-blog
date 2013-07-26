Graphing Calculator, Part 3
###########################

:tags: d3.js, svg, graphing-calculator
:category: code
:author: Eric Plumb
:summary: Simple plotting of mathematical functions using d3.js, part 3

Welcome!  This is the third and final installation of my exploration of `d3.js
<http://d3js.org>`_ by creating a small graphing calculator app.  (If you missed `part 1
<|filename|2013-07-07_graphing-calculator-part-1.rst>`_
or `part 2 <|filename|2013-07-09_graphing-calculator-part-2.rst>`_, go on back and check them out; I'll wait here.)

We won't actually spend too much time on d3 in this lesson: I will spend most of the time making the previous weeks'
code more modular.  However, I will introduce an exciting new JS library, so stay tuned.

A Little Less Conversation
==========================

The previous weeks' demos (`week 1 <|filename|../demo-examples/gc-demo1.html>`_ and `week 2
<|filename|../demo-examples/gc-demo2.html>`_) used an immediately-invoked ``<script>`` tag in the ``body`` of the
document.  This was OK because I cared more about the output than making the calculator reusable.  But if we want to
be able to change the dimensions of the graph, or display different functions, we'll first have to refactor this into a
reusable function.

I am assuming that you are more or less capable with Javascript :html_entity:`mdash` likely more so than I :html_entity:`mdash` and will just display the
differences from week 2's example here, rather than posting the entire code.  This function goes inside a ``<script>``
block in the ``<head>`` element of the page.

.. code-block:: javascript

    function draw(el_name, _bounds, _fx) {
        var default_bounds = { x_min: -10, x_max: 10, y_min: -10, y_max: 10, w: 500, h: 250},
            plot_bounds = _bounds || {},
            fx = _fx || Math.sin;

        // copy defaults to plot_bounds without overwriting
        for (var key in default_bounds) {
            if (default_bounds.hasOwnProperty(key) && !plot_bounds.hasOwnProperty(key)) {
                plot_bounds[key] = default_bounds[key]
            }
        }

        var svg = d3.select(el_name).append('svg:svg'),
            w = plot_bounds.w || default_bounds.w,
            h = plot_bounds.h || default_bounds.h;
        svg.attr('width', w).attr('height', h);

        var plot_data = [];
        var dx = plot_bounds.dx || 1;
        for (var i=plot_bounds.x_min; i<=plot_bounds.x_max; i+= dx) {
            plot_data.push([i, fx(i)]);
        }

        var padding = 20,
                xMax = d3.max(plot_data, function(d) { return d[0]; }),
                yMax = d3.max(plot_data, function(d) { return d[1]; }),
                xScale = d3.scale.linear()
                        .domain([plot_bounds.x_min, plot_bounds.x_max])
                        .range([padding, w - padding]),
                yScale = d3.scale.linear()
                        .domain([plot_bounds.y_min, plot_bounds.y_max])
                        .range([h - padding, padding]),
        ...
    }

As you can see, I've allowed the user to customize the DOM element to which the graph will be appended (``el_name``),
the bounds of the graph (``_bounds``, which gets some defaults if the user chooses not to include them), and the function
which is plotted (``_fx``, which is also assigned a default of ``Math.sin`` if not provided.)

Let's invoke this function using the defaults and see what we get:

.. code-block:: html

    <body onload="draw('body');">

.. raw:: html

    <style type="text/css">
        svg .axis path, svg .axis line {
            fill: none;
            stroke: black;
            shape-rendering: crispEdges;
        }
        svg .axis text {
            font-family: sans-serif;
            font-size: 11px;
            text-anchor: middle;
        }
    </style>

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-10</text></g><g class="tick major" transform="translate(66,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-8</text></g><g class="tick major" transform="translate(112,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-6</text></g><g class="tick major" transform="translate(158.00000000000003,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-4</text></g><g class="tick major" transform="translate(204,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-2</text></g><g class="tick major" transform="translate(250,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(296.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(342.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(388,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(434,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(20,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-10</text></g><g class="tick major" transform="translate(0,209)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-8</text></g><g class="tick major" transform="translate(0,188)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-6</text></g><g class="tick major" transform="translate(0,167)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-4</text></g><g class="tick major" transform="translate(0,146)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-2</text></g><g class="tick major" transform="translate(0,125)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0</text></g><g class="tick major" transform="translate(0,103.99999999999999)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">2</text></g><g class="tick major" transform="translate(0,83)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">4</text></g><g class="tick major" transform="translate(0,62)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">6</text></g><g class="tick major" transform="translate(0,41)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">8</text></g><g class="tick major" transform="translate(0,20)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">10</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,119.28777833566161L23.83333333333333,120.96102262889107C27.666666666666664,122.63426692212055,35.33333333333333,125.98075550857949,43,128.66416938422682C50.666666666666664,131.3475832598741,58.33333333333333,133.3679224247098,66,133.7964416232946C73.66666666666667,134.2249608218794,81.33333333333334,133.06166005421332,89,130.8413060007743C96.66666666666667,128.62095194733524,104.33333333333333,125.34354460812325,112,122.51570057970488C119.66666666666666,119.68785655128652,127.33333333333333,117.30957583366177,135,116.47414858872102C142.66666666666669,115.63872134378028,150.33333333333334,116.3461475715235,158,118.27122506628876C165.66666666666669,120.19630256105401,173.33333333333337,123.3390313228413,181.00000000000003,126.25470618657512C188.66666666666669,129.17038105030895,196.33333333333334,131.8590020159893,204,133.08461622529833C211.66666666666666,134.31023043460738,219.33333333333331,134.07283788754515,226.99999999999997,132.48156739060022C234.66666666666663,130.89029689365526,242.33333333333331,127.94514844682763,250,125C257.66666666666663,122.05485155317236,265.3333333333333,119.10970310634471,273,117.51843260939977C280.6666666666667,115.92716211245482,288.33333333333337,115.68976956539258,296.00000000000006,116.91538377470164C303.6666666666667,118.14099798401068,311.33333333333337,120.82961894969102,319,123.74529381342484C326.6666666666667,126.66096867715866,334.33333333333337,129.80369743894596,342,131.7287749337112C349.6666666666667,133.65385242847645,357.3333333333333,134.3612786562197,365,133.52585141127895C372.66666666666663,132.69042416633818,380.33333333333326,130.31214344871344,387.99999999999994,127.48429942029507C395.66666666666663,124.6564553918767,403.3333333333333,121.3790480526647,410.99999999999994,119.15869399922566C418.66666666666663,116.93833994578662,426.3333333333333,115.77503917812055,434,116.20355837670536C441.66666666666663,116.63207757529017,449.33333333333337,118.65241674012586,453.1666666666667,119.6625863225437L457.00000000000006,120.67275590496155" style="stroke: #06789b; fill: none;"></path></svg>

Very nice!  Let's zoom in a little bit:

.. code-block:: html

    <body onload="draw('body', {y_min: -1.5, y_max: +1.5});">

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-10</text></g><g class="tick major" transform="translate(66,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-8</text></g><g class="tick major" transform="translate(112,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-6</text></g><g class="tick major" transform="translate(158.00000000000003,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-4</text></g><g class="tick major" transform="translate(204,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-2</text></g><g class="tick major" transform="translate(250,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(296.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(342.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(388,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(434,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(20,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-1.5</text></g><g class="tick major" transform="translate(0,195)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-1.0</text></g><g class="tick major" transform="translate(0,160)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">-0.5</text></g><g class="tick major" transform="translate(0,125)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.0</text></g><g class="tick major" transform="translate(0,90)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.5</text></g><g class="tick major" transform="translate(0,55.00000000000003)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.0</text></g><g class="tick major" transform="translate(0,20)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.5</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,86.91852223774416L23.83333333333333,98.07348419260728C27.666666666666664,109.22844614747041,35.33333333333333,131.53837005719666,43,149.42779589484542C50.666666666666664,167.3172217324942,58.33333333333333,180.78614949806547,66,183.6429441552975C73.66666666666667,186.49973881252956,81.33333333333334,178.74440036142238,89,163.94204000516214C96.66666666666667,149.13967964890188,104.33333333333333,127.29029738748854,112,108.43800386469938C119.66666666666666,89.58571034191023,127.33333333333333,73.73050555774526,135,68.16099059147356C142.66666666666669,62.59147562520187,150.33333333333334,67.30765047682344,158,80.14150044192517C165.66666666666669,92.97535040702691,173.33333333333337,113.9268754856088,181.00000000000003,133.36470791050093C188.66666666666669,152.80254033539305,196.33333333333334,170.72668010659538,204,178.89744150198905C211.66666666666666,187.06820289738272,219.33333333333331,185.48558591696775,226.99999999999997,174.8771159373348C234.66666666666663,164.26864595770184,242.33333333333331,144.63432297885092,250,124.99999999999999C257.66666666666663,105.36567702114908,265.3333333333333,85.73135404229816,273,75.12288406266521C280.6666666666667,64.51441408303225,288.33333333333337,62.93179710261727,296.00000000000006,71.10255849801095C303.6666666666667,79.27331989340462,311.33333333333337,97.19745966460697,319,116.63529208949909C326.6666666666667,136.0731245143912,334.33333333333337,157.0246495929731,342,169.8584995580748C349.6666666666667,182.69234952317655,357.3333333333333,187.4085243747981,365,181.83900940852644C372.66666666666663,176.2694944422547,380.33333333333326,160.41428965808976,387.99999999999994,141.5619961353006C395.66666666666663,122.70970261251145,403.3333333333333,100.86032035109811,410.99999999999994,86.05795999483786C418.66666666666663,71.25559963857759,426.3333333333333,63.50026118747043,434,66.35705584470247C441.66666666666663,69.21385050193452,449.33333333333337,82.68277826750577,453.1666666666667,89.4172421502914L457.00000000000006,96.15170603307703" style="stroke: #06789b; fill: none;"></path></svg>

See how easy that was?  We can move the "window" of the graph around as we will, and even change the width and height
of the ``svg`` element using the ``w`` and ``h`` parameters.

Putting On The Fancy Shoes
==========================

We have a couple aesthetic tweaks to make before we handle customization.  First, see how the path goes
all the way to the left edge of the graph but stops short of the right edge?  This is a `fencepost error
<http://en.wikipedia.org/wiki/Off-by-one_error#Fencepost_error>`_ and easy to fix with a :html_entity:`8804` instead of
:html_entity:`lt`:

.. code-block:: javascript

    for (var i=plot_bounds.x_min; i<=plot_bounds.x_max; i+= dx) {
        ...

Second, we should do something about the axes :html_entity:`mdash` it makes little sense for them to stay on the left
and bottom.  We could just move them to the middle of the graph:

.. code-block:: javascript

    svg.append('svg:g')
            .attr('class', "axis")
            .attr('transform', "translate(0," + (h / 2) + ")")  // only changed this line
            .call(xAxis);
    svg.append('svg:g')
            .attr('class', "axis")
            .attr('transform', "translate(" + (w / 2) + ",0)")  // and this one
            .call(yAxis);

but that would be somewhat naive:

.. code-block:: html

    <body onload="draw('body', {y_min: -0, y_max: +1.5});">

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,125)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-10</text></g><g class="tick major" transform="translate(66,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-8</text></g><g class="tick major" transform="translate(112,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-6</text></g><g class="tick major" transform="translate(158.00000000000003,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-4</text></g><g class="tick major" transform="translate(204,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-2</text></g><g class="tick major" transform="translate(250,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(296.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(342.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(388,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(434,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(250,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.0</text></g><g class="tick major" transform="translate(0,202)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.2</text></g><g class="tick major" transform="translate(0,174)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.4</text></g><g class="tick major" transform="translate(0,146)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.6</text></g><g class="tick major" transform="translate(0,118)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.8</text></g><g class="tick major" transform="translate(0,90)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.0</text></g><g class="tick major" transform="translate(0,62)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.2</text></g><g class="tick major" transform="translate(0,34.00000000000003)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.4</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,153.83704447548826L23.83333333333333,176.1469683852145C27.666666666666664,198.45689229494081,35.33333333333333,243.07674011439337,43,278.8555917896909C50.666666666666664,314.6344434649884,58.33333333333333,341.57229899613094,66,347.28588831059506C73.66666666666667,352.9994776250591,81.33333333333334,337.48880072284476,89,307.8840800103242C96.66666666666667,278.27935929780375,104.33333333333333,234.58059477497707,112,196.87600772939876C119.66666666666666,159.17142068382046,127.33333333333333,127.46101111549054,135,116.32198118294716C142.66666666666669,105.18295125040376,150.33333333333334,114.6153009536469,158,140.28300088385038C165.66666666666669,165.95070081405382,173.33333333333337,207.8537509712176,181.00000000000003,246.72941582100182C188.66666666666669,285.60508067078604,196.33333333333334,321.45336021319076,204,337.7948830039781C211.66666666666666,354.13640579476544,219.33333333333331,350.97117183393544,226.99999999999997,329.75423187466953C234.66666666666663,308.53729191540367,242.33333333333331,269.2686459577018,250,230C257.66666666666663,190.73135404229814,265.3333333333333,151.46270808459633,273,130.24576812533041C280.6666666666667,109.02882816606451,288.33333333333337,105.86359420523453,296.00000000000006,122.20511699602189C303.6666666666667,138.54663978680924,311.33333333333337,174.3949193292139,319,213.27058417899815C326.6666666666667,252.14624902878236,334.33333333333337,294.04929918594615,342,319.7169991161496C349.6666666666667,345.3846990463531,357.3333333333333,354.8170487495962,365,343.6780188170528C372.66666666666663,332.5389888845094,380.33333333333326,300.8285793161795,387.99999999999994,263.1239922706012C395.66666666666663,225.4194052250229,403.3333333333333,181.72064070219622,410.99999999999994,152.11591998967572C418.66666666666663,122.51119927715521,426.3333333333333,107.00052237494089,434,112.71411168940497C441.66666666666663,118.42770100386906,449.33333333333337,145.36555653501156,457,181.1444082103091C464.6666666666667,216.92325988560663,472.33333333333337,261.5431077050592,476.1666666666667,283.85303161478544L480,306.16295552451174" style="stroke: #06789b; fill: none;"></path></svg>

As you can see, the x-axis stays in the middle, crossing y at +0.75.  We would rather have the axes cross at (0, 0)
regardless of whether that's in the middle.  This requires calculating where it is in the x and y domains and finding
the location on the graph which corresponds to that fraction of the width or height.  Fortunately, that's exactly what
the scale functions we created as part of `Scott Murray's tutorial <http://alignedleft.com/tutorials/d3/>`_ are designed
to do.

.. code-block:: javascript

    svg.append('svg:g')
            .attr('class', "axis")
            .attr('transform', "translate(0," + yScale(0) + ")")
            .call(xAxis);
    svg.append('svg:g')
            .attr('class', "axis")
            .attr('transform', "translate(" + xScale(0) + ",0)")
            .call(yAxis);

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-10</text></g><g class="tick major" transform="translate(66,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-8</text></g><g class="tick major" transform="translate(112,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-6</text></g><g class="tick major" transform="translate(158.00000000000003,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-4</text></g><g class="tick major" transform="translate(204,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-2</text></g><g class="tick major" transform="translate(250,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(296.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(342.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(388,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(434,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(250,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.0</text></g><g class="tick major" transform="translate(0,202)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.2</text></g><g class="tick major" transform="translate(0,174)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.4</text></g><g class="tick major" transform="translate(0,146)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.6</text></g><g class="tick major" transform="translate(0,118)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.8</text></g><g class="tick major" transform="translate(0,90)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.0</text></g><g class="tick major" transform="translate(0,62)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.2</text></g><g class="tick major" transform="translate(0,34.00000000000003)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.4</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,153.83704447548826L23.83333333333333,176.1469683852145C27.666666666666664,198.45689229494081,35.33333333333333,243.07674011439337,43,278.8555917896909C50.666666666666664,314.6344434649884,58.33333333333333,341.57229899613094,66,347.28588831059506C73.66666666666667,352.9994776250591,81.33333333333334,337.48880072284476,89,307.8840800103242C96.66666666666667,278.27935929780375,104.33333333333333,234.58059477497707,112,196.87600772939876C119.66666666666666,159.17142068382046,127.33333333333333,127.46101111549054,135,116.32198118294716C142.66666666666669,105.18295125040376,150.33333333333334,114.6153009536469,158,140.28300088385038C165.66666666666669,165.95070081405382,173.33333333333337,207.8537509712176,181.00000000000003,246.72941582100182C188.66666666666669,285.60508067078604,196.33333333333334,321.45336021319076,204,337.7948830039781C211.66666666666666,354.13640579476544,219.33333333333331,350.97117183393544,226.99999999999997,329.75423187466953C234.66666666666663,308.53729191540367,242.33333333333331,269.2686459577018,250,230C257.66666666666663,190.73135404229814,265.3333333333333,151.46270808459633,273,130.24576812533041C280.6666666666667,109.02882816606451,288.33333333333337,105.86359420523453,296.00000000000006,122.20511699602189C303.6666666666667,138.54663978680924,311.33333333333337,174.3949193292139,319,213.27058417899815C326.6666666666667,252.14624902878236,334.33333333333337,294.04929918594615,342,319.7169991161496C349.6666666666667,345.3846990463531,357.3333333333333,354.8170487495962,365,343.6780188170528C372.66666666666663,332.5389888845094,380.33333333333326,300.8285793161795,387.99999999999994,263.1239922706012C395.66666666666663,225.4194052250229,403.3333333333333,181.72064070219622,410.99999999999994,152.11591998967572C418.66666666666663,122.51119927715521,426.3333333333333,107.00052237494089,434,112.71411168940497C441.66666666666663,118.42770100386906,449.33333333333337,145.36555653501156,457,181.1444082103091C464.6666666666667,216.92325988560663,472.33333333333337,261.5431077050592,476.1666666666667,283.85303161478544L480,306.16295552451174" style="stroke: #06789b; fill: none;"></path></svg>

(Note that the x-axis is translated along the y-scale, and the y-axis along the x-scale.  Note also that I'm mixing
camelCase and under_score style variable names in my Javascript.  Don't do this at home, kids: pick one and stick with
it.)

One last improvement: let's get rid of the zero-value tick labels as they're just cluttering things up.

This turns out
to be a wee bit hairy: it looks from the `d3 axis API <https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-tickValues>`_
as if calling ``axis.tickValues()`` without any arguments will return the current tick values, which we could filter
for nonzero values.  However, if no explicit tick values have been set, it returns ``null`` which means to use the scale's
tick generator.  In the `d3 Scale API documentation <https://github.com/mbostock/d3/wiki/Quantitative-Scales#wiki-linear_ticks>`_
we find that ``scale.ticks(count)`` will generate an array of ticks if given a number.  Where do we get that number,
though?  Back to the `axis documentation <https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-ticks>`_ and it's simply
``axis.ticks()``!

So our tick value generation looks like this:

.. code-block:: javascript

    xAxis.tickValues(xScale.ticks(xAxis.ticks()).filter(function(x) { return x !== 0; }));
    yAxis.tickValues(yScale.ticks(yAxis.ticks()).filter(function(x) { return x !== 0; }));

Got that?  We're calling the ``ticks()`` method on the axis to get the number of ticks desired.  (We could customize
this if we want but we're passing on the default of 10.)  We then call the ``ticks()`` method on the scale to subdivide
the axis into that many sections and return the locations of the "fenceposts".  Finally, we filter this array of ticks
to remove zero, and pass the whole array to the axis's ``tickValues`` function. [1]_ [2]_

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-10</text></g><g class="tick major" transform="translate(66,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-8</text></g><g class="tick major" transform="translate(112,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-6</text></g><g class="tick major" transform="translate(158.00000000000003,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-4</text></g><g class="tick major" transform="translate(204,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">-2</text></g><g class="tick major" transform="translate(296.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(342.00000000000006,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(388,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(434,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(250,0)"><g class="tick major" transform="translate(0,202)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.2</text></g><g class="tick major" transform="translate(0,174)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.4</text></g><g class="tick major" transform="translate(0,146)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.6</text></g><g class="tick major" transform="translate(0,118)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.8</text></g><g class="tick major" transform="translate(0,90)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.0</text></g><g class="tick major" transform="translate(0,62)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.2</text></g><g class="tick major" transform="translate(0,34.00000000000003)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.4</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,153.83704447548826L23.83333333333333,176.1469683852145C27.666666666666664,198.45689229494081,35.33333333333333,243.07674011439337,43,278.8555917896909C50.666666666666664,314.6344434649884,58.33333333333333,341.57229899613094,66,347.28588831059506C73.66666666666667,352.9994776250591,81.33333333333334,337.48880072284476,89,307.8840800103242C96.66666666666667,278.27935929780375,104.33333333333333,234.58059477497707,112,196.87600772939876C119.66666666666666,159.17142068382046,127.33333333333333,127.46101111549054,135,116.32198118294716C142.66666666666669,105.18295125040376,150.33333333333334,114.6153009536469,158,140.28300088385038C165.66666666666669,165.95070081405382,173.33333333333337,207.8537509712176,181.00000000000003,246.72941582100182C188.66666666666669,285.60508067078604,196.33333333333334,321.45336021319076,204,337.7948830039781C211.66666666666666,354.13640579476544,219.33333333333331,350.97117183393544,226.99999999999997,329.75423187466953C234.66666666666663,308.53729191540367,242.33333333333331,269.2686459577018,250,230C257.66666666666663,190.73135404229814,265.3333333333333,151.46270808459633,273,130.24576812533041C280.6666666666667,109.02882816606451,288.33333333333337,105.86359420523453,296.00000000000006,122.20511699602189C303.6666666666667,138.54663978680924,311.33333333333337,174.3949193292139,319,213.27058417899815C326.6666666666667,252.14624902878236,334.33333333333337,294.04929918594615,342,319.7169991161496C349.6666666666667,345.3846990463531,357.3333333333333,354.8170487495962,365,343.6780188170528C372.66666666666663,332.5389888845094,380.33333333333326,300.8285793161795,387.99999999999994,263.1239922706012C395.66666666666663,225.4194052250229,403.3333333333333,181.72064070219622,410.99999999999994,152.11591998967572C418.66666666666663,122.51119927715521,426.3333333333333,107.00052237494089,434,112.71411168940497C441.66666666666663,118.42770100386906,449.33333333333337,145.36555653501156,457,181.1444082103091C464.6666666666667,216.92325988560663,472.33333333333337,261.5431077050592,476.1666666666667,283.85303161478544L480,306.16295552451174" style="stroke: #06789b; fill: none;"></path></svg>

The Final Function
==================

Now we're finally ready to allow our users to graph whatever they like, wherever they like.  We will set up a page with
inputs for the minimum and maximum x and y, the width and height of the graph, and the function to be graphed, passing
those to our ``draw()`` function.  This is straightforward Javascript and HTML so you can view the source of the
`demo <|filename|../demo-examples/gc-demo3.html>`_ instead of cluttering up this space.

There is one large exception, however: the function to be graphed.  How do we let the user enter this themselves?  We
could have them enter Javascript code and ``eval()`` it, but I'd prefer to be able to use pure mathematical notation.
[3]_  Fortunately, there's `math.js <http://mathjs.org/>`_ which contains a fully-featured function parser.  Here's how
it works:

.. code-block:: javascript

        function validate_and_draw(form) {
            ... // snip code for validating window bounds and display size
            var func;
            try {
                func = math.eval("function f(x) = " + form.elements['func'].value);
            } catch (err) {
                alert("Error: " + err.message);
                return false;
            }

            document.getElementById('graph').innerHTML = "";
            draw('#graph', bounds, func);
            return false;
        }

It's that simple!  We catch and display any errors returned by ``math.eval`` (for example, if the user tries to define
a function of y), and it works exactly like you would expect.

Wrapping Up
===========

You can see this calculator in action at `gc-demo3.html
<|filename|../demo-examples/gc-demo3.html>`_.  If I turn this into an actual app, there are plenty of fixes to make (try
graphing tan(x), for example) and tons of features I'd like to add: think panning, zooming, multiple functions, etc.
:html_entity:`mdash` but this will do for now.

Hope you've enjoyed this three-part series as much as I have!  The final project is `on Github
<https://github.com/professorplumb/graphing-calculator-demo>`_ so feel free to clone or fork.

Footnotes
---------

.. [1] As a dog owner, saying "ticks" so many times makes me think of something else entirely.  I will resolve to think
       of `this <http://www.youtube.com/watch?v=kdeci6W3HyU>`_ instead.

.. [2] I am far from a Javascript guru, but it would seem to make sense to me, in the chained function calls for the
       d3 axis/scale/etc. objects, to bind ``this`` to the object so you could do ``xAxis.tickValues(xScale.ticks(this.ticks()))``.
       However, this doesn't seem to work :html_entity:`mdash` ``this`` is bound to the global object.  Anyone know why
       d3 chose to do it this way?

.. [3] Also, it runs against every grain in my body to use ``eval()`` on user-supplied input, even if it's only on the
       client and can't be used for XSS.