Graphing Calculator, Part 2
###########################

:tags: d3.js, svg, graphing-calculator
:category: code
:author: Eric Plumb
:summary: Simple plotting of mathematical functions using d3.js, part 2

Welcome!  This is part 2 of my documentation of writing a simple graphing calculator/function plotter using `d3.js
<http://d3js.org>`_ (see `part 1 <|filename|2013-07-07_graphing-calculator-part-1.rst>`_ if you missed it).  Today I
will replace the line segments I used for plotting with the more involved (and actually easier to use, as you will see)
SVG ``path`` element.  Let's get started!

Paths To Success
================

The SVG ``path`` element is different from the other elements like ``circle`` and ``line`` we've seen so far.  Instead
of adding a discrete circle or line to the graph for each datapoint, you add a single element which comprises all the
datapoints, and whose components are described in a graphical language similar to `Logo
<http://en.wikipedia.org/wiki/Logo_(programming_language)>`_.  For example:

.. code-block:: html

    <svg width="100" height="100">
        <path d=" M 25 25
             L 25 75
             L 75 75
             L 75 25
             L 25 25"
             stroke="red" fill="none" />
    </svg>

produces:

.. raw:: html

    <svg width="100" height="100">
        <path d=" M 25 25
             L 25 75
             L 75 75
             L 75 25
             L 25 25"
             stroke="red" fill="none" />
    </svg>

Don't worry about what ``M`` and ``L`` mean for now - these SVG ``path`` mini-language commands are abstracted away by
d3. [1]_  Remember what I said above about not having to enter a distinct element for each datapoint in your set?  For
a ``path``, d3 asks for a ``line()`` function which provides each of the points, plus an interpolation style which
tells d3 how to draw lines between the explicitly plotted points.

We will change our previous code:

.. code-block:: javascript

    svg.selectAll('#line_not_in_axis_tick')
            .data(plotdata.slice(0, plotdata.length :html_entity:`mdash` 1))
        .enter()
            .append('svg:line')
            .attr("x1", function(d, i) { return xScale(d[0]); })
            .attr("y1", function(d, i) { return yScale(d[1]); })
            .attr("x2", function(d, i) { return xScale(plotdata[i+1][0]); })
            .attr("y2", function(d, i) { return yScale(plotdata[i+1][1]); })

to the following:

