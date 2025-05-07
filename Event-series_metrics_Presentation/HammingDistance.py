from manim import *
from manim import XKCD
import json

# Load custom configuration
with open("RQA_Kurzgesagt/manim_erudite_theme.json", "r") as file:
	config_data = json.load(file)

BACKGROUND_COLOR = config_data.get("background_color", BLACK)
TEXT_COLOR = config_data.get("text_color", WHITE)
#Doesn't yet work with non-default Manim colours

Text.set_default(color=XKCD.DARK)  # Set default color for text
MathTex.set_default(color=XKCD.DARK)  # Set default color for text
NumberLine.set_default(color=XKCD.DARK)  # Set default color for number 
Arrow.set_default(color=XKCD.DARK)

class HammingDistance(Scene):
	def construct(self):
		self.camera.background_color = XKCD.OFFWHITE
		# Define words and their positions
		word1 = Text("WORD", color=XKCD.MIDNIGHTBLUE).scale(2).move_to(UP)
		word2 = Text("CORD", color=XKCD.MIDNIGHTBLUE).scale(2).move_to(DOWN)
		
		# Highlight changing letter
		changing_letter1 = Text("W", color=XKCD.CARMINE).scale(2).move_to(word1[0].get_center())
		changing_letter2 = Text("C", color=XKCD.CARMINE).scale(2).move_to(word2[0].get_center())
		
		arrow = Arrow(start=word1.get_bottom(), end=word2.get_top(), buff=0.2)
		
		# Display initial word
		self.play(Write(word1))
		self.wait(1)
		
		# Highlight change
		self.play(Transform(word1[0], changing_letter1))
		self.wait(1)
		
		# Animate transition to new word
		self.play(Write(arrow), Transform(changing_letter1, changing_letter2))
		self.wait(1)
		
		# Display final word
		self.play(Write(word2))
		self.wait(2)

if __name__ == "__main__":
	from manim import config
	config.media_width = "75%"  # Adjust preview size
	scene = HammingDistance() #LogisticMapRecurrence()
	scene.render()