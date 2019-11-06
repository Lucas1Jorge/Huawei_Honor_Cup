# Huawei_Honor_Cup_华为

<b>Problem:</b>
<br>
An image was divided into a grid of mxm squared and shuffled. Reconstruct the original image

<b>Solution approach:</b>
<br>
For each square block in the shuffled image, calculate the root squared difference between it's
borders and all the other blocks borders, considering the 4 possible directions:

<ul>
  <li>left-right</li>
  <li>botton-up</li>
  <li>right-left</li>
  <li>top-down</li>
</ul>

<p>Build a graph using the blocks as nodes and these differences as weights.</p>

<p>Get the Minimum Spanning Tree to represent the image.</p>

<b>Examples:</b>

<p>To improve the accuracy rate, post processing might be required.</p>
