<div align="center">

<h1>Motion-to-Attention: Attention Motion Composer using Optical Flow for Text-to-Video Editing</h1>

[🖼️ Project Page](https://currycurry915.github.io/Motion-to-Attention/) — Visit our project page for more visual results and detailed explanations.
<br>
[📄 Paper (PDF)](results/readme_images/Motion-to-Attention.pdf) — Read the full paper for technical details, methodology, and experimental results.

</div>
---

<br>

<image src="results/readme_images/TCVST_fig1.png"  />
Existing T2V (Text-to-Video) models often struggle to accurately estimate attention maps for motion prompts (e.g., floating, moving), which limits the editability of generated videos. To address this limitation, we propose the Motion-to-Attention (M2A) module. M2A enhances the attention maps across the entire prompt, significantly improving the editing capabilities of existing video editing models.
<br>

</div>

## Abstract
Recent text-guided video editing research attempts to expand from image to video based on the text-guided image editing model. To this end, most research focuses on achieving temporal consistency between frames as a primary challenge in text-guided video editing. However, despite their efforts, the editability is still limited when there is a prompt indicating motion, such as "floating". In our experiment, we found that this phenomenon was due to the inaccurate attention map of the motion prompt. In this paper, we suggest the Motion-to-Attention (M2A) module to perform precise video editing by explicitly taking motion into account. First, we convert the optical flow extracted from the video into a motion map. During conversion, users can selectively apply direction information to extract the motion map. The proposed M2A module uses two methods: "Attention-Motion Swap", which directly replaces the motion map with the attention map, and "Attention-Motion Fusion", which uses the association between the motion map and the attention map, measured by a Fusion metric, as a weight to enhance the attention map using the motion map. The Text-to-Video editing model with the proposed M2A module showed better quantitative and qualitative results compared to the existing model.


## Our Frameworks
<image src="results/TCSVT_framework.png"  />
The left side of the figure shows the overall framework of video editing by enhancing the attention map. First, the Text-to-Video (T2V) Model generates an attention map by receiving video and prompts as input. Simultaneously, the optical flow estimation model estimates the optical flow from the input video frames. The estimated optical flow is converted to a motion map by default using only magnitude information. Optionally, when direction information is provided by the user, the Direction Control converts the optical flow to a motion map that only shows movement in the user-specified direction. If the user indicates directional words with \textbf{[]}, the model captures the direction information and performs Direction Control. Then, the motion map is injected into the attention map of the T2V-Model in two ways from the M2A module: Attention-Motion Swap and Attention Motion Fusion. After that, text-to-video editing is performed using the attention map enhanced by the motion map. The right side of the figure shows how the Attention-Motion Swap and Attention-Motion Fusion of the M2A module enhance the attention map with the motion map.


## Experimental Results
<image src="results/experimental_results.png"  />


### You can find more experimental results [on our project page](https://currycurry915.github.io/Motion-to-Attention/).

<table class="center">
<tr>
  <td align="center" ><b>Input Video</b></td>
  <td align="center" ><b>Video-P2P</b></td>
  <td align="center" ><b>Ours</b></td>
</tr>

 <tr>
  <td align="center" width=25% style="text-align:center;color:gray;">"Clouds {flowing} under a skyscraper"</td>
  <td align="center" width=25% style="text-align:center;">"Waves {flowing} under a skyscraper"</td>
  <td align="center" width=25% style="text-align:center;color:gray;">"Waves {flowing} under a skyscraper"</td>
</tr>

<tr>
  <td align="center" style colspan="1"><img src="results/clouds_waves_input.gif" loop=infinite></td>
  <td align="center" style colspan="1"><img src="results/clouds_waves_ori.gif"></td>
  <td align="center" style colspan="1"><img src="results/clouds_waves_MMI.gif"></td>
</tr>


<tr>
  <td align="center" width=25% style="text-align:center;color:gray;">"Clouds {flowing} on the mountain"</td>
  <td align="center" width=25% style="text-align:center;">"Lava {flowing} on the mountain"</td>
  <td align="center" width=25% style="text-align:center;color:gray;">"Lava {flowing} on the mountain"</td>
</tr>

<tr>
  <td align="center" style colspan="1"><img src="results/clouds_lava_input.gif"></td>
  <td align="center" style colspan="1"><img src="results/clouds_lava_ori.gif"></td>
  <td align="center" style colspan="1"><img src="results/clouds_lava_MMI.gif"></td>       
</tr>

<tr>
  <td align="center" width=25% style="text-align:center;color:gray;">"{Spinning} wings of windmill are beside the river"</td>
  <td align="center" width=25% style="text-align:center;">"Yellow {spinning} wings of windmill are beside the river"</td>
  <td align="center" width=25% style="text-align:center;color:gray;">"Yellow {spinning} wings of windmill are beside the river"</td>
</tr>

<tr>
  <td align="center" style colspan="1"><img src="results/yellow_windmill_input.gif"></td>
  <td align="center" style colspan="1"><img src="results/yellow_windmill_ori.gif"></td>
  <td align="center" style colspan="1"><img src="results/yellow_windmill_MMI.gif"></td>       
</tr>
</table>




## Setup

The environment is very similar to [Video-P2P](https://github.com/ShaoTengLiu/Video-P2P).

The versions of the packages we installed are:

torch: 1.12.1 \
xformers: 0.0.15.dev0+0bad001.d20230712

In the case of xformers, I installed it through the [link](https://github.com/bryandlee/Tune-A-Video/issues/4) introduced by Video-P2P.

```shell
pip install -r requirements.txt
```


## Weights

We use the pre-trained stable diffusion model. You can download it [here](https://huggingface.co/runwayml/stable-diffusion-v1-5). 


## Quickstart

Since we developed our codes based on Video-P2P codes, you could refer to their [github](https://github.com/ShaoTengLiu/Video-P2P), if you need.

Please replace **pretrained_model_path** with the path to your stable-diffusion.

To download the pre-trained model, please refer to [diffusers](https://github.com/huggingface/diffusers).


``` bash
# Stage 1: Tuning to do model initialization.

# You can minimize the tuning epochs to speed up.
python run_tuning.py  --config="configs/cloud-1-tune.yaml"
```

``` bash
# Stage 2: Attention Control

python run_motion_to_attention.py --config="configs/cloud-1-p2p.yaml" --motion_prompt "Please enter motion prompt"

# If the prompt is "clouds flowing under a skyscraper", the motion prompt is "flowing".
# You can input the motion prompt as below.

python run_motion_to_attention.py --config="configs/cloud-1-p2p.yaml" --motion_prompt "flowing"
```

Find your results in **Video-P2P/outputs/xxx/results**.


## Acknowledgements
This repository borrows heavily from [Video-P2P](https://github.com/ShaoTengLiu/Video-P2P). Thanks to the authors for sharing their code and models.

