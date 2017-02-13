import sys, datetime
# from Tkinter import *

sys.path.append( 'exp_tools' )

from PRFSession import *
# from plot_staircases import *
try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

def main():
    initials = raw_input('Your initials: ')
    run_nr = int(raw_input('Run number: '))
    scanner = raw_input('Are you in the scanner (y/n)?: ')
    track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    task_type = 'bar'#raw_input('Attention task (fix/bar): ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False

    ts = PRFSession( initials, run_nr, scanner, tracker_on, task_type )
    ts.run()

    # plot_staircases(initials, run_nr)

if __name__ == '__main__':
    main()
# def run_exp(root,e):
#    #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

#     sid = e['SubjectID'].get().strip()
#     run = e['Run nr'].get().strip()
#     scanner = e['In Scanner'].get().strip()
#     task = e['Task'].get().strip()
#     et = e['EyeTracker'].get().strip()

#     if (not sid) or (sid == ""):
#         Label(root, text = 'Please enter a subject ID!').pack()
#     elif (not run) or (run == ""):
#         Label(root, text = 'Run number must be 1 or higher').pack()
#     else:

#         run = int(run)
#         scanner = bool(scanner)

#         ts = PRFSession( sid, run, scanner, et, task )
#         root.quit()
#         ts.run()  


# fields = 'SubjectID','Run nr','Timestamp','In Scanner','Task','EyeTracker'

# def makeform(root, fields):
#    entries = {}
#    for field in fields:
#       row = Frame(root)
#       lab = Label(row, width=15, text=field, anchor='w')
#       ent = Entry(row)
#       row.pack(side=TOP, fill=X, padx=5, pady=5)
#       lab.pack(side=LEFT)
#       ent.pack(side=RIGHT, expand=YES, fill=X)
#       entries[field] = ent
#    # for checkbox in checkboxes:
#    #      row = Frame(root)
#    #      c = Checkbutton(master, text="Expand", variable=var)
#    return entries



# if __name__ == '__main__':
#    root = Tk()

#    Label(root, text = 'Start nPRF session').pack()

#    ents = makeform(root, fields)

#    ents['Timestamp'].insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#    ents['EyeTracker'].insert(0, '0')
#    ents['In Scanner'].insert(0, '0')
#    ents['Task'].insert(0, 'bar')

#    # root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
#    b1 = Button(root, text='Run nPRF',
#           command=(lambda e=ents: run_exp(root,e)))
#    b1.pack(side=LEFT, padx=5, pady=5)
#    root.mainloop()
