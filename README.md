# Trim mp3

A python script to trim leading and trailing silence parts from MP3

# Quick start

Open this repository as container in Visual Studio Code.

Just press **F5**, or run `python trim_mp3.py -i <inputFiles> -o <outputDirectory>` (wildcards accepted!); example:

```bash
python trim_mp3.py -i ./input/*.mp3 -o ./output
```

Find the processed files in the `<outputDirectory>` folder.