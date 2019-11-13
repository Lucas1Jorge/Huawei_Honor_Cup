# Huawei_Honor_Cup_华为

<b>Problem:</b>
<br>
An image was divided into a grid of <b>m</b>x<b>m</b> squares and shuffled. Reconstruct the original image

<b>Solution approach:</b>
<br>
For each square block in the shuffled image, calculate the root squared difference between it's
borders and all the other blocks borders, considering the 4 possible directions:

<p>left-right</p>
<p>botton-up</p>
<p>right-left</p>
<p>top-down</p>

<p>Build a graph using the blocks as nodes and these differences as weights.</p>

<p>Get the Minimum Spanning Tree to represent the image.</p>

<b>Examples:</b>

<div>
  <img src="img/6_shuffled.png" width="33.4%">
  <img src="img/6_reconstructed.jpeg" width="33.4%">
</div>

<div>
  <img src="img/10_shuffled.png" width="33.4%">
  <img src="img/10_reconstructed.jpeg" width="33.4%">
</div>

<div>
  <img src="img/5_shuffled.png" width="33.4%">
  <img src="img/5_reconstructed.jpeg" width="33.4%">
</div>

<div>
  <img src="img/1_shuffled.png" width="33.4%">
  <img src="img/1_reconstructed.jpeg" width="33.4%">
</div>

<div>
  <img src="img/8_shuffled.png" width="33.4%">
  <img src="img/8_reconstructed.jpeg" width="33.4%">
</div>

<br>

<p>To improve the accuracy rate, post processing might be required.</p>
