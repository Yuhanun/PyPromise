# PyPromise
JavaScript-alike promises in python

## How to set this up ##
Simply download the following files:
```
PyPromise.py
```

Add it either to your sys.path, or move it to where you want to use it.

Usage:
```py
import PyPromise

PyPromise.Promise(lambda: "Hello")
```

For example usage, check PyPromise.py

```py
if __name__ == '__main__':
    def throw_error():
        raise RuntimeError("Test")

    Promise(lambda: throw_error()) \
        .then(lambda: print("Succesfully finished")) \
        .catch(lambda x: print(f"An exception has occured: {x}"))

    Promise(lambda: print("Hello")) \
        .then(lambda: print("Finished")) \
        .catch(lambda x: print(x))
```

## Feel free to pull request any changes / improvements you make :) ##

# License #
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/Yuhanun/PyPromise/blob/master/LICENSE) file for details

# Acknowledgments #
Thanks to Guido for creating the language :)

### Buy me a coffee ;) (BTC) ###
32dcJ31dsxj8BMD5oD3mWKTDFSzpFHuHP1