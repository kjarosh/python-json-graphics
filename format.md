# Graphics Format

## `palette`

The palette defines a mapping between color names and color values.
For example:

```
{ "palette": {
	"black": "#000000",
	"red":   "#ff0000"
} }
```

Every color with an unknown format will be looked up in the palette.

## `screen`

This section defines basic properties of the canvas. Example:

```
{ "screen": {
	"width": 1920,
	"height: 1080,
	"background": "#000000"
} }
```

### `width` and `height`

They define the canvas size, in pixels.

### `background`

Defines the background color.

### `default_color`

Defines the default color to use for a figure when no color
is specified.

## `figures`

This is an array of figures to draw. They are stored in the following format:

```
{ "type": <type>, <parameters> [, "color": <color> ] }
```

### Supported types

There are some supported types along with format which they use:

* `point` &ndash; parameters: `x`, `y`
* `square` &ndash; parameters: `x`, `y`, `size`
* `circle` &ndash; parameters: `x`, `y`, `radius`
* `ellipse` &ndash; parameters: `x`, `y`, `radiusx`, `radiusy`
* `rectangle` &ndash; parameters: `x`, `y`, `width`, `height`
* `polygon` &ndash; parameters: `points` &ndash; list of vertices
