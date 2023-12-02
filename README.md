# Improving Run-Time Performance of TEXTure Method

## [[Baseline Method: Project Page]](https://texturepaper.github.io/TEXTurePaper/)

<a href="https://arxiv.org/abs/2302.01721"><img src="https://img.shields.io/badge/arXiv-2302.01721-b31b1b.svg" height=22.5></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" height=22.5></a>  [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/TEXTurePaper/TEXTure)

> Abstract
In this paper, we present TEXTure, a novel method for text-guided generation, editing, and transfer of textures for 3D shapes.
Leveraging a pretrained depth-to-image diffusion model, TEXTure applies an iterative scheme that paints a 3D model from different viewpoints. Yet, while depth-to-image models can create plausible textures from a single viewpoint, the stochastic nature of the generation process can cause many inconsistencies when texturing an entire 3D object.
To tackle these problems, we dynamically define a trimap
partitioning of the rendered image into three progression states, and present a novel elaborated diffusion sampling process that uses this trimap representation to generate seamless textures from different views.
We then show that one can transfer the generated texture maps to new 3D geometries without requiring explicit surface-to-surface mapping, as well as extract semantic textures from a set of images without requiring any explicit reconstruction.
Finally, we show that TEXTure can be used to not only generate new textures but also edit and refine existing textures using either a text prompt or user-provided scribbles.
We demonstrate that our TEXTuring method excels at generating, transferring, and editing textures through extensive evaluation, and further close the gap between 2D image generation and 3D texturing.

## Description :scroll:	
Official Implementation for "TEXTure: Semantic Texture Transfer using Text Tokens".

> TL;DR - TEXTure takes an input mesh and a conditioning text prompt and paints the mesh with high-quality textures, using an iterative diffusion-based process.
> In the paper we show that TEXTure can be used to not only generate new textures but also edit and refine existing textures using either a text prompt or user-provided scribbles.


## Recent Updates :newspaper:
* `Feb 06 2023` - Code release



## Getting Started


### Installation :floppy_disk:	
Install the common dependencies from the `requirements.txt` file
```bash
pip install -r requirements.txt
```

and Kaolin

```bash
pip install kaolin==0.11.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/{TORCH_VER}_{CUDA_VER}.html
```

The remaining dependencies are the ones related to PyTorch and they can be installed with the command:
```
pip install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio==0.10.1 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

Note that you also need a :hugs: token for StableDiffusion. 
First accept conditions for the model you want to use, default one is [`stabilityai/stable-diffusion-2-depth`]( https://huggingface.co/stabilityai/stable-diffusion-2-depth). Then, add a TOKEN file [access token](https://huggingface.co/settings/tokens) to the root folder of this project, or use the `huggingface-cli login` command


## Running

### Text Conditioned Texture Generation

Try out painting the [Napoleon](https://threedscans.com/nouveau-musee-national-de-monaco/napoleon-ler/) from [Three D Scans](https://threedscans.com/) with a text prompt 
```bash
python -m scripts.run_texture --config_path=configs/text_guided/napoleon.yaml
```
Or a next gen nascar from [ModelNet40](https://modelnet.cs.princeton.edu/)
```bash
python -m scripts.run_texture --config_path=configs/text_guided/nascar.yaml
```


## Difference Between Original Method

### New Option: Using Random Viewpoint

To boost-up run-time performance of TEXTure method, we add a new option which uses random viewpoint during the geneartion process. With option, you can boost-up speed about 20%.

### How to use

Just add option use_random_viewpoint to the text guided .yaml file.

```yaml
guide:
  use_random_viewpoint: True
```

For convenience, bunny object is provided with random viewpoint option.

```bash
python -m scripts.run_texture --config_path=configs/text_guided/bunny.yaml
```

Or you can use cat instead of bunny.

```bash
python -m scripts.run_texture --config_path=configs/text_guided/cat.yaml
```