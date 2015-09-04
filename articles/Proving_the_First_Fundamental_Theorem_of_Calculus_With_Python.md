###Explaining the Theorem

The first fundamental theorem of calculus sounds scary -- but really, it's very simple on the surface. It says that if we have a function, $F(x)$, which defines the area between some other function, $f(t)$ (note the case change between the two), $F'(x)$ is equal to $f(x)$. Note that now, $f(t)$ is with respect to $x$ instead of $t$. We can write this in a more concise form:
 
$$F(x) = \int\limits_a^x f(t) dt $$
$$F'(x) = f(x)$$

We also know that:

$$F(x) = \lim_{n \to \infty} \sum_{k=1}^{n} f(x_k *)\Delta x$$

You'll want to keep that last equation in your back pocket, because it really comes into play later. For now, let's try to apply this idea in terms of python, to illustrate its meaning. First, let's say we want to find the area under $y = x^2$:

    ::python
    def f(t): return t**2

Calling this function over a given interval would return each integer, but squared. For example:

    ::python
    >>> f(1)
    1
    >>> f(2)
    4
    >>> for t in range(0, 4):
    ...    f(t)
    0
    1
    4
    9

Now, we *could* find the area without integrating, using Riemann sums.

####What is a Riemann Sum? 

In principle, a Riemann sum is very simple. It says that we can approximate the area under the curve using rectangles. Here's an animation to illustrate the concept:

![Riemann sum for y=x^2][1]     

First, we create a series of terms to describe the total area of $n$ amount of rectangles, and observe that quantity as $n$ approaches $\infty$. Let's try approximating the area using 4 rectangles first:

    ::python
    >>> delta_x = (3-1)/4
    >>> (delta_x * 1.5**2) + (0.5 * 2**2) + (0.5 * 2.5**2) + (0.5 * 3**2)
    10.75

So according to this result, an approximation of the area under $y=x^2$ in the interval $[1, 3]$ is 10.75. Our method could be improved and refactored. Using the previous value of `delta_x`, we can change our code to the following:

    ::python
    area = 0
    for n in range(3, 7):
        area += float(delta_x) * f(delta_x*n)
    print(area)

This could be done in many different ways: for example, I chose to make the starting value of `range()` 3, so I would get the needed initial value of $\frac{3}{4}$, but you could accomplish the same result using any number of methods.

###Exact value

By this point, if you've looked up the area (or already know it) the *actual* area is more like $\frac{26}{3}$, or $8.\bar{6}$. That seems pretty far off from 10.75. How can we improve our approximation? Normally, you'd do that by taking the limit of our area function as *n* rectangles approaches infinity, which is what the equation at the beginning of this article describes. For us, using python, we can't actually **go** to infinity -- but let's see how close we can get by changing our code a bit more. 

1. One of our terms, `delta_x`, depends on the number of rectangles
2. We'll need to change our `range()` to iterate $n$ times

First, let's see how changing 4 rectangles to 50 rectangles changes our terms.

    ::python
    >>> delta_x = (3-1)/50
    >>> (delta_x * 1.04**2) + (delta_x * 1.08**2) + (delta_x * 1.12**2) + ...

To incorporate this into our `for` loop, we need to take the number of rectangles into account:

    ::python
    delta_x = float((3-1)/50)
    area = 0
    for n in range(1, 51):
        area += float(delta_x) * f(delta_x*n + 1) 
    print(area)

When we run, we should get 8.8272. Closer! What about 1000 rectangles?

    ::python
    delta_x = float((3-1)/1000)
    area = 0
    for n in range(1, 1001):
        area += float(delta_x) * f(delta_x*n + 1)
    print(area)

8.674668. Not bad. Now, with that last example, you may have noticed something exciting: in order to change the number of rectangles, we only have to change two values (which are related mathematically). This means we can make a function to approximate the area under $y=x^2$ from $[1,3]$ for *any* number of rectangles:

    ::python
    def F(x):
        delta_x = float((3-1)/x)
        area = 0
        for n in range(1, x+1):
            area += float(delta_x) * f(delta_x*n + 1)
        return area 

    >>> F(4)
    10.75
    >>> F(50)
    8.8272
    >>> F(1000)
    8.674668

Notice the case change for `F(x)`? Now we have a function for approximating the area under the curve of $y=x^2$, for as many rectangles as we'd like. How far can we take our code?

    ::python
    >>> F(10000)
    8.66746668
    >>> F(100000)
    8.6667466668
    >>> F(1000000)
    8.66667466667

As you'll notice, the value *as we approach* (eg, the limit) a large number of rectangles is $8.66\bar{6}$. Interesting; with one million rectangles, we confirmed the area under the curve (on that interval) to 4 decimal places.

###The proof

