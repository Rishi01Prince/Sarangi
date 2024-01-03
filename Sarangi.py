#Music Player by Rishi Raj 

import os
import pickle
import tkinter as tk
from tkinter import Canvas, Label, filedialog
from tkinter.constants import E, NW, W
from PIL import ImageTk , Image  
from tkinter import PhotoImage 
from pygame import mixer



music_root = tk.Tk()
music_root.geometry('700x560')
music_root.maxsize(700,560)
music_root.minsize(700,560)
music_root["bg"]="green"
music_root.wm_title('Sarangi')


# Main Centre Photo
main_photo = Image.open('Rishi_Music_Images/Center_Photo2.jpg')
resampling_filter = Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS
resized_main_photo = main_photo.resize((500, 320), resampling_filter)
new_main_photo = ImageTk.PhotoImage(resized_main_photo)

# ...

# Next Button Image
Next_Button = Image.open('Rishi_Music_Images/Next_Button.jpg')
resized_Next_Button = Next_Button.resize((110, 90), resampling_filter)
new_Next_Button = ImageTk.PhotoImage(resized_Next_Button)

# Previous Button Image
Previous_Button = Image.open('Rishi_Music_Images/Previous_Song.jpg')
resized_Previous_Button = Previous_Button.resize((110, 90), resampling_filter)
new_Previous_Button = ImageTk.PhotoImage(resized_Previous_Button)

# Play Button Image
Play_Button = Image.open('Rishi_Music_Images/Play_Button.jpg')
resized_Play_Button = Play_Button.resize((85, 90), resampling_filter)
new_Play_Button = ImageTk.PhotoImage(resized_Play_Button)

# Pause Button Image
Pause_Button = Image.open('Rishi_Music_Images/Pause_Song.jpg')
resized_Pause_Button = Pause_Button.resize((85, 90), resampling_filter)
new_Pause_Button = ImageTk.PhotoImage(resized_Pause_Button)

# Load or Add Song Button Image
Load_Button = Image.open('Rishi_Music_Images/Load_Song.jpg')
resized_Load_Button = Load_Button.resize((85, 90), resampling_filter)
new_Load_Button = ImageTk.PhotoImage(resized_Load_Button)


class Sarangi(tk.Frame):

	#Constructor 

	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()

		mixer.init()

		if os.path.exists('songs.pickle'):
			with open('songs.pickle', 'rb') as f:
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]

		self.current = 0
		self.paused = True
		self.played = False

		self.Frame_Creation()
		self.Track_Widgets()
		self.Control_Widgets()
		self.Tracklist_Widgets()


	#Basic Frame Creation
	def Frame_Creation(self):

		self.track = tk.LabelFrame(self, text='Let us Play Some Music', 
					font=("Castellar",15,"bold"),
					bg="green",fg="white",bd=5,relief=tk.FLAT)

		self.track.config(width=300,height=400)
		self.track.grid(row=0, column=0, padx=165,pady=20,sticky=NW)


		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
							font=("times new roman",15,"bold"),
							bg="green",fg="white",bd=5 ,relief=tk.FLAT )

		self.tracklist.config(width=40,height=400)
		self.tracklist.grid(row=0, column=0, pady=20,padx=20 ,sticky=W)

		self.controls = tk.LabelFrame(self,
							font=("times new roman",15,"bold "),
							bg  ="white",fg="black",bd=2,relief=tk.SUNKEN )
		
		self.controls.config(width=660,height=95)
		self.controls.grid(row=2, column=0 ,padx=20 , sticky=NW)
		
		

	# Visual Main Track Player 
	def Track_Widgets(self):
		self.canvas = tk.Label(self.track, image=new_main_photo)
		self.canvas.configure(width=520,height=320)
		self.canvas.grid(row=0,column=1 , sticky=W)

		self.songtrack = tk.Label(self.track, font=("Bell MT",16,"bold"),
						bg="white",fg="maroon")
		self.songtrack['text'] = 'Sarangi MP3 Player'
		self.songtrack.config(width=40, height=1)
		self.songtrack.grid(row=1,column=1,)
		


	#Control Widgests 
	def Control_Widgets(self):
		self.loadSongs = tk.Button(self.controls, image=new_Load_Button)
		self.loadSongs['command'] = self.retrieve_songs
		self.loadSongs.grid(row=0, column=0, padx=24 ,pady=8)

		self.prev = tk.Button(self.controls, image=new_Previous_Button)
		self.prev['command'] = self.prev_song
		self.prev.grid(row=0, column=1,padx=4,pady=8)

		self.pause = tk.Button(self.controls, image=new_Pause_Button)
		self.pause['command'] = self.pause_song
		self.pause.grid(row=0, column=2,padx=4,pady=8)

		self.next = tk.Button(self.controls, image = new_Next_Button)
		self.next['command'] = self.next_song
		self.next.grid(row=0, column=3,padx=4,pady=8)


		#Music Volume Adjuster/Slider
		self.volume = tk.DoubleVar(self)
		self.slider = tk.Scale(self.controls, from_ = 0, to = 100, orient = tk.HORIZONTAL)
		self.slider['variable'] = self.volume
		self.slider.set(8)
		mixer.music.set_volume(0.8)
		self.slider['command'] = self.change_volume
		self.slider.grid(row=0, column=4, padx=30)

	#Function for Tracklist
	def Tracklist_Widgets(self):
		self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
		self.scrollbar.grid(row=0,column=0, rowspan=5, sticky=W)

		self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
					 yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
		self.enumerate_songs()
		self.list.config(height=22)
		self.list.bind('<Double-1>', self.play_song) 

		self.scrollbar.config(command=self.list.yview)
		self.list.grid(row=0, column=0, rowspan=5,padx=4)

	#Function for Rertriving Songs from any Directory
	def retrieve_songs(self):
		self.songlist = []
	
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)

		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
			
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()

	#Function for Inserting Songs name in the playlist
	def enumerate_songs(self):
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))

	#Function for Playing Song
	def play_song(self, event=None):
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")

		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])
		self.songtrack['anchor'] = 'w' 
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])

		self.pause['image'] = new_Pause_Button
		self.paused = False
		self.played = True
		self.list.activate(self.current) 
		self.list.itemconfigure(self.current, bg='sky blue')

		mixer.music.play()

	#Function For Pausing Song
	def pause_song(self):
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pause['image'] = new_Play_Button
		else:
			if self.played == False:
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause['image'] = new_Pause_Button

	#Function for Previous Song
	def prev_song(self):
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.list.itemconfigure(self.current + 1, bg='white')
		self.play_song()

	#Function for Next Song
	def next_song(self):
		if self.current < len(self.playlist) - 1:
			self.current += 1
		else:
			self.current = 0
		
		self.list.itemconfigure(self.current - 1, bg='white')
		self.play_song()

	#Function for Adjusting Volume
	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 100)



#Object Creation
Peace = Sarangi(master=music_root) 

Peace.mainloop()