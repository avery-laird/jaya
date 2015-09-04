I conclude my blog hiatus with a (kind-of) silly post. As I'm sure most of you have noticed, the internet is full of ads and articles that have titles with a certain structure. For example:   

* 17 Celebrity Instagrams You Need To See This Week    
* How To Get Organized: 2 Solutions From Philosophy And Kindergarten   
* How The Most Powerful People Get Things Done: 4 Tips From A White House Staffer.

And those were just from a 2 minute Google search. The web is full of them! And it seemed to me that they all followed a similar format, one that might easily be quantified and automated. Thus began my journey to generate random BuzzFeed-style titles!


Let the hilarity ensue.


# Propound Their Chara: Breaking down the structure

Before we can begin programatically generating the titles, we first have to identify which words should go where. Since all the titles are *similar*, but not strictly the same, we should choose a **compromise** between the numerous variants out there. I decided to go with the following structure. **Note** -- words to be generated or selected randomly are enclosed by `<>`:

    <verb><possessive determiner><noun>: <number><adjective><tips,tricks,etc> to <verb><possessive determiner><noun>

At first glance, one of the things I noticed was that the first three words and the last three words are of the exact same *structure*, but are not the same word. To give you a better idea of the format I'm going for, I'll give you an example of a title in this format:  

* Organize your calendar: 17 great tips to increase your productivity

The verbs won't be too tricky: most verbs in the present tense should work fine. However, the "possessive determiner" might be difficult, because even within the domain of possessive determiners there are few words which realistically make sense in that sentence. That's why I simply chose three off the top of my head: your, our, and their.   

Similar to the verbs, any noun in the present tense should fit in a sentence of that structure. The same goes for the adjectives. And finally, numbers can easily be generated randomly (pseudo-randomly).

# Flex our Hygrostats: Writing the Code

I didn't want to use any dedicated libraries for this, mainly because I think using one like **nltk** would be overkill, but also because I'm not knowledgeable enough about using it to even look like I know what I'm doing.

For this script, I used a plaintext list of verbs, nouns and adjectives placed in the same directory as the code. You can use any list you want, but here are the ones I used: [verbs.txt][1], [nouns.txt][2], and [adjectives.txt][3].

The first thing we should do is establish a method of reading lines from a file at random. I thought there was no pretty way to do it until I came across [this][4] on stackoverflow. It's beautiful! One thing that may trip people up, however, is confusing the type of parameter to pass. `random_line()` takes a file object. So first, we make use of this awesome code sample:

    ::python
    import random
    random.seed()

    def random_line(afile):
        line = next(afile)
        for num, aline in enumerate(afile):
            if random.randrange(num + 2): continue
            line = aline
        return line

We need a total of 2 verbs, so to keep everything organized, let's get those first and at the same time:

    ::python
    verbs = [verb.rstrip() for verb in [random_line(open('verbs.txt', 'r')) for x in range(2)]]

Next, let's make a list with the possessive determiners:

    ::python
    pd = ['your','our','their']

And generate the nouns the same way as the verbs:

    ::python
    nouns = [noun.rstrip() for noun in [random_line(open('nouns.txt','r')) for x in range(2)]]

We only need one adjective, so the line is a bit simpler:

    ::python
    adjs = random_line(open('adjectives.txt','r')).rstrip()

Next we'll need what I call the "filler text":

    ::python
    ft = ['tips', 'tricks', 'suggestions', 'choices']

Lastly, the mother of all print statements:

    ::python
    print verbs[0] + " " + pd[random.randint(0, 2)] + " " + nouns[0] + ": " + str(random.randint(0,15000)) + " " + adjs + " " + ft[random.randint(0,3)] + " to " + verbs[1] + " " + pd[random.randint(0,2)] + " " + nouns[1]

Here's the whole script, for copying/viewing ease:

    ::python
    # main.py

    import random
    random.seed()

    def random_line(afile):
        line = next(afile)
        for num, aline in enumerate(afile):
            if random.randrange(num + 2): continue
            line = aline    
        return line


    verbs = [verb.rstrip() for verb in [random_line(open('verbs.txt', 'r')) for x in range(2)]]

    pd = ['your','our','their']

    nouns = [noun.rstrip() for noun in [random_line(open('nouns.txt','r')) for x in range(2)]]

    adjs = random_line(open('adjectives.txt','r')).rstrip()
    ft = ['tips', 'tricks', 'suggestions', 'choices']


    print verbs[0] + " " + pd[random.randint(0, 2)] + " " + nouns[0] + ": " + str(random.randint(0,15000)) + " " + adjs + " " + ft[random.randint(0,3)] + " to " + verbs[1] + " " + pd[random.randint(0,2)] + " " + nouns[1]

Well, it's not winning any PEP awards, but I got to use some fancy list comprehensions. Let's take it for a spin:

    $ python main.py
    titter your gorgons: 8358 longhand tips to polarize your grits

Here are some other titles that were generated during testing:  

* flex our hygrostats: 15 Lemnian tricks to isolate your Mariolater
* bemusing their recusants: 0.550137098499 gory choices to deep-freeze their functionary
* propound their chara: 4073 ecstatic tricks to paik their expiation
* hade our linguine: 13337 teind tricks to obturate your frequentation 

So it works! However, not perfectly. There are two main issues:

### Present tense verbs

Because we just use one big list o' verbs, some of them are in the wrong tense. I opted to leave this out of the code, for you to tweak after if you need to. This is where using a library like **nltk** can come in handy, or finding a list with verbs of only the proper tense.

### Any combination is possible

This is great, except that there are a lot of words in the English language, some of them ranging from funny to really, really offensive. I know from playing around with the script a bit that if you're in doubt about what a word means, look it up. 

----

# Improvements

How can we make this better? I've got a couple ideas. 

### Generalize

Let's say I want to create a sentence with any structure, using random words. The script could be modified to take an argument, similar to the pseudo-code used earlier in the article, and construct a sentence from a user-defined structure. 

### Contextualize

Right now, some sentences need a bit of tweaking. For example, they might be in the wrong tense. Using a natural language library could be the solution, but that would also add a level of complexity.

# Conclusion

Have fun creating your very own random titles. I'm interested to see what ones you guys might generate! If you notice any errors or typos, please send me an email at laird.avery@gmail.com or comment below.


  [1]: http://www.averylaird.com/static/media/uploads/blog/verbs.txt
  [2]: http://www.averylaird.com/static/media/uploads/blog/nouns.txt
  [3]: http://www.averylaird.com/static/media/uploads/blog/adjectives.txt
  [4]: http://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file-in-python