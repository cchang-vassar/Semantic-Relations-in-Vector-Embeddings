# Semantic Relations in Vector Embeddings

remember not to post OpenAI API key on here :> <br>
To start virtual env: <br>
`source openai-env/bin/activate` <br>
`python -m venv openai-en`<br><br>

TODO: <br>
1.  Check out what other people have tried

1.  Try using an older model like GloVe, BERT, esp those more bag of words kinda models
2.  Try constructing arguments for these kinds of models where there is large lexical overlap, but all the key evaluative terms are opposed
3.  Ask GPT to make a counterargument for an argument and then pop that text into embedding space and then see if there is regularity between that vector and the original argument
4.  ask GPT to explain both arguments in its own words and then map that
5.  -> can see if this is in embedding space vs weights
6.  can get longer arguments from ballot initiatives
7.  compare to human embedding spaces like liwc, cmv (those that hv delta award -> actually changed), can test each reply under forum paired with original post
8.  ask humans to rate individual arguments on certian dimensions like persuasion
10.  classification system for argumentation
11.  srm relates to project -> start with ada002 embedding vectrors, and then can move onto higher level chatgpt generated pairs -> can then look at output of each layer, esp hidden layer (latent representations) (elman paper and semantic cognition)


# What are some possible ways of categorizing argument-counterargument relations?

_Categories_

1. Logical negation-ey thing
   - often one word different
   - e.g. people are born good | people are born bad
   - e.g. pineapple on pizza is tasty | pineapple on pizza is not tasty
2. Same material, different understanding
   - e.g. i dunno 90% of the non-analytic philosophy readings
3. Different perspective on same topic
   - e.g. political/social issues, which seems like most of what idebate.org is
4. Emotional
   - e.g. r/CMV, r/AITA?

_From argument theory_
Either attack premise, conclusion or reasoning between them 

\*P.S. How do these models do in 3+ party conversations?