.. code-block:: javascript

    // Line function which returns an X,Y pair for each point in our set, plus an interpolation method
    // (more on the latter later).
    var lineFunction = d3.svg.line()
            .x(function(d) { return xScale(d[0]); })
            .y(function(d) { return yScale(d[1]); })
            .interpolate('linear');

    // This is all we need to do to set up our path!
    svg.append('svg:path')
            .attr('d', lineFunction(plotdata))

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
    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(66.46464646464648,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><g class="tick major" transform="translate(112.92929292929294,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">20</text></g><g class="tick major" transform="translate(159.3939393939394,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">30</text></g><g class="tick major" transform="translate(205.85858585858588,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">40</text></g><g class="tick major" transform="translate(252.32323232323233,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">50</text></g><g class="tick major" transform="translate(298.7878787878788,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">60</text></g><g class="tick major" transform="translate(345.2525252525253,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">70</text></g><g class="tick major" transform="translate(391.71717171717177,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">80</text></g><g class="tick major" transform="translate(438.18181818181824,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">90</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(20,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0</text></g><g class="tick major" transform="translate(0,208.89420587955655)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1</text></g><g class="tick major" transform="translate(0,187.7884117591131)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">2</text></g><g class="tick major" transform="translate(0,166.68261763866963)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">3</text></g><g class="tick major" transform="translate(0,145.57682351822618)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">4</text></g><g class="tick major" transform="translate(0,124.47102939778273)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">5</text></g><g class="tick major" transform="translate(0,103.36523527733928)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">6</text></g><g class="tick major" transform="translate(0,82.25944115689583)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">7</text></g><g class="tick major" transform="translate(0,61.153647036452355)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">8</text></g><g class="tick major" transform="translate(0,40.04785291600891)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">9</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,230L24.646464646464647,208.89420587955655L29.292929292929294,200.15189971021454L33.93939393939394,193.44369224930347L38.58585858585859,187.7884117591131L43.23232323232324,182.80600962757305L47.878787878787875,178.30157378868026L52.52525252525253,174.15931753477741L57.17171717171718,170.30379942042907L61.81818181818182,166.68261763866963L66.46464646464648,163.25761875280853L71.11111111111111,160L75.75757575757575,156.88738449860693L80.40404040404042,153.90197708935474L85.05050505050507,151.0293495255127L89.6969696969697,148.2576108630401L94.34343434343435,145.57682351822618L98.989898989899,142.97858152887147L103.63636363636364,140.4556991306436L108.28282828282829,138.00197630581204L112.92929292929294,135.6120192551461L117.57575757575758,133.28110084091395L122.22222222222223,131.00505063388334L126.86868686868688,128.78016723262903L131.5151515151515,126.60314757736052L136.16161616161617,124.47102939778273L140.80808080808083,122.38114392998698L145.45454545454547,120.33107674791036L150.10101010101013,118.3186350695548L154.74747474747474,116.34182027596158L159.3939393939394,114.39880466173213L164.04040404040404,112.48791164696755L168.6868686868687,110.60759884085815L173.33333333333334,108.7564434701786L177.979797979798,106.93312978118543L182.62626262626264,105.13643809778173L187.27272727272728,103.36523527733928L191.91919191919192,101.6184663519781L196.56565656565658,99.89514718015809L201.21212121212122,98.19435796322196L205.85858585858588,96.51523750561705L210.50505050505052,94.8569781171208L215.15151515151516,93.21882107142477L219.79797979797982,91.60005254861744L224.44444444444446,90L229.09090909090912,88.41802888271914L233.73737373737376,86.85353971924735L238.38383838383842,85.30596544306451L243.03030303030303,83.77476899721384L247.6767676767677,82.25944115689583L252.32323232323233,80.75949855107271L256.969696969697,79.27448186129257L261.61616161616166,77.80395417870949L266.26262626262627,76.347499502641L270.90909090909093,74.90472136604075L275.55555555555554,73.47524157501473L280.20202020202026,72.05869905102546L284.8484848484849,70.65474876574109L289.4949494949495,69.26306075962614L294.14141414141415,67.88331923636551L298.7878787878788,66.51522172608017L303.4343434343435,65.15847831105395L308.0808080808081,63.812810908356056L312.72727272727275,62.47795260433219L317.3737373737374,61.153647036452355L322.020202020202,59.839647818460804L326.6666666666667,58.5357180051775L331.31313131313135,57.2416295936589L335.959595959596,55.95716305774292L340.6060606060606,54.68210691328841L345.2525252525253,53.41625731167045L349.89898989898995,52.15941765931845L354.54545454545456,50.911398261287246L359.1919191919192,49.67201598703042L363.83838383838383,48.44109395670955L368.48484848484856,47.21846124651725L373.13131313131316,46.0039526116241L377.77777777777777,44.79740822547865L382.42424242424244,43.59867343429514L387.0707070707071,42.40759852566231L391.71717171717177,41.22403851029222L396.3636363636364,40.04785291600891L401.01010101010104,38.87890559314826L405.6565656565657,37.717064530605626L410.3030303030303,36.56220168182793L414.949494949495,35.41419280010075L419.59595959595964,34.2729172825311L424.2424242424243,33.138258022170646L428.8888888888889,32.010101267766686L433.5353535353536,30.888336490665267L438.18181818181824,29.772856258425605L442.82828282828285,28.663556114737077L447.4747474747475,27.56033446525808L452.1212121212121,26.463092469024843L456.76767676767685,25.371733935100536L461.41414141414145,24.286165224159475L466.06060606060606,23.206295154721033L470.7070707070707,22.132034913768138L475.3535353535354,21.063297971501754L480,20" style="stroke: #06789b; fill: #06789b;"></path></svg>

Ah, one more thing :html_entity:`mdash` the ``fill`` attribute on a ``path`` element isn't just for show as it is with the ``line`` element!
With a ``path`` it works the way you'd expect :html_entity:`mdash` it closes the path by drawing a line back to the starting point, and
fills in the polygon created thereby.  All we need to do is change

.. code-block:: javascript

    .style('fill', "rgb(6, 120, 155)");

from our previous code to:

.. code-block:: javascript

    .style('fill', "none");

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(66.46464646464648,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">10</text></g><g class="tick major" transform="translate(112.92929292929294,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">20</text></g><g class="tick major" transform="translate(159.3939393939394,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">30</text></g><g class="tick major" transform="translate(205.85858585858588,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">40</text></g><g class="tick major" transform="translate(252.32323232323233,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">50</text></g><g class="tick major" transform="translate(298.7878787878788,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">60</text></g><g class="tick major" transform="translate(345.2525252525253,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">70</text></g><g class="tick major" transform="translate(391.71717171717177,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">80</text></g><g class="tick major" transform="translate(438.18181818181824,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">90</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(20,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0</text></g><g class="tick major" transform="translate(0,208.89420587955655)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1</text></g><g class="tick major" transform="translate(0,187.7884117591131)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">2</text></g><g class="tick major" transform="translate(0,166.68261763866963)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">3</text></g><g class="tick major" transform="translate(0,145.57682351822618)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">4</text></g><g class="tick major" transform="translate(0,124.47102939778273)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">5</text></g><g class="tick major" transform="translate(0,103.36523527733928)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">6</text></g><g class="tick major" transform="translate(0,82.25944115689583)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">7</text></g><g class="tick major" transform="translate(0,61.153647036452355)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">8</text></g><g class="tick major" transform="translate(0,40.04785291600891)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">9</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,230L24.646464646464647,208.89420587955655L29.292929292929294,200.15189971021454L33.93939393939394,193.44369224930347L38.58585858585859,187.7884117591131L43.23232323232324,182.80600962757305L47.878787878787875,178.30157378868026L52.52525252525253,174.15931753477741L57.17171717171718,170.30379942042907L61.81818181818182,166.68261763866963L66.46464646464648,163.25761875280853L71.11111111111111,160L75.75757575757575,156.88738449860693L80.40404040404042,153.90197708935474L85.05050505050507,151.0293495255127L89.6969696969697,148.2576108630401L94.34343434343435,145.57682351822618L98.989898989899,142.97858152887147L103.63636363636364,140.4556991306436L108.28282828282829,138.00197630581204L112.92929292929294,135.6120192551461L117.57575757575758,133.28110084091395L122.22222222222223,131.00505063388334L126.86868686868688,128.78016723262903L131.5151515151515,126.60314757736052L136.16161616161617,124.47102939778273L140.80808080808083,122.38114392998698L145.45454545454547,120.33107674791036L150.10101010101013,118.3186350695548L154.74747474747474,116.34182027596158L159.3939393939394,114.39880466173213L164.04040404040404,112.48791164696755L168.6868686868687,110.60759884085815L173.33333333333334,108.7564434701786L177.979797979798,106.93312978118543L182.62626262626264,105.13643809778173L187.27272727272728,103.36523527733928L191.91919191919192,101.6184663519781L196.56565656565658,99.89514718015809L201.21212121212122,98.19435796322196L205.85858585858588,96.51523750561705L210.50505050505052,94.8569781171208L215.15151515151516,93.21882107142477L219.79797979797982,91.60005254861744L224.44444444444446,90L229.09090909090912,88.41802888271914L233.73737373737376,86.85353971924735L238.38383838383842,85.30596544306451L243.03030303030303,83.77476899721384L247.6767676767677,82.25944115689583L252.32323232323233,80.75949855107271L256.969696969697,79.27448186129257L261.61616161616166,77.80395417870949L266.26262626262627,76.347499502641L270.90909090909093,74.90472136604075L275.55555555555554,73.47524157501473L280.20202020202026,72.05869905102546L284.8484848484849,70.65474876574109L289.4949494949495,69.26306075962614L294.14141414141415,67.88331923636551L298.7878787878788,66.51522172608017L303.4343434343435,65.15847831105395L308.0808080808081,63.812810908356056L312.72727272727275,62.47795260433219L317.3737373737374,61.153647036452355L322.020202020202,59.839647818460804L326.6666666666667,58.5357180051775L331.31313131313135,57.2416295936589L335.959595959596,55.95716305774292L340.6060606060606,54.68210691328841L345.2525252525253,53.41625731167045L349.89898989898995,52.15941765931845L354.54545454545456,50.911398261287246L359.1919191919192,49.67201598703042L363.83838383838383,48.44109395670955L368.48484848484856,47.21846124651725L373.13131313131316,46.0039526116241L377.77777777777777,44.79740822547865L382.42424242424244,43.59867343429514L387.0707070707071,42.40759852566231L391.71717171717177,41.22403851029222L396.3636363636364,40.04785291600891L401.01010101010104,38.87890559314826L405.6565656565657,37.717064530605626L410.3030303030303,36.56220168182793L414.949494949495,35.41419280010075L419.59595959595964,34.2729172825311L424.2424242424243,33.138258022170646L428.8888888888889,32.010101267766686L433.5353535353536,30.888336490665267L438.18181818181824,29.772856258425605L442.82828282828285,28.663556114737077L447.4747474747475,27.56033446525808L452.1212121212121,26.463092469024843L456.76767676767685,25.371733935100536L461.41414141414145,24.286165224159475L466.06060606060606,23.206295154721033L470.7070707070707,22.132034913768138L475.3535353535354,21.063297971501754L480,20" style="stroke: #06789b; fill: none;"></path></svg>

There it is!  Now we have a ``path`` which exactly matches what our previous ``line``-based graph did, and in fewer
lines of code.

Smoothing Things Out
====================

Look closely at the bottom left of the function graph :html_entity:`mdash` there's a "kink" at (1, 1) where the path
segment from (0, 0) to (1, 1) meets the segment from (1, 1) to (2, 1.414).  This is an artifact of the ``'linear'``
interpolation method I chose above.  It's more obvious if we change the function and the viewing window:

.. code-block:: javascript

    var plotfunc = function(x) { return 1 + Math.sin(x); },
            plotdata = [];
    var lowX = 0, highX = 10, dX = 1;

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(71.11111111111111,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">1</text></g><g class="tick major" transform="translate(122.22222222222221,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(173.33333333333331,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">3</text></g><g class="tick major" transform="translate(224.44444444444443,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(275.55555555555554,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">5</text></g><g class="tick major" transform="translate(326.66666666666663,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(377.7777777777777,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">7</text></g><g class="tick major" transform="translate(428.88888888888886,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">9</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(20,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.0</text></g><g class="tick major" transform="translate(0,208.8876638628119)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.2</text></g><g class="tick major" transform="translate(0,187.77532772562378)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.4</text></g><g class="tick major" transform="translate(0,166.66299158843566)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.6</text></g><g class="tick major" transform="translate(0,145.55065545124756)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.8</text></g><g class="tick major" transform="translate(0,124.43831931405946)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.0</text></g><g class="tick major" transform="translate(0,103.32598317687135)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.2</text></g><g class="tick major" transform="translate(0,82.21364703968325)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.4</text></g><g class="tick major" transform="translate(0,61.10131090249513)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.6</text></g><g class="tick major" transform="translate(0,39.988974765307034)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.8</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,124.43831931405946L71.11111111111111,35.61122790928434L122.22222222222221,28.451354694939454L173.33333333333331,109.54145408484641L224.44444444444443,204.327662666078L275.55555555555554,225.66397739804682L326.66666666666663,153.93388891363747L377.7777777777777,55.085709765164495L428.88888888888886,20L480,80.93439937019565" style="stroke: #06789b; fill: none;"></path></svg>

Now that's ugly.  Fortunately, changing the interpolation method used by d3 is simple: [2]_

.. code-block:: javascript

    var lineFunction = d3.svg.line()
            .x(function(d) { return xScale(d[0]); })
            .y(function(d) { return yScale(d[1]); })
            .interpolate('basis');  // only this line was changed

.. raw:: html

    <svg width="500" height="250"><g class="axis" transform="translate(0,230)"><g class="tick major" transform="translate(20,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">0</text></g><g class="tick major" transform="translate(71.11111111111111,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">1</text></g><g class="tick major" transform="translate(122.22222222222221,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">2</text></g><g class="tick major" transform="translate(173.33333333333331,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">3</text></g><g class="tick major" transform="translate(224.44444444444443,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">4</text></g><g class="tick major" transform="translate(275.55555555555554,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">5</text></g><g class="tick major" transform="translate(326.66666666666663,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">6</text></g><g class="tick major" transform="translate(377.7777777777777,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">7</text></g><g class="tick major" transform="translate(428.88888888888886,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">8</text></g><g class="tick major" transform="translate(480,0)" style="opacity: 1;"><line y2="6" x2="0"></line><text y="9" x="0" dy=".71em" style="text-anchor: middle;">9</text></g><path class="domain" d="M20,6V0H480V6"></path></g><g class="axis" transform="translate(20,0)"><g class="tick major" transform="translate(0,230)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.0</text></g><g class="tick major" transform="translate(0,208.8876638628119)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.2</text></g><g class="tick major" transform="translate(0,187.77532772562378)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.4</text></g><g class="tick major" transform="translate(0,166.66299158843566)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.6</text></g><g class="tick major" transform="translate(0,145.55065545124756)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">0.8</text></g><g class="tick major" transform="translate(0,124.43831931405946)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.0</text></g><g class="tick major" transform="translate(0,103.32598317687135)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.2</text></g><g class="tick major" transform="translate(0,82.21364703968325)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.4</text></g><g class="tick major" transform="translate(0,61.10131090249513)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.6</text></g><g class="tick major" transform="translate(0,39.988974765307034)" style="opacity: 1;"><line x2="-6" y2="0"></line><text x="-9" y="0" dy=".32em" style="text-anchor: end;">1.8</text></g><path class="domain" d="M-6,20H0V230H-6"></path></g><path d="M20,124.43831931405946L28.518518518518515,109.63380407993027C37.03703703703704,94.82928884580107,54.07407407407407,65.2202583775427,71.11111111111111,49.2224309410227C88.14814814814814,33.22460350450271,105.18518518518516,30.83797909972108,122.2222222222222,43.15968346231475C139.25925925925924,55.48138782490843,156.29629629629628,82.51142095487741,173.33333333333331,111.82413895006718C190.37037037037035,141.1368569452569,207.4074074074074,172.73225980566747,224.44444444444443,192.08601369120083C241.48148148148147,211.43976757673425,258.5185185185185,218.55187248739054,275.55555555555554,210.1529101953171C292.59259259259255,201.75394790324367,309.62962962962956,177.84391840844057,326.66666666666663,149.4142071362935C343.70370370370364,120.98449586414647,360.74074074074065,88.03510281465549,377.7777777777777,65.7127879957159C394.8148148148147,43.390473176776325,411.85185185185173,31.695236588388163,428.8888888888888,36.003351522560024C445.92592592592587,40.31146645673188,462.96296296296293,60.622932913463764,471.48148148148147,70.77866614182972L480,80.93439937019565" style="stroke: #06789b; fill: none;"></path></svg>

Wrapping Up
===========

The full code for this exercise can be found `here <|filename|../demo-examples/gc-demo2.html>`_.  We still need to
change the x and y domains to be dynamic rather than hardcoded, and allow the user to graph arbitrary functions,
so tune in next week for part 3!

Footnotes
---------

.. [1] If you are interested in SVG's ``path`` mini-language, W3Schools has a `quick reference
       <http://www.w3schools.com/svg/svg_path.asp>`_, and Mozilla has a more `in-depth tutorial
       <https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths>`_.

.. [2] A full list of interpolation methods with visual examples can be found at the bottom of `this page
        <http://www.dashingd3js.com/svg-paths-and-d3js>`_.