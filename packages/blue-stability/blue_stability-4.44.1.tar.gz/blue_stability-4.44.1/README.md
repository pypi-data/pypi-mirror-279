# 🟦 blue-stability

🟦 `blue-stability` (`bstab`) is a bash cli for [stability-sdk](https://github.com/Stability-AI/stability-sdk).

## installation

```bash
pip install blue-stability
```

```bash
 > blue_stability help
blue_stability dashboard
 . browse blue-stability dashboard.
blue_stability generate image \
	[~dryrun,height=<576>,~sign,~tag,width=<768>] \
	[<image>] [<previous-image>] \
	["<prompt>"] \
	[--seed 42]
 . <prompt> -[<previous-image>]-> <image>.png.
blue_stability generate video \
	[~dryrun,frame_count=16,marker=PART,~publish,~render,resize_to=1280x1024,~sign,slice_by=words|sentences,~upload,url] \
	<filename.txt|url> \
	[--seed 42 --start_schedule 0.9]
 . <filename.txt>|url -> video.mp4
blue_stability generate validate \
	[dryrun,what=all|image|video]
 . validate blue_stability.
blue_stability notebook
 . browse blue stability notebook.
blue_stability transform \
	[count=<1>,~dryrun,extension=jpg,~sign,~tag,~upload] \
	[<object-name>] \
	["<prompt>"] \
	[-]
 . <object-name> -<prompt>-> 2023-12-27-18-08-30-90155.
```

## sentence -> image

```bash
abcli select; \
open .; \
blue_stability generate image \
  ~dryrun,height=576,width=768 \
  carrot - \
  "an orange carrot walking on Mars."
```

![image](./assets/carrot.png)

## text -> video

```bash
abcli select; \
open .; \
blue_stability generate video \
  ~dryrun,frame_count=5,marker=PART,url \
  https://www.gutenberg.org/cache/epub/51833/pg51833.txt
```

![image](./assets/minds.gif)

## notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamangir/blue-stability/blob/main/nbs/demo_colab.ipynb)

```bash
blue_stability notebook
```

---

[![PyPI version](https://img.shields.io/pypi/v/blue-stability.svg)](https://pypi.org/project/blue-stability/)
