# Aggressive image optimizer cli

This CLI tries to bring all images to a size of 500kb without losing to much quality.
You can see the results in this repo (`HQ_unsplash1.jpg` original to reduced `unsplash1 copy.jpg`).
It uses `pillow` package to accomplish that.


## Install

It's recommended to use pipx to install package, but pip should work as well. 

```shell
pipx install aggimg
```

## Usage

You can specify path to folder which contains images you want to shrink/optimize image size.

```shell
aggimg --path ./images
```

You can also don't specify the path and `aggimg` will look into current directory for images.

```shell
aggimg
```
Images that start with `HQ_` prefix will ignored.

```shell
$: aggimg --path ./images
INFO - Trying to optimize ./images/unsplash1 copy.jpg
INFO - Reduced from 2222333 to 752461 which is a 66.14% reduction
INFO - Trying to optimize ./images/unsplash2 copy.jpg
INFO - Reduced from 1720129 to 478766 which is a 72.17% reduction
INFO - Trying to optimize ./images/unsplash3 copy.jpg
INFO - Reduced from 3054558 to 573479 which is a 81.23% reduction
```

*Please note that images will be modified in place (overwritten).*
