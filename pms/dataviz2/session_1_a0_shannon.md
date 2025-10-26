# Computing Shannon Entropy for Information Density (ID)

Notes for [Graphic Semiology Fundamentals](session_1_a.md) from Session 1
{: .pm-subtitle}



## Notes

- 1️⃣ Session 1: [Graphic Semiology Fundamentals](session_1_a.md) 
  - <span class="font-heading sm:text-lg">1.3. An example from a research paper</span>
  - Research paper: [Different languages, similar encoding efficiency: Comparable information rates across the human communicative niche](https://www.science.org/doi/10.1126/sciadv.aaw2594) by Christophe Coupé, Yoon Mi Oh, Dan Dediu, and François Pellegrino.


[TOC]

## About this study


>  *Different languages, similar encoding efficiency: Comparable information rates across the human communicative niche* by Christophe Coupé, Yoon Mi Oh, Dan Dediu, and François Pellegrino.<br>[Source: Science.org](https://www.science.org/doi/10.1126/sciadv.aaw2594)

In the study, **Shannon entropy** is used to estimate the **Information Density ($ID$)** per syllable, specifically as the **second-order conditional entropy** to account for syllable dependencies within words. Here's a simplified explanation of how it's computed, based on the methodology described:




## Protocol for computing $ID$


### 1. Syllable Probabilities
   - Collect a large written corpus for each language (e.g., texts, lexical databases).
   - Transcribe the corpus phonetically and segment it into syllables (using rule-based programs or existing syllabification for some languages).
   - For each language, calculate:
     - **Unigram probabilities**: $p(x)$, the probability of each syllable $x$ occurring in the corpus.
     - **Bigram probabilities**: $p(x, y)$, the probability of a syllable $y$ following a syllable $x$ within the same word (or a null marker for word-initial syllables).

### 2. First-Order Entropy ($ShE$)
   - Compute the standard Shannon entropy for syllables (unigram-based):
     $$
     ShE = -\sum_{x} p(x) \cdot \log_2(p(x))
     $$
     - $p(x)$: Probability of syllable $x$.
     - This measures the average uncertainty or information content per syllable, ignoring context.

### 3. Second-Order Entropy ($ID$)
   - Compute the **conditional entropy** to account for syllable dependencies (bigrams within words):
     $$
     ID = -\sum_{x, y} p(x, y) \cdot \log_2\left(\frac{p(x, y)}{p(x)}\right)
     $$
     - $p(x, y)$: Joint probability of syllable $y$ following syllable $x$.
     - $\dfrac{p(x, y)}{p(x)}$: Conditional probability $p(y|x)$, the likelihood of $y$ given $x$.
     - This reflects the information content per syllable, considering the context of the previous syllable, making it a more accurate measure of linguistic information.

### 4. Information Rate ($IR$)
   - Multiply the ID (bits per syllable) by the **Speech Rate (SR)** (syllables per second):
     $$
     IR = ID \cdot SR
     $$
     - $SR$ is calculated as the number of syllables ($NS$) divided by the duration of speech (in seconds, excluding pauses > $150$ ms).



## Key Notes
- **The data source**: Large written corpora provide syllable frequencies, while spoken corpora ($170$ speakers, $17$ languages, $\sim 240,000$ syllables) provide $SR$.
- **Why Conditional Entropy?**: It accounts for syllable predictability within words, reducing redundancy compared to first-order entropy ($ShE$), which assumes syllables are independent.
- **Result**: Across $17$ languages, $ID$ varies (e.g., $4.8$ bits/syllable for Basque to $8.0$ for Vietnamese), but $IR$ converges around $\sim 39$ bits/s due to a trade-off between $ID$ and $SR$.

For detailed implementation, the study provides R code and data in the GitHub repository: [https://github.com/keruiduo/SupplMatInfoRate](https://github.com/keruiduo/SupplMatInfoRate).

