# Watson weekly timetable

This is a small script which parses the output of
[Watson](https://github.com/TailorDev/Watson), more precisely of the `watson log
--week -j` command. It aims at producing a matplot-lib based view of a
work-week (similar to an ical/google calendar week-view).

## Screenshot

![Screenshot](./Semaine.png?raw=true "Screenshot")

## Usage

Watson output should be put in JSON in a file. The name of the file should be
put in the `timetable.cfg` file, in the `[input]` section (value: framesfile,
default: ./datawatson.json). A test file is provided. 

Some colors can be used, based on tags. If a frame has a tag, it will appear in
a certain color (order of the tags in the config file matters, the block will
have the first listed color in the file if several are possible).

Week-ends are in grey by default. Some config values are hard-coded at the
moment and should appear in the configuration in the future (e.g.: start and end
hours, border colors).
