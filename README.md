# IMDB_Series_Visualization
A tool to generate heatmaps from the IMDB scores of a TV series. The original idea is from reddit user u\Hbenne.

# Usage
run main.py with either the IMDB's ID (numerical) of the desired series or the name (experimental) and the output png name.

# Examples
```shell
$ python ./main.py -i "Dr House" -o drhouse.png
```
![drhouse.png](https://imgur.com/hKlSu5e.png)

```shell
$ python ./main.py -i 0804503 -o madmen.png --dpi 80
```
![madmen.png](https://i.imgur.com/94kvpo4.png)
