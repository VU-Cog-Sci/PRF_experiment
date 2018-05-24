import os

programs = [
'Safari','Messages','Mail','Calendar','Notes','Preview','Photos','Keynote','Numbers','Pages','Contacts','FaceTime' # mac os programs
'Google Drive','Dropbox','Carbonite', # backup programs
'Adobe Photoshop CS6','Adobe Illustrator','Adobe Photoshop Lightroom 5',# adobe
'Microsoft Excel','Microsoft Word','Microsoft Powerpoint', # office programs
'Skype','Flexiglass','Adobe','Slack','Papers','Evernote','Spotify', # other
]

for program in programs:

	os.system("sudo killall '%s'"%program)
