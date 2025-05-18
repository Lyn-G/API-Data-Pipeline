### YuGiOh Data Pipeline

#### By Lynelle Goh

---

To set up this script, simply type `python main.py` into your terminal to run the script. <br>

The program will ask what emails you'd like to share the spreadsheet too. Type them in one at a time and press enter. Type `n` to let the program know you're done.<br>

You'll then be prompted to type the name of the sheet you'd like to edit.<br>

- If the sheet name is **not found**, the program will make a new one and share it with the emails provided.
- If the sheet name is **found**, the program will edit that one and share it with the emails provided. <br><br>

Now the script will ask you which YuGiOh archetype you'd like to search up cards for. If nothing is placed down, the default archetype search will be "Dark Magician".<br>

Let the program do its job. 😎<br>

Voila! It'll set up and edit the spreadsheet! The terminal will print out the link, and you can click on it!

---

Being the nerd I am, I chose the YuGiOh API because I grew up watching YuGiOh and playing card games. It piqued my interest to see that there was an entire API ready for me to data transform. Using YuGiOh's archetypes to find my data, I calculated a custom "power score" for each one by averaging its attack and defense stats. Then I sorted the cards by this score and edit into the Google Sheet the top 15 most powerful ones.

My class structure can most definitely be applied to other playing card games. It can easily be adapted by changing the base URL and adjusting the transformation logic to match the structure of those APIs. Several examples that come to mind are Pokemon, Digimon, Bakugan, etc.

<!-- - README with setup instructions (including any API keys if used)
- Brief explanation (1–3 paragraphs) of:
  - Why you chose your API
  - What transformation you performed
  - How your class structure could be extended to other APIs -->
