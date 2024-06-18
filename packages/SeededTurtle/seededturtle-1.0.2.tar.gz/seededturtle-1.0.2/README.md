# SeededTurtle

SeededTurtle is a Python library that allows you to generate random turtles with various properties. It's a fun and creative way to explore the world of programming with Python's turtle graphics. The idea is that the randTurtle function takes a seed as input and produces a resulting "randomized" turtle graphic when you run the program.

The turtle graphic randomization is reproducable based on what the seed is, so if you enter in "iloveturtles" as the seed two seperate times, it will return the same turtle. The library also provides support for randomizing this seed, so you can call the function to get a random seed and use that as the seed for generating a random turtle.

## Installation

To install SeededTurtle, you can use pip:

```bash
pip install seededturtle
```

Afterwards, just use an `import` statement in your program in order to use functions from the library (see [Usage](#usage) examples below)
## Usage

The main function in the RandTurtle library is `generateRandomTurtle()`. This function generates a turtle with random properties based on the provided seed.

Here is an example of how to use it:

```python
import seededturtle.randTurtle as rt

# Generate a random turtle
turtle = rt.generateRandomTurtle("your_seed_here")
```

The `generateRandomTurtle()` function takes the following parameters:

- `seed`: A string of 16 or more alphanumeric characters or special characters (!@#$%^&*()). This is used to seed the random number generator for the turtle's properties.

- `time` (optional): The time in seconds that the turtle will be displayed for before doing anything else. Defaults to 0.

- `fill` (optional): The fill color of the turtle. Can be "none", "random", or a string of three comma-separated integers in the format "R,G,B". Defaults to "none".

- `color` (optional): The color of the turtle. Can be "random" or a string of three comma-separated integers in the format "R,G,B". Defaults to "random".

If invalid parameters are passed in, the function will raise a `RandomTurtleValueError`.

For seed randomization as well, simply do:

```python
import seededturtle.randturtle as rt

# Generate a random turtle using a random seed
turtle = rt.generateRandomTurtle(rt.generateRandomSeed())
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Dependencies

`random`, `turtle`, `regex`, and `time.sleep()`.

### Known Issues

The fill only works when there is enough `iterations` to make a complete loop for the shape. Otherwise, the turtle library cannot fill an incomplete shape because there is no closed object. This isn't exactly an issue, but more something that the user needs to understand before trying to enable filling for their random turtle.

## Notes from the creator

This was my second python library deployed (I also created chainhashing), so I still have lots to learn. I know there are probably a few issues with the library/optimizations that could be made, but hopefully people looking to use this library still find use out of it! Any advice/change recommendations are greatly appreciated; feel free to email me at rt.kellar@gmail.com or open an issue on the GitHub page for this library, https://github.com/Ruxton07/SeededTurtle. Enjoy!

## License

[MIT](https://choosealicense.com/licenses/mit/)