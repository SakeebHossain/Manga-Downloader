# SleepyComputer's Manga Downloader

A tool that scrapes various manga sites as saves them as `.jpegs` on your computer for offline reading. 

## Installation

Run the install script `install.sh`. This will generate a `build` and `dist` directories in your repository. This will generate the bundle in a subdirectory called `dist` where you will find the application.

## Usage

`help`
    Prints the usage guide.

`search [WORD]`
    Find all manga titles containing `WORD` in its title.

`info [TITLE]` 
    Prints all details about Manga with the specified title.

`download [TITLE] [OPTIONS]`
    Downloads all the chapters of the manga with title [TITLE].

    [OPTIONS]:
        -all
              downloads all chapters of the manga
        -range [START] [END]
              downloads all chapters between [START] and [END]
        -only [n...]
              downloads all chapters numbers listed in [n...]

## Supported sites
- [mangareader](https://www.mangareader.net)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)