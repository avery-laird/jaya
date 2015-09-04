### Area Under A Curve

I recently wrote an article about finding the area under $y=x^2$. I had a lot of interesting insights from that project, and it got me thinking about some other things we could do with the code. If you haven't read the article, you can get it [here][1]. I was thinking about ways to improve my code and expand its use, so that it could be used in a wider range of applications. Let's take a random polynomial, like $x^3 - x^2 +2$. Our current code has no support for using a different function like this. Let's start by translating it into code:

    ::python
    def h(x): return (x**3 - x**2 + 2)

Next, I'm going to create another function to wrap around our current `F(x)` function called `integrate()`, change the name of `F(x)` to `findArea()`, and update the parameters of `findArea()`:

    def integrate(f, a):
        def findArea(b, rectangles=1000):
            delta_x = float((b-a)/rectangles)
            area = 0
            for n in range(1, rectangles+1):
                area += float(delta_x) * f(delta_x*n + 1)
            return area
        return findArea

Now, let's try computing the area under `h(x)` from 1 to 3:

    ::python
    >>> F = integrate(h, 1)
    >>> F(3)
    15.35134

The actual area is $\frac{46}{3}$, or $15.\bar{3}$. Remember, this approximation is with 1000 rectangles; if more accuracy is required, the `rectangles` parameter can be specified to a non-default value.

You might have noticed that I changed the location of the  integral limits to be parameters on `integrate()`. This is mostly for usability. I want the function and lower limit of integration to be defined with the integral, and the higher limit to be defined by `F(x)`. This way, the code and the math are somewhat interchangeable.

## Trigonometry Proofs

So far, we've only tested our code on simple polynomial functions. I would like to accomplish two things in this section:

1. Stress test our code on trigonometric functions, and fix it if it breaks
2. Use our improved code to prove some trigonometric integrals

#### Testing the code

If it ain't broke, don't fix it. Before we try to fix anything about our code, let's see if it works as-is. I can't really think of a reason why it *shouldn't*.

    ::python
    import math
    >>> def g(x): return math.sin(x)
    >>> F = integrate(g, 1)
    >>> F(3)
    1.5295939413935349

Okay, so far this answer seems to make sense. Let's see what the actual answer is.

We proved [last time][2] that the first fundamental theorem of calculus is actually true. This means we can make use of it, and its corollaries, to mathematically find the area under $\sin{x}$ from 1 to 3.
$$
\int_1^3 \sin{x}\, \mathrm{d}x = -\cos{x} \Big|_1^3 = -\cos{3} + \cos{1} = 1.530294802...
$$

That seems about right. Wolfram Alpha's approximation is $\approx 1.5303$. We haven't really tried anything terribly complicated with the code yet, but it seems to hold its own with trig (so far). Now you might have noticed that in my math above, I make use of the fact that the anti-derivative of $\sin{x} = \cos{x}$. We know that because if you take a $-\cos{x}$ graph (which is just a flipped $\cos{x}$ graph):

TODO: insert -cosx graph

then the slope at each point is equal to the $y$ value of $\sin{x}$ at the same point. Meaning, if you took the derivative of $-\cos{x}$, it would be $\sin{x}$. Since an integral is the **anti-derivative**, we can work in reverse and use $-\cos{x}$ as the integral.

### I don't believe you

Don't take my word for it -- see for yourself. How can we leverage our existing codebase to prove that $\int \sin{x}\, \mathrm{d}x = -\cos{x}$? Well I just said that **the derivative of $-\cos{x}$ would be $\sin{x}$**, so let's start there. We already used the definition of a derivative last time, so let's adapt the code to work for our current purposes.

    ::python
    def l(x): return -math.cos(x)

    >>> dl = derivative(l)
    >>> dl(1)
    0.8414709848914015
    >>> g(1)
    0.8414709848078965

The first 10 decimals are the same. I was going to take this further and calculate percent deviation, but then, out of curiosity, I decided to plot some test points using matplotlib. Here's what I got:

![d/dx[-cosx] and sinx][3]


You're probably thinking "hey, that's only one graph!" Actually, no; it's a plot of `dl(n)` and `g(n)` on the same graph. And in case you don't believe me, here's both of them side by side:

![d/dx[-cosx] Vs. sinx][4]

### Integrating in Three Dimensions

Now that I've completed all of objectives outlined in the previous section, it's time to move on to the big event. We will use our existing code to

[1]: /blog/proving-the-first-fundamental-theorem-of-calculus-with-python/
[2]: /blog/proving-the-first-fundamental-theorem-of-calculus-with-python/
[3]: /static/media/uploads/-cosx-sinx.png
[4]: /static/media/uploads/side-by-side.png
  