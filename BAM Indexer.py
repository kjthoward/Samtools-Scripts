import os, subprocess, tkFileDialog, Tkinter, textwrap, textwrap, time
rootwindow = Tkinter.Tk()
rootwindow.withdraw()

#change this depending on where samtools is installed. Everything else is dynamic/selected during use
samtools_location="D:\\My Documents\\samtools"
Bam_Count=0

os.system("title Bam file Indexer")
print("Please select of folder of BAM files")
path=tkFileDialog.askdirectory(parent=rootwindow, title='Please select a folder of BAM files')
os.chdir(samtools_location)
start_time=time.time()
for root, dirnames, filenames in os.walk(path):
    
    for filename in filenames:
        if filename[-4:]==".bam":
            
            command=["samtools", "index",
                     "{}".format(os.path.join(root,os.path.dirname(filename), filename)), "{}".format(os.path.join(root,os.path.dirname(filename),filename+".bai"))]
            p=subprocess.Popen(command, shell=True)
            print("Indexing {}".format(filename))
            p.wait()
            Bam_Count+=1

if Bam_Count>0:
    seconds=int(time.time() - start_time)
    time_string = "{0} sec".format(seconds) if (seconds<60) else "{0} min {1} sec".format(seconds/60, seconds%60)
    print textwrap.fill("Successfully created .bam.bai files for {0} .bam files in {1}".format(Bam_Count, time_string))
elif Bam_Count==0:
    print textwrap.fill("No .bam files could be found in {}, or it's subfolders. Please check the folder and try again".format(path))

raw_input("Press enter to quit: ")
    


        
