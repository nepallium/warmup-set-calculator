# WARMUP SET CALCULATOR
### Video Demo:  [https://youtu.be/UR5NkRY25zc?feature=shared]

> [!NOTE]
> This project was done in March 2024 as a final project for Harvard's CS50P curriculum

### Description
Tired of manually calculating your warmup sets' weights? This program automates this process by outputting the weight of each warmup set based on your working sets' weight. The weights and sets will be calculated in a "pyramid" style, wherein the weight gets heavier as the reps diminish. This primes your body for your working sets so that you can give your best effort on those sets.

The percentages used for the calculations, in order of first to last warmup set, are 55%, 75%, and 85%. These are the percentages that work best for me and are hardcoded for ease of use.

### Features
- For convenience, the weights will be rounded *down* to the nearest multiple of 5. A multiple of 5 in order to make plate-loading easier, and down because it's usually better to warmup with lighter rather than heavier weight.
- This means that the percentages outlined in the description are there for a general estimate at first of the pyramid progression. To have a general idea of how heavy the weight you are warming up with is, I added a "%" column in the final output.
- The `Dumbbell` class contains a list of weights in lb that my personal gym has. An independant list was necessary for this, as the weight increments are not linear. Further, I assume the user will input their dumbbell's weights in lb as it is the only metric I know how to implement correctly with this independant list feature.
- The warmup set calculator has a built-in plate calculator which outputs the number of plates you need on each side of the bar. This "plates" column only appears if you choose an equipment type that utilizes plates.

### Usage
#### 1. The program first prompts you to input your working set's weight.

It must be formatted as follows: (weight) (unit). The unit should be written per the common syntax (without an ending *s*)
```
Input your working weight by following this format: x lb or y kg
Add decimals if necessary
```
> [!NOTE]
> If you are using dumbbells, input the weight of ***one*** dumbbell.

**Example Inputs**

- 25.5 kg
- 150 lb
- 30.255 kg

> [!WARNING]
> Inputting anything other than a *float* or an *int* followed by an appropriate weight unit will yield a reprompt.

#### 2. Then, you will need to select the equipment you are using for your exercise by inputting a number representitive of said equipment.
```
Input number to choose equipment:
1: Barbell
2: Dumbbells
3: Pin-loaded (cable, machine, etc.)
4: Plate-loaded machine
```
> [!WARNING]
> Inputting anything other than an *int* from 1 to 4 will yield a reprompt.

These are the most common equipment types I could think of. Any other equipment type is usually a derivative of one of these 4 types, or at the very least you can select an equipment that uses similar logic. For example, you could select "4: Plate-loaded machine" if you are using an EZ-bar.

#### 3. The program then outputs a table containing your warmup sets.

In each of the warmup sets, you will see the percentage of your working weight the warmup weight represents, the weight itself, the number of reps you should perform with said weight, and, if using a plate-type equipment (barbell or plate-loaded machine), the plates needed on each side of the bar.

**Example Outputs**

The following examples will output the warmup sets based on the working weight and the equipment used.
- 50 kg with a barbell
```
+-------+-----+---------------+--------+--------------------+
|  Set  |  %  |  Weight (kg)  |  Reps  | Plates/side (kg)   |
+=======+=====+===============+========+====================+
|   1   | 50  |      25       |   5    | 2.5                |
+-------+-----+---------------+--------+--------------------+
|   2   | 70  |      35       |   3    | 5                  |
|       |     |               |        | 2.5                |
+-------+-----+---------------+--------+--------------------+
|   3   | 80  |      40       |   2    | 10                 |
+-------+-----+---------------+--------+--------------------+
```

- 30 kg with a barbell
```
+-------+-----+---------------+--------+--------------------+
|  Set  |  %  |  Weight (kg)  |  Reps  | Plates/side (kg)   |
+=======+=====+===============+========+====================+
|   1   | 67  |      20       |   3    | Empty              |
+-------+-----+---------------+--------+--------------------+
|   2   | 83  |      25       |   2    | 2.5                |
+-------+-----+---------------+--------+--------------------+
```

- 25 lb with a dumbbell
```
+-------+-----+---------------+--------+
|  Set  |  %  |  Weight (lb)  |  Reps  |
+=======+=====+===============+========+
|   1   | 48  |      12       |   5    |
+-------+-----+---------------+--------+
|   2   | 70  |     17.5      |   3    |
+-------+-----+---------------+--------+
|   3   | 80  |      20       |   2    |
+-------+-----+---------------+--------+
```

### Tests
I tried my best to find corner cases for each equipment type. I made the sure the program outputted the appropriate number of sets based on the working weight, which was especially challenging with the barbell equipment, since I had to make sure the weight's never went below the weight of the bar.

This was also an area of learning and skill-acquisition, wherein I learnt how to iterate over multiple objects found in my `setUp` function. Indeed, I didn't want to create a new object for each corner case I thought of and assigning it to a new variable each time, so I list of dictionaries containing the values I wanted to test. I then iterated over the dictionaries, instantiating a new object and testing it.

### Challenges
The whole code was overall quite enjoyable to write as I was constantly thinking and learning about concepts and how they interact with each other. The following points highlight the parts with which I had the most difficulty with. They are not the only difficulties I faced while writing my program, but they are the ones that stand out the most.

1. Figuring out how to correctly iterate over the given weights for the dumbbells under 15 lbs, as in finding the lowest match among the list, was quite challenging, and required me to go online and learn about a new library (`bisect`).
2. There was quite a bit of arithmetic logic implicated in my program, especially for the `Plates` class. This also explains the presence of the `plates_warmups` class method, unlike the other classes, as its logic is more intricate than the others.

### Improvements
In the future, implementing a non-hardcoded version of the percentages could be interesting, allowing the user to decide what percentages they want to warmup with and the number of warmup sets they want. This would require a greater number of elif statements, instead of hardcoding values into my program. This would also demand more logic in the assignement of reps for each warmup set.This feature would of course make my program much more robust, but I feel like it would extend the time to completion of said program by a good margin for minimal learning gains, and I am already satisfied with what I've learnt up until now. I want to delve into other programming languages, but eventually, if I end up bringing this program to life and implementing more usable UI that I can use in the real-world (while I'm working out) and not just on a Python compiler, I will probably implement that feature.

Further, I believe adding in an extra question asking the user if this is their first time working a muscle or not. A muscle group is usually already warm after the first exercise, therefore the following exercises using it don't need much of a warmup. The warmup sets should reflect that.