At this point, our code is functional. However, If you were reading carefully -- or have a knowledge of calculus -- you may have noticed an error in logic that needs to be corrected before we can move forward. `F(x)` takes one parameter which determines the number of rectangles to be used when approximating the area. However, `x` is actually the **second limit of integration, relative to $a$ **. I want to retain the ability to dynamically define the number of rectangles used, but the use of `x` is still misleading and needs to be fixed. To remedy the situation, I will add another parameter, which serves the proper purpose:

    ::python
    def F(x, rectangles=1000):
        delta_x = float((x-1)/rectangles)
        area = 0
        for n in range(1, rectangles+1):
            area += float(delta_x) * f(delta_x*n + 1)
        return area

    >>> F(3)
    8.674667999999999
 
I have given `rectangles` a default value of 1000, which seems to be a decent approximation, so that my calls to `F(x)` are more clear. If need be, I can increase the value of `rectangles` to gain a greater degree of accuracy.

> As an interesting side note, try finding the area on $[-1, 1]$:
>  
    ::python
    >>> F(-1)
    -0.6666679999999993
    >>> F(-1, 1000000000)
    -0.6666666666653588

> Since we are moving from 1 *backwards* to -1, the area is negative. If you were to actually mathematically compute this area, it would be $-\frac{2}{3}$, or $-0.6\bar{6}$. Our code works!

At this point, we're ready to prove the statement I made at the beginning: that $F'(x) = f(x)$. We have `F(x)`, and we have `f(x)`. It is also known that $f(t) = t^2$, which in terms of $x$ would mean that $f(x) = x^2$. So, what we are really trying to prove, in relation to the code we've created, is as follows: if we were to graph the slope of `F(x)` over $[a, b]$, the graph would perfectly match `f(x)` over the same interval. In order to graph the slope of `F(x)`, we need to take the derivative, and for that we need **the definition of a derivative** (in terms of our area function):

$$
F'(x) = \lim_{h \to 0}\frac{F(x+h) - F(x)}{h}
$$

Just like the Riemann sums, this is an approximation, since $F'(x)$ would be undefined if $h=0$. The closer $h$ is to 0, the more accurate the result. This is a really lucky situation, because translating the math to code really just involves copying it almost symbol for symbol:

    ::python
    def derivative(f, h=0.1e-5):
        def df(x, h)
            return (f(x+h/2) - f(x-h/2))/h
        return df
    >>> d = derivative(f)
    >>> d(2)
    4.00000000012

This makes sense, because $\frac{d}{dx}[x^2] = 2x$. And, $2 \cdot 2 = 4$. I also divided $h$ by 2, to get a better approximation (thanks to advice from [this][2] article). Let's see what happens when we use this new `derivative()` function on `F(x)`:

    ::python
    >>> d = derivative(F)
    >>> d(2)
    4.003500499560886
    >>> f(2)
    4

Just to remind you, let's review what equals what:

`f(x)` = $f(x)$
    
`F(x)` = $F(x)$
    
`d` = $F'(x)$
    
$F'(x) = f(x)$
    
So in terms of our code, we want `d` to equal `f(x)`. From our test run above, that has been confirmed to 2 decimal places. Don't believe me? Let's try some more values:

    ::python
    >>> d(3)
    9.010001999598671
    >>> f(3)
    9
    >>> d(4)
    16.01950448559819
    >>> f(4)
    16

Maybe that's *still* not enough to convince me. How about we compute these value over a range, and compute the percent deviation between them:

    ::python
    y = {d(n): f(n) for n in range(0, 100)} #create values
    diff = []
    for y1, y2 in y.iteritems():
        '''
        Calculate the percent difference between each pair of values
        '''
        diff.append(abs((y2 - y1)/((y2 + y1)/2)) * 100)
    percentSum = 0
    for percent in diff:
        percentSum += percent
    print(percentSum/len(diff))

    2.14244620353

So an approximation (definition of a derivative) of an approximation (Riemann sum) has proven the first fundamental theorem of calculus to within 2%. For individual numbers, that difference seems even smaller -- for example, the percent difference between `d(1)` and `f(1)` is 2.8839...e-09 percent, or about $2.9 \cdot 10^{-9}$ percent. Obviously, with a larger test sample this number will continue to decrease.

###Conclusion and Extension

So there you have it -- the first fundamental theorem of calculus would appear to be true. You could go even further by using a larger sample size and a greater number of rectangles; graphing `d` and `f(x)` would yield the exact same line. I lack the computing power and the time to generate the data, but this could be a cool exercise for the reader (and easy to do with matplotlib or some other python graphing library). Additionally, computing the derivative with an even smaller value of $h$ would improve your results further. If you find any errors or misconceptions in the article, or have any suggestions for improvement, please send me an email at laird.avery@gmail.com or leave a comment below. 
 
  [1]: /static/media/uploads/riemann_sum_%28y=x%5E2%29.gif
  [2]: http://aroberge.blogspot.ca/2005/04/computing-derivatives-using-python.html